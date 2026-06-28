# Page Informations generales sans gestion, peageur, niveaux
# Co-authored with CoCo
import streamlit as st
from core.queries import (
    get_parks, get_villes, get_secteurs, get_districts, get_type,
    get_flag, insert_park, update_park, delete_park, get_history,
    park_code_exists
)
from core.functions import (
    show_notification, notify
)
import pandas as pd

user = st.user.user_name

show_notification()

st.title("📋 Informations générales")
st.caption(f"Gestion du référentiel des parcs — Connecté : **{user}**")
st.divider()

df_parks = get_parks()
df_villes = get_villes()
df_secteurs = get_secteurs()
df_districts = get_districts()
df_type = get_type()
df_flag_fourriere = get_flag()
df_flag_metstation = get_flag()

ville_dict = dict(zip(df_villes["CODE_VILLE"], df_villes["LIBELLE_VILLE"]))
secteur_dict = dict(zip(df_secteurs["CODE_SECTEUR"], df_secteurs["LIBELLE_SECTEUR"]))
district_dict = dict(zip(df_districts["CODE_DISTRICT"], df_districts["LIBELLE_DISTRICT"]))
type_dict = dict(zip(df_type["CODE_TYPE_PARC"], df_type["LIBELLE_TYPE_PARC"]))
fourriere_dict = dict(zip(df_flag_fourriere["CODE_FLAG"], df_flag_fourriere["LIBELLE_FLAG"]))
metstation_dict = dict(zip(df_flag_metstation["CODE_FLAG"], df_flag_metstation["LIBELLE_FLAG"]))

ville_labels = {code: lib for code, lib in ville_dict.items()}
secteur_labels = {code: lib for code, lib in secteur_dict.items()}
district_labels = {code: lib for code, lib in district_dict.items()}
type_labels = {code: lib for code, lib in type_dict.items()}
fourriere_labels = {code: lib for code, lib in fourriere_dict.items()}
metstation_labels = {code: lib for code, lib in metstation_dict.items()}

df_view = df_parks.copy()
if not df_view.empty:
    df_view["VILLE"] = df_view["CODE_VILLE"].map(ville_labels)
    df_view["SECTEUR"] = df_view["CODE_SECTEUR"].map(secteur_labels)
    df_view["DISTRICT"] = df_view["CODE_DISTRICT"].map(district_labels)
    df_view["TYPE"] = df_view["CODE_TYPE_PARC"].map(type_labels)
    df_view["FOURRIERE"] = df_view["CODE_FLAG_FOURRIERE"].map(fourriere_labels)
    df_view["METSTATION"] = df_view["CODE_FLAG_METSTATION"].map(metstation_labels)

DISPLAY_COLS = ["CODE_PARC", "NOM_PARC", "ADRESSE_PARC", "VILLE", "SECTEUR", "DISTRICT", "TYPE", "FOURRIERE", "METSTATION"]

tab_search, tab_create, tab_edit, tab_delete, tab_history = st.tabs([
    "🔍 Rechercher", "➕ Créer", "✏️ Modifier", "🗑️ Supprimer", "📜 Historique"
])

with tab_search:
    st.subheader("Rechercher un parc")
    search_term = st.text_input("🔍 Recherche", placeholder="Tapez votre recherche...", key="search_info")
    if df_view.empty:
        st.info("Aucun parc actif.")
    else:
        if search_term:
            term = search_term.lower()
            mask = pd.Series([False] * len(df_view))
            for col in DISPLAY_COLS:
                if col in df_view.columns:
                    mask = mask | df_view[col].astype(str).str.lower().str.contains(term, na=False)
            df_results = df_view[mask]
        else:
            df_results = df_view
        st.caption(f"{len(df_results)} parc(s)")
        st.dataframe(df_results[DISPLAY_COLS], use_container_width=True, hide_index=True,
            column_config={
                "CODE_PARC": st.column_config.TextColumn("Code Parc", width="small"),
                "NOM_PARC": st.column_config.TextColumn("Nom Parc", width="medium"),
                "ADRESSE_PARC": st.column_config.TextColumn("Adresse"),
                "VILLE": st.column_config.TextColumn("Ville"),
                "SECTEUR": st.column_config.TextColumn("Secteur"),
                "DISTRICT": st.column_config.TextColumn("District"),
                "TYPE": st.column_config.TextColumn("Type d'ouvrage"),
                "FOURRIERE": st.column_config.TextColumn("Fourrière"),
                "METSTATION": st.column_config.TextColumn("Metstation"),
            })

