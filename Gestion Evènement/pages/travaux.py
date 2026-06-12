import streamlit as st
import pandas as pd

from core.queries import (
    get_evenements, get_ref_types, get_ref_impacts,
    get_parkings, get_parcs_evenement, get_historique_complet,
    insert_evenement, update_evenement, delete_evenement,
    insert_parc_evenement, delete_parcs_evenement, get_max_code_evenement,
    get_phases_travaux, insert_phase_travaux, delete_phases_travaux, delete_phase_by_id, update_phase,
    get_all_phases_travaux,
    close_all_snapshots, recalculer_disponibilite,
    get_contacts_internes
)
from core.functions import (
    get_current_user, search_evenements, log_modification,
    show_notification, notify
)

# -- User --
sf_user = get_current_user()

# -- Page title --
st.title("🏗️ Gestion des Travaux")
st.caption(f"Travaux internes et externes impactant les parcs — Connecté : **{sf_user}**")

# -- Notification --
show_notification()

# -- Tabs --
tab_search, tab_create, tab_edit, tab_delete, tab_history = st.tabs([
    "🔍 Rechercher", "➕ Créer", "✏️ Modifier / Phases", "🗑️ Supprimer", "📜 Historique"
])

# Filtrer uniquement les événements travaux
def filter_travaux(df):
    if df.empty:
        return df
    return df[df["TYPE_EVENEMENT"].str.contains("Travaux", na=False)]


