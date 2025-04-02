import streamlit as st
import streamlit_javascript as stj
import pandas as pd
import requests

st.set_page_config(page_title="Meta Reklam Paneli", layout="centered")
st.title("📊 Meta Reklam Verisi Analiz Paneli")

# ✅ Token localStorage'dan okunur ve session'a yazılır
if "access_token" not in st.session_state:
    token = stj.st_javascript("""
        async () => {
            return localStorage.getItem("fb_token");
        }
    """)
    if token:
        st.session_state.access_token = token
        st.experimental_rerun()
    else:
        st.warning("Token alınamadı. Lütfen tekrar giriş yapın.")
        st.markdown("[👉 Facebook ile Giriş Yap](https://www.facebook.com/v18.0/dialog/oauth?client_id=2162760587483637&redirect_uri=https://keremyavas.streamlit.app/login&scope=ads_read,business_management,pages_show_list,public_profile&response_type=token&display=popup)")
        st.stop()

# ✅ Token varsa devam
access_token = st.session_state.access_token
test = requests.get(f"https://graph.facebook.com/me?access_token={access_token}")
if test.status_code != 200:
    st.error("❌ Token geçersiz veya süresi dolmuş olabilir.")
    st.session_state.access_token = None
    st.markdown("[👉 Facebook ile Giriş Yap](https://www.facebook.com/v18.0/dialog/oauth?client_id=2162760587483637&redirect_uri=https://keremyavas.streamlit.app/login&scope=ads_read,business_management,pages_show_list,public_profile&response_type=token&display=popup)")
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
