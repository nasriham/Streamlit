import streamlit as st
import pandas as pd
from core.queries import (
    get_parks_incendie,
    insert_incendie,
    update_incendie
)
from core.functions import (
    has_changed
)

# =========================
# ⚙️ CONFIG (DOIT ÊTRE EN HAUT)
# =========================
st.set_page_config(
    page_title="Exploitation des parcs - Incendie",
    layout="wide"
)

# =========================
# 👤 USER
# =========================
user = getattr(st.user, "user_name", "SYSTEM")


# =========================
# 💬 MESSAGES
# =========================
if "message" in st.session_state:
    if st.session_state["message_type"] == "success":
        st.success(st.session_state["message"])
    elif st.session_state["message_type"] == "warning":
        st.warning(st.session_state["message"])

    del st.session_state["message"]
    del st.session_state["message_type"]

# =========================
# 🧾 HEADER
# =========================
col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.png", width=100)

with col2:
    st.title("🚗 Information incendie des parcs ")

# =========================
# 📦 LOAD
# =========================
df = get_parks_incendie()

# =========================
# ✏️ EDITOR
# =========================

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic"
)

# =========================
# 💾 SAVE
# =========================
if st.button("💾 Sauvegarder"):

    base = df.copy()

    nb_insert = 0
    nb_update = 0

    # nettoyage global
    edited_df = edited_df.astype(object).where(pd.notnull(edited_df), None)

    for _, row in edited_df.iterrows():

        row_dict = row.to_dict()
        code = row_dict["CODE_PARC"]

        old = base[base["CODE_PARC"] == code]

        # ➕ INSERT
        if old.empty:
            insert_incendie(row_dict, user)
            nb_insert += 1
            continue

        old = old.iloc[0]

        # 🔍 UPDATE si changement
        if has_changed(old, row):
            update_incendie(row_dict, user)
            nb_update += 1
            
    # =========================
    # 💬 MESSAGE
    # =========================
    st.session_state["message"] = f"✅ {nb_update} mises à jour / {nb_insert} insertions"
    st.session_state["message_type"] = "success"

    st.rerun()