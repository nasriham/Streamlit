# Page Juridique avec onglets et formulaire de modification (sans suppression)
# Co-authored with CoCo
import streamlit as st
import pandas as pd
from core.queries import (
    get_parks,
    get_flag,
    get_nature_juridique,
    get_parks_juridique,
    update_juridique,
    insert_park_juridique,
    get_history_juridique
)
from core.functions import (
    show_notification,
    notify
)

user = st.user.user_name

show_notification()

st.title("⚖️ Juridique")
st.caption(f"Informations juridiques des parcs — Connecté : **{user}**")
st.divider()

df = get_parks_juridique()
df_parks_ref = get_parks()
df_flag = get_flag()
df_nature = get_nature_juridique()

flag_dict = dict(zip(df_flag["CODE_FLAG"], df_flag["LIBELLE_FLAG"]))
flag_labels = {code: lib for code, lib in flag_dict.items()}
nature_dict = dict(zip(df_nature["CODE_NATURE_JURIDIQUE"], df_nature["LIBELLE_NATURE_JURIDIQUE"]))
nature_labels = {code: lib for code, lib in nature_dict.items()}

# Joindre NOM_PARC
parc_names = df_parks_ref.set_index("CODE_PARC")["NOM_PARC"].to_dict()
if not df.empty:
    df["NOM_PARC"] = df["CODE_PARC"].map(parc_names)

tab_search, tab_edit, tab_history = st.tabs([
    "🔍 Rechercher", "✏️ Modifier", "📜 Historique"
])

# ===== CONSULTER =====
with tab_search:
    st.subheader("Données juridiques")
    search = st.text_input("🔍 Rechercher", key="search_jur")
    if df.empty:
        st.info("Aucune donnée juridique.")
    else:
        df_d = df.copy()
        df_d["NATURE"] = df_d["CODE_NATURE_JURIDIQUE"].map(nature_labels)
        df_d["COPRO"] = df_d["CODE_FLAG_COPRO"].map(flag_labels)
        display_cols = [c for c in ["NOM_PARC", "MISE_EN_SERVICE", "NATURE", "TYPE_CONVENTION", "NOM_TIERS_ATTENANT", "SIRET", "COPRO", "NOM_COPRO", "NOM_CREATEUR", "NOM_MODIFICATEUR", "DATE_DEBUT", "DATE_FIN", "IS_ACTIVE"] if c in df_d.columns]
        df_d = df_d[display_cols]
        if search:
            term = search.lower()
            mask = pd.Series([False] * len(df_d))
            for col in display_cols:
                mask = mask | df_d[col].astype(str).str.lower().str.contains(term, na=False)
            df_d = df_d[mask]
        st.caption(f"{len(df_d)} ligne(s)")
        st.dataframe(df_d, use_container_width=True, hide_index=True, column_config={
            "NOM_PARC": st.column_config.TextColumn("Nom Parc", width="medium"),
            "MISE_EN_SERVICE": st.column_config.TextColumn("Mise en service"),
            "NATURE": st.column_config.TextColumn("Nature"),
            "TYPE_CONVENTION": st.column_config.TextColumn("Type de convention"),
            "NOM_TIERS_ATTENANT": st.column_config.TextColumn("Nom tiers attenant au parc"),
            "SIRET": st.column_config.TextColumn("SIRET"),
            "COPRO": st.column_config.TextColumn("Copro"),
            "NOM_COPRO": st.column_config.TextColumn("Nom copro"),
            "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
            "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
            "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
            "DATE_FIN": st.column_config.TextColumn("Date fin"),
            "IS_ACTIVE": st.column_config.TextColumn("Actif"),
        })

