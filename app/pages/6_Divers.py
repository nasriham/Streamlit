import streamlit as st
import pandas as pd
from datetime import datetime
from core.queries import (
    get_flag,
    get_parks_divers,
    update_divers,
    insert_park_divers,
    get_history_divers
)
from core.functions import (
    has_changed
)

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(page_title="Gestion Parc Informations Diverses", layout="wide")

st.title("🏢 Gestion Parc Informations Diverses")

# =========================================================
# USER
# =========================================================

user = st.user.user_name

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
# 📦 LOAD DATA
# =========================
df_parks_divers = get_parks_divers()
df_flag = get_flag()
df_history = get_history_divers()

# dict : 1 -> Oui
mapping = dict(
    zip(
        df_flag["CODE_FLAG"],
        df_flag["LIBELLE_FLAG"]
    )
)

# dict : Oui -> 1
reverse_mapping = dict(
    zip(
        df_flag["LIBELLE_FLAG"],
        df_flag["CODE_FLAG"]
    )
)

# liste des valeurs dropdown
flag_options = df_flag["LIBELLE_FLAG"].tolist()

flag_columns = [
    "CODE_FLAG_PRESENCE_HUMAINE",
    "CODE_FLAG_LAPI"
]

# =========================================================
# AFFICHAGE
# =========================================================

display_df = df_parks_divers.copy()

for col in flag_columns:
    display_df[col] = display_df[col].map(mapping)

edited_df = st.data_editor(
    display_df,
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    column_config={

        "CODE_PARC": st.column_config.TextColumn(
            "Code Parc"
        ),

        "GABARIT_STANDARD": st.column_config.TextColumn(
            "Gabarit standard"
        ),

        "CODE_FLAG_PRESENCE_HUMAINE": st.column_config.SelectboxColumn(
            "Présence Humaine",
            options=flag_options,
            required=True
        ),

        "NB_ASCENCEURS": st.column_config.NumberColumn(
            "Nombre d'ascenceurs",
            required=False
        ),
  
        "NB_PEAGEURS": st.column_config.NumberColumn(
            "Nombre de péageurs",
            required=False
        ),
        
        "CODE_FLAG_LAPI": st.column_config.SelectboxColumn(
            "LAPI",
            options=flag_options,
            required=True
        ),

        "NOM_CREATEUR": st.column_config.TextColumn(
            "Créateur",
            disabled=True
        ),

        "NOM_MODIFICATEUR": st.column_config.TextColumn(
            "Modificateur",
            disabled=True
        ),

        "DATE_DEBUT": st.column_config.DateColumn(
            "Date début",
            disabled=True
        ),

        "DATE_FIN": st.column_config.DateColumn(
            "Date fin",
            disabled=True
        ),

        "IS_ACTIVE": st.column_config.CheckboxColumn(
            "Actif",
            disabled=True
        )
    }
)

# =========================
# 💾 SAVE
# =========================
if st.button("💾 Sauvegarder"):

    base = df_parks_divers.copy()

    save_df = edited_df.copy() 
    
    # Remap libellés -> valeurs 
    for col in flag_columns: 
        edited_df[col] = edited_df[col].map(reverse_mapping)

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
            insert_park_divers(row_dict, user)
            nb_insert += 1
            continue

        old = old.iloc[0]

        # 🔍 UPDATE si changement
        if has_changed(old, row):
            update_divers(row_dict, user)
            nb_update += 1
            
    # =========================
    # 💬 MESSAGE
    # =========================
    st.session_state["message"] = f"✅ {nb_update} mises à jour / {nb_insert} insertions"
    st.session_state["message_type"] = "success"

    st.rerun()

# =========================================================
# HISTORIQUE
# =========================================================

st.divider()

with st.expander("📜 Historique complet"):

    for col in flag_columns:
        df_history[col] = df_history[col].map(mapping)

    st.dataframe(
        df_history,
        use_container_width=True,
        hide_index=True
    )