import streamlit as st

# -- Page config --
st.set_page_config(
    page_title="MetPark - Gestion des évènements",
    page_icon="🅿️",
    layout="wide",
)

# -- Navigation --
page = st.navigation([
    st.Page("pages/accueil.py", title="Accueil", icon="🏠"),
    st.Page("pages/evenements_externes.py", title="Événements externes", icon="📋"),
    st.Page("pages/evenements_techniques.py", title="Événements techniques", icon="🔧"),
    st.Page("pages/occupation_parking.py", title="Impact Parking", icon="⚠️"),
])

page.run()
