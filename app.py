import streamlit as st
import requests
import json

# Sayfa ayarları
st.set_page_config(page_title="Meta Reklam Verisi Analiz Paneli", layout="centered")

st.markdown("""
<h1>📊 Meta Reklam Verisi Analiz Paneli</h1>
""", unsafe_allow_html=True)

# ✅ Query params ile token yakalama
query_params = st.query_params
access_token = None

if "access_token" in query_params:
    token_string = query_params["access_token"]
    if isinstance(token_string, list):
        token_string = token_string[0]
    access_token = token_string.split("&")[0]

# Kullanıcıya bilgi verme
if access_token:
    st.success("✅ Token alındı!")

    # ➤ Facebook API'den hesapları çekme
    url = f"https://graph.facebook.com/v18.0/me/adaccounts?access_token={access_token}"
    response = requests.get(url)

    if response.status_code == 200:
        hesaplar = response.json()
        st.json(hesaplar)
    else:
        st.error("❌ Hesaplar çekilemedi. Token geçersiz veya süresi dolmuş olabilir.")
        st.code(response.text, language="json")

else:
    st.warning("⚠️ Token alınamadı. Lütfen tekrar giriş yapın.")
    login_url = (
        "https://www.facebook.com/v18.0/dialog/oauth"
        "?client_id=2162760587483637"
        "&redirect_uri=http://49.12.213.210:8501/"
        "&scope=ads_read,business_management,pages_show_list,public_profile"
        "&response_type=token&display=popup"
    )
    st.markdown(f"👉 [Facebook ile Giriş Yap]({login_url})")
