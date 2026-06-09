import streamlit as st
import pandas as pd

from core.queries import (
    get_evenements, get_ref_types, get_ref_descriptions, get_ref_impacts,
    get_parkings, get_parcs_evenement, get_historique_complet,
    insert_evenement, update_evenement, delete_evenement,
    insert_parc_evenement, delete_parcs_evenement, get_max_code_evenement,
    get_phases_travaux, get_all_phases_travaux, insert_phase_travaux, delete_phases_travaux, delete_phase_by_id, update_phase,
    insert_type_evenement,
    close_all_snapshots, recalculer_disponibilite
)
from core.functions import (
    get_current_user, search_evenements, log_modification,
    show_notification, notify
)

# -- User --
sf_user = get_current_user()

# -- Page title --
st.title("🔧 Événements techniques")
st.caption(f"Événements techniques / opérationnels liés au fonctionnement des parcs — Connecté : **{sf_user}**")

# -- Notification --
show_notification()

# -- Tabs --
tab_search, tab_create, tab_edit, tab_delete, tab_history = st.tabs([
    "🔍 Rechercher", "➕ Créer", "✏️ Modifier", "🗑️ Supprimer", "📜 Historique"
])

CATEGORIE = "Technique"

# -- Chargement des données une seule fois --
df_all_events = get_evenements()
df_events_tech = df_all_events[df_all_events["CATEGORIE"] == CATEGORIE] if not df_all_events.empty else df_all_events


# ===== TAB: RECHERCHE =====
with tab_search:
    st.subheader("Rechercher un événement technique")
    search_term = st.text_input("🔍 Recherche (titre, type, ID...)", placeholder="Tapez votre recherche ici...")

    if df_events_tech.empty:
        st.info("Aucun événement technique actif.")
    else:
        df_results = search_evenements(df_events_tech, search_term)
        st.caption(f"{len(df_results)} événement(s) trouvé(s)")

        if not df_results.empty:
            display_cols = ["CODE_EVENEMENT", "TITRE_EVENEMENT", "TYPE_EVENEMENT",
                            "DESCRIPTION", "IMPACT",
                            "DATE_DEBUT", "DATE_FIN", "CRENEAU",
                            "NB_PLACES_IMPACTEES", "FERMETURE_TOTALE",
                            "TYPE_TRAVAUX", "CONTACT_INTERNE", "IS_TRAVAUX_PHASES",
                            "COMMENTAIRE"]
            available_cols = [c for c in display_cols if c in df_results.columns]
            st.dataframe(df_results[available_cols], use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre", width="medium"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "DESCRIPTION": st.column_config.TextColumn("Description"),
                    "IMPACT": st.column_config.TextColumn("Impact"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY HH:mm"),
                    "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY HH:mm"),
                    "CRENEAU": st.column_config.TextColumn("Créneau"),
                    "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                    "FERMETURE_TOTALE": st.column_config.CheckboxColumn("Fermeture totale"),
                    "TYPE_TRAVAUX": st.column_config.TextColumn("Travaux"),
                    "CONTACT_INTERNE": st.column_config.TextColumn("Contact int."),
                    "IS_TRAVAUX_PHASES": st.column_config.CheckboxColumn("Phasé"),
                    "COMMENTAIRE": st.column_config.TextColumn("Commentaire", width="large"),
                })

            # Détail + phases de travaux
            st.markdown("---")
            evt_detail_opts = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_results.iterrows()}
            selected_detail = st.selectbox("Voir le détail :", options=[""] + list(evt_detail_opts.keys()), key="detail_tech")

            if selected_detail:
                code_detail = evt_detail_opts[selected_detail]
                evt = df_results[df_results["CODE_EVENEMENT"] == code_detail].iloc[0]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Type :** {evt['TYPE_EVENEMENT']}")
                    if evt.get('TYPE_TRAVAUX') and pd.notna(evt['TYPE_TRAVAUX']):
                        st.markdown(f"**Travaux :** {evt['TYPE_TRAVAUX']}")
                    if evt.get('CONTACT_INTERNE') and pd.notna(evt['CONTACT_INTERNE']):
                        st.markdown(f"**Contact interne :** {evt['CONTACT_INTERNE']}")
                    if evt.get('CONTACT_EXTERNE') and pd.notna(evt['CONTACT_EXTERNE']):
                        st.markdown(f"**Contact externe :** {evt['CONTACT_EXTERNE']}")
                with col2:
                    st.markdown(f"**Début :** {evt['DATE_DEBUT']}")
                    st.markdown(f"**Fin :** {evt['DATE_FIN'] if pd.notna(evt['DATE_FIN']) else '-'}")
                    if evt.get('NB_PLACES_IMPACTEES') and pd.notna(evt['NB_PLACES_IMPACTEES']):
                        st.markdown(f"**Places impactées :** {int(evt['NB_PLACES_IMPACTEES'])}")
                    if evt.get('FERMETURE_TOTALE'):
                        st.error("🚫 FERMETURE TOTALE")
                with col3:
                    if evt.get('IS_PISTES_IMPACTEES'):
                        pistes = []
                        if evt.get('NB_PISTES_ENTREE_FERMEES') and pd.notna(evt['NB_PISTES_ENTREE_FERMEES']):
                            pistes.append(f"{int(evt['NB_PISTES_ENTREE_FERMEES'])} entrée(s)")
                        if evt.get('NB_PISTES_SORTIE_FERMEES') and pd.notna(evt['NB_PISTES_SORTIE_FERMEES']):
                            pistes.append(f"{int(evt['NB_PISTES_SORTIE_FERMEES'])} sortie(s)")
                        st.markdown(f"**Pistes fermées :** {', '.join(pistes)}")

                    df_parcs = get_parcs_evenement(code_detail)
                    if not df_parcs.empty:
                        st.markdown(f"**Parkings :** {', '.join(df_parcs['NOM_PARC'].tolist())}")

                # Phases de travaux
                if evt.get('IS_TRAVAUX_PHASES'):
                    st.markdown("---")
                    st.markdown("**📋 Phases de travaux :**")
                    df_phases = get_phases_travaux(code_detail)
                    if not df_phases.empty:
                        st.dataframe(df_phases, use_container_width=True, hide_index=True,
                            column_config={
                                "NUMERO_PHASE": st.column_config.NumberColumn("Phase"),
                                "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                                "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                                "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places"),
                                "COMMENTAIRE": st.column_config.TextColumn("Secteur impacté"),
                            })
                    else:
                        st.info("Aucune phase définie. Ajoutez-les dans l'onglet Modifier.")


