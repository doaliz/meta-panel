import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Facebook Giriş", layout="centered")
st.title("🔑 Facebook Giriş")

components.html(
    """
    <script>
        const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
        if (tokenMatch) {
            const token = tokenMatch[1];
            console.log("TOKEN FOUND:", token);
            localStorage.setItem("fb_token", token);
            window.location.replace(window.location.origin);  // ana sayfaya yönlendir
        } else {
            document.write("❌ Token bulunamadı. Lütfen tekrar deneyin.");
        }
    </script>
    """,
    height=100
)
