import streamlit as st
import pandas as pd

from core.queries import get_evenements_par_parking, get_stats_par_parking

st.title("🚗 Impact par Parking")
st.caption("Vue des événements impactant chaque parking MetPark — Taux d'occupation mis à jour automatiquement")

# -- Load data --
df_events_parking = get_evenements_par_parking()
df_stats = get_stats_par_parking()

if df_stats.empty:
    st.info("Aucun événement associé à un parking pour le moment.")
    st.stop()

# -- KPIs globaux --
st.subheader("📊 Vue d'ensemble")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Parkings impactés", len(df_stats))
with col2:
    st.metric("Événements actifs", df_events_parking["CODE_EVENEMENT"].nunique())
with col3:
    max_sev = df_stats["SEVERITE_MAX"].max() if not df_stats.empty else 0
    st.metric("Sévérité max", f"{max_sev}/4")
with col4:
    total_places = df_stats["TOTAL_PLACES_IMPACTEES"].sum() if "TOTAL_PLACES_IMPACTEES" in df_stats.columns else 0
    st.metric("Total places impactées", int(total_places))

st.markdown("---")

# -- Classement des parkings avec taux d'occupation --
st.subheader("🏆 Classement par impact")

# Calculer le taux d'occupation impacté
df_display_stats = df_stats.copy()
if "CAPACITE" in df_display_stats.columns and "TOTAL_PLACES_IMPACTEES" in df_display_stats.columns:
    df_display_stats["TAUX_IMPACT"] = df_display_stats.apply(
        lambda row: min(100, round((row["TOTAL_PLACES_IMPACTEES"] / row["CAPACITE"]) * 100, 1))
        if pd.notna(row.get("CAPACITE")) and row["CAPACITE"] > 0 else 0,
        axis=1
    )
    df_display_stats["PLACES_DISPONIBLES"] = df_display_stats.apply(
        lambda row: max(0, int(row["CAPACITE"] - row["TOTAL_PLACES_IMPACTEES"]))
        if pd.notna(row.get("CAPACITE")) else None,
        axis=1
    )

st.dataframe(df_display_stats, use_container_width=True, hide_index=True,
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

# Bar chart
if not df_display_stats.empty:
    st.bar_chart(df_display_stats.set_index("PARKING")["NB_EVENEMENTS"])

# Chart taux d'impact
if "TAUX_IMPACT" in df_display_stats.columns:
    st.subheader("📈 Taux d'impact par parking")
    st.bar_chart(df_display_stats.set_index("PARKING")["TAUX_IMPACT"])

st.markdown("---")

# -- Alertes fermetures totales --
if not df_events_parking.empty and "FERMETURE_TOTALE" in df_events_parking.columns:
    df_fermetures = df_events_parking[df_events_parking["FERMETURE_TOTALE"] == True]
    if not df_fermetures.empty:
        st.subheader("🚫 Fermetures totales en cours")
        for _, row in df_fermetures.iterrows():
            st.error(f"**{row['PARKING']}** — {row['TITRE_EVENEMENT']} (du {row['DATE_DEBUT']} au {row['DATE_FIN'] if pd.notna(row['DATE_FIN']) else '?'})")
        st.markdown("---")

# -- Detail par parking --
st.subheader("📋 Détail par parking")

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