with tab_create:
    st.subheader("Nouveau parc")
    col1, col2 = st.columns(2)
    with col1:
        code_parc = st.text_input("Code parc *", key="c_code")
        nom = st.text_input("Nom parc *", key="c_nom")
        adresse = st.text_input("Adresse", key="c_adresse")
        ville_options = {v: k for k, v in ville_labels.items()}
        ville = st.selectbox("Ville", list(ville_options.keys()), key="c_ville")
        code_ville = ville_options[ville]
        secteur_options = {v: k for k, v in secteur_labels.items()}
        secteur = st.selectbox("Secteur", list(secteur_options.keys()), key="c_secteur")
        code_secteur = secteur_options[secteur]
    with col2:
        district_options = {v: k for k, v in district_labels.items()}
        district = st.selectbox("District", list(district_options.keys()), key="c_district")
        code_district = district_options[district]
        type_options = {v: k for k, v in type_labels.items()}
        type_parc = st.selectbox("Type d'ouvrage", list(type_options.keys()), key="c_type")
        code_type = type_options[type_parc]
        fourriere_options = {v: k for k, v in fourriere_labels.items()}
        fourriere = st.selectbox("Fourrière", list(fourriere_options.keys()), key="c_fourriere")
        code_fourriere = fourriere_options[fourriere]
        metstation_options = {v: k for k, v in metstation_labels.items()}
        metstation = st.selectbox("Metstation", list(metstation_options.keys()), key="c_metstation")
        code_metstation = metstation_options[metstation]
    st.divider()
    if st.button("Créer le parc", type="primary", key="btn_create"):
        if not code_parc or not nom:
            st.error("Le code parc et le nom sont obligatoires.")
        elif park_code_exists(code_parc.strip().upper()):
            st.error(f"Le code parc **{code_parc}** existe déjà. Veuillez utiliser un code unique.")
        elif not df_parks.empty and nom.strip().upper() in df_parks["NOM_PARC"].str.upper().values:
            st.error(f"Le nom de parc **{nom}** existe déjà. Veuillez utiliser un nom unique.")
        else:
            insert_park({
                "CODE_PARC": code_parc.strip().upper(), "NOM_PARC": nom, "ADRESSE_PARC": adresse,
                "CODE_VILLE": code_ville, "CODE_SECTEUR": code_secteur,
                "CODE_DISTRICT": code_district, "CODE_TYPE_PARC": code_type,
                "CODE_FLAG_FOURRIERE": code_fourriere, "CODE_FLAG_METSTATION": code_metstation,
                "NOM_CREATEUR": user, "NOM_MODIFICATEUR": user
            })
            notify("✅ Parc créé avec succès", "success")
            st.rerun()