# ===== TAB: RECHERCHE =====
with tab_search:
    st.subheader("Travaux en cours")
    df_events = get_evenements()
    df_travaux = filter_travaux(df_events)

    if df_travaux.empty:
        st.info("Aucun travaux en cours.")
    else:
        # Pour les travaux phasés, calculer le total des places par phase
        df_all_ph = get_all_phases_travaux()
        if not df_all_ph.empty and "NB_PLACES_IMPACTEES" in df_all_ph.columns:
            phases_sum = df_all_ph.groupby("CODE_EVENEMENT")["NB_PLACES_IMPACTEES"].sum().reset_index()
            phases_sum.columns = ["CODE_EVENEMENT", "PLACES_PHASES"]
            df_travaux = df_travaux.merge(phases_sum, on="CODE_EVENEMENT", how="left")
            # Remplir NB_PLACES_IMPACTEES avec le total des phases si NULL et phasé
            mask = df_travaux["IS_TRAVAUX_PHASES"] == True
            df_travaux.loc[mask & df_travaux["NB_PLACES_IMPACTEES"].isna(), "NB_PLACES_IMPACTEES"] = df_travaux.loc[mask & df_travaux["NB_PLACES_IMPACTEES"].isna(), "PLACES_PHASES"]
            df_travaux = df_travaux.drop(columns=["PLACES_PHASES"], errors="ignore")

        st.caption(f"{len(df_travaux)} travaux actif(s)")
        display_cols = ["CODE_EVENEMENT", "TITRE_EVENEMENT", "TYPE_EVENEMENT",
                        "TYPE_TRAVAUX", "CONTACT_INTERNE", "CONTACT_EXTERNE",
                        "NB_PLACES_IMPACTEES", "FERMETURE_TOTALE", "IS_TRAVAUX_PHASES",
                        "COMMENTAIRE"]
        available_cols = [c for c in display_cols if c in df_travaux.columns]
        st.dataframe(df_travaux[available_cols], use_container_width=True, hide_index=True,
            column_config={
                "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                "TITRE_EVENEMENT": st.column_config.TextColumn("Titre", width="medium"),
                "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                "TYPE_TRAVAUX": st.column_config.TextColumn("Int./Ext."),
                "CONTACT_INTERNE": st.column_config.TextColumn("Contact int."),
                "CONTACT_EXTERNE": st.column_config.TextColumn("Contact ext."),
                "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                "FERMETURE_TOTALE": st.column_config.CheckboxColumn("Fermeture totale"),
                "IS_TRAVAUX_PHASES": st.column_config.CheckboxColumn("Phasé"),
                "COMMENTAIRE": st.column_config.TextColumn("Commentaire"),
            })

        # Détail avec phases
        st.markdown("---")
        evt_opts = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_travaux.iterrows()}
        selected_detail = st.selectbox("Voir le détail :", options=[""] + list(evt_opts.keys()), key="trav_detail")

        if selected_detail:
            code_detail = evt_opts[selected_detail]
            evt = df_travaux[df_travaux["CODE_EVENEMENT"] == code_detail].iloc[0]

            # Stocker le parking pour pré-sélection du Gantt (variable intermédiaire)
            df_parcs_detail_pre = get_parcs_evenement(code_detail)
            if not df_parcs_detail_pre.empty:
                preselected_parking_name = df_parcs_detail_pre["NOM_PARC"].tolist()[0]
                if st.session_state.get("gantt_filter_parking") != preselected_parking_name:
                    st.session_state["gantt_filter_parking"] = preselected_parking_name

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type :** {evt['TYPE_TRAVAUX'] if pd.notna(evt.get('TYPE_TRAVAUX')) else '-'}")
                st.markdown(f"**Début :** {evt['DATE_DEBUT']}")
                st.markdown(f"**Contact interne :** {evt['CONTACT_INTERNE'] if pd.notna(evt.get('CONTACT_INTERNE')) else '-'}")
                st.markdown(f"**Contact externe :** {evt['CONTACT_EXTERNE'] if pd.notna(evt.get('CONTACT_EXTERNE')) else '-'}")
            with col2:
                st.markdown(f"**Fin :** {evt['DATE_FIN'] if pd.notna(evt['DATE_FIN']) else '-'}")
                places_val = int(evt['NB_PLACES_IMPACTEES']) if pd.notna(evt.get('NB_PLACES_IMPACTEES')) else '-'
                st.markdown(f"**Places impactées :** {places_val}")
                if evt.get('FERMETURE_TOTALE'):
                    st.error("🚫 FERMETURE TOTALE")

            df_parcs = get_parcs_evenement(code_detail)
            if not df_parcs.empty:
                parkings_names = df_parcs['NOM_PARC'].tolist()
                st.markdown(f"**Parkings :** {', '.join(parkings_names)}")
                # Afficher la capacité si un seul parking
                if len(parkings_names) == 1:
                    from core.queries import get_parkings
                    df_pk = get_parkings()
                    pk_row = df_pk[df_pk["NOM_PARC"] == parkings_names[0]]
                    if not pk_row.empty and pd.notna(pk_row.iloc[0].get("CAPACITE")):
                        capacite = int(pk_row.iloc[0]["CAPACITE"])
                        st.info(f"📊 Capacité de **{parkings_names[0]}** : {capacite} places")

            if evt.get('IS_TRAVAUX_PHASES'):
                df_phases = get_phases_travaux(code_detail)
                if not df_phases.empty:
                    # Afficher places impactées par phase (pas le total global)
                    st.markdown("**📋 Phases de travaux :**")
                    display_phases = df_phases.drop(columns=["CODE_PHASE"], errors="ignore")
                    st.dataframe(display_phases, use_container_width=True, hide_index=True,
                        column_config={
                            "NUMERO_PHASE": st.column_config.NumberColumn("Phase n°"),
                            "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                            "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                            "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                            "COMMENTAIRE": st.column_config.TextColumn("Secteur impacté"),
                        })

        # -- DIAGRAMMES DE GANTT --
        st.markdown("---")

        # Séparer internes et externes
        df_internes = df_travaux[df_travaux["TYPE_TRAVAUX"] == "INTERNE"] if "TYPE_TRAVAUX" in df_travaux.columns else pd.DataFrame()
        df_externes = df_travaux[df_travaux["TYPE_TRAVAUX"] == "EXTERNE"] if "TYPE_TRAVAUX" in df_travaux.columns else pd.DataFrame()

        # === VUE MICRO : Travaux INTERNES (par parking + phases) ===
        if not df_internes.empty:
            with st.expander("🔧 Travaux internes — Vue par parking", expanded=bool(selected_detail)):
                # Collecter tous les parkings impactés par des travaux internes
                all_parkings_internes = []
                for _, row in df_internes.iterrows():
                    df_parcs_evt = get_parcs_evenement(int(row["CODE_EVENEMENT"]))
                    if not df_parcs_evt.empty:
                        for p in df_parcs_evt["NOM_PARC"].tolist():
                            if p not in all_parkings_internes:
                                all_parkings_internes.append(p)

                if all_parkings_internes:
                    selected_parking = st.selectbox(
                        "Filtrer par parking",
                        options=sorted(all_parkings_internes),
                        key="gantt_filter_parking"
                    )

                    gantt_internes = []
                    for _, row in df_internes.iterrows():
                        if pd.notna(row["DATE_DEBUT"]) and pd.notna(row.get("DATE_FIN")):
                            df_parcs_evt = get_parcs_evenement(int(row["CODE_EVENEMENT"]))
                            parkings_list = df_parcs_evt["NOM_PARC"].tolist() if not df_parcs_evt.empty else []

                            # Ne garder que les travaux qui impactent le parking sélectionné
                            if selected_parking not in parkings_list:
                                continue

                            gantt_internes.append({
                                "Tâche": row['TITRE_EVENEMENT'],
                                "Début": pd.to_datetime(row["DATE_DEBUT"]).isoformat(),
                                "Fin": pd.to_datetime(row["DATE_FIN"]).isoformat(),
                                "Catégorie": "Global",
                                "Places": int(row["NB_PLACES_IMPACTEES"]) if pd.notna(row.get("NB_PLACES_IMPACTEES")) else 0,
                            })

                            if row.get("IS_TRAVAUX_PHASES"):
                                df_ph = get_phases_travaux(int(row["CODE_EVENEMENT"]))
                                if not df_ph.empty:
                                    for _, phase in df_ph.iterrows():
                                        if pd.notna(phase["DATE_DEBUT"]) and pd.notna(phase["DATE_FIN"]):
                                            commentaire = phase.get('COMMENTAIRE', '') or ''
                                            parts = [f"↳ Phase {int(phase['NUMERO_PHASE'])}"]
                                            if commentaire:
                                                parts.append(f"— {commentaire}")
                                            label = "  " + " ".join(parts)
                                            gantt_internes.append({
                                                "Tâche": label,
                                                "Début": pd.to_datetime(phase["DATE_DEBUT"]).isoformat(),
                                                "Fin": pd.to_datetime(phase["DATE_FIN"]).isoformat(),
                                                "Catégorie": "Phase",
                                                "Places": int(phase["NB_PLACES_IMPACTEES"]) if pd.notna(phase.get("NB_PLACES_IMPACTEES")) else 0,
                                            })

                    if gantt_internes:
                        df_gantt_int = pd.DataFrame(gantt_internes)
                        st.vega_lite_chart(df_gantt_int, {
                            "mark": {"type": "bar", "cornerRadiusEnd": 4, "height": 20},
                            "encoding": {
                                "y": {
                                    "field": "Tâche",
                                    "type": "ordinal",
                                    "sort": None,
                                    "axis": {"title": "", "labelLimit": 500, "labelOverlap": False}
                                },
                                "x": {
                                    "field": "Début",
                                    "type": "temporal",
                                    "axis": {"title": "Période", "format": "%d/%m/%Y"}
                                },
                                "x2": {"field": "Fin", "type": "temporal"},
                                "color": {
                                    "field": "Catégorie",
                                    "type": "nominal",
                                    "scale": {"domain": ["Global", "Phase"], "range": ["#3b82f6", "#f59e0b"]},
                                    "legend": {"title": ""}
                                },
                                "tooltip": [
                                    {"field": "Tâche", "type": "nominal"},
                                    {"field": "Places", "type": "quantitative", "title": "Places impactées"},
                                    {"field": "Début", "type": "temporal", "format": "%d/%m/%Y"},
                                    {"field": "Fin", "type": "temporal", "format": "%d/%m/%Y"}
                                ]
                            },
                            "height": max(200, len(gantt_internes) * 40),
                            "title": f"Travaux internes — {selected_parking}"
                        }, use_container_width=True)
                    else:
                        st.info(f"Aucun travaux interne sur {selected_parking}.")
                else:
                    st.info("Aucun parking associé aux travaux internes.")

        # === VUE MACRO : Travaux EXTERNES (multi-parkings) ===
        if not df_externes.empty:
            with st.expander("🚧 Travaux externes — Vue multi-parkings", expanded=False):
                gantt_externes = []

                for _, row in df_externes.iterrows():
                    if pd.notna(row["DATE_DEBUT"]) and pd.notna(row.get("DATE_FIN")):
                        df_parcs_evt = get_parcs_evenement(int(row["CODE_EVENEMENT"]))
                        parkings_list = df_parcs_evt["NOM_PARC"].tolist() if not df_parcs_evt.empty else ["Non défini"]

                        for parc_name in parkings_list:
                            gantt_externes.append({
                                "Tâche": f"{row['TITRE_EVENEMENT']}",
                                "Début": pd.to_datetime(row["DATE_DEBUT"]).isoformat(),
                                "Fin": pd.to_datetime(row["DATE_FIN"]).isoformat(),
                                "Parking": parc_name,
                                "Catégorie": "Global",
                                "Places": int(row["NB_PLACES_IMPACTEES"]) if pd.notna(row.get("NB_PLACES_IMPACTEES")) else 0,
                            })

                        # Ajouter les phases si phasé
                        if row.get("IS_TRAVAUX_PHASES"):
                            df_ph = get_phases_travaux(int(row["CODE_EVENEMENT"]))
                            if not df_ph.empty:
                                for _, phase in df_ph.iterrows():
                                    if pd.notna(phase["DATE_DEBUT"]) and pd.notna(phase["DATE_FIN"]):
                                        commentaire = phase.get('COMMENTAIRE', '') or ''
                                        parts = [f"↳ Phase {int(phase['NUMERO_PHASE'])}"]
                                        if commentaire:
                                            parts.append(f"— {commentaire}")
                                        label = "  " + " ".join(parts)
                                        for parc_name in parkings_list:
                                            gantt_externes.append({
                                                "Tâche": label,
                                                "Début": pd.to_datetime(phase["DATE_DEBUT"]).isoformat(),
                                                "Fin": pd.to_datetime(phase["DATE_FIN"]).isoformat(),
                                                "Parking": parc_name,
                                                "Catégorie": "Phase",
                                                "Places": int(phase["NB_PLACES_IMPACTEES"]) if pd.notna(phase.get("NB_PLACES_IMPACTEES")) else 0,
                                            })

                if gantt_externes:
                    df_gantt_ext = pd.DataFrame(gantt_externes)
                    st.vega_lite_chart(df_gantt_ext, {
                        "mark": {"type": "bar", "cornerRadiusEnd": 4, "height": 20},
                        "encoding": {
                            "y": {
                                "field": "Tâche",
                                "type": "ordinal",
                                "sort": None,
                                "axis": {"title": "", "labelLimit": 500, "labelOverlap": False}
                            },
                            "x": {
                                "field": "Début",
                                "type": "temporal",
                                "axis": {"title": "Période", "format": "%d/%m/%Y"}
                            },
                            "x2": {"field": "Fin", "type": "temporal"},
                            "color": {
                                "field": "Catégorie",
                                "type": "nominal",
                                "scale": {"domain": ["Global", "Phase"], "range": ["#3b82f6", "#f59e0b"]},
                                "legend": {"title": ""}
                            },
                            "tooltip": [
                                {"field": "Tâche", "type": "nominal"},
                                {"field": "Parking", "type": "nominal"},
                                {"field": "Places", "type": "quantitative", "title": "Places impactées"},
                                {"field": "Début", "type": "temporal", "format": "%d/%m/%Y"},
                                {"field": "Fin", "type": "temporal", "format": "%d/%m/%Y"}
                            ]
                        },
                        "height": max(200, len(gantt_externes) * 40),
                        "title": "Travaux externes — Impact multi-parkings (avec phases)"
                    }, use_container_width=True)
                else:
                    st.info("Aucun travaux externe avec dates complètes.")

        # === DISPONIBILITE DU PARKING SELECTIONNE ===
        if selected_detail:
            st.markdown("---")
            df_parcs_detail = get_parcs_evenement(code_detail)
            if not df_parcs_detail.empty:
                parking_filtre = df_parcs_detail["NOM_PARC"].tolist()[0]
                from core.queries import get_fait_disponibilite
                df_fait = get_fait_disponibilite()
                if not df_fait.empty:
                    df_fait_filtre = df_fait[df_fait["NOM_PARC"] == parking_filtre]
                    if not df_fait_filtre.empty:
                        with st.expander(f"📊 Disponibilité — {parking_filtre}", expanded=True):
                            st.dataframe(df_fait_filtre, use_container_width=True, hide_index=True,
                                column_config={
                                    "NOM_PARC": st.column_config.TextColumn("Parking"),
                                    "TITRE_EVENEMENT": st.column_config.TextColumn("Événement"),
                                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                                    "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                                    "CAPACITE_EXPLOITEE": st.column_config.NumberColumn("Capacité"),
                                    "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                                    "PLACES_DISPONIBLES": st.column_config.NumberColumn("Places disponibles"),
                                    "TAUX_IMPACT": st.column_config.ProgressColumn("Taux impact", format="%.1f%%", min_value=0, max_value=100),
                                    "IS_EN_COURS": st.column_config.CheckboxColumn("En cours"),
                                })


