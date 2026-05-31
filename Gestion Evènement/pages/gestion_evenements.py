import streamlit as st
import pandas as pd

from core.queries import (
    get_evenements, get_ref_types, get_ref_lieux, get_ref_impacts,
    get_parkings, get_parcs_evenement, get_historique_complet,
    insert_evenement, update_evenement, delete_evenement,
    insert_parc_evenement, delete_parcs_evenement, get_max_code_evenement,
    close_all_snapshots
)
from core.functions import (
    get_current_user, search_evenements, log_modification,
    show_notification, notify
)

# -- User --
sf_user = get_current_user()

# -- Page title --
st.title("📋 Gestion des évènements")
st.caption(f"Connecté en tant que : **{sf_user}**")

# -- Notification --
show_notification()

# -- Tabs --
tab_search, tab_create, tab_edit, tab_delete, tab_history = st.tabs([
    "🔍 Rechercher", "➕ Créer", "✏️ Modifier", "🗑️ Supprimer", "📜 Historique"
])

# ===== TAB: RECHERCHE =====
with tab_search:
    st.subheader("Rechercher un événement")
    search_term = st.text_input("🔍 Recherche (titre, type, catégorie, lieu, ville, impact, ID...)", placeholder="Tapez votre recherche ici...")

    df_events = get_evenements()

    if df_events.empty:
        st.info("Aucun événement actif.")
    else:
        df_results = search_evenements(df_events, search_term)
        st.caption(f"{len(df_results)} événement(s) trouvé(s)")

        if not df_results.empty:
            display_cols = ["CODE_EVENEMENT", "TITRE_EVENEMENT", "TYPE_EVENEMENT", "CATEGORIE",
                            "LIEU", "VILLE", "IMPACT", "NIVEAU_SEVERITE", "DATE_DEBUT", "DATE_FIN",
                            "COMMENTAIRE", "NOM_CREATEUR", "NOM_MODIFICATEUR", "DATE_CREATION", "DATE_MODIFICATION"]
            st.dataframe(df_results[display_cols], use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre", width="medium"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "CATEGORIE": st.column_config.TextColumn("Catégorie"),
                    "LIEU": st.column_config.TextColumn("Lieu"),
                    "VILLE": st.column_config.TextColumn("Ville"),
                    "IMPACT": st.column_config.TextColumn("Impact"),
                    "NIVEAU_SEVERITE": st.column_config.NumberColumn("Sévérité", format="%d ⚠️"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY HH:mm"),
                    "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY HH:mm"),
                    "COMMENTAIRE": st.column_config.TextColumn("Commentaire", width="large"),
                    "NOM_CREATEUR": st.column_config.TextColumn("Créé par"),
                    "NOM_MODIFICATEUR": st.column_config.TextColumn("Modifié par"),
                    "DATE_CREATION": st.column_config.DatetimeColumn("Créé le", format="DD/MM/YYYY HH:mm"),
                    "DATE_MODIFICATION": st.column_config.DatetimeColumn("Modifié le", format="DD/MM/YYYY HH:mm"),
                })

            # Detail view
            st.markdown("---")
            st.subheader("📄 Détail")
            evt_detail_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_results.iterrows()}
            selected_detail = st.selectbox("Voir le détail de :", options=[""] + list(evt_detail_options.keys()), key="detail_select")

            if selected_detail:
                code_detail = evt_detail_options[selected_detail]
                evt = df_results[df_results["CODE_EVENEMENT"] == code_detail].iloc[0]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Titre :** {evt['TITRE_EVENEMENT']}")
                    st.markdown(f"**Type :** {evt['TYPE_EVENEMENT']} ({evt['CATEGORIE']})")
                    st.markdown(f"**Lieu :** {evt['LIEU']} ({evt['VILLE']})")
                with col2:
                    st.markdown(f"**Impact :** {evt['IMPACT']} (sévérité {evt['NIVEAU_SEVERITE']})")
                    st.markdown(f"**Début :** {evt['DATE_DEBUT']}")
                    st.markdown(f"**Fin :** {evt['DATE_FIN'] if pd.notna(evt['DATE_FIN']) else 'Non définie'}")
                with col3:
                    st.markdown(f"**Commentaire :** {evt['COMMENTAIRE'] if pd.notna(evt['COMMENTAIRE']) else '-'}")
                    st.markdown(f"**Créé par :** {evt['NOM_CREATEUR'] if pd.notna(evt['NOM_CREATEUR']) else '-'}")
                    st.markdown(f"**Modifié par :** {evt['NOM_MODIFICATEUR'] if pd.notna(evt['NOM_MODIFICATEUR']) else '-'}")
                df_parcs = get_parcs_evenement(code_detail)
                if not df_parcs.empty:
                    st.markdown(f"**Parkings impactés :** {', '.join(df_parcs['NOM_PARC'].tolist())}")