# ===== TAB: CREATION =====
with tab_create:
    st.subheader("Nouvel événement technique")

    # Compteur de version pour réinitialiser les widgets
    if "tech_form_v" not in st.session_state:
        st.session_state["tech_form_v"] = 0
    v = st.session_state["tech_form_v"]

    df_types = get_ref_types()
    df_types_tech = df_types[(df_types["CATEGORIE"] == CATEGORIE) & (df_types["IS_TRAVAUX"] == False)]
    df_impacts = get_ref_impacts()
    df_parkings = get_parkings()

    titre = st.text_input("Titre de l'événement *", max_chars=300, key=f"tech_titre_{v}")

    # -- Type d'événement technique --
    st.markdown("##### Type d'événement technique")
    type_options = dict(zip(df_types_tech["LIBELLE_TYPE_EVENEMENT"], df_types_tech["CODE_TYPE_EVENEMENT"]))
    selected_type = st.selectbox(
        "Type *",
        options=[""] + list(type_options.keys()) + ["Autre (nouveau type)"],
        index=0,
        key=f"tech_type_{v}"
    )

    nouveau_type_libelle = ""
    if selected_type == "Autre (nouveau type)":
        nouveau_type_libelle = st.text_input(
            "Nom du nouveau type *", max_chars=200,
            placeholder="Ex: Fuite d'eau, Problème ascenseur...",
            key=f"tech_new_type_{v}"
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
            selected_desc = st.selectbox("Description / Libellé", options=[""] + list(desc_options.keys()), key=f"tech_desc_{v}")

    if selected_desc == "Autre":
        description_autre = st.text_input("Préciser la description", max_chars=500, key=f"tech_desc_autre_{v}")

    # -- Impact --
    st.markdown("##### Impact")
    impact_options = dict(zip(
        df_impacts["LIBELLE_IMPACT"] + " (niv. " + df_impacts["NIVEAU_SEVERITE"].astype(str) + ")",
        df_impacts["CODE_IMPACT"]
    ))
    selected_impact = st.selectbox("Impact", options=[""] + list(impact_options.keys()), index=0, key=f"tech_impact_{v}")

    # -- Dates --
    st.markdown("##### Dates")
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date de début *", value=None, key=f"tech_dd_{v}")
        heure_debut = st.time_input("Heure de début", value=None, key=f"tech_hd_{v}")
    with col2:
        date_fin = st.date_input("Date de fin", value=None, key=f"tech_df_{v}")
        heure_fin = st.time_input("Heure de fin", value=None, key=f"tech_hf_{v}")

    # Journée partielle
    is_journee_partielle = st.checkbox("📅 Journée partielle", key=f"tech_jp_{v}")
    creneau = None
    if is_journee_partielle:
        creneau = st.selectbox("Créneau", options=["Matin", "Après-midi", "Nuit"], key=f"tech_creneau_{v}")

    # -- Parkings --
    st.markdown("##### Parkings impactés")
    parking_options = dict(zip(df_parkings["NOM_PARC"], df_parkings["CODE_PARC"]))
    selected_parkings = st.multiselect("Sélectionner les parkings impactés", options=list(parking_options.keys()), key=f"tech_parkings_{v}")

    if len(selected_parkings) == 1:
        parc_info = df_parkings[df_parkings["NOM_PARC"] == selected_parkings[0]].iloc[0]
        if pd.notna(parc_info.get("CAPACITE")):
            st.info(f"📊 Capacité : **{int(parc_info['CAPACITE'])} places** | Pistes entrée : {int(parc_info.get('NB_PISTES_ENTREE', 0))} | Pistes sortie : {int(parc_info.get('NB_PISTES_SORTIE', 0))}")

    # -- Places impactées (DYNAMIQUE) --
    is_places_impactees = st.checkbox("🅿️ Impact sur le nombre de places", key=f"tech_places_cb_{v}")
    nb_places_impactees = None
    fermeture_totale = False
    if is_places_impactees:
        fermeture_totale = st.checkbox("🚫 Fermeture totale du parking (places disponibles = 0)", key=f"tech_fermeture_{v}")
        if not fermeture_totale:
            nb_places_impactees = st.number_input("Nombre de places impactées", min_value=0, value=0, key=f"tech_nb_places_{v}")

    # -- Pistes impactées (DYNAMIQUE) --
    is_pistes_impactees = st.checkbox("🚧 Piste(s) impactée(s)", key=f"tech_pistes_cb_{v}")
    nb_pistes_entree = None
    nb_pistes_sortie = None
    if is_pistes_impactees:
        col1, col2 = st.columns(2)
        with col1:
            nb_pistes_entree = st.number_input("Nb pistes ENTRÉE fermées", min_value=0, value=0, key=f"tech_pe_{v}")
        with col2:
            nb_pistes_sortie = st.number_input("Nb pistes SORTIE fermées", min_value=0, value=0, key=f"tech_ps_{v}")

    # -- Commentaire --
    commentaire = st.text_area("Commentaire", max_chars=2000, key=f"tech_comm_{v}")

    # -- Submit (bouton standard, pas form_submit_button) --
    st.markdown("---")
    if st.button("💾 Créer l'événement technique", type="primary", key=f"btn_create_tech_{v}"):
        if not titre.strip():
            st.error("Le titre est obligatoire.")
        elif not selected_type:
            st.error("Le type est obligatoire.")
        elif selected_type == "Autre (nouveau type)" and not nouveau_type_libelle.strip():
            st.error("Veuillez saisir le nom du nouveau type.")
        elif date_debut is None:
            st.error("La date de début est obligatoire.")
        else:
            if selected_type == "Autre (nouveau type)":
                is_new_travaux = "travaux" in nouveau_type_libelle.lower()
                code_type_final = insert_type_evenement(nouveau_type_libelle.strip(), CATEGORIE, is_new_travaux)
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

            code_impact = int(impact_options[selected_impact]) if selected_impact else None

            insert_evenement(
                titre=titre,
                code_type=code_type_final,
                code_description=code_description,
                description_autre=description_autre if selected_desc == "Autre" else None,
                code_lieu=None,
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
                    insert_parc_evenement(new_code, parking_options[parc_name], parc_name)

            log_modification(new_code, "CREATION", sf_user)
            recalculer_disponibilite()
            notify("✅ Événement technique créé avec succès !")
            st.session_state["tech_form_v"] += 1
            st.rerun()


# ===== TAB: MODIFICATION =====
with tab_edit:
    st.subheader("Modifier un événement technique")

    df_events_edit = df_events_tech

    if df_events_edit.empty:
        st.info("Aucun événement technique à modifier.")
    else:
        df_parkings_edit = get_parkings()

        search_edit = st.text_input("🔍 Rechercher", placeholder="Tapez pour filtrer...", key="search_edit_tech")
        df_edit_filtered = search_evenements(df_events_edit, search_edit)

        if df_edit_filtered.empty:
            st.warning("Aucun événement trouvé.")
        else:
            evt_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_edit_filtered.iterrows()}
            selected_edit = st.selectbox("Sélectionner l'événement", options=list(evt_options.keys()), key="edit_sel_tech")

            if selected_edit:
                code_edit = evt_options[selected_edit]
                evt_row = df_events_edit[df_events_edit["CODE_EVENEMENT"] == code_edit].iloc[0]

                with st.expander("📄 Valeurs actuelles", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Titre :** {evt_row['TITRE_EVENEMENT']}")
                        st.markdown(f"**Type :** {evt_row['TYPE_EVENEMENT']}")
                        if evt_row.get('TYPE_TRAVAUX') and pd.notna(evt_row['TYPE_TRAVAUX']):
                            st.markdown(f"**Travaux :** {evt_row['TYPE_TRAVAUX']}")
                    with col2:
                        st.markdown(f"**Début :** {evt_row['DATE_DEBUT']}")
                        st.markdown(f"**Fin :** {evt_row['DATE_FIN'] if pd.notna(evt_row['DATE_FIN']) else '-'}")
                        if evt_row.get('CONTACT_INTERNE') and pd.notna(evt_row['CONTACT_INTERNE']):
                            st.markdown(f"**Contact int. :** {evt_row['CONTACT_INTERNE']}")
                    with col3:
                        if evt_row.get('NB_PLACES_IMPACTEES') and pd.notna(evt_row['NB_PLACES_IMPACTEES']):
                            st.markdown(f"**Places impactées :** {int(evt_row['NB_PLACES_IMPACTEES'])}")
                        if evt_row.get('FERMETURE_TOTALE'):
                            st.error("🚫 FERMETURE TOTALE")

                new_titre = st.text_input("Titre", placeholder="Laisser vide pour conserver", max_chars=300, key=f"tech_edit_titre_{code_edit}")

                col1, col2 = st.columns(2)
                with col1:
                    new_date_debut = st.date_input("Date de début", value=None, key=f"tech_edit_dd_{code_edit}")
                    new_heure_debut = st.time_input("Heure de début", value=None, key=f"tech_edit_hd_{code_edit}")
                with col2:
                    new_date_fin = st.date_input("Date de fin", value=None, key=f"tech_edit_df_{code_edit}")
                    new_heure_fin = st.time_input("Heure de fin", value=None, key=f"tech_edit_hf_{code_edit}")

                new_commentaire = st.text_input("Commentaire", placeholder="Laisser vide pour conserver", max_chars=2000, key=f"tech_edit_comm_{code_edit}")

                st.markdown("##### Options")
                new_fermeture = st.checkbox(
                    "🚫 Fermeture totale",
                    value=bool(evt_row.get('FERMETURE_TOTALE')),
                    key=f"tech_edit_ferm_{code_edit}"
                )
                if not new_fermeture:
                    new_nb_places = st.number_input("Nb places impactées (0 = ne pas modifier)", min_value=0, value=0, key=f"tech_edit_pl_{code_edit}")
                else:
                    st.info("🚫 Fermeture totale : les places impactées = capacité totale du parking.")
                    new_nb_places = 0

                new_contact_interne = st.text_input("Contact interne", placeholder="Laisser vide pour conserver", key=f"tech_edit_ci_{code_edit}")
                new_contact_externe = st.text_input("Contact externe", placeholder="Laisser vide pour conserver", key=f"tech_edit_ce_{code_edit}")

                parking_options_edit = dict(zip(df_parkings_edit["NOM_PARC"], df_parkings_edit["CODE_PARC"]))
                new_parkings = st.multiselect("Parkings (sélectionner pour remplacer)", options=list(parking_options_edit.keys()), default=[], key=f"tech_edit_park_{code_edit}")

                st.markdown("---")
                if st.button("💾 Enregistrer", type="primary", key=f"btn_edit_tech_{code_edit}"):
                    set_parts = []
                    if new_titre.strip():
                        set_parts.append(f"TITRE_EVENEMENT = '{new_titre.replace(chr(39), chr(39)+chr(39))}'")
                    if new_date_debut is not None:
                        h = new_heure_debut.strftime("%H:%M:%S") if new_heure_debut else "00:00:00"
                        set_parts.append(f"DATE_DEBUT = '{new_date_debut} {h}'")
                    if new_date_fin is not None:
                        h = new_heure_fin.strftime("%H:%M:%S") if new_heure_fin else "00:00:00"
                        set_parts.append(f"DATE_FIN = '{new_date_fin} {h}'")
                    if new_commentaire.strip():
                        set_parts.append(f"COMMENTAIRE = '{new_commentaire.replace(chr(39), chr(39)+chr(39))}'")
                    if new_fermeture:
                        set_parts.append("FERMETURE_TOTALE = TRUE")
                        set_parts.append("IS_PLACES_IMPACTEES = TRUE")
                        set_parts.append("NB_PLACES_IMPACTEES = NULL")
                    elif not new_fermeture and bool(evt_row.get('FERMETURE_TOTALE')):
                        # On décoche fermeture totale → remettre à FALSE
                        set_parts.append("FERMETURE_TOTALE = FALSE")
                    if not new_fermeture and new_nb_places > 0:
                        set_parts.append(f"IS_PLACES_IMPACTEES = TRUE")
                        set_parts.append(f"NB_PLACES_IMPACTEES = {new_nb_places}")
                    if new_contact_interne.strip():
                        set_parts.append(f"CONTACT_INTERNE = '{new_contact_interne.replace(chr(39), chr(39)+chr(39))}'")
                    if new_contact_externe.strip():
                        set_parts.append(f"CONTACT_EXTERNE = '{new_contact_externe.replace(chr(39), chr(39)+chr(39))}'")

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
                                    insert_parc_evenement(code_edit, parking_options_edit[p], p)
                        log_modification(code_edit, "MODIFICATION", sf_user)
                        recalculer_disponibilite()
                        notify("✏️ Événement modifié")
                        st.rerun()

                # -- SECTION PHASES DE TRAVAUX (hors formulaire) --
                if evt_row.get('IS_TRAVAUX_PHASES'):
                    st.markdown("---")
                    st.markdown("##### 📋 Phases de travaux")

                    df_phases = get_phases_travaux(code_edit)
                    if not df_phases.empty:
                        st.markdown("##### Gestion des phases de travaux")
                        for idx, phase_row in df_phases.iterrows():
                            code_ph = int(phase_row['CODE_PHASE'])
                            num_ph = int(phase_row['NUMERO_PHASE'])
                            col_info, col_edit, col_del = st.columns([5, 0.5, 0.5])
                            with col_info:
                                debut = pd.to_datetime(phase_row['DATE_DEBUT']).strftime('%d/%m/%Y') if pd.notna(phase_row['DATE_DEBUT']) else '?'
                                fin = pd.to_datetime(phase_row['DATE_FIN']).strftime('%d/%m/%Y') if pd.notna(phase_row['DATE_FIN']) else '?'
                                places = int(phase_row['NB_PLACES_IMPACTEES']) if pd.notna(phase_row.get('NB_PLACES_IMPACTEES')) else '-'
                                comm = phase_row.get('COMMENTAIRE', '') or ''
                                st.markdown(f"**Phase {num_ph}** : {debut} → {fin} | {places} places fermées | {comm}")
                            with col_edit:
                                if st.button("✏️", key=f"edit_ph_{code_ph}", help="Modifier cette phase"):
                                    st.session_state[f"editing_phase_{code_ph}"] = True
                            with col_del:
                                if st.button("🗑️", key=f"del_ph_{code_ph}", help="Supprimer cette phase"):
                                    delete_phase_by_id(code_ph)
                                    notify(f"Phase {num_ph} supprimée")
                                    st.rerun()

                            # Formulaire de modification inline
                            if st.session_state.get(f"editing_phase_{code_ph}", False):
                                with st.form(f"form_edit_ph_{code_ph}"):
                                    st.markdown(f"_Modifier la phase {num_ph} :_")
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        edit_dd = st.date_input("Début", value=pd.to_datetime(phase_row['DATE_DEBUT']).date() if pd.notna(phase_row['DATE_DEBUT']) else None, key=f"edit_ph_dd_{code_ph}")
                                        if not evt_row.get('FERMETURE_TOTALE'):
                                            edit_places = st.number_input("Places impactées", min_value=0, value=int(phase_row['NB_PLACES_IMPACTEES']) if pd.notna(phase_row.get('NB_PLACES_IMPACTEES')) else 0, key=f"edit_ph_pl_{code_ph}")
                                        else:
                                            st.info("🚫 Fermeture totale — places = capacité")
                                            edit_places = 0
                                    with col2:
                                        edit_df = st.date_input("Fin", value=pd.to_datetime(phase_row['DATE_FIN']).date() if pd.notna(phase_row['DATE_FIN']) else None, key=f"edit_ph_df_{code_ph}")
                                        edit_comm = st.text_input("Secteur", value=phase_row.get('COMMENTAIRE', '') or '', key=f"edit_ph_co_{code_ph}")

                                    col_save, col_cancel = st.columns(2)
                                    with col_save:
                                        submitted = st.form_submit_button("💾 Enregistrer")
                                    with col_cancel:
                                        cancelled = st.form_submit_button("❌ Annuler")

                                    if submitted:
                                        update_phase(code_ph, str(edit_dd), str(edit_df), edit_places if edit_places > 0 else None, edit_comm)
                                        del st.session_state[f"editing_phase_{code_ph}"]
                                        log_modification(code_edit, "MODIFICATION_PHASE", sf_user)
                                        recalculer_disponibilite()
                                        notify(f"Phase {num_ph} modifiée !")
                                        st.rerun()
                                    elif cancelled:
                                        del st.session_state[f"editing_phase_{code_ph}"]
                                        st.rerun()

                        st.markdown("")
                        if st.button("🗑️ Supprimer toutes les phases", key=f"del_phases_{code_edit}"):
                            delete_phases_travaux(code_edit)
                            notify("Toutes les phases supprimées")
                            st.rerun()
                    else:
                        st.info("Aucune phase définie.")

                    st.markdown("**Ajouter une phase :**")
                    if "phase_form_v" not in st.session_state:
                        st.session_state["phase_form_v"] = 0
                    pv = st.session_state["phase_form_v"]
                    with st.form(f"form_add_phase_{code_edit}_{pv}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            phase_date_debut = st.date_input("Début de la phase", value=None, key=f"ph_dd_{pv}")
                            if not evt_row.get('FERMETURE_TOTALE'):
                                phase_nb_places = st.number_input("Nb places impactées cette phase", min_value=0, value=0, key=f"ph_pl_{pv}")
                            else:
                                st.info("🚫 Fermeture totale — places = capacité")
                                phase_nb_places = 0
                        with col2:
                            phase_date_fin = st.date_input("Fin de la phase", value=None, key=f"ph_df_{pv}")
                            phase_commentaire = st.text_input("Secteur du parking impacté", key=f"ph_comm_{pv}",
                                placeholder="Ex: Niveau -2 zone A, Rampe nord...")

                        if st.form_submit_button("➕ Ajouter la phase"):
                            if phase_date_debut and phase_date_fin:
                                next_num = len(df_phases) + 1 if not df_phases.empty else 1
                                insert_phase_travaux(
                                    code_edit, next_num,
                                    str(phase_date_debut), str(phase_date_fin),
                                    phase_nb_places if phase_nb_places > 0 else None,
                                    phase_commentaire
                                )
                                log_modification(code_edit, "AJOUT_PHASE", sf_user)
                                st.session_state["phase_form_v"] += 1
                                notify(f"Phase {next_num} ajoutée !")
                                st.rerun()
                            else:
                                st.error("Les dates de début et fin sont obligatoires.")


# ===== TAB: SUPPRESSION =====
with tab_delete:
    st.subheader("Supprimer un événement technique")

    df_events_del = df_events_tech

    if df_events_del.empty:
        st.info("Aucun événement technique à supprimer.")
    else:
        evt_del_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_events_del.iterrows()}
        selected_del = st.selectbox("Sélectionner", options=list(evt_del_options.keys()), key="del_sel_tech")

        if selected_del:
            code_del = evt_del_options[selected_del]
            evt_del = df_events_del[df_events_del["CODE_EVENEMENT"] == code_del].iloc[0]

            st.markdown(f"**{evt_del['TITRE_EVENEMENT']}** — {evt_del['TYPE_EVENEMENT']} — {evt_del['DATE_DEBUT']}")
            st.error("⚠️ Cette action est irréversible. Les phases de travaux associées seront aussi supprimées.")

            if st.button("🗑️ Confirmer la suppression", type="primary", key="btn_del_tech"):
                delete_evenement(code_del, sf_user)
                log_modification(code_del, "SUPPRESSION", sf_user)
                close_all_snapshots(code_del)
                recalculer_disponibilite()
                notify("🗑️ Événement supprimé")
                st.rerun()


# ===== TAB: HISTORIQUE =====
with tab_history:
    st.subheader("Historique")
    df_hist = get_historique_complet()
    if df_hist.empty:
        st.info("Aucun historique.")
    else:
        df_hist_tech = df_hist[df_hist["CATEGORIE"] == CATEGORIE] if "CATEGORIE" in df_hist.columns else df_hist
        if df_hist_tech.empty:
            st.info("Aucun historique pour les événements techniques.")
        else:
            st.caption(f"{len(df_hist_tech)} entrée(s)")
            st.dataframe(df_hist_tech, use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "TYPE_TRAVAUX": st.column_config.TextColumn("Travaux"),
                    "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                    "MODIFIE_PAR": st.column_config.TextColumn("Par"),
                    "ACTION": st.column_config.TextColumn("Action"),
                    "DATE_DEBUT_VALIDITE": st.column_config.DatetimeColumn("Date modif", format="DD/MM/YYYY HH:mm"),
                })

            # Historique par phase pour les travaux phasés
            st.markdown("---")
            st.subheader("📋 Historique des phases de travaux")
            df_all_phases = get_all_phases_travaux()
            if not df_all_phases.empty:
                # Filtrer sur les événements techniques
                codes_tech = df_hist_tech["CODE_EVENEMENT"].unique().tolist()
                df_phases_tech = df_all_phases[df_all_phases["CODE_EVENEMENT"].isin(codes_tech)]
                if not df_phases_tech.empty:
                    st.dataframe(df_phases_tech, use_container_width=True, hide_index=True,
                        column_config={
                            "CODE_EVENEMENT": st.column_config.NumberColumn("ID événement", width="small"),
                            "NUMERO_PHASE": st.column_config.NumberColumn("Phase"),
                            "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                            "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                            "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                            "COMMENTAIRE": st.column_config.TextColumn("Secteur"),
                        })
                else:
                    st.info("Aucune phase de travaux pour les événements techniques.")
            else:
                st.info("Aucune phase de travaux enregistrée.")
