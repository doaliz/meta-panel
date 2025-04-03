import streamlit as st
import urllib.parse

st.set_page_config(page_title="Meta Reklam Verisi Analiz Paneli", page_icon="📊", layout="centered")

st.markdown("<h1 style='text-align: center;'>📊 Meta Reklam Verisi Analiz Paneli</h1>", unsafe_allow_html=True)

def get_access_token():
    # URL'deki access_token'ı al
    query_params = st.query_params
    full_url = st.experimental_get_query_params()
    fragment = st.experimental_get_query_params().get("access_token", [None])[0]

    if fragment:
        return fragment
    else:
        return None

token = get_access_token()

if token:
    st.success("✅ Token alındı!")
    st.write("Token:", token)
    # Buraya token ile işlem yapılacak kısım entegre edilir
else:
    st.warning("⚠️ Token alınamadı. Lütfen tekrar giriş yapın.")
    # Kullanıcıyı Facebook login'e yönlendirecek bağlantı
    client_id = "2162760587483637"
    redirect_uri = "http://49.12.213.210:8501"
    scope = "ads_read,business_management,pages_show_list,public_profile"
    oauth_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&scope={scope}&response_type=token&display=popup"
    
    st.markdown(f"👉 [Facebook ile Giriş Yap]({oauth_url})")
