import streamlit as st

# -- Page config --
st.set_page_config(
    page_title="MetPark - Gestion des évènements",
    page_icon="🅿️",
    layout="wide",
)

# -- Logo MetPark (carré orange, coins arrondis, MTPK blanc) --
LOGO_SVG = """
<div style="text-align:center; padding: 10px 0 20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="120" height="120">
  <rect width="200" height="200" rx="24" fill="#F05A28"/>
  <text x="52" y="95" font-family="'Helvetica Neue',Arial,sans-serif" font-size="52" font-weight="600" fill="#FFFFFF" letter-spacing="4">MT</text>
  <text x="52" y="158" font-family="'Helvetica Neue',Arial,sans-serif" font-size="52" font-weight="600" fill="#FFFFFF" letter-spacing="4">PK</text>
</svg>
<p style="margin:8px 0 0 0; font-size:13px; color:#666; font-weight:500;">Gestion des évènements</p>
</div>
"""

with st.sidebar:
    st.markdown(LOGO_SVG, unsafe_allow_html=True)
    st.markdown("---")

# -- Navigation --
page = st.navigation([
    st.Page("pages/gestion_evenements.py", title="Gestion des évènements", icon="📋"),
    st.Page("pages/occupation_parking.py", title="Occupation Parking", icon="🚗"),
])

page.run()
