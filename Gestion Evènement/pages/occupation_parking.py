import streamlit as st
import pandas as pd

from core.queries import get_evenements_par_parking, get_stats_par_parking

st.title("🚗 Impact par Parking")
st.caption("Vue des événements impactant chaque parking MetPark")

# -- Load data --
df_events_parking = get_evenements_par_parking()
df_stats = get_stats_par_parking()

if df_stats.empty:
    st.info("Aucun événement associé à un parking pour le moment.")
    st.stop()

# -- KPIs globaux --
st.subheader("📊 Vue d'ensemble")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Parkings impactés", len(df_stats))
with col2:
    st.metric("Événements actifs", df_events_parking["CODE_EVENEMENT"].nunique())
with col3:
    max_sev = df_stats["SEVERITE_MAX"].max() if not df_stats.empty else 0
    st.metric("Sévérité max", f"{max_sev}/4")

st.markdown("---")

# -- Classement des parkings --
st.subheader("🏆 Classement par nombre d'événements")

st.dataframe(df_stats, use_container_width=True, hide_index=True,
    column_config={
        "PARKING": st.column_config.TextColumn("Parking"),
        "NB_EVENEMENTS": st.column_config.NumberColumn("Nb événements", format="%d"),
        "SEVERITE_MAX": st.column_config.NumberColumn("Sévérité max", format="%d ⚠️"),
        "PREMIER_EVENEMENT": st.column_config.DatetimeColumn("Premier événement", format="DD/MM/YYYY"),
        "DERNIER_EVENEMENT": st.column_config.DatetimeColumn("Dernier événement", format="DD/MM/YYYY"),
    })

# Bar chart
if not df_stats.empty:
    st.bar_chart(df_stats.set_index("PARKING")["NB_EVENEMENTS"])

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

    st.caption(f"{len(df_display)} événement(s)")
    st.dataframe(df_display, use_container_width=True, hide_index=True,
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
        })