# ===== TAB: CREATION =====
with tab_create:
    st.subheader("Nouvel événement")

    df_types = get_ref_types()
    df_lieux = get_ref_lieux()
    df_impacts = get_ref_impacts()
    df_parkings = get_parkings()

    with st.form("form_create_event", clear_on_submit=True):
        titre = st.text_input("Titre de l'événement *", max_chars=300)

        col1, col2 = st.columns(2)
        with col1:
            type_options = dict(zip(df_types["LIBELLE_TYPE_EVENEMENT"] + " (" + df_types["CATEGORIE"] + ")", df_types["CODE_TYPE_EVENEMENT"]))
            selected_type = st.selectbox("Type d'événement *", options=[""] + list(type_options.keys()), index=0)
            lieu_options = dict(zip(df_lieux["LIBELLE_LIEU"] + " - " + df_lieux["VILLE"], df_lieux["CODE_LIEU"]))
            selected_lieu = st.selectbox("Lieu *", options=[""] + list(lieu_options.keys()), index=0)
        with col2:
            impact_options = dict(zip(df_impacts["LIBELLE_IMPACT"] + " (niv. " + df_impacts["NIVEAU_SEVERITE"].astype(str) + ")", df_impacts["CODE_IMPACT"]))
            selected_impact = st.selectbox("Impact *", options=[""] + list(impact_options.keys()), index=0)
            date_debut = st.date_input("Date de début *", value=None)
            heure_debut = st.time_input("Heure de début", value=None)
            date_fin = st.date_input("Date de fin (optionnel)", value=None)
            heure_fin = st.time_input("Heure de fin", value=None)

        commentaire = st.text_area("Commentaire", max_chars=2000)
        st.markdown("**Parkings impactés**")
        parking_options = dict(zip(df_parkings["NOM_PARC"], df_parkings["CODE_PARC"]))
        selected_parkings = st.multiselect("Sélectionner les parkings impactés", options=list(parking_options.keys()))

        submitted = st.form_submit_button("💾 Créer l'événement", type="primary")

        if submitted:
            if not titre.strip():
                st.error("Le titre est obligatoire.")
            elif not selected_type:
                st.error("Le type d'événement est obligatoire.")
            elif not selected_lieu:
                st.error("Le lieu est obligatoire.")
            elif not selected_impact:
                st.error("L'impact est obligatoire.")
            elif date_debut is None:
                st.error("La date de début est obligatoire.")
            else:
                heure_debut_str = heure_debut.strftime("%H:%M:%S") if heure_debut else "00:00:00"
                timestamp_debut = f"{date_debut} {heure_debut_str}"
                if date_fin:
                    heure_fin_str = heure_fin.strftime("%H:%M:%S") if heure_fin else "00:00:00"
                    timestamp_fin_sql = f"'{date_fin} {heure_fin_str}'"
                else:
                    timestamp_fin_sql = "NULL"

                insert_evenement(titre, type_options[selected_type], lieu_options[selected_lieu],
                                 impact_options[selected_impact], timestamp_debut, timestamp_fin_sql, commentaire, sf_user)

                new_code = get_max_code_evenement()

                if selected_parkings:
                    for parc_name in selected_parkings:
                        insert_parc_evenement(new_code, parking_options[parc_name], parc_name)

                # Log creation in history
                log_modification(new_code, "CREATION", sf_user)

                notify("✅ Événement créé avec succès !")
                st.rerun()