# ===== TAB: CREATION =====
with tab_create:
    st.subheader("Déclarer de nouveaux travaux")

    # Compteur de version pour réinitialiser les widgets
    if "trav_form_v" not in st.session_state:
        st.session_state["trav_form_v"] = 0
    v = st.session_state["trav_form_v"]

    df_types = get_ref_types()
    df_types_trav = df_types[df_types["IS_TRAVAUX"] == True]
    df_impacts = get_ref_impacts()
    df_parkings = get_parkings()

    titre = st.text_input("Titre des travaux *", max_chars=300, key=f"trav_titre_{v}",
        placeholder="Ex: Peinture sol niveau -2, Réfection barrière entrée...")

    # -- Type de travaux : METPARK / EXTERNE --
    st.markdown("##### 🔧 Type de travaux")
    type_travaux = st.radio(
        "Les travaux sont réalisés par *",
        options=["METPARK", "EXTERNE"],
        captions=["Équipe MetPark", "Prestataire externe"],
        horizontal=True,
        key=f"trav_type_{v}"
    )

    # Contacts
    st.markdown("##### 👤 Contacts")
    df_contacts = get_contacts_internes()
    contact_opts = {f"{row['NOM']} — {row['EMAIL']}": f"{row['NOM']} ({row['EMAIL']})" for _, row in df_contacts.iterrows()} if not df_contacts.empty else {}
    if type_travaux == "METPARK":
        selected_contact = st.selectbox("Contact interne Metpark *",
            options=[""] + list(contact_opts.keys()), index=0, key=f"trav_ci_{v}")
        contact_interne = contact_opts[selected_contact] if selected_contact else ""
        contact_externe = ""
    else:
        col1, col2 = st.columns(2)
        with col1:
            selected_contact = st.selectbox("Contact interne Metpark *",
                options=[""] + list(contact_opts.keys()), index=0, key=f"trav_ci_ext_{v}")
            contact_interne = contact_opts[selected_contact] if selected_contact else ""
        with col2:
            contact_externe = st.text_input("Nom de la société (externe) *", max_chars=200,
                placeholder="Ex: Vinci, Bouygues, Eiffage...", key=f"trav_ce_{v}")

    # -- Dates globales --
    st.markdown("##### 📅 Dates globales des travaux")
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("Date de début *", value=None, key=f"trav_dd_{v}")
    with col2:
        date_fin = st.date_input("Date de fin *", value=None, key=f"trav_df_{v}")

    # Journée partielle
    is_journee_partielle = st.checkbox("📅 Journée partielle", key=f"trav_jp_{v}")
    creneau = None
    if is_journee_partielle:
        creneau = st.selectbox("Créneau", options=["Matin", "Après-midi", "Nuit"], key=f"trav_creneau_{v}")

    # -- Parkings --
    st.markdown("##### 🅿️ Parking impacté")
    parking_options = dict(zip(df_parkings["NOM_PARC"], df_parkings["CODE_PARC"]))
    selected_parking = st.selectbox("Sélectionner le parking *", options=[""] + list(parking_options.keys()), index=0, key=f"trav_parkings_{v}")

    if selected_parking:
        parc_info = df_parkings[df_parkings["NOM_PARC"] == selected_parking].iloc[0]
        if pd.notna(parc_info.get("CAPACITE")):
            st.info(f"📊 Capacité : **{int(parc_info['CAPACITE'])} places** | Pistes entrée : {int(parc_info.get('NB_PISTES_ENTREE', 0))} | Pistes sortie : {int(parc_info.get('NB_PISTES_SORTIE', 0))}")

    # -- Places impactées --
    st.markdown("##### Impact sur les places")
    is_places_impactees = st.checkbox("🅿️ Impact sur le nombre de places", key=f"trav_places_cb_{v}")
    nb_places_impactees = None
    fermeture_totale = False
    if is_places_impactees:
        fermeture_totale = st.checkbox("🚫 Fermeture totale du parking (places disponibles = 0)", key=f"trav_fermeture_{v}")
        if not fermeture_totale:
            nb_places_impactees = st.number_input("Nombre de places impactées (phase 1)", min_value=0, value=0, key=f"trav_nb_places_{v}")

    # -- Pistes impactées --
    is_pistes_impactees = st.checkbox("🚧 Piste(s) impactée(s)", key=f"trav_pistes_cb_{v}")
    nb_pistes_entree = None
    nb_pistes_sortie = None
    fermeture_globale_pistes = False
    if is_pistes_impactees:
        fermeture_globale_pistes = st.checkbox("🚫 Fermeture globale des pistes (toutes entrées/sorties fermées)", key=f"trav_ferm_pistes_{v}")
        if not fermeture_globale_pistes:
            col1, col2 = st.columns(2)
            with col1:
                nb_pistes_entree = st.number_input("Nb pistes ENTRÉE fermées", min_value=0, value=0, key=f"trav_pe_{v}")
            with col2:
                nb_pistes_sortie = st.number_input("Nb pistes SORTIE fermées", min_value=0, value=0, key=f"trav_ps_{v}")
        else:
            st.info("🚫 Toutes les pistes (entrées et sorties) sont fermées.")

    # -- PHASAGE --
    st.markdown("---")
    st.markdown("##### 📋 Travaux phasés")
    is_travaux_phases = st.checkbox(
        "Travaux phasés (plusieurs phases avec places/secteurs différents)",
        help="Cocher si les places impactées ou le secteur changent au cours des travaux",
        key=f"trav_phases_cb_{v}"
    )

    # Si phasé, ignorer nb_places global (mais garder fermeture_totale)
    if is_travaux_phases:
        nb_places_impactees = None
        if is_places_impactees and not fermeture_totale:
            st.warning("⚠️ Pour les travaux phasés, les places impactées sont définies par phase (ci-dessous). Le nombre global est ignoré.")

    # Gestion dynamique des phases dans session_state
    if is_travaux_phases:
        st.info("💡 Définissez les phases de travaux ci-dessous.")

        if "phases_list" not in st.session_state:
            st.session_state["phases_list"] = []

        # Bouton pour ajouter une phase
        if st.button("➕ Ajouter une phase", key=f"trav_add_phase_{v}"):
            num = len(st.session_state["phases_list"]) + 1
            st.session_state["phases_list"].append({
                "numero": num,
                "date_debut": date_debut if num == 1 else None,
                "date_fin": date_fin,
                "nb_places": 0,
                "commentaire": ""
            })

        # Afficher les phases existantes
        phases_to_remove = []
        for i, phase in enumerate(st.session_state["phases_list"]):
            with st.container():
                st.markdown(f"**Phase {phase['numero']}**")
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    p_dd = st.date_input(
                        f"Début phase {phase['numero']}",
                        value=phase.get("date_debut"),
                        min_value=date_debut if date_debut else None,
                        max_value=date_fin if date_fin else None,
                        key=f"phase_dd_{i}"
                    )
                    st.session_state["phases_list"][i]["date_debut"] = p_dd
                with col2:
                    p_df = st.date_input(
                        f"Fin phase {phase['numero']}",
                        value=phase.get("date_fin"),
                        min_value=date_debut if date_debut else None,
                        max_value=date_fin if date_fin else None,
                        key=f"phase_df_{i}"
                    )
                    st.session_state["phases_list"][i]["date_fin"] = p_df
                with col3:
                    if not fermeture_totale:
                        p_pl = st.number_input(
                            f"Places phase {phase['numero']}",
                            min_value=0, value=phase.get("nb_places", 0),
                            key=f"phase_pl_{i}"
                        )
                        st.session_state["phases_list"][i]["nb_places"] = p_pl
                    else:
                        st.caption("🚫 Fermé")
                        st.session_state["phases_list"][i]["nb_places"] = 0

                p_comm = st.text_input(
                    f"Secteur impacté phase {phase['numero']} *",
                    value=phase.get("commentaire", ""),
                    placeholder="Ex: Niveau -2 zone A, Rampe d'accès nord...",
                    key=f"phase_comm_{i}"
                )
                st.session_state["phases_list"][i]["commentaire"] = p_comm

                if st.button(f"🗑️ Supprimer phase {phase['numero']}", key=f"phase_del_{i}"):
                    phases_to_remove.append(i)

                st.markdown("---")

        # Supprimer les phases marquées
        for idx in sorted(phases_to_remove, reverse=True):
            st.session_state["phases_list"].pop(idx)
        # Renuméroter
        for j, p in enumerate(st.session_state["phases_list"]):
            p["numero"] = j + 1

    # -- Impact --
    st.markdown("##### Impact")
    impact_options = dict(zip(
        df_impacts["LIBELLE_IMPACT"] + " (niv. " + df_impacts["NIVEAU_SEVERITE"].astype(str) + ")",
        df_impacts["CODE_IMPACT"]
    ))
    selected_impact = st.selectbox("Impact", options=[""] + list(impact_options.keys()), index=0, key=f"trav_impact_{v}")

    # -- Commentaire --
    commentaire = st.text_area("Commentaire général", max_chars=2000, key=f"trav_comm_{v}")

    # -- Submit --
    st.markdown("---")
    if st.button("💾 Créer les travaux", type="primary", key=f"btn_create_trav_{v}"):
        if not titre.strip():
            st.error("Le titre est obligatoire.")
        elif date_debut is None:
            st.error("La date de début est obligatoire.")
        elif date_fin is None:
            st.error("La date de fin est obligatoire.")
        elif not contact_interne.strip():
            st.error("Le contact interne est obligatoire.")
        elif type_travaux == "EXTERNE" and not contact_externe.strip():
            st.error("Le contact externe est obligatoire pour les travaux externes.")
        elif not selected_parking:
            st.error("Sélectionnez un parking impacté.")
        elif is_travaux_phases and "phases_list" in st.session_state and any(
            not phase.get("commentaire", "").strip() for phase in st.session_state["phases_list"]
        ):
            st.error("Le secteur impacté est obligatoire pour chaque phase.")
        else:
            # Déterminer le code type
            if type_travaux == "METPARK":
                type_row = df_types_trav[df_types_trav["LIBELLE_TYPE_EVENEMENT"].str.contains("interne", case=False)]
            else:
                type_row = df_types_trav[df_types_trav["LIBELLE_TYPE_EVENEMENT"].str.contains("externe", case=False)]

            code_type_final = int(type_row.iloc[0]["CODE_TYPE_EVENEMENT"]) if not type_row.empty else int(df_types_trav.iloc[0]["CODE_TYPE_EVENEMENT"])

            timestamp_debut = f"{date_debut} 00:00:00"
            timestamp_fin_sql = f"'{date_fin} 23:59:00'"

            code_impact = int(impact_options[selected_impact]) if selected_impact else None

            insert_evenement(
                titre=titre,
                code_type=code_type_final,
                code_description=None,
                description_autre=None,
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
                nb_pistes_entree=nb_pistes_entree if is_pistes_impactees and not fermeture_globale_pistes else None,
                nb_pistes_sortie=nb_pistes_sortie if is_pistes_impactees and not fermeture_globale_pistes else None,
                fermeture_globale_pistes=fermeture_globale_pistes,
                type_travaux=type_travaux,
                contact_interne=contact_interne,
                contact_externe=contact_externe if type_travaux == "EXTERNE" else None,
                is_travaux_phases=is_travaux_phases,
                commentaire=commentaire,
                user=sf_user
            )

            new_code = get_max_code_evenement()

            # Parking
            insert_parc_evenement(new_code, parking_options[selected_parking], selected_parking)

            # Phases
            if is_travaux_phases and "phases_list" in st.session_state:
                for phase in st.session_state["phases_list"]:
                    if phase["date_debut"] and phase["date_fin"]:
                        insert_phase_travaux(
                            new_code, phase["numero"],
                            str(phase["date_debut"]), str(phase["date_fin"]),
                            phase["nb_places"] if phase["nb_places"] > 0 else None,
                            phase["commentaire"]
                        )
                st.session_state["phases_list"] = []

            log_modification(new_code, "CREATION", sf_user)
            recalculer_disponibilite()
            notify("✅ Travaux créés avec succès !")
            st.session_state["trav_form_v"] += 1
            if "phases_list" in st.session_state:
                del st.session_state["phases_list"]
            st.rerun()


