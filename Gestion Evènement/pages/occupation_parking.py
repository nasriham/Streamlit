import streamlit as st
import pandas as pd

from core.queries import (
    get_evenements_par_parking, get_stats_par_parking,
    get_disponibilite_parkings, get_fait_disponibilite, recalculer_disponibilite
)

st.title("🚗 Impact par Parking")
st.caption("Vue des événements impactant chaque parking MetPark — Disponibilité calculée depuis la table de fait")

# -- Bouton de rafraîchissement --
if st.button("🔄 Recalculer la disponibilité", help="Recalcule la table de fait à partir des événements actifs"):
    recalculer_disponibilite()
    st.toast("Disponibilité recalculée !")
    st.rerun()

# -- Load data --
df_dispo = get_disponibilite_parkings()
df_fait = get_fait_disponibilite()
df_events_parking = get_evenements_par_parking()
df_stats = get_stats_par_parking()

# ===== SECTION 1 : DISPONIBILITE EN COURS =====
st.subheader("📊 Disponibilité des parkings")

# Toggle pour voir tout ou seulement en cours
vue_complete = st.toggle("Inclure les événements à venir", value=True, help="Affiche tous les parkings impactés, pas seulement ceux avec un événement en cours")

if vue_complete:
    # Utiliser get_stats_par_parking qui montre tous les événements actifs
    df_vue = df_stats.copy() if not df_stats.empty else pd.DataFrame()
    if not df_vue.empty and "CAPACITE" in df_vue.columns and "TOTAL_PLACES_IMPACTEES" in df_vue.columns:
        df_vue["TAUX_IMPACT"] = df_vue.apply(
            lambda row: min(100, round((row["TOTAL_PLACES_IMPACTEES"] / row["CAPACITE"]) * 100, 1))
            if pd.notna(row.get("CAPACITE")) and row["CAPACITE"] > 0 else 0,
            axis=1
        )
        df_vue["PLACES_DISPONIBLES"] = df_vue.apply(
            lambda row: max(0, int(row["CAPACITE"] - row["TOTAL_PLACES_IMPACTEES"]))
            if pd.notna(row.get("CAPACITE")) else None,
            axis=1
        )
else:
    df_vue = df_dispo.copy() if not df_dispo.empty else pd.DataFrame()

if df_vue.empty:
    st.success("Aucun parking impacté." if not vue_complete else "Aucun événement associé à un parking.")
else:
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Parkings impactés", len(df_vue))
    with col2:
        col_places = "TOTAL_PLACES_IMPACTEES" if "TOTAL_PLACES_IMPACTEES" in df_vue.columns else None
        total_impactees = int(df_vue[col_places].sum()) if col_places else 0
        st.metric("Places impactées", total_impactees)
    with col3:
        col_dispo = "PLACES_DISPONIBLES" if "PLACES_DISPONIBLES" in df_vue.columns else None
        total_dispo = int(df_vue[col_dispo].sum()) if col_dispo else 0
        st.metric("Places disponibles", total_dispo)
    with col4:
        if "FERMETURE_TOTALE" in df_vue.columns:
            nb_fermetures = int(df_vue["FERMETURE_TOTALE"].sum())
        else:
            nb_fermetures = 0
        st.metric("Fermetures totales", nb_fermetures)

    # Alertes fermetures totales
    if "FERMETURE_TOTALE" in df_vue.columns:
        df_ferme = df_vue[df_vue["FERMETURE_TOTALE"] == True]
        if not df_ferme.empty:
            for _, row in df_ferme.iterrows():
                parc = row.get('NOM_PARC', row.get('PARKING', ''))
                cap = int(row.get('CAPACITE_EXPLOITEE', row.get('CAPACITE', 0))) if pd.notna(row.get('CAPACITE_EXPLOITEE', row.get('CAPACITE'))) else '?'
                st.error(f"🚫 **{parc}** — Fermeture totale ({cap} places indisponibles)")

    st.markdown("---")

    # Tableau de disponibilité / classement
    titre_section = "🏆 Classement par taux d'impact" + (" (tous événements)" if vue_complete else " (en cours uniquement)")
    st.subheader(titre_section)

    if vue_complete:
        st.dataframe(df_vue, use_container_width=True, hide_index=True,
            column_config={
                "PARKING": st.column_config.TextColumn("Parking"),
                "CAPACITE": st.column_config.NumberColumn("Capacité", format="%d"),
                "NB_EVENEMENTS": st.column_config.NumberColumn("Nb événements", format="%d"),
                "SEVERITE_MAX": st.column_config.NumberColumn("Sévérité max", format="%d ⚠️"),
                "TOTAL_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées", format="%d"),
                "PLACES_DISPONIBLES": st.column_config.NumberColumn("Places disponibles", format="%d"),
                "TAUX_IMPACT": st.column_config.ProgressColumn("Taux d'impact", format="%.1f%%", min_value=0, max_value=100),
                "PREMIER_EVENEMENT": st.column_config.DatetimeColumn("Premier événement", format="DD/MM/YYYY"),
                "DERNIER_EVENEMENT": st.column_config.DatetimeColumn("Dernier événement", format="DD/MM/YYYY"),
            })
    else:
        st.dataframe(df_vue, use_container_width=True, hide_index=True,
            column_config={
                "CODE_PARC": st.column_config.TextColumn("Code"),
                "NOM_PARC": st.column_config.TextColumn("Parking"),
                "CAPACITE_EXPLOITEE": st.column_config.NumberColumn("Capacité exploitée", format="%d"),
                "TOTAL_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées", format="%d"),
                "PLACES_DISPONIBLES": st.column_config.NumberColumn("Places disponibles", format="%d"),
                "TAUX_IMPACT": st.column_config.ProgressColumn("Taux d'impact", format="%.1f%%", min_value=0, max_value=100),
                "NB_EVENEMENTS_EN_COURS": st.column_config.NumberColumn("Nb événements"),
                "FERMETURE_TOTALE": st.column_config.CheckboxColumn("Fermé"),
            })

    # Chart
    if "TAUX_IMPACT" in df_vue.columns:
        col_parking = "NOM_PARC" if "NOM_PARC" in df_vue.columns else "PARKING"
        if col_parking in df_vue.columns:
            st.bar_chart(df_vue.set_index(col_parking)["TAUX_IMPACT"])