with tab_edit:
    st.subheader("Modifier un parc existant")
    if df_parks.empty:
        st.info("Aucun parc à modifier.")
    else:
        parc_list = df_parks["CODE_PARC"].tolist()
        parc_names = df_parks.set_index("CODE_PARC")["NOM_PARC"].to_dict()
        options = [parc_names.get(code, code) for code in parc_list]

        selected_idx = st.selectbox("Sélectionner un parc", range(len(options)),
                                     format_func=lambda i: options[i], key="edit_select")
        selected_row = df_parks.iloc[selected_idx]
        pk = selected_row["CODE_PARC"]
        st.divider()
        with st.form(key=f"form_edit_{pk}"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom parc", value=selected_row["NOM_PARC"] or "")
                adresse = st.text_input("Adresse", value=selected_row["ADRESSE_PARC"] or "")
                ville_options = {v: k for k, v in ville_labels.items()}
                ville_keys = list(ville_options.keys())
                default_ville = ville_labels.get(selected_row["CODE_VILLE"], "")
                ville_idx = ville_keys.index(default_ville) if default_ville in ville_keys else 0
                ville = st.selectbox("Ville", ville_keys, index=ville_idx)
                code_ville = ville_options[ville]
                secteur_options = {v: k for k, v in secteur_labels.items()}
                secteur_keys = list(secteur_options.keys())
                default_secteur = secteur_labels.get(selected_row["CODE_SECTEUR"], "")
                secteur_idx = secteur_keys.index(default_secteur) if default_secteur in secteur_keys else 0
                secteur = st.selectbox("Secteur", secteur_keys, index=secteur_idx)
                code_secteur = secteur_options[secteur]
            with col2:
                district_options = {v: k for k, v in district_labels.items()}
                district_keys = list(district_options.keys())
                default_district = district_labels.get(selected_row["CODE_DISTRICT"], "")
                district_idx = district_keys.index(default_district) if default_district in district_keys else 0
                district = st.selectbox("District", district_keys, index=district_idx)
                code_district = district_options[district]
                type_options = {v: k for k, v in type_labels.items()}
                type_keys = list(type_options.keys())
                default_type = type_labels.get(selected_row["CODE_TYPE_PARC"], "")
                type_idx = type_keys.index(default_type) if default_type in type_keys else 0
                type_parc = st.selectbox("Type d'ouvrage", type_keys, index=type_idx)
                code_type = type_options[type_parc]
                fourriere_options = {v: k for k, v in fourriere_labels.items()}
                fourriere_keys = list(fourriere_options.keys())
                default_fourriere = fourriere_labels.get(selected_row["CODE_FLAG_FOURRIERE"], "")
                fourriere_idx = fourriere_keys.index(default_fourriere) if default_fourriere in fourriere_keys else 0
                fourriere = st.selectbox("Fourrière", fourriere_keys, index=fourriere_idx)
                code_fourriere = fourriere_options[fourriere]
                metstation_options = {v: k for k, v in metstation_labels.items()}
                metstation_keys = list(metstation_options.keys())
                default_metstation = metstation_labels.get(selected_row["CODE_FLAG_METSTATION"], "")
                metstation_idx = metstation_keys.index(default_metstation) if default_metstation in metstation_keys else 0
                metstation = st.selectbox("Metstation", metstation_keys, index=metstation_idx)
                code_metstation = metstation_options[metstation]
            submitted = st.form_submit_button("Mettre à jour", type="primary")
        if submitted:
            update_park({
                "CODE_PARC": pk, "NOM_PARC": nom, "ADRESSE_PARC": adresse,
                "CODE_VILLE": code_ville, "CODE_SECTEUR": code_secteur,
                "CODE_DISTRICT": code_district, "CODE_TYPE_PARC": code_type,
                "CODE_FLAG_FOURRIERE": code_fourriere, "CODE_FLAG_METSTATION": code_metstation,
                "NOM_CREATEUR": user, "NOM_MODIFICATEUR": user
            })
            notify("✅ Parc mis à jour avec succès", "success")
            st.rerun()

with tab_delete:
    st.subheader("Supprimer un parc")
    if df_parks.empty:
        st.info("Aucun parc à supprimer.")
    else:
        parc_list = df_parks["CODE_PARC"].tolist()
        parc_names = df_parks.set_index("CODE_PARC")["NOM_PARC"].to_dict()
        options_del = [f"{code} — {parc_names.get(code, '')}" for code in parc_list]
        selected_del_idx = st.selectbox("Sélectionner le parc à supprimer", range(len(options_del)),
                                         format_func=lambda i: options_del[i], key="del_select")
        code_to_delete = parc_list[selected_del_idx]
        st.warning(f"⚠️ Vous allez supprimer le parc **{code_to_delete}** — **{parc_names.get(code_to_delete, '')}**")
        st.divider()

        @st.dialog("Confirmation de suppression")
        def confirm_delete(code, nom):
            st.markdown(
                f"Vous vous apprêtez à supprimer le parc **{code}** — **{nom}**.\n\n"
                "Cette action est irréversible. Confirmez-vous la suppression ?"
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Annuler", key="btn_cancel_delete", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("Supprimer", type="primary", key="btn_confirm_delete", use_container_width=True):
                    delete_park(code, user)
                    notify("🗑️ Parc supprimé", "warning")
                    st.rerun()

        if st.button("Supprimer ce parc", type="primary", key="btn_delete"):
            confirm_delete(code_to_delete, parc_names.get(code_to_delete, ""))

with tab_history:
    @st.fragment
    def show_history_info():
        st.subheader("Historique des modifications")
        if df_parks.empty:
            st.info("Aucun parc.")
        else:
            parc_list = df_parks["CODE_PARC"].tolist()
            parc_names = df_parks.set_index("CODE_PARC")["NOM_PARC"].to_dict()
            options_hist = [f"{code} — {parc_names.get(code, '')}" for code in parc_list]
            with st.form(key="form_hist_info"):
                selected_hist_idx = st.selectbox("Sélectionner un parc", range(len(options_hist)),
                                                  format_func=lambda i: options_hist[i], key="hist_select")
                submitted_hist = st.form_submit_button("Afficher l'historique", type="primary")
            if submitted_hist:
                code_hist = parc_list[selected_hist_idx]

                from core.db import get_session
                session = get_session()
                df_hist = session.sql(f"""
                    SELECT * FROM S_REFERENTIEL.T_R_PARC
                    WHERE CODE_PARC = '{code_hist}'
                    ORDER BY DATE_DEBUT DESC
                """).to_pandas()

                if df_hist.empty:
                    st.info("Aucun historique pour ce parc.")
                else:
                    df_h = df_hist.copy()
                    df_h["VILLE"] = df_h["CODE_VILLE"].map(ville_labels)
                    df_h["SECTEUR"] = df_h["CODE_SECTEUR"].map(secteur_labels)
                    df_h["DISTRICT"] = df_h["CODE_DISTRICT"].map(district_labels)
                    df_h["TYPE"] = df_h["CODE_TYPE_PARC"].map(type_labels)
                    df_h["FOURRIERE"] = df_h["CODE_FLAG_FOURRIERE"].map(fourriere_labels)
                    df_h["METSTATION"] = df_h["CODE_FLAG_METSTATION"].map(metstation_labels)
                    st.caption(f"Historique du parc **{code_hist}** — {len(df_h)} version(s)")
                    st.dataframe(
                        df_h[["CODE_PARC", "NOM_PARC", "ADRESSE_PARC", "VILLE", "SECTEUR", "DISTRICT", "TYPE",
                              "FOURRIERE", "METSTATION", "DATE_CREATION", "NOM_CREATEUR",
                              "DATE_MODIFICATION", "NOM_MODIFICATEUR", "DATE_DEBUT", "DATE_FIN", "IS_ACTIVE"]],
                        use_container_width=True, hide_index=True,
                        column_config={
                            "CODE_PARC": st.column_config.TextColumn("Code Parc"),
                            "NOM_PARC": st.column_config.TextColumn("Nom Parc"),
                            "ADRESSE_PARC": st.column_config.TextColumn("Adresse"),
                            "VILLE": st.column_config.TextColumn("Ville"),
                            "SECTEUR": st.column_config.TextColumn("Secteur"),
                            "DISTRICT": st.column_config.TextColumn("District"),
                            "TYPE": st.column_config.TextColumn("Type d'ouvrage"),
                            "FOURRIERE": st.column_config.TextColumn("Fourrière"),
                            "METSTATION": st.column_config.TextColumn("Metstation"),
                            "DATE_CREATION": st.column_config.DatetimeColumn("Date création", format="DD/MM/YYYY HH:mm"),
                            "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
                            "DATE_MODIFICATION": st.column_config.DatetimeColumn("Date modification", format="DD/MM/YYYY HH:mm"),
                            "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
                            "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                            "DATE_FIN": st.column_config.TextColumn("Date fin"),
                            "IS_ACTIVE": st.column_config.TextColumn("Actif"),
                        }
                    )

    show_history_info()
