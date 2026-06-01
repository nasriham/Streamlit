import streamlit as st
import pandas as pd

from core.queries import (
    get_evenements, get_ref_types, get_ref_descriptions, get_ref_lieux, get_ref_impacts,
    get_parkings, get_parcs_evenement, get_historique_complet,
    insert_evenement, update_evenement, delete_evenement,
    insert_parc_evenement, delete_parcs_evenement, get_max_code_evenement,
    insert_type_evenement,
    close_all_snapshots
)
from core.functions import (
    get_current_user, search_evenements, log_modification,
    show_notification, notify
)

# -- User --
sf_user = get_current_user()

# -- Page title --
st.title("📋 Événements externes")
st.caption(f"Événements territoriaux se déroulant dans la ville ou à proximité — Connecté : **{sf_user}**")

# -- Notification --
show_notification()

# -- Tabs --
tab_search, tab_create, tab_edit, tab_delete, tab_history = st.tabs([
    "🔍 Rechercher", "➕ Créer", "✏️ Modifier", "🗑️ Supprimer", "📜 Historique"
])

CATEGORIE = "Externe"


# ===== TAB: RECHERCHE =====
with tab_search:
    st.subheader("Rechercher un événement externe")
    search_term = st.text_input("🔍 Recherche (titre, type, lieu, ville, impact, ID...)", placeholder="Tapez votre recherche ici...")

    df_events = get_evenements()
    # Filtrer uniquement les événements externes
    df_events = df_events[df_events["CATEGORIE"] == CATEGORIE] if not df_events.empty else df_events

    if df_events.empty:
        st.info("Aucun événement externe actif.")
    else:
        df_results = search_evenements(df_events, search_term)
        st.caption(f"{len(df_results)} événement(s) trouvé(s)")

        if not df_results.empty:
            display_cols = ["CODE_EVENEMENT", "TITRE_EVENEMENT", "TYPE_EVENEMENT",
                            "DESCRIPTION", "LIEU", "VILLE", "IMPACT",
                            "DATE_DEBUT", "DATE_FIN", "CRENEAU", "NB_PLACES_IMPACTEES",
                            "COMMENTAIRE"]
            available_cols = [c for c in display_cols if c in df_results.columns]
            st.dataframe(df_results[available_cols], use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre", width="medium"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "DESCRIPTION": st.column_config.TextColumn("Description"),
                    "LIEU": st.column_config.TextColumn("Lieu"),
                    "VILLE": st.column_config.TextColumn("Ville"),
                    "IMPACT": st.column_config.TextColumn("Impact"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY HH:mm"),
                    "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY HH:mm"),
                    "CRENEAU": st.column_config.TextColumn("Créneau"),
                    "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                    "COMMENTAIRE": st.column_config.TextColumn("Commentaire", width="large"),
                })


