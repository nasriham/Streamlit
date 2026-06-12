import streamlit as st

# -- Page config --
st.set_page_config(
    page_title="MetPark - Gestion des évènements",
    page_icon="🅿️",
    layout="wide",
)

# -- Thème MetPark : fond clair + accents orange --
st.markdown("""
<style>
    /* Fond principal */
    .stApp {
        background-color: #F8F9FA;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid #E8611A;
    }

    /* Boutons primaires en orange MetPark */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #E8611A;
        border-color: #E8611A;
        color: white;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #D4550F;
        border-color: #D4550F;
    }

    /* Tabs actifs en orange */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #E8611A;
        border-bottom-color: #E8611A;
    }

    /* Titres en bleu foncé MetPark */
    h1, h2, h3 {
        color: #1D2B3A !important;
    }

    /* Liens et accents */
    a {
        color: #E8611A;
    }
</style>
""", unsafe_allow_html=True)

# -- Navigation --
page = st.navigation([
    st.Page("pages/accueil.py", title="Accueil", icon="🏠"),
    st.Page("pages/evenements_externes.py", title="Événements externes", icon="📋"),
    st.Page("pages/evenements_techniques.py", title="Événements techniques", icon="🔧"),
    st.Page("pages/travaux.py", title="Travaux", icon="🏗️"),
    st.Page("pages/occupation_parking.py", title="Impact Parking", icon="⚠️"),
])

page.run()
