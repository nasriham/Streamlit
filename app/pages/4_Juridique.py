import streamlit as st
import pandas as pd
from datetime import datetime
from core.queries import (
    get_flag,
    get_nature_juridique,
    get_parks_juridique,
    update_juridique,
    insert_park_juridique,
    get_history_juridique
)
from core.functions import (
    has_changed
)

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(page_title="Gestion Parc Juridique", layout="wide")

st.title("🏢 Gestion des informations Parc Juridique")

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
df_parks_juridique = get_parks_juridique()
df_flag = get_flag()
df_nature = get_nature_juridique()
df_history = get_history_juridique()

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
    "CODE_FLAG_COPRO"
]

# dict nature
mapping_nature = dict(
    zip(
        df_nature["CODE_NATURE_JURIDIQUE"],
        df_nature["LIBELLE_NATURE_JURIDIQUE"]
    )
)

# dict : Oui -> 1
reverse_mapping_nature = dict(
    zip(
        df_nature["LIBELLE_NATURE_JURIDIQUE"],
        df_nature["CODE_NATURE_JURIDIQUE"]
    )
)

# liste des valeurs dropdown
nature_options = df_nature["LIBELLE_NATURE_JURIDIQUE"].tolist()

nature_columns = [
    "CODE_NATURE_JURIDIQUE"
]

# =========================================================
# AFFICHAGE
# =========================================================

display_df = df_parks_juridique.copy()

for col in flag_columns:
    display_df[col] = display_df[col].map(mapping)

for col in nature_columns:
    display_df[col] = display_df[col].map(mapping_nature)
    
edited_df = st.data_editor(
    display_df,
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    column_config={

        "CODE_PARC": st.column_config.TextColumn(
            "Code Parc"
        ),

        "MISE_EN_SERVICE": st.column_config.TextColumn(
            "Mise en service"
        ),

        "CODE_NATURE_JURIDIQUE": st.column_config.SelectboxColumn(
            "Nature",
            options=nature_options,
            required=True
        ),

        "SIRET": st.column_config.TextColumn(
            "SIRET"
        ),
        
        "CODE_FLAG_COPRO": st.column_config.SelectboxColumn(
            "Copro",
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

    base = df_parks_juridique.copy()

    save_df = edited_df.copy() 
    
    # Remap libellés -> valeurs 
    for col in flag_columns: 
        edited_df[col] = edited_df[col].map(reverse_mapping)
    for col in nature_columns: 
        edited_df[col] = edited_df[col].map(reverse_mapping_nature)

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
            insert_park_juridique(row_dict, user)
            nb_insert += 1
            continue

        old = old.iloc[0]

        # 🔍 UPDATE si changement
        if has_changed(old, row):
            update_juridique(row_dict, user)
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
    for col in nature_columns:
        df_history[col] = df_history[col].map(mapping_nature)

    st.dataframe(
        df_history,
        use_container_width=True,
        hide_index=True
    )