# ===== TAB: MODIFICATION / PHASES =====
with tab_edit:
    st.subheader("Modifier des travaux / Gérer les phases")

    df_events_edit = get_evenements()
    df_trav_edit = filter_travaux(df_events_edit)

    if df_trav_edit.empty:
        st.info("Aucun travaux à modifier.")
    else:
        df_parkings_edit = get_parkings()

        search_edit = st.text_input("🔍 Rechercher", placeholder="Tapez pour filtrer...", key="trav_search_edit")
        df_edit_filtered = search_evenements(df_trav_edit, search_edit)

        if df_edit_filtered.empty:
            st.warning("Aucun travaux trouvé.")
        else:
            evt_options = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_edit_filtered.iterrows()}
            selected_edit = st.selectbox("Sélectionner les travaux", options=list(evt_options.keys()), key="trav_edit_sel")

            if selected_edit:
                code_edit = evt_options[selected_edit]
                evt_row = df_trav_edit[df_trav_edit["CODE_EVENEMENT"] == code_edit].iloc[0]

                with st.expander("📄 Valeurs actuelles", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Titre :** {evt_row['TITRE_EVENEMENT']}")
                        st.markdown(f"**Type :** {evt_row.get('TYPE_TRAVAUX', '-')}")
                        st.markdown(f"**Contact int. :** {evt_row.get('CONTACT_INTERNE', '-')}")
                        st.markdown(f"**Contact ext. :** {evt_row.get('CONTACT_EXTERNE', '-') if pd.notna(evt_row.get('CONTACT_EXTERNE')) else '-'}")
                    with col2:
                        st.markdown(f"**Début :** {evt_row['DATE_DEBUT']}")
                        st.markdown(f"**Fin :** {evt_row['DATE_FIN'] if pd.notna(evt_row['DATE_FIN']) else '-'}")
                    with col3:
                        if evt_row.get('NB_PLACES_IMPACTEES') and pd.notna(evt_row['NB_PLACES_IMPACTEES']):
                            st.markdown(f"**Places :** {int(evt_row['NB_PLACES_IMPACTEES'])}")
                        if evt_row.get('FERMETURE_TOTALE'):
                            st.error("🚫 FERMETURE TOTALE")
                        df_parcs = get_parcs_evenement(code_edit)
                        if not df_parcs.empty:
                            st.markdown(f"**Parkings :** {', '.join(df_parcs['NOM_PARC'].tolist())}")

                # Modification rapide
                new_titre = st.text_input("Titre", placeholder="Laisser vide pour conserver", key=f"trav_edit_titre_{code_edit}")
                col1, col2 = st.columns(2)
                with col1:
                    new_date_debut = st.date_input("Date de début", value=None, key=f"trav_e_dd_{code_edit}")
                    df_contacts_edit = get_contacts_internes()
                    contact_opts_edit = {f"{row['NOM']} — {row['EMAIL']}": f"{row['NOM']} ({row['EMAIL']})" for _, row in df_contacts_edit.iterrows()} if not df_contacts_edit.empty else {}
                    new_selected_contact = st.selectbox("Contact interne Metpark",
                        options=["(conserver)"] + list(contact_opts_edit.keys()), index=0, key=f"trav_edit_ci_{code_edit}")
                    new_contact_interne = contact_opts_edit[new_selected_contact] if new_selected_contact != "(conserver)" else ""
                with col2:
                    new_date_fin = st.date_input("Date de fin", value=None, key=f"trav_e_df_{code_edit}")
                    new_contact_externe = st.text_input("Nom de la société (externe)", placeholder="Laisser vide pour conserver", key=f"trav_edit_ce_{code_edit}")

                new_fermeture = st.checkbox(
                    "🚫 Fermeture totale",
                    value=bool(evt_row.get('FERMETURE_TOTALE')),
                    key=f"trav_edit_ferm_{code_edit}"
                )
                if not new_fermeture:
                    new_nb_places = st.number_input("Nb places impactées (0 = ne pas modifier)", min_value=0, value=0, key=f"trav_edit_pl_{code_edit}")
                else:
                    st.info("🚫 Fermeture totale : les places impactées = capacité totale du parking.")
                    new_nb_places = 0

                new_commentaire = st.text_input("Commentaire", placeholder="Laisser vide pour conserver", key=f"trav_edit_comm_{code_edit}")

                st.markdown("---")
                if st.button("💾 Enregistrer modifications", type="primary", key=f"btn_edit_trav_{code_edit}"):
                    set_parts = []
                    if new_titre.strip():
                        set_parts.append(f"TITRE_EVENEMENT = '{new_titre.replace(chr(39), chr(39)+chr(39))}'")
                    if new_date_debut:
                        set_parts.append(f"DATE_DEBUT = '{new_date_debut} 00:00:00'")
                    if new_date_fin:
                        set_parts.append(f"DATE_FIN = '{new_date_fin} 23:59:00'")
                    if new_contact_interne.strip():
                        set_parts.append(f"CONTACT_INTERNE = '{new_contact_interne.replace(chr(39), chr(39)+chr(39))}'")
                    if new_contact_externe.strip():
                        set_parts.append(f"CONTACT_EXTERNE = '{new_contact_externe.replace(chr(39), chr(39)+chr(39))}'")
                    if new_fermeture:
                        set_parts.append("FERMETURE_TOTALE = TRUE")
                        set_parts.append("IS_PLACES_IMPACTEES = TRUE")
                        set_parts.append("NB_PLACES_IMPACTEES = NULL")
                    elif not new_fermeture and bool(evt_row.get('FERMETURE_TOTALE')):
                        set_parts.append("FERMETURE_TOTALE = FALSE")
                    if not new_fermeture and new_nb_places > 0:
                        set_parts.append(f"NB_PLACES_IMPACTEES = {new_nb_places}")
                        set_parts.append("IS_PLACES_IMPACTEES = TRUE")
                    if new_commentaire.strip():
                        set_parts.append(f"COMMENTAIRE = '{new_commentaire.replace(chr(39), chr(39)+chr(39))}'")

                    if set_parts:
                        update_evenement(code_edit, set_parts, sf_user)
                        log_modification(code_edit, "MODIFICATION", sf_user)
                        recalculer_disponibilite()
                        notify("✏️ Travaux modifiés")
                        st.rerun()
                    else:
                        st.info("Aucune modification.")

                # -- SECTION PHASES --
                st.markdown("---")
                st.markdown("##### 📋 Gestion des phases de travaux")

                df_phases = get_phases_travaux(code_edit)
                if not df_phases.empty:
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
                            if st.button("✏️", key=f"edit_ph_trav_{code_ph}", help="Modifier cette phase"):
                                st.session_state[f"editing_phase_trav_{code_ph}"] = True
                        with col_del:
                            if st.button("🗑️", key=f"del_ph_trav_{code_ph}", help="Supprimer cette phase"):
                                delete_phase_by_id(code_ph)
                                log_modification(code_edit, "SUPPRESSION_PHASE", sf_user)
                                notify(f"Phase {num_ph} supprimée")
                                st.rerun()

                        # Formulaire de modification inline
                        if st.session_state.get(f"editing_phase_trav_{code_ph}", False):
                            with st.form(f"form_edit_ph_trav_{code_ph}"):
                                st.markdown(f"_Modifier la phase {num_ph} :_")
                                col1, col2 = st.columns(2)
                                with col1:
                                    edit_dd = st.date_input("Début", value=pd.to_datetime(phase_row['DATE_DEBUT']).date() if pd.notna(phase_row['DATE_DEBUT']) else None, key=f"edit_ph_trav_dd_{code_ph}")
                                    if not evt_row.get('FERMETURE_TOTALE'):
                                        edit_places = st.number_input("Places impactées", min_value=0, value=int(phase_row['NB_PLACES_IMPACTEES']) if pd.notna(phase_row.get('NB_PLACES_IMPACTEES')) else 0, key=f"edit_ph_trav_pl_{code_ph}")
                                    else:
                                        st.info("🚫 Fermeture totale — places = capacité")
                                        edit_places = 0
                                with col2:
                                    edit_df = st.date_input("Fin", value=pd.to_datetime(phase_row['DATE_FIN']).date() if pd.notna(phase_row['DATE_FIN']) else None, key=f"edit_ph_trav_df_{code_ph}")
                                    edit_comm = st.text_input("Secteur", value=phase_row.get('COMMENTAIRE', '') or '', key=f"edit_ph_trav_co_{code_ph}")

                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    submitted = st.form_submit_button("💾 Enregistrer")
                                with col_cancel:
                                    cancelled = st.form_submit_button("❌ Annuler")

                                if submitted:
                                    update_phase(code_ph, str(edit_dd), str(edit_df), edit_places if edit_places > 0 else None, edit_comm)
                                    del st.session_state[f"editing_phase_trav_{code_ph}"]
                                    log_modification(code_edit, "MODIFICATION_PHASE", sf_user)
                                    recalculer_disponibilite()
                                    notify(f"Phase {num_ph} modifiée !")
                                    st.rerun()
                                elif cancelled:
                                    del st.session_state[f"editing_phase_trav_{code_ph}"]
                                    st.rerun()

                    st.markdown("")
                    if st.button("🗑️ Supprimer toutes les phases", key=f"del_all_ph_{code_edit}"):
                        delete_phases_travaux(code_edit)
                        log_modification(code_edit, "SUPPRESSION_PHASES", sf_user)
                        notify("Toutes les phases supprimées")
                        st.rerun()
                else:
                    st.info("Aucune phase définie. Ajoutez-en ci-dessous.")

                # Ajouter une phase
                st.markdown("**➕ Ajouter une phase :**")
                col1, col2 = st.columns(2)
                with col1:
                    ph_dd = st.date_input("Début de la phase", value=None, key=f"ph_add_dd_{code_edit}")
                with col2:
                    ph_df = st.date_input("Fin de la phase", value=None, key=f"ph_add_df_{code_edit}")

                ph_places = st.number_input("Nb places impactées cette phase", min_value=0, value=0, key=f"ph_add_pl_{code_edit}") if not evt_row.get('FERMETURE_TOTALE') else 0
                if evt_row.get('FERMETURE_TOTALE'):
                    st.info("🚫 Fermeture totale — places = capacité")
                ph_comm = st.text_input("Secteur du parking impacté", placeholder="Ex: Niveau -2 zone A, Rampe nord...", key=f"ph_add_co_{code_edit}")

                if st.button("➕ Ajouter la phase", key=f"btn_add_ph_{code_edit}"):
                    if ph_dd and ph_df:
                        next_num = len(df_phases) + 1 if not df_phases.empty else 1
                        insert_phase_travaux(
                            code_edit, next_num,
                            str(ph_dd), str(ph_df),
                            ph_places if ph_places > 0 else None,
                            ph_comm
                        )
                        # Marquer l'événement comme phasé si pas encore
                        if not evt_row.get('IS_TRAVAUX_PHASES'):
                            update_evenement(code_edit, ["IS_TRAVAUX_PHASES = TRUE"], sf_user)
                        log_modification(code_edit, "AJOUT_PHASE", sf_user)
                        notify(f"Phase {next_num} ajoutée !")
                        st.rerun()
                    else:
                        st.error("Les dates de début et fin de la phase sont obligatoires.")


# ===== TAB: SUPPRESSION =====
with tab_delete:
    st.subheader("Supprimer des travaux")

    df_events_del = get_evenements()
    df_trav_del = filter_travaux(df_events_del)

    if df_trav_del.empty:
        st.info("Aucun travaux à supprimer.")
    else:
        evt_del_opts = {f"{row['CODE_EVENEMENT']} - {row['TITRE_EVENEMENT']}": row['CODE_EVENEMENT'] for _, row in df_trav_del.iterrows()}
        selected_del = st.selectbox("Sélectionner", options=list(evt_del_opts.keys()), key="trav_del_sel")

        if selected_del:
            code_del = evt_del_opts[selected_del]
            evt_del = df_trav_del[df_trav_del["CODE_EVENEMENT"] == code_del].iloc[0]

            st.markdown(f"**{evt_del['TITRE_EVENEMENT']}** — {evt_del.get('TYPE_TRAVAUX', '')} — {evt_del['DATE_DEBUT']}")
            st.error("⚠️ Les travaux et toutes leurs phases seront supprimés.")

            if st.button("🗑️ Confirmer la suppression", type="primary", key="btn_del_trav"):
                delete_evenement(code_del, sf_user)
                log_modification(code_del, "SUPPRESSION", sf_user)
                close_all_snapshots(code_del)
                recalculer_disponibilite()
                notify("🗑️ Travaux supprimés")
                st.rerun()


# ===== TAB: HISTORIQUE =====
with tab_history:
    st.subheader("Historique des travaux")
    df_hist = get_historique_complet()
    if df_hist.empty:
        st.info("Aucun historique.")
    else:
        # Filtrer sur les travaux
        df_hist_trav = df_hist[df_hist["TYPE_EVENEMENT"].str.contains("Travaux", na=False)] if "TYPE_EVENEMENT" in df_hist.columns else df_hist
        if df_hist_trav.empty:
            st.info("Aucun historique pour les travaux.")
        else:
            st.caption(f"{len(df_hist_trav)} entrée(s)")
            st.dataframe(df_hist_trav, use_container_width=True, hide_index=True,
                column_config={
                    "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
                    "TITRE_EVENEMENT": st.column_config.TextColumn("Titre"),
                    "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
                    "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places"),
                    "FERMETURE_TOTALE": st.column_config.CheckboxColumn("Fermé"),
                    "PARKINGS_IMPACTES": st.column_config.TextColumn("Parkings"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                    "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                    "MODIFIE_PAR": st.column_config.TextColumn("Par"),
                    "ACTION": st.column_config.TextColumn("Action"),
                    "DATE_DEBUT_VALIDITE": st.column_config.DatetimeColumn("Date modif", format="DD/MM/YYYY HH:mm"),
                })

            # Historique par phase
            st.markdown("---")
            st.subheader("📋 Détail des phases")
            df_all_phases = get_all_phases_travaux()
            if not df_all_phases.empty:
                codes_trav = df_hist_trav["CODE_EVENEMENT"].unique().tolist()
                df_phases_trav = df_all_phases[df_all_phases["CODE_EVENEMENT"].isin(codes_trav)]
                if not df_phases_trav.empty:
                    st.dataframe(df_phases_trav, use_container_width=True, hide_index=True,
                        column_config={
                            "CODE_EVENEMENT": st.column_config.NumberColumn("ID événement", width="small"),
                            "NUMERO_PHASE": st.column_config.NumberColumn("Phase"),
                            "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY"),
                            "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY"),
                            "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
                            "COMMENTAIRE": st.column_config.TextColumn("Secteur"),
                        })
                else:
                    st.info("Aucune phase de travaux.")
            else:
                st.info("Aucune phase de travaux enregistrée.")
