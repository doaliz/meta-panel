import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Facebook Giriş", layout="centered")
st.title("🔑 Facebook Giriş")

st.markdown("Giriş yapılıyor... Lütfen bekleyin.")

components.html(
    """
    <script>
        const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
        if (tokenMatch) {
            const token = tokenMatch[1];
            const newUrl = window.location.origin + "/?token=" + token;
            window.location.href = newUrl;
        } else {
            document.write("Access token bulunamadı.");
        }
    </script>
    """,
    height=0,
)
