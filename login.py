import streamlit as st
import streamlit_javascript as stj

st.set_page_config(page_title="Facebook Giriş", layout="centered")
st.title("🔑 Facebook Giriş")

st.markdown("Giriş işlemi yapılıyor... Lütfen bekleyin.")

# 1. Adım: Token'ı hash kısmından alıp URL query'e yaz
result = stj.st_javascript("""
    async () => {
        const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
        if (tokenMatch) {
            const token = tokenMatch[1];
            const newUrl = window.location.origin + "/?token=" + token;
            window.location.href = newUrl;
        }
        return null;
    }
""")
