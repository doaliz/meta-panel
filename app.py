# streamlit_meta_panel/app.py

import streamlit as st
import pandas as pd
import requests
import streamlit_javascript as stj

st.set_page_config(page_title="Meta Reklam Paneli", layout="centered")
st.title("📊 Meta Reklam Verisi Analiz Paneli")

APP_ID = "2162760587483637"
REDIRECT_URI = "https://keremyavas.streamlit.app/"  # Streamlit Cloud URL
SCOPES = "ads_read,business_management,pages_show_list,public_profile"

login_url = f"https://www.facebook.com/v18.0/dialog/oauth?client_id={APP_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}&response_type=token&display=popup"

if "access_token" not in st.session_state:
    st.session_state.access_token = None

# Token yoksa giriş linki + JS ile access_token yakala
if not st.session_state.access_token:
    st.markdown(f"[👉 Facebook ile Giriş Yap]({login_url})")
    result = stj.st_javascript("""
        async function() {
            const tokenMatch = window.location.hash.match(/access_token=([^&]+)/);
            if (tokenMatch) {
                return tokenMatch[1];
            }
            return null;
        }
    """)
    if result and result != "null":
        st.session_state.access_token = result

# Token varsa devam
if st.session_state.access_token:
    access_token = st.session_state.access_token

    test = requests.get(f"https://graph.facebook.com/me?access_token={access_token}")
    if test.status_code == 200:
        st.success("🔓 Facebook erişimi sağlandı!")

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
    else:
        st.error("Token geçersiz. Lütfen yeniden giriş yapın.")
        st.session_state.access_token = None
        st.markdown(f"[👉 Facebook ile Giriş Yap]({login_url})")
