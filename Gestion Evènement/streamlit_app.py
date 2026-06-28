# Application de gestion des événements MetPark
# Co-authored with CoCo
import streamlit as st

# -- Page config --
st.set_page_config(
    page_title="MetPark - Gestion des évènements",
    page_icon="🅿️",
    layout="wide",
)

# -- Thème MetPark : bleu marine + accent rouge/orange --
st.markdown("""
<style>
    /* ===== FOND & LAYOUT ===== */
    .stApp {
        background-color: #F7F9FC;
    }

    /* Sidebar sobre avec accent orange discret */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 2px solid rgba(233, 75, 46, 0.3);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #0B2545 !important;
    }

    /* ===== TYPOGRAPHIE ===== */
    h1, h2, h3 {
        color: #0B2545 !important;
        font-weight: 700;
    }
    h4, h5, h6 {
        color: #123C69 !important;
        font-weight: 600;
    }
    p, li, span, label {
        color: #1E293B;
    }

    /* ===== BOUTONS ===== */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    .stFormSubmitButton > button {
        background-color: #E94B2E !important;
        border-color: #E94B2E !important;
        color: white !important;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #C7391F !important;
        border-color: #C7391F !important;
        color: white !important;
    }
    /* Boutons secondaires */
    .stButton > button {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        color: #0B2545;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #E94B2E;
        border-color: #E94B2E;
        color: white;
    }

    /* ===== ONGLETS (Tabs) ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
        color: #64748B;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #0B2545;
        font-weight: 700;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #E94B2E;
    }

    /* ===== MÉTRIQUES (KPI cards) ===== */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 18px 22px;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }
    [data-testid="stMetric"] label {
        color: #64748B !important;
        font-size: 0.85rem;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #0B2545 !important;
        font-weight: 700;
    }

    /* ===== TABLEAUX ===== */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }
    div[data-testid="stDataFrame"] table {
        border-collapse: separate;
    }
    div[data-testid="stDataFrame"] thead th {
        background-color: #0B2545 !important;
        color: white !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }

    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        font-weight: 600;
        color: #0B2545;
    }

    /* ===== SELECTBOX & INPUTS ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border-color: #E2E8F0;
    }
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #123C69;
        box-shadow: 0 0 0 2px rgba(18, 60, 105, 0.1);
    }

    /* ===== CHECKBOX ===== */
    .stCheckbox label span[data-testid="stCheckbox"] {
        color: #0B2545;
    }

    /* ===== LIENS ===== */
    a {
        color: #E94B2E;
    }
    a:hover {
        color: #0B2545;
    }

    /* ===== ALERTES ===== */
    .stAlert[data-baseweb="notification"] {
        border-radius: 10px;
    }

    /* ===== DIVIDER ===== */
    hr {
        border-color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# -- Navigation --
page = st.navigation([
    st.Page("pages/accueil.py", title="Accueil", icon="🏠"),
    st.Page("pages/evenements_externes.py", title="Événements externes", icon="📋"),
    st.Page("pages/evenements_techniques.py", title="Événements techniques", icon="🔧"),
    st.Page("pages/travaux.py", title="Travaux", icon="🏗️"),
])

# -- Sidebar : badge environnement + logo --
with st.sidebar:
    from core.db import ENV
    if ENV != "PROD":
        colors = {"DEV": ("#FEF3C7", "#92400E", "DEV"), "QUA": ("#E0E7FF", "#3730A3", "QUA"), "PPD": ("#D1FAE5", "#065F46", "PPD")}
        bg, txt, label = colors.get(ENV, ("#F3F4F6", "#374151", ENV))
        st.markdown(
            f'<div style="text-align:center;margin-bottom:8px;">'
            f'<span style="background:{bg};color:{txt};padding:4px 12px;border-radius:20px;font-size:0.7rem;font-weight:700;letter-spacing:1px;">'
            f'{label}</span></div>',
            unsafe_allow_html=True,
        )
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image("assets/MTPK_logo.png", width=160)

    # -- Footer sidebar : support --
    st.markdown("---")
    with st.popover("Contacter Equipe Data — Seenovate"):
        st.markdown("**Equipe Data — Seenovate**")
        st.markdown("[Arssalane BOURASS](mailto:Arssalane.BOURASS@seenovate.com)")
        st.markdown("[Hamza NASRI](mailto:hamza.nasri@seenovate.com)")
        st.markdown("[Benoit OTTAVI](mailto:benoit.ottavi@seenovate.com)")
        st.markdown("[Thibault ZIBERT](mailto:thibault.zibert@seenovate.com)")
    st.markdown(
        '<p style="text-align:center;font-size:0.6rem;color:#94A3B8;margin:8px 0 0 0;">v1.0 — 2026</p>',
        unsafe_allow_html=True,
    )

page.run()