# ===== TAB: MODIFICATION =====
with tab_edit:
    st.subheader("Modifier un événement")

    df_events_edit = get_evenements()
    if df_events_edit.empty:
        st.info("Aucun événement à modifier.")
    else:
        df_types = get_ref_types()
        df_lieux = get_ref_lieux()
        df_impacts = get_ref_impacts()
        df_parkings_edit = get_parkings()

        search_edit = st.text_input("🔍 Rechercher l'événement à modifier", placeholder="Tapez pour filtrer...", key="search_edit")
        df_edit_filtered = search_evenements(df_events_edit, search_edit)

        if df_edit_filtered.empty:
            st.warning("Aucun événement trouvé.")
        else:
            evt_edit_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_edit_filtered.iterrows()}
            selected_edit = st.selectbox("Sélectionner l'événement", options=list(evt_edit_options.keys()), key="edit_select")

            if selected_edit:
                code_edit = evt_edit_options[selected_edit]
                evt_row = df_events_edit[df_events_edit["CODE_EVENEMENT"] == code_edit].iloc[0]

                with st.expander("📄 Valeurs actuelles", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Titre :** {evt_row['TITRE_EVENEMENT']}")
                        st.markdown(f"**Type :** {evt_row['TYPE_EVENEMENT']} ({evt_row['CATEGORIE']})")
                        st.markdown(f"**Lieu :** {evt_row['LIEU']} - {evt_row['VILLE']}")
                    with col2:
                        st.markdown(f"**Impact :** {evt_row['IMPACT']} (sévérité {evt_row['NIVEAU_SEVERITE']})")
                        st.markdown(f"**Début :** {evt_row['DATE_DEBUT']}")
                        st.markdown(f"**Fin :** {evt_row['DATE_FIN'] if pd.notna(evt_row['DATE_FIN']) else 'Non définie'}")
                    with col3:
                        st.markdown(f"**Commentaire :** {evt_row['COMMENTAIRE'] if pd.notna(evt_row['COMMENTAIRE']) else '-'}")
                        st.markdown(f"**Créé par :** {evt_row['NOM_CREATEUR'] if pd.notna(evt_row['NOM_CREATEUR']) else '-'}")
                        st.markdown(f"**Modifié par :** {evt_row['NOM_MODIFICATEUR'] if pd.notna(evt_row['NOM_MODIFICATEUR']) else '-'}")

                st.markdown("**Nouvelles valeurs** _(remplir uniquement les champs à modifier)_")

                with st.form("form_edit_event"):
                    new_titre = st.text_input("Titre", placeholder="Laisser vide pour conserver", max_chars=300)
                    col1, col2 = st.columns(2)
                    with col1:
                        type_options_edit = dict(zip(df_types["LIBELLE_TYPE_EVENEMENT"] + " (" + df_types["CATEGORIE"] + ")", df_types["CODE_TYPE_EVENEMENT"]))
                        new_type = st.selectbox("Type d'événement", options=["-- Ne pas modifier --"] + list(type_options_edit.keys()))
                        lieu_options_edit = dict(zip(df_lieux["LIBELLE_LIEU"] + " - " + df_lieux["VILLE"], df_lieux["CODE_LIEU"]))
                        new_lieu = st.selectbox("Lieu", options=["-- Ne pas modifier --"] + list(lieu_options_edit.keys()))
                    with col2:
                        impact_options_edit = dict(zip(df_impacts["LIBELLE_IMPACT"] + " (niv. " + df_impacts["NIVEAU_SEVERITE"].astype(str) + ")", df_impacts["CODE_IMPACT"]))
                        new_impact = st.selectbox("Impact", options=["-- Ne pas modifier --"] + list(impact_options_edit.keys()))
                        new_date_debut = st.date_input("Date de début", value=None)
                        new_heure_debut = st.time_input("Heure de début", value=None, key="edit_heure_debut")
                        new_date_fin = st.date_input("Date de fin", value=None)
                        new_heure_fin = st.time_input("Heure de fin", value=None, key="edit_heure_fin")

                    new_commentaire = st.text_input("Commentaire", placeholder="Laisser vide pour conserver", max_chars=2000)

                    st.markdown("**Parkings impactés** _(sélectionner pour remplacer, laisser vide pour conserver)_")
                    parking_options_edit = dict(zip(df_parkings_edit["NOM_PARC"], df_parkings_edit["CODE_PARC"]))
                    new_parkings = st.multiselect("Parkings", options=list(parking_options_edit.keys()), default=[], key="edit_parkings")

                    submitted_edit = st.form_submit_button("💾 Enregistrer les modifications", type="primary")

                    if submitted_edit:
                        changes = []
                        set_parts = []
                        current_parcs = get_parcs_evenement(code_edit)
                        current_parc_names = current_parcs["NOM_PARC"].tolist() if not current_parcs.empty else []

                        if new_titre.strip():
                            changes.append(("TITRE_EVENEMENT", str(evt_row["TITRE_EVENEMENT"]), new_titre))
                            set_parts.append(f"TITRE_EVENEMENT = '{new_titre.replace(chr(39), chr(39)+chr(39))}'")

                        if new_type != "-- Ne pas modifier --":
                            changes.append(("TYPE_EVENEMENT", str(evt_row["TYPE_EVENEMENT"]), new_type.split(" (")[0]))
                            set_parts.append(f"CODE_TYPE_EVENEMENT = {type_options_edit[new_type]}")

                        if new_lieu != "-- Ne pas modifier --":
                            changes.append(("LIEU", str(evt_row["LIEU"]), new_lieu.split(" - ")[0]))
                            set_parts.append(f"CODE_LIEU = {lieu_options_edit[new_lieu]}")

                        if new_impact != "-- Ne pas modifier --":
                            changes.append(("IMPACT", str(evt_row["IMPACT"]), new_impact.split(" (")[0]))
                            set_parts.append(f"CODE_IMPACT = {impact_options_edit[new_impact]}")

                        if new_date_debut is not None:
                            heure_deb_str = new_heure_debut.strftime("%H:%M:%S") if new_heure_debut else "00:00:00"
                            ts = f"{new_date_debut} {heure_deb_str}"
                            changes.append(("DATE_DEBUT", str(evt_row["DATE_DEBUT"]), ts))
                            set_parts.append(f"DATE_DEBUT = '{ts}'")

                        if new_date_fin is not None:
                            heure_fin_str = new_heure_fin.strftime("%H:%M:%S") if new_heure_fin else "00:00:00"
                            ts = f"{new_date_fin} {heure_fin_str}"
                            changes.append(("DATE_FIN", str(evt_row["DATE_FIN"]), ts))
                            set_parts.append(f"DATE_FIN = '{ts}'")

                        if new_commentaire.strip():
                            current_comment = evt_row["COMMENTAIRE"] if pd.notna(evt_row["COMMENTAIRE"]) else ""
                            if new_commentaire != current_comment:
                                changes.append(("COMMENTAIRE", current_comment, new_commentaire))
                                set_parts.append(f"COMMENTAIRE = '{new_commentaire.replace(chr(39), chr(39)+chr(39))}'")

                        if new_parkings and sorted(new_parkings) != sorted(current_parc_names):
                            changes.append(("PARKINGS_IMPACTES", ", ".join(current_parc_names), ", ".join(new_parkings)))

                        if not changes:
                            st.info("Aucune modification détectée. Remplissez au moins un champ.")
                        else:
                            if set_parts:
                                update_evenement(code_edit, set_parts, sf_user)
                            if new_parkings and sorted(new_parkings) != sorted(current_parc_names):
                                delete_parcs_evenement(code_edit)
                                for parc_name in new_parkings:
                                    insert_parc_evenement(code_edit, parking_options_edit[parc_name], parc_name)

                            log_modification(code_edit, "MODIFICATION", sf_user)

                            notify(f"✏️ Événement modifié ({len(changes)} champ(s) mis à jour)")
                            st.rerun()


# ===== TAB: SUPPRESSION =====
with tab_delete:
    st.subheader("Supprimer un événement")

    df_events_del = get_evenements()
    if df_events_del.empty:
        st.info("Aucun événement à supprimer.")
    else:
        search_del = st.text_input("🔍 Rechercher l'événement à supprimer", placeholder="Tapez pour filtrer...", key="search_del")
        df_del_filtered = search_evenements(df_events_del, search_del)

        if df_del_filtered.empty:
            st.warning("Aucun événement trouvé.")
        else:
            evt_del_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_del_filtered.iterrows()}
            selected_del = st.selectbox("Sélectionner l'événement à supprimer", options=list(evt_del_options.keys()), key="del_select")

            if selected_del:
                code_del = evt_del_options[selected_del]
                evt_del = df_events_del[df_events_del["CODE_EVENEMENT"] == code_del].iloc[0]

                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**ID :** {evt_del['CODE_EVENEMENT']}")
                    st.markdown(f"**Titre :** {evt_del['TITRE_EVENEMENT']}")
                    st.markdown(f"**Type :** {evt_del['TYPE_EVENEMENT']} ({evt_del['CATEGORIE']})")
                with col2:
                    st.markdown(f"**Lieu :** {evt_del['LIEU']} ({evt_del['VILLE']})")
                    st.markdown(f"**Impact :** {evt_del['IMPACT']} (sévérité {evt_del['NIVEAU_SEVERITE']})")
                    st.markdown(f"**Début :** {evt_del['DATE_DEBUT']}")
                with col3:
                    st.markdown(f"**Fin :** {evt_del['DATE_FIN'] if pd.notna(evt_del['DATE_FIN']) else 'Non définie'}")
                    st.markdown(f"**Commentaire :** {evt_del['COMMENTAIRE'] if pd.notna(evt_del['COMMENTAIRE']) else '-'}")

                df_parcs_del = get_parcs_evenement(code_del)
                if not df_parcs_del.empty:
                    st.markdown(f"**Parkings impactés :** {', '.join(df_parcs_del['NOM_PARC'].tolist())}")

                st.markdown("---")
                st.error("⚠️ Cette action est irréversible (l'événement sera désactivé).")

                if st.button("🗑️ Confirmer la suppression", type="primary"):
                    delete_evenement(code_del, sf_user)
                    log_modification(code_del, "SUPPRESSION", sf_user)
                    close_all_snapshots(code_del)
                    notify("🗑️ Événement supprimé avec succès")
                    st.rerun()