# ===== TAB: CREATION =====
with tab_create:
    st.subheader("Nouvel événement externe")

    df_types = get_ref_types()
    df_types_ext = df_types[df_types["CATEGORIE"] == CATEGORIE]
    df_lieux = get_ref_lieux()
    df_impacts = get_ref_impacts()
    df_parkings = get_parkings()

    with st.form("form_create_ext", clear_on_submit=True):
        titre = st.text_input("Titre de l'événement *", max_chars=300)

        # -- Type d'événement --
        st.markdown("##### Type d'événement")
        type_options = dict(zip(df_types_ext["LIBELLE_TYPE_EVENEMENT"], df_types_ext["CODE_TYPE_EVENEMENT"]))
        selected_type = st.selectbox(
            "Type *",
            options=[""] + list(type_options.keys()) + ["Autre (nouveau type)"],
            index=0
        )

        # Si "Autre" → saisie nouveau type
        nouveau_type_libelle = ""
        if selected_type == "Autre (nouveau type)":
            nouveau_type_libelle = st.text_input(
                "Nom du nouveau type *",
                max_chars=200,
                placeholder="Ex: Inauguration, Visite officielle..."
            )

        # -- Description prédéfinie --
        selected_desc = ""
        description_autre = ""
        desc_options = {}
        if selected_type and selected_type != "Autre (nouveau type)" and selected_type in type_options:
            code_type_selected = type_options[selected_type]
            df_descriptions = get_ref_descriptions(int(code_type_selected))
            if not df_descriptions.empty:
                desc_options = dict(zip(df_descriptions["LIBELLE_DESCRIPTION"], df_descriptions["CODE_DESCRIPTION"]))
                selected_desc = st.selectbox("Description / Libellé", options=[""] + list(desc_options.keys()))
            else:
                st.info("Pas de descriptions prédéfinies — utilisez le commentaire")

        if selected_desc == "Autre":
            description_autre = st.text_input("Préciser la description", max_chars=500)

        # -- Lieu et Impact --
        st.markdown("##### Localisation et impact")
        col1, col2 = st.columns(2)
        with col1:
            lieu_options = dict(zip(df_lieux["LIBELLE_LIEU"] + " - " + df_lieux["VILLE"], df_lieux["CODE_LIEU"]))
            selected_lieu = st.selectbox("Lieu", options=[""] + list(lieu_options.keys()), index=0)
        with col2:
            impact_options = dict(zip(
                df_impacts["LIBELLE_IMPACT"] + " (niv. " + df_impacts["NIVEAU_SEVERITE"].astype(str) + ")",
                df_impacts["CODE_IMPACT"]
            ))
            selected_impact = st.selectbox("Impact", options=[""] + list(impact_options.keys()), index=0)

        # -- Dates --
        st.markdown("##### Dates")
        col1, col2 = st.columns(2)
        with col1:
            date_debut = st.date_input("Date de début *", value=None)
            heure_debut = st.time_input("Heure de début", value=None)
        with col2:
            date_fin = st.date_input("Date de fin", value=None)
            heure_fin = st.time_input("Heure de fin", value=None)

        # Journée partielle
        is_journee_partielle = st.checkbox("📅 Journée partielle")
        creneau = None
        if is_journee_partielle:
            creneau = st.selectbox("Créneau", options=["Matin", "Après-midi", "Nuit"])

        # -- Parkings --
        st.markdown("##### Parkings impactés")
        parking_options = dict(zip(df_parkings["NOM_PARC"], df_parkings["CODE_PARC"]))
        selected_parkings = st.multiselect("Sélectionner les parkings impactés", options=list(parking_options.keys()))

        if len(selected_parkings) == 1:
            parc_info = df_parkings[df_parkings["NOM_PARC"] == selected_parkings[0]].iloc[0]
            if pd.notna(parc_info.get("CAPACITE")):
                st.info(f"📊 Capacité : **{int(parc_info['CAPACITE'])} places**")

        # -- Places impactées --
        is_places_impactees = st.checkbox("🅿️ Impact sur le nombre de places")
        nb_places_impactees = None
        fermeture_totale = False
        if is_places_impactees:
            fermeture_totale = st.checkbox("🚫 Fermeture totale (places disponibles = 0)")
            if not fermeture_totale:
                nb_places_impactees = st.number_input("Nombre de places impactées", min_value=0, value=0)

        # -- Pistes impactées --
        is_pistes_impactees = st.checkbox("🚧 Piste(s) impactée(s)")
        nb_pistes_entree = None
        nb_pistes_sortie = None
        if is_pistes_impactees:
            col1, col2 = st.columns(2)
            with col1:
                nb_pistes_entree = st.number_input("Nb pistes ENTRÉE fermées", min_value=0, value=0)
            with col2:
                nb_pistes_sortie = st.number_input("Nb pistes SORTIE fermées", min_value=0, value=0)

        # -- Commentaire --
        commentaire = st.text_area("Commentaire", max_chars=2000)

        # -- Submit --
        submitted = st.form_submit_button("💾 Créer l'événement", type="primary")

        if submitted:
            if not titre.strip():
                st.error("Le titre est obligatoire.")
            elif not selected_type:
                st.error("Le type d'événement est obligatoire.")
            elif selected_type == "Autre (nouveau type)" and not nouveau_type_libelle.strip():
                st.error("Veuillez saisir le nom du nouveau type.")
            elif date_debut is None:
                st.error("La date de début est obligatoire.")
            else:
                if selected_type == "Autre (nouveau type)":
                    code_type_final = insert_type_evenement(nouveau_type_libelle.strip(), CATEGORIE)
                else:
                    code_type_final = int(type_options[selected_type])

                heure_debut_str = heure_debut.strftime("%H:%M:%S") if heure_debut else "00:00:00"
                timestamp_debut = f"{date_debut} {heure_debut_str}"
                if date_fin:
                    heure_fin_str = heure_fin.strftime("%H:%M:%S") if heure_fin else "00:00:00"
                    timestamp_fin_sql = f"'{date_fin} {heure_fin_str}'"
                else:
                    timestamp_fin_sql = "NULL"

                code_description = None
                if selected_desc and selected_desc != "Autre" and selected_desc in desc_options:
                    code_description = int(desc_options[selected_desc])

                code_lieu = int(lieu_options[selected_lieu]) if selected_lieu else None
                code_impact = int(impact_options[selected_impact]) if selected_impact else None

                insert_evenement(
                    titre=titre,
                    code_type=code_type_final,
                    code_description=code_description,
                    description_autre=description_autre if selected_desc == "Autre" else None,
                    code_lieu=code_lieu,
                    code_impact=code_impact,
                    timestamp_debut=timestamp_debut,
                    timestamp_fin_sql=timestamp_fin_sql,
                    is_journee_partielle=is_journee_partielle,
                    creneau=creneau,
                    is_places_impactees=is_places_impactees,
                    nb_places_impactees=nb_places_impactees if is_places_impactees and not fermeture_totale else None,
                    fermeture_totale=fermeture_totale,
                    is_pistes_impactees=is_pistes_impactees,
                    nb_pistes_entree=nb_pistes_entree if is_pistes_impactees else None,
                    nb_pistes_sortie=nb_pistes_sortie if is_pistes_impactees else None,
                    type_travaux=None,
                    contact_interne=None,
                    contact_externe=None,
                    is_travaux_phases=False,
                    commentaire=commentaire,
                    user=sf_user
                )

                new_code = get_max_code_evenement()
                if selected_parkings:
                    for parc_name in selected_parkings:
                        insert_parc_evenement(new_code, int(parking_options[parc_name]), parc_name)

                log_modification(new_code, "CREATION", sf_user)
                notify("✅ Événement externe créé avec succès !")
                st.rerun()


