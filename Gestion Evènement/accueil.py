import streamlit as st
from core.db import ENV

# -- Bandeau environnement --
if ENV == "DEV":
    st.error("🚧 ENVIRONNEMENT DEVELOPPEMENT")
elif ENV == "QUA":
    st.warning("🧪 ENVIRONNEMENT QUALIFICATION")
elif ENV == "PPD":
    st.success("✅ ENVIRONNEMENT PRE-PRODUCTION")

# -- Logo MetPark --
LOGO_SVG = """
<div style="display: flex; align-items: center; gap: 24px; padding: 20px 0;">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 180" width="100" height="128">
    <circle cx="70" cy="65" r="55" fill="#E8692A"/>
    <text x="70" y="55" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MT</text>
    <text x="70" y="82" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PK</text>
    <text x="32" y="155" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#2D3748" letter-spacing="1">MET</text>
    <text x="82" y="155" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#E8692A" letter-spacing="1">PARK</text>
  </svg>
  <div>
    <h1 style="margin:0; font-size:2.2rem;">Gestion des évènements</h1>
    <p style="margin:8px 0 0 0; color:#666; font-size:1rem;">Utilisez le menu à gauche pour naviguer dans les fonctions.</p>
  </div>
</div>
"""

st.markdown(LOGO_SVG, unsafe_allow_html=True)
