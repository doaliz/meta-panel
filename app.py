import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests

st.set_page_config(page_title="Meta Reklam Paneli", layout="centered")
st.title("📊 Meta Reklam Verisi Analiz Paneli")

# ✅ JavaScript ile hash içindeki access_token'ı al ve URL query'ye aktar
if "access_token" not in st.session_state:
    components.html(
        """
        <script>
            const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
            if (tokenMatch) {
                const token = tokenMatch[1];
                window.location.href = window.location.origin + '/?token=' + token;
            }
        </script>
        """,
        height=0
    )

# ✅ token query parametresinden alınır ve session'a yazılır
token_param = st.query_params.get("token")
if token_param and "access_token" not in st.session_state:
    st.session_state.access_token = token_param
    st.experimental_rerun()

# ✅ Token yoksa girişe yönlendir
if "access_token" not in st.session_state:
    login_url = "https://www.facebook.com/v18.0/dialog/oauth?client_id=2162760587483637&redirect_uri=https://keremyavas.streamlit.app/&scope=ads_read,business_management,pages_show_list,public_profile&response_type=token&display=popup"
    st.warning("Token alınamadı. Lütfen tekrar giriş yapın.")
    st.markdown(f"[👉 Facebook ile Giriş Yap]({login_url})")
    st.stop()

# ✅ Token mevcut, kontrol et ve devam et
access_token = st.session_state.access_token
test = requests.get(f"https://graph.facebook.com/me?access_token={access_token}")
if test.status_code != 200:
    st.error("❌ Token geçersiz veya süresi dolmuş olabilir.")
    st.session_state.access_token = None
    st.markdown(f"[👉 Facebook ile Giriş Yap]({login_url})")
    st.stop()

st.success("🔓 Facebook erişimi sağlandı!")

# ➕ Devamında reklam hesapları çekilir...
url = f"https://graph.facebook.com/v18.0/me/adaccounts?access_token={access_token}"
response = requests.get(url)
data = response.json()

if "data" in data:
    hesaplar = data["data"]
    hesap_secimi = []
    for h in hesaplar:
        hesap_secimi.append({
            "id": h.get("account_id", "-"),
            "name": h.get("name", "Reklam Hesabı")
        })

    secenekler = [f"{h['name']} (act_{h['id']})" for h in hesap_secimi]
    secilen = st.selectbox("📂 Bir reklam hesabı seçin:", secenekler)

    if secilen:
        secilen_id = secilen.split("(act_")[-1].replace(")", "")
        act_id = f"act_{secilen_id}"
        st.write(f"Seçilen hesap: `{act_id}`")
        st.info("📌 Bir sonraki adımda bu hesaptan veri çekerek analiz yapılacak.")
else:
    st.error("Hesaplar çekilemedi. Geçerli hesap bulunamadı.")
    st.json(data)