# ===== MODIFIER =====
with tab_edit:
    st.subheader("Modifier les données juridiques")
    if df.empty:
        st.info("Aucune donnée.")
    else:
        mod_options = [str(row.get('NOM_PARC') or row['CODE_PARC']) for _, row in df.iterrows()]
        sel_mod_idx = st.selectbox("Sélectionner un parc", range(len(mod_options)),
                                    format_func=lambda i: mod_options[i], key="jur_mod_select")
        sel = df.iloc[sel_mod_idx]
        pk = sel["CODE_PARC"]

        st.divider()
        with st.form(key=f"form_jur_{pk}"):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Parc", value=f"{pk} — {sel.get('NOM_PARC', '')}", disabled=True)
                mise_en_service = st.text_input("Mise en service", value=sel.get("MISE_EN_SERVICE") or "")
                nature_options = {v: k for k, v in nature_labels.items()}
                nature_keys = list(nature_options.keys())
                default_nature = nature_labels.get(sel.get("CODE_NATURE_JURIDIQUE"), "")
                nature_idx = nature_keys.index(default_nature) if default_nature in nature_keys else 0
                nature = st.selectbox("Nature juridique", nature_keys, index=nature_idx)
                code_nature = nature_options[nature]
                siret = st.text_input("SIRET (chiffres uniquement)", value=sel.get("SIRET") or "")
            with col2:
                copro_options = {v: k for k, v in flag_labels.items()}
                copro_keys = list(copro_options.keys())
                default_copro = flag_labels.get(sel.get("CODE_FLAG_COPRO"), "")
                copro_idx = copro_keys.index(default_copro) if default_copro in copro_keys else 0
                copro = st.selectbox("Copropriété", copro_keys, index=copro_idx)
                code_copro = copro_options[copro]
                type_conv = st.text_input("Type convention", value=sel.get("TYPE_CONVENTION") or "")
                nom_tiers = st.text_input("Nom tiers attenant", value=sel.get("NOM_TIERS_ATTENANT") or "")
                nom_copro = st.text_input("Nom copropriété", value=sel.get("NOM_COPRO") or "")
            submitted = st.form_submit_button("Mettre à jour", type="primary")

        if submitted:
            if siret and not siret.strip().isdigit():
                st.error("Le SIRET doit contenir uniquement des chiffres.")
            else:
                update_juridique({
                    "CODE_PARC": pk, "MISE_EN_SERVICE": mise_en_service,
                    "CODE_NATURE_JURIDIQUE": code_nature, "SIRET": siret.strip() if siret else None,
                    "CODE_FLAG_COPRO": code_copro, "TYPE_CONVENTION": type_conv,
                    "NOM_TIERS_ATTENANT": nom_tiers, "NOM_COPRO": nom_copro,
                }, user)
                notify("✅ Données juridiques mises à jour", "success")
                st.rerun()

# ===== HISTORIQUE =====
with tab_history:
    st.subheader("Historique")

    if df.empty:
        st.info("Aucun parc.")
    else:
        from core.db import get_session
        session = get_session()
        parc_codes = df["CODE_PARC"].unique().tolist()
        hist_options = [f"{code} — {parc_names.get(code, '')}" for code in parc_codes]
        with st.form(key="form_hist_jur"):
            sel_h_idx = st.selectbox("Parc", range(len(hist_options)), format_func=lambda i: hist_options[i], key="jur_hist_select")
            submitted_hist = st.form_submit_button("Afficher l'historique", type="primary")
        if submitted_hist:
            sel_h = parc_codes[sel_h_idx]

            df_hist = session.sql(f"""
                SELECT CODE_PARC, MISE_EN_SERVICE, CODE_NATURE_JURIDIQUE, SIRET,
                       CODE_FLAG_COPRO, TYPE_CONVENTION, NOM_TIERS_ATTENANT, NOM_COPRO,
                       DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR,
                       DATE_DEBUT, DATE_FIN, IS_ACTIVE
                FROM S_REFERENTIEL.T_R_PARC_JURIDIQUE
                WHERE CODE_PARC = '{sel_h}' ORDER BY DATE_DEBUT DESC
            """).to_pandas()

            if df_hist.empty:
                st.info("Aucun historique pour ce parc.")
            else:
                st.caption(f"{len(df_hist)} version(s) pour **{sel_h}**")
                st.dataframe(df_hist, use_container_width=True, hide_index=True, column_config={
                    "CODE_PARC": st.column_config.TextColumn("Code Parc"),
                    "MISE_EN_SERVICE": st.column_config.TextColumn("Mise en service"),
                    "CODE_NATURE_JURIDIQUE": st.column_config.TextColumn("Nature"),
                    "SIRET": st.column_config.TextColumn("SIRET"),
                    "CODE_FLAG_COPRO": st.column_config.TextColumn("Copro"),
                    "TYPE_CONVENTION": st.column_config.TextColumn("Type de convention"),
                    "NOM_TIERS_ATTENANT": st.column_config.TextColumn("Nom tiers attenant au parc"),
                    "NOM_COPRO": st.column_config.TextColumn("Nom copro"),
                    "DATE_CREATION": st.column_config.DatetimeColumn("Date création", format="DD/MM/YYYY HH:mm"),
                    "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
                    "DATE_MODIFICATION": st.column_config.DatetimeColumn("Date modification", format="DD/MM/YYYY HH:mm"),
                    "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                    "DATE_FIN": st.column_config.TextColumn("Date fin"),
                    "IS_ACTIVE": st.column_config.TextColumn("Actif"),
                })
