import streamlit as st
import urllib.parse

st.set_page_config(page_title="Meta Reklam Paneli", layout="centered")

st.title("📊 Meta Reklam Verisi Analiz Paneli")

# Token'ı URL hash'inden alıp query string'e yazan JavaScript kodu
st.markdown("""
<script>
    const url = new URL(window.location.href);
    const hash = url.hash;
    if (hash.includes("access_token")) {
        const params = new URLSearchParams(hash.substring(1));
        const token = params.get("access_token");
        const expires = params.get("expires_in");

        // Token'ı URL query string'ine ekle
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("access_token", token);
        newUrl.searchParams.set("expires_in", expires);
        newUrl.hash = "";
        window.location.replace(newUrl);
    }
</script>
""", unsafe_allow_html=True)

# Query parametreden token'ı al
query_params = st.query_params
access_token = query_params.get("access_token", None)

# Duruma göre mesaj göster
if access_token:
    st.success("✅ Token alındı ve giriş başarılı!")
    st.code(access_token, language="bash")

    # Burada Meta API'den veri çekme işlemini başlatabilirsin
    # response = requests.get("https://graph.facebook.com/v18.0/me/adaccounts", headers={...})

else:
    st.warning("⚠️ Token alınamadı. Lütfen yeniden giriş yapın.")
    st.markdown("👉 [Facebook ile Giriş Yap](https://www.facebook.com/v18.0/dialog/oauth?client_id=2162760587483637&redirect_uri=http://49.12.213.210:8501/&scope=ads_read,business_management,pages_show_list,public_profile&response_type=token&display=popup)")