# ===== TAB: HISTORIQUE =====
with tab_history:
    st.subheader("Historique des modifications")

    search_hist = st.text_input("🔍 Rechercher dans l'historique", placeholder="Tapez pour filtrer...", key="search_hist")
    df_hist = get_historique_complet()

    if df_hist.empty:
        st.info("Aucun historique de modification.")
    else:
        if search_hist:
            term = search_hist.lower()
            df_hist = df_hist[
                df_hist["TITRE_EVENEMENT"].str.lower().str.contains(term, na=False) |
                df_hist["CODE_EVENEMENT"].astype(str).str.contains(term, na=False) |
                df_hist["ACTION"].str.lower().str.contains(term, na=False) |
                df_hist["MODIFIE_PAR"].str.lower().str.contains(term, na=False)
            ]

        st.caption(f"{len(df_hist)} entrée(s) d'historique")
        st.dataframe(df_hist, use_container_width=True, hide_index=True,
            column_config={
                "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                "TITRE_EVENEMENT": st.column_config.TextColumn("Titre"),
                "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                "CATEGORIE": st.column_config.TextColumn("Catégorie"),
                "LIEU": st.column_config.TextColumn("Lieu"),
                "VILLE": st.column_config.TextColumn("Ville"),
                "IMPACT": st.column_config.TextColumn("Impact"),
                "NIVEAU_SEVERITE": st.column_config.NumberColumn("Sévérité"),
                "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                "DATE_FIN": st.column_config.DatetimeColumn("Date fin", format="DD/MM/YYYY HH:mm"),
                "COMMENTAIRE": st.column_config.TextColumn("Commentaire"),
                "PARKINGS_IMPACTES": st.column_config.TextColumn("Parkings"),
                "IS_ACTIVE": st.column_config.NumberColumn("IS_ACTIVE", format="%d"),
                "MODIFIE_PAR": st.column_config.TextColumn("Modifié par"),
                "ACTION": st.column_config.TextColumn("Action"),
                "DATE_DEBUT_VALIDITE": st.column_config.DatetimeColumn("Début validité", format="DD/MM/YYYY HH:mm:ss"),
                "DATE_FIN_VALIDITE": st.column_config.DatetimeColumn("Fin validité", format="DD/MM/YYYY HH:mm:ss"),
            })