# ===== TAB: MODIFICATION =====
with tab_edit:
    st.subheader("Modifier un événement externe")

    df_events_edit = get_evenements()
    df_events_edit = df_events_edit[df_events_edit["CATEGORIE"] == CATEGORIE] if not df_events_edit.empty else df_events_edit

    if df_events_edit.empty:
        st.info("Aucun événement externe à modifier.")
    else:
        df_types_edit = get_ref_types()
        df_types_edit = df_types_edit[df_types_edit["CATEGORIE"] == CATEGORIE]
        df_lieux_edit = get_ref_lieux()
        df_impacts_edit = get_ref_impacts()
        df_parkings_edit = get_parkings()

        search_edit = st.text_input("🔍 Rechercher", placeholder="Tapez pour filtrer...", key="search_edit_ext")
        df_edit_filtered = search_evenements(df_events_edit, search_edit)

        if df_edit_filtered.empty:
            st.warning("Aucun événement trouvé.")
        else:
            evt_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_edit_filtered.iterrows()}
            selected_edit = st.selectbox("Sélectionner l'événement", options=list(evt_options.keys()), key="edit_sel_ext")

            if selected_edit:
                code_edit = evt_options[selected_edit]
                evt_row = df_events_edit[df_events_edit["CODE_EVENEMENT"] == code_edit].iloc[0]

                with st.expander("📄 Valeurs actuelles", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Titre :** {evt_row['TITRE_EVENEMENT']}")
                        st.markdown(f"**Type :** {evt_row['TYPE_EVENEMENT']}")
                    with col2:
                        st.markdown(f"**Lieu :** {evt_row.get('LIEU', '-')}")
                        st.markdown(f"**Impact :** {evt_row.get('IMPACT', '-')}")
                    with col3:
                        st.markdown(f"**Début :** {evt_row['DATE_DEBUT']}")
                        st.markdown(f"**Fin :** {evt_row['DATE_FIN'] if pd.notna(evt_row['DATE_FIN']) else 'Non définie'}")

                with st.form("form_edit_ext"):
                    new_titre = st.text_input("Titre", placeholder="Laisser vide pour conserver", max_chars=300)

                    type_options_edit = dict(zip(df_types_edit["LIBELLE_TYPE_EVENEMENT"], df_types_edit["CODE_TYPE_EVENEMENT"]))
                    new_type = st.selectbox("Type", options=["-- Ne pas modifier --"] + list(type_options_edit.keys()))

                    col1, col2 = st.columns(2)
                    with col1:
                        lieu_options_edit = dict(zip(df_lieux_edit["LIBELLE_LIEU"] + " - " + df_lieux_edit["VILLE"], df_lieux_edit["CODE_LIEU"]))
                        new_lieu = st.selectbox("Lieu", options=["-- Ne pas modifier --"] + list(lieu_options_edit.keys()))
                    with col2:
                        impact_options_edit = dict(zip(
                            df_impacts_edit["LIBELLE_IMPACT"] + " (niv. " + df_impacts_edit["NIVEAU_SEVERITE"].astype(str) + ")",
                            df_impacts_edit["CODE_IMPACT"]
                        ))
                        new_impact = st.selectbox("Impact", options=["-- Ne pas modifier --"] + list(impact_options_edit.keys()))

                    col1, col2 = st.columns(2)
                    with col1:
                        new_date_debut = st.date_input("Date de début", value=None, key="ext_edit_dd")
                        new_heure_debut = st.time_input("Heure de début", value=None, key="ext_edit_hd")
                    with col2:
                        new_date_fin = st.date_input("Date de fin", value=None, key="ext_edit_df")
                        new_heure_fin = st.time_input("Heure de fin", value=None, key="ext_edit_hf")

                    new_commentaire = st.text_input("Commentaire", placeholder="Laisser vide pour conserver", max_chars=2000)

                    parking_options_edit = dict(zip(df_parkings_edit["NOM_PARC"], df_parkings_edit["CODE_PARC"]))
                    new_parkings = st.multiselect("Parkings (sélectionner pour remplacer)", options=list(parking_options_edit.keys()), default=[], key="ext_edit_park")

                    submitted_edit = st.form_submit_button("💾 Enregistrer", type="primary")

                    if submitted_edit:
                        set_parts = []
                        if new_titre.strip():
                            set_parts.append(f"TITRE_EVENEMENT = '{new_titre.replace(chr(39), chr(39)+chr(39))}'")
                        if new_type != "-- Ne pas modifier --":
                            set_parts.append(f"CODE_TYPE_EVENEMENT = {type_options_edit[new_type]}")
                        if new_lieu != "-- Ne pas modifier --":
                            set_parts.append(f"CODE_LIEU = {lieu_options_edit[new_lieu]}")
                        if new_impact != "-- Ne pas modifier --":
                            set_parts.append(f"CODE_IMPACT = {impact_options_edit[new_impact]}")
                        if new_date_debut is not None:
                            h = new_heure_debut.strftime("%H:%M:%S") if new_heure_debut else "00:00:00"
                            set_parts.append(f"DATE_DEBUT = '{new_date_debut} {h}'")
                        if new_date_fin is not None:
                            h = new_heure_fin.strftime("%H:%M:%S") if new_heure_fin else "00:00:00"
                            set_parts.append(f"DATE_FIN = '{new_date_fin} {h}'")
                        if new_commentaire.strip():
                            set_parts.append(f"COMMENTAIRE = '{new_commentaire.replace(chr(39), chr(39)+chr(39))}'")

                        if not set_parts and not new_parkings:
                            st.info("Aucune modification détectée.")
                        else:
                            if set_parts:
                                update_evenement(code_edit, set_parts, sf_user)
                            if new_parkings:
                                current_parcs = get_parcs_evenement(code_edit)
                                current_names = current_parcs["NOM_PARC"].tolist() if not current_parcs.empty else []
                                if sorted(new_parkings) != sorted(current_names):
                                    delete_parcs_evenement(code_edit)
                                    for p in new_parkings:
                                        insert_parc_evenement(code_edit, int(parking_options_edit[p]), p)
                            log_modification(code_edit, "MODIFICATION", sf_user)
                            notify("✏️ Événement modifié")
                            st.rerun()


# ===== TAB: SUPPRESSION =====
with tab_delete:
    st.subheader("Supprimer un événement externe")

    df_events_del = get_evenements()
    df_events_del = df_events_del[df_events_del["CATEGORIE"] == CATEGORIE] if not df_events_del.empty else df_events_del

    if df_events_del.empty:
        st.info("Aucun événement externe à supprimer.")
    else:
        evt_del_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_events_del.iterrows()}
        selected_del = st.selectbox("Sélectionner l'événement", options=list(evt_del_options.keys()), key="del_sel_ext")

        if selected_del:
            code_del = evt_del_options[selected_del]
            evt_del = df_events_del[df_events_del["CODE_EVENEMENT"] == code_del].iloc[0]

            st.markdown(f"**{evt_del['TITRE_EVENEMENT']}** — {evt_del['TYPE_EVENEMENT']} — {evt_del['DATE_DEBUT']}")
            st.error("⚠️ Cette action est irréversible.")

            if st.button("🗑️ Confirmer la suppression", type="primary", key="btn_del_ext"):
                delete_evenement(code_del, sf_user)
                log_modification(code_del, "SUPPRESSION", sf_user)
                close_all_snapshots(code_del)
                notify("🗑️ Événement supprimé")
                st.rerun()


# ===== TAB: HISTORIQUE =====
with tab_history:
    st.subheader("Historique")
    df_hist = get_historique_complet()
    if df_hist.empty:
        st.info("Aucun historique.")
    else:
        # Filtrer par catégorie externe
        df_hist_ext = df_hist[df_hist["CATEGORIE"] == CATEGORIE] if "CATEGORIE" in df_hist.columns else df_hist
        if df_hist_ext.empty:
            st.info("Aucun historique pour les événements externes.")
        else:
            st.caption(f"{len(df_hist_ext)} entrée(s)")
            st.dataframe(df_hist_ext, use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY HH:mm"),
                    "MODIFIE_PAR": st.column_config.TextColumn("Par"),
                    "ACTION": st.column_config.TextColumn("Action"),
                    "DATE_DEBUT_VALIDITE": st.column_config.DatetimeColumn("Date modif", format="DD/MM/YYYY HH:mm"),
                })
