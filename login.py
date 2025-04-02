import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Facebook Giriş", layout="centered")
st.title("🔑 Facebook Giriş")

st.markdown("Giriş yapılıyor...")

components.html(
    """
    <script>
        const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
        if (tokenMatch) {
            const token = tokenMatch[1];
            localStorage.setItem("fb_token", token);
            window.location.href = window.location.origin;  // ana sayfaya yönlendir
        }
    </script>
    """,
    height=0
)