st.markdown("---")

# ===== SECTION 2 : DETAIL PAR PARKING =====
st.subheader("🔍 Détail par parking")

if not df_events_parking.empty:
    parkings_list = sorted(df_events_parking["PARKING"].dropna().unique().tolist())
    selected_parking = st.selectbox("Sélectionner un parking", options=["Tous"] + parkings_list)

    if selected_parking == "Tous":
        df_display = df_events_parking
    else:
        df_display = df_events_parking[df_events_parking["PARKING"] == selected_parking]

    # Afficher capacité si un parking est sélectionné
    if selected_parking != "Tous" and "CAPACITE" in df_display.columns:
        capacite = df_display.iloc[0]["CAPACITE"] if not df_display.empty else None
        if capacite and pd.notna(capacite):
            st.info(f"📊 Capacité de **{selected_parking}** : {int(capacite)} places")

    st.caption(f"{len(df_display)} événement(s)")

    display_cols = ["PARKING", "CODE_EVENEMENT", "TITRE_EVENEMENT", "TYPE_EVENEMENT", "CATEGORIE",
                    "IMPACT", "NIVEAU_SEVERITE", "DATE_DEBUT", "DATE_FIN",
                    "NB_PLACES_IMPACTEES", "FERMETURE_TOTALE"]
    available_cols = [c for c in display_cols if c in df_display.columns]

    st.dataframe(df_display[available_cols], use_container_width=True, hide_index=True,
        column_config={
            "PARKING": st.column_config.TextColumn("Parking"),
            "CODE_EVENEMENT": st.column_config.NumberColumn("ID", width="small"),
            "TITRE_EVENEMENT": st.column_config.TextColumn("Événement"),
            "TYPE_EVENEMENT": st.column_config.TextColumn("Type"),
            "CATEGORIE": st.column_config.TextColumn("Catégorie"),
            "IMPACT": st.column_config.TextColumn("Impact"),
            "NIVEAU_SEVERITE": st.column_config.NumberColumn("Sévérité", format="%d ⚠️"),
            "DATE_DEBUT": st.column_config.DatetimeColumn("Début", format="DD/MM/YYYY HH:mm"),
            "DATE_FIN": st.column_config.DatetimeColumn("Fin", format="DD/MM/YYYY HH:mm"),
            "NB_PLACES_IMPACTEES": st.column_config.NumberColumn("Places impactées"),
            "FERMETURE_TOTALE": st.column_config.CheckboxColumn("Fermeture totale"),
        })

st.markdown("---")

# ===== SECTION 3 : DETAIL DISPONIBILITE (filtré par parking sélectionné) =====
with st.expander("📄 Détail disponibilité par événement"):
    if df_fait.empty:
        st.info("Aucune donnée de disponibilité.")
    else:
        # Filtrer par le parking sélectionné au-dessus
        if selected_parking and selected_parking != "Tous":
            df_fait_display = df_fait[df_fait["NOM_PARC"] == selected_parking]
            st.caption(f"{len(df_fait_display)} ligne(s) — Filtré sur **{selected_parking}**")
        else:
            df_fait_display = df_fait
            st.caption(f"{len(df_fait_display)} ligne(s) — Tous les parkings")

        if df_fait_display.empty:
            st.info(f"Aucune donnée de disponibilité pour {selected_parking}.")
        else:
            st.dataframe(df_fait_display, use_container_width=True, hide_index=True)
