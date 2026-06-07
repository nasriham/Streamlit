import streamlit as st
from core.db import get_session

st.set_page_config(
    page_title="Gestion des référentiels",
    page_icon="assets/logo.png"
)

session = get_session()
current_db = session.get_current_database()

if "DEV" in current_db:
    ENV = "DEV"
elif "QUA" in current_db:
    ENV = "QUA"
elif "PPD" in current_db:
    ENV = "PPD"
else:
    ENV = "PROD"

if ENV == "DEV":
    st.error("🚧 ENVIRONNEMENT DEVELOPPEMENT")
elif ENV == "QUA":
    st.warning("🧪 ENVIRONNEMENT QUALIFICATION")
elif ENV == "PPD":
    st.success("✅ ENVIRONNEMENT PRE-PRODUCTION")

    
# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=120)
with col2:
    st.title("Gestion des référentiels")

st.write("Utilisez le menu à gauche pour naviguer dans les fonctions.")