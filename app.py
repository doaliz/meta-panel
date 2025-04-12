import streamlit as st
import requests
import urllib.parse

# Sayfa ayarı
st.set_page_config(page_title="Meta Reklam Verisi", layout="centered")

st.title("📊 Meta Reklam Verisi Analiz Paneli")

# ✅ Token yakalama (query string üzerinden)
query_params = st.query_params
access_token = None

if "access_token" in query_params:
    token_string = query_params["access_token"]
    if isinstance(token_string, list):
        token_string = token_string[0]
    access_token = token_string.split("&")[0]  # sadece token'ı al

# ✅ Token varsa işlem yap
if access_token:
    st.success("✅ Token alındı!")
    st.code(access_token, language="bash")

    # Facebook API'den hesap bilgilerini çek
    url = f"https://graph.facebook.com/v18.0/me/adaccounts?access_token={access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        hesaplar = response.json()
        st.subheader("📂 Hesaplar")
        for hesap in hesaplar.get("data", []):
            st.write(f"🔹 {hesap['name']} — {hesap['id']}")
    else:
        st.error("❌ API isteği başarısız oldu.")
        st.code(response.text, language="json")

# ✅ Token yoksa login ekranı göster
else:
    st.warning("⚠️ Token alınamadı. Lütfen Facebook ile giriş yapın.")
    client_id = "2162760587483637"
    redirect_uri = "https://49.12.213.210:8501"
    scope = "ads_read,business_management,pages_show_list,public_profile"

    login_url = (
        f"https://www.facebook.com/v18.0/dialog/oauth?"
        f"client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&scope={scope}&response_type=token&display=popup"
    )

    st.markdown(f"👉 [Facebook ile Giriş Yap]({login_url})")
