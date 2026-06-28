# Page Securite incendie avec onglets et formulaire (sans suppression)
# Co-authored with CoCo
import streamlit as st
import pandas as pd
from core.queries import (
    get_parks,
    get_parks_incendie,
    insert_incendie,
    update_incendie
)
from core.functions import (
    show_notification,
    notify
)

user = getattr(st.user, "user_name", "SYSTEM")

show_notification()

st.title("🔥 Sécurité incendie")
st.caption(f"Données de sécurité incendie — Connecté : **{user}**")
st.divider()

df = get_parks_incendie()
df_parks_ref = get_parks()
parc_names = df_parks_ref.set_index("CODE_PARC")["NOM_PARC"].to_dict()
if not df.empty:
    df["NOM_PARC"] = df["CODE_PARC"].map(parc_names)

OUI_NON_OPTIONS = ["", "O", "N"]
OUI_NON_DISPLAY = {"": "Non renseigné", "O": "Oui", "N": "Non"}

TARIFS_ELEC_OPTIONS = ["", "Bleu", "Jaune", "Vert"]
AVIS_COMMISSION_OPTIONS = ["", "Favorable", "Favorable avec prescriptions", "Defavorable"]

def safe_int(val):
    if pd.notna(val):
        try:
            return int(val)
        except (ValueError, TypeError):
            pass
    return 0

tab_search, tab_edit, tab_history = st.tabs([
    "🔍 Rechercher", "✏️ Modifier", "📜 Historique"
])

# ===== CONSULTER =====
with tab_search:
    st.subheader("Données incendie par parc")
    search = st.text_input("🔍 Rechercher", key="search_inc")
    if df.empty:
        st.info("Aucune donnée.")
    else:
        DATA_COLS = [c for c in ["NOM_PARC", "EAE_SPRINKLEURS", "NB_POSTES", "NB_TETES",
            "NB_DAI", "FLAG_SSI", "TYPE_SSI", "MARQUE_SSI", "DATE_MISE_EN_SERVICE_SSI",
            "NB_EXTINCTEURS_TOTAL", "NB_DETECTION_CO_NO", "NB_PORTE_COMPARTIMENTAGE",
            "NB_EXTRACTEURS", "NB_INSUFFLATEURS", "NB_COLONNES_SECHES", "NB_BAES",
            "TYPE_ALIMENTATION_BAES", "NB_TRAPPE_EVACUATION_MOTORISEE",
            "TYPE_TARIFS_ELEC", "FLAG_CELLULES_HT", "FLAG_GROUPE_ELECTROGENE", "FLAG_TGS",
            "CAPACITE_CUVE_FIOUL", "DATE_DERNIERE_COMMISSION", "AVIS_COMMISSION",
            "NOM_CREATEUR", "NOM_MODIFICATEUR", "DATE_DEBUT", "DATE_FIN", "IS_ACTIVE"] if c in df.columns]
        df_d = df[DATA_COLS].copy()
        if search:
            term = search.lower()
            mask = pd.Series([False] * len(df_d))
            for col in DATA_COLS:
                mask = mask | df_d[col].astype(str).str.lower().str.contains(term, na=False)
            df_d = df_d[mask]
        st.caption(f"{len(df_d)} ligne(s)")
        st.dataframe(df_d, use_container_width=True, hide_index=True, column_config={
            "NOM_PARC": st.column_config.TextColumn("Nom Parc", width="medium"),
            "EAE_SPRINKLEURS": st.column_config.TextColumn("EAE Sprinklers"),
            "NB_POSTES": st.column_config.NumberColumn("Postes"),
            "NB_TETES": st.column_config.NumberColumn("Têtes"),
            "NB_DAI": st.column_config.NumberColumn("DAI"),
            "FLAG_SSI": st.column_config.TextColumn("SSI"),
            "TYPE_SSI": st.column_config.TextColumn("Type SSI"),
            "MARQUE_SSI": st.column_config.TextColumn("Marque SSI"),
            "DATE_MISE_EN_SERVICE_SSI": st.column_config.DateColumn("Date mise en service SSI", format="DD/MM/YYYY"),
            "NB_EXTINCTEURS_TOTAL": st.column_config.NumberColumn("Extincteurs"),
            "NB_DETECTION_CO_NO": st.column_config.NumberColumn("Détection CO-NO"),
            "NB_PORTE_COMPARTIMENTAGE": st.column_config.NumberColumn("Portes compartimentage"),
            "NB_EXTRACTEURS": st.column_config.NumberColumn("Extracteurs"),
            "NB_INSUFFLATEURS": st.column_config.NumberColumn("Insufflateurs"),
            "NB_COLONNES_SECHES": st.column_config.NumberColumn("Colonnes sèches"),
            "NB_BAES": st.column_config.NumberColumn("BAES"),
            "TYPE_ALIMENTATION_BAES": st.column_config.TextColumn("Type Alimentation BAES"),
            "NB_TRAPPE_EVACUATION_MOTORISEE": st.column_config.NumberColumn("Trappes d'évacuation motorisées"),
            "TYPE_TARIFS_ELEC": st.column_config.TextColumn("Type de tarifs élec"),
            "FLAG_CELLULES_HT": st.column_config.TextColumn("Cellules HT"),
            "FLAG_GROUPE_ELECTROGENE": st.column_config.TextColumn("Groupe électrogène"),
            "FLAG_TGS": st.column_config.TextColumn("TGS"),
            "CAPACITE_CUVE_FIOUL": st.column_config.NumberColumn("Capacité cuve fioul (L)"),
            "DATE_DERNIERE_COMMISSION": st.column_config.DateColumn("Date dernière commission", format="DD/MM/YYYY"),
            "AVIS_COMMISSION": st.column_config.TextColumn("Avis commission"),
            "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
            "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
            "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
            "DATE_FIN": st.column_config.TextColumn("Date fin"),
            "IS_ACTIVE": st.column_config.TextColumn("Actif"),
        })

# ===== MODIFIER =====
with tab_edit:
    st.subheader("Modifier les données incendie")
    if df.empty:
        st.info("Aucune donnée.")
    else:
        mode = st.radio("Mode de saisie", ["Formulaire", "Grille (type Excel)"], horizontal=True, key="inc_mode")

        if mode == "Formulaire":
            mod_options = [str(row.get('NOM_PARC') or row['CODE_PARC']) for _, row in df.iterrows()]
            sel_mod_idx = st.selectbox("Sélectionner un parc", range(len(mod_options)),
                                        format_func=lambda i: mod_options[i], key="inc_mod_select")
            sel = df.iloc[sel_mod_idx]
            pk = sel["CODE_PARC"]

            st.divider()
            with st.form(key=f"form_inc_{pk}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.text_input("Parc", value=f"{pk} — {sel.get('NOM_PARC', '')}", disabled=True)
                    eae = st.text_input("EAE Sprinkleurs", value=sel.get("EAE_SPRINKLEURS") or "")
                    nb_postes = st.number_input("Nb postes", min_value=0, value=safe_int(sel.get("NB_POSTES")))
                    nb_tetes = st.number_input("Nb têtes", min_value=0, value=safe_int(sel.get("NB_TETES")))
                    nb_ext_total = st.number_input("Extincteurs total", min_value=0, value=safe_int(sel.get("NB_EXTINCTEURS_TOTAL")))
                    nb_bac = st.number_input("Bacs à sable", min_value=0, value=safe_int(sel.get("NB_BAC_A_SABLE")))
                    nb_dai = st.number_input("DAI", min_value=0, value=safe_int(sel.get("NB_DAI")))
                    cur_ssi = sel.get("FLAG_SSI") or ""
                    ssi_idx = OUI_NON_OPTIONS.index(cur_ssi) if cur_ssi in OUI_NON_OPTIONS else 0
                    flag_ssi = st.selectbox("SSI", OUI_NON_OPTIONS, index=ssi_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="inc_ssi")
                    type_ssi = st.text_input("Type SSI", value=sel.get("TYPE_SSI") or "")
                    marque_ssi = st.text_input("Marque SSI", value=sel.get("MARQUE_SSI") or "")
                with col2:
                    nb_detection_co_no = st.number_input("Détection CO/NO", min_value=0, value=safe_int(sel.get("NB_DETECTION_CO_NO")))
                    nb_porte_compartimentage = st.number_input("Portes compartimentage", min_value=0, value=safe_int(sel.get("NB_PORTE_COMPARTIMENTAGE")))
                    nb_extracteurs = st.number_input("Extracteurs", min_value=0, value=safe_int(sel.get("NB_EXTRACTEURS")))
                    nb_insufflateurs = st.number_input("Insufflateurs", min_value=0, value=safe_int(sel.get("NB_INSUFFLATEURS")))
                    nb_col_seches = st.number_input("Colonnes sèches", min_value=0, value=safe_int(sel.get("NB_COLONNES_SECHES")))
                    nb_baes = st.number_input("BAES", min_value=0, value=safe_int(sel.get("NB_BAES")))
                    type_baes = st.text_input("Type alimentation BAES", value=sel.get("TYPE_ALIMENTATION_BAES") or "")
                    nb_trappe = st.number_input("Trappes évacuation mot.", min_value=0, value=safe_int(sel.get("NB_TRAPPE_EVACUATION_MOTORISEE")))
                with col3:
                    cur_tarif = sel.get("TYPE_TARIFS_ELEC") or ""
                    tarif_idx = TARIFS_ELEC_OPTIONS.index(cur_tarif) if cur_tarif in TARIFS_ELEC_OPTIONS else 0
                    type_tarif = st.selectbox("Type tarifs élec", TARIFS_ELEC_OPTIONS, index=tarif_idx, key="inc_tarif_elec")
                    cur_ht = sel.get("FLAG_CELLULES_HT") or ""
                    ht_idx = OUI_NON_OPTIONS.index(cur_ht) if cur_ht in OUI_NON_OPTIONS else 0
                    flag_ht = st.selectbox("Cellules HT", OUI_NON_OPTIONS, index=ht_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="inc_ht")
                    cur_ge = sel.get("FLAG_GROUPE_ELECTROGENE") or ""
                    ge_idx = OUI_NON_OPTIONS.index(cur_ge) if cur_ge in OUI_NON_OPTIONS else 0
                    flag_ge = st.selectbox("Groupe électrogène", OUI_NON_OPTIONS, index=ge_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="inc_ge")
                    cur_tgs = sel.get("FLAG_TGS") or ""
                    tgs_idx = OUI_NON_OPTIONS.index(cur_tgs) if cur_tgs in OUI_NON_OPTIONS else 0
                    flag_tgs = st.selectbox("TGS", OUI_NON_OPTIONS, index=tgs_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="inc_tgs")
                    cuve = st.number_input("Capacité cuve fioul (L)", min_value=0, value=safe_int(sel.get("CAPACITE_CUVE_FIOUL")))
                    date_mes_ssi = st.date_input("Date mise en service SSI", value=sel.get("DATE_MISE_EN_SERVICE_SSI") if pd.notna(sel.get("DATE_MISE_EN_SERVICE_SSI")) else None)
                    date_comm = st.date_input("Date dernière commission", value=sel.get("DATE_DERNIERE_COMMISSION") if pd.notna(sel.get("DATE_DERNIERE_COMMISSION")) else None)
                    cur_avis = sel.get("AVIS_COMMISSION") or ""
                    avis_idx = AVIS_COMMISSION_OPTIONS.index(cur_avis) if cur_avis in AVIS_COMMISSION_OPTIONS else 0
                    avis = st.selectbox("Avis commission", AVIS_COMMISSION_OPTIONS, index=avis_idx, key="inc_avis_comm")
                submitted = st.form_submit_button("Mettre à jour", type="primary")

            if submitted:
                update_incendie({
                    "CODE_PARC": pk, "EAE_SPRINKLEURS": eae,
                    "NB_POSTES": nb_postes, "NB_TETES": nb_tetes,
                    "NB_EXTINCTEURS_TOTAL": nb_ext_total, "NB_BAC_A_SABLE": nb_bac,
                    "NB_DAI": nb_dai, "FLAG_SSI": flag_ssi, "TYPE_SSI": type_ssi, "MARQUE_SSI": marque_ssi,
                    "DATE_MISE_EN_SERVICE_SSI": str(date_mes_ssi) if date_mes_ssi else None,
                    "NB_DETECTION_CO_NO": nb_detection_co_no, "NB_PORTE_COMPARTIMENTAGE": nb_porte_compartimentage,
                    "NB_EXTRACTEURS": nb_extracteurs, "NB_INSUFFLATEURS": nb_insufflateurs,
                    "NB_COLONNES_SECHES": nb_col_seches, "NB_BAES": nb_baes,
                    "TYPE_ALIMENTATION_BAES": type_baes, "NB_TRAPPE_EVACUATION_MOTORISEE": nb_trappe,
                    "TYPE_TARIFS_ELEC": type_tarif, "FLAG_CELLULES_HT": flag_ht,
                    "FLAG_GROUPE_ELECTROGENE": flag_ge, "FLAG_TGS": flag_tgs,
                    "CAPACITE_CUVE_FIOUL": cuve,
                    "DATE_DERNIERE_COMMISSION": str(date_comm) if date_comm else None,
                    "AVIS_COMMISSION": avis,
                }, user)
                notify("✅ Données incendie mises à jour", "success")
                st.rerun()

        else:
            # ===== MODE GRILLE (type Excel) =====
            st.info("Modifiez directement les cellules ci-dessous puis cliquez sur **Enregistrer les modifications**.")

            # CSS pour afficher une petite flèche sur les colonnes selectbox
            st.markdown("""
            <style>
                div[data-testid="stDataEditor"] [data-testid="column-header"] {
                    position: relative;
                }
                div[data-testid="stDataEditor"] td[data-column-type="select"] {
                    position: relative;
                }
                div[data-testid="stDataEditor"] td[data-column-type="select"]::after {
                    content: "▾";
                    position: absolute;
                    right: 8px;
                    top: 50%;
                    transform: translateY(-50%);
                    font-size: 0.7rem;
                    color: #94A3B8;
                    pointer-events: none;
                }
            </style>
            """, unsafe_allow_html=True)

            GRID_COLS = [
                "CODE_PARC", "NOM_PARC", "EAE_SPRINKLEURS",
                "NB_POSTES", "NB_TETES", "NB_EXTINCTEURS_TOTAL", "NB_BAC_A_SABLE",
                "NB_DAI", "FLAG_SSI", "TYPE_SSI", "MARQUE_SSI",
                "DATE_MISE_EN_SERVICE_SSI",
                "NB_DETECTION_CO_NO", "NB_PORTE_COMPARTIMENTAGE",
                "NB_EXTRACTEURS", "NB_INSUFFLATEURS", "NB_COLONNES_SECHES", "NB_BAES",
                "TYPE_ALIMENTATION_BAES", "NB_TRAPPE_EVACUATION_MOTORISEE",
                "TYPE_TARIFS_ELEC", "FLAG_CELLULES_HT", "FLAG_GROUPE_ELECTROGENE", "FLAG_TGS",
                "CAPACITE_CUVE_FIOUL", "DATE_DERNIERE_COMMISSION", "AVIS_COMMISSION"
            ]
            available_grid_cols = [c for c in GRID_COLS if c in df.columns]
            df_grid = df[available_grid_cols].copy()

            # Convertir les flags O/N en Oui/Non pour l'affichage grille
            flag_cols = [c for c in df_grid.columns if c.startswith("FLAG_")]
            flag_map_display = {"O": "Oui", "N": "Non"}
            flag_map_store = {"Oui": "O", "Non": "N"}
            for col in flag_cols:
                df_grid[col] = df_grid[col].map(flag_map_display)

            num_cols = [c for c in df_grid.columns if c.startswith("NB_") or c == "CAPACITE_CUVE_FIOUL"]

            column_config = {
                "CODE_PARC": st.column_config.TextColumn("Code Parc", disabled=True),
                "NOM_PARC": st.column_config.TextColumn("Nom Parc", disabled=True),
            }
            for col in flag_cols:
                column_config[col] = st.column_config.SelectboxColumn(
                    col.replace("FLAG_", "").replace("_", " ").title() + " ▾",
                    options=["Oui", "Non"],
                    required=False
                )
            for col in num_cols:
                column_config[col] = st.column_config.NumberColumn(
                    col.replace("NB_", "").replace("_", " ").title(),
                    min_value=0
                )
            column_config["DATE_MISE_EN_SERVICE_SSI"] = st.column_config.DateColumn(
                "Date MES SSI",
                format="DD/MM/YYYY"
            )
            column_config["DATE_DERNIERE_COMMISSION"] = st.column_config.DateColumn(
                "Date dernière commission",
                format="DD/MM/YYYY"
            )
            column_config["TYPE_TARIFS_ELEC"] = st.column_config.SelectboxColumn(
                "Type tarifs élec ▾",
                options=["Bleu", "Jaune", "Vert"],
                required=False
            )
            column_config["AVIS_COMMISSION"] = st.column_config.SelectboxColumn(
                "Avis commission ▾",
                options=["Favorable", "Favorable avec prescriptions", "Defavorable"],
                required=False
            )

            edited_df = st.data_editor(
                df_grid,
                column_config=column_config,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                key="inc_grid_editor"
            )

            if st.button("Enregistrer les modifications", type="primary", key="btn_save_grid"):
                changes_count = 0
                for idx in range(len(df_grid)):
                    original_row = df_grid.iloc[idx]
                    edited_row = edited_df.iloc[idx]
                    row_changed = False
                    for col in available_grid_cols:
                        if col in ("CODE_PARC", "NOM_PARC"):
                            continue
                        old_val = original_row[col] if pd.notna(original_row[col]) else None
                        new_val = edited_row[col] if pd.notna(edited_row[col]) else None
                        if str(old_val) != str(new_val):
                            row_changed = True
                            break
                    if row_changed:
                        # Reconvertir Oui/Non → O/N pour la base
                        update_incendie({
                            "CODE_PARC": edited_row["CODE_PARC"],
                            "EAE_SPRINKLEURS": edited_row.get("EAE_SPRINKLEURS"),
                            "NB_POSTES": safe_int(edited_row.get("NB_POSTES")),
                            "NB_TETES": safe_int(edited_row.get("NB_TETES")),
                            "NB_EXTINCTEURS_TOTAL": safe_int(edited_row.get("NB_EXTINCTEURS_TOTAL")),
                            "NB_BAC_A_SABLE": safe_int(edited_row.get("NB_BAC_A_SABLE")),
                            "NB_DAI": safe_int(edited_row.get("NB_DAI")),
                            "FLAG_SSI": flag_map_store.get(edited_row.get("FLAG_SSI")),
                            "TYPE_SSI": edited_row.get("TYPE_SSI"),
                            "MARQUE_SSI": edited_row.get("MARQUE_SSI"),
                            "DATE_MISE_EN_SERVICE_SSI": edited_row.get("DATE_MISE_EN_SERVICE_SSI") if pd.notna(edited_row.get("DATE_MISE_EN_SERVICE_SSI")) else None,
                            "NB_DETECTION_CO_NO": safe_int(edited_row.get("NB_DETECTION_CO_NO")),
                            "NB_PORTE_COMPARTIMENTAGE": safe_int(edited_row.get("NB_PORTE_COMPARTIMENTAGE")),
                            "NB_EXTRACTEURS": safe_int(edited_row.get("NB_EXTRACTEURS")),
                            "NB_INSUFFLATEURS": safe_int(edited_row.get("NB_INSUFFLATEURS")),
                            "NB_COLONNES_SECHES": safe_int(edited_row.get("NB_COLONNES_SECHES")),
                            "NB_BAES": safe_int(edited_row.get("NB_BAES")),
                            "TYPE_ALIMENTATION_BAES": edited_row.get("TYPE_ALIMENTATION_BAES"),
                            "NB_TRAPPE_EVACUATION_MOTORISEE": safe_int(edited_row.get("NB_TRAPPE_EVACUATION_MOTORISEE")),
                            "TYPE_TARIFS_ELEC": edited_row.get("TYPE_TARIFS_ELEC"),
                            "FLAG_CELLULES_HT": flag_map_store.get(edited_row.get("FLAG_CELLULES_HT")),
                            "FLAG_GROUPE_ELECTROGENE": flag_map_store.get(edited_row.get("FLAG_GROUPE_ELECTROGENE")),
                            "FLAG_TGS": flag_map_store.get(edited_row.get("FLAG_TGS")),
                            "CAPACITE_CUVE_FIOUL": safe_int(edited_row.get("CAPACITE_CUVE_FIOUL")),
                            "DATE_DERNIERE_COMMISSION": edited_row.get("DATE_DERNIERE_COMMISSION") if pd.notna(edited_row.get("DATE_DERNIERE_COMMISSION")) else None,
                            "AVIS_COMMISSION": edited_row.get("AVIS_COMMISSION"),
                        }, user)
                        changes_count += 1
                if changes_count > 0:
                    notify(f"✅ {changes_count} parc(s) mis à jour", "success")
                    st.rerun()
                else:
                    st.info("Aucune modification détectée.")

# ===== HISTORIQUE =====
with tab_history:
    st.subheader("Historique")
    if df.empty:
        st.info("Aucune donnée.")
    else:
        from core.db import get_session
        session = get_session()
        parc_codes = df["CODE_PARC"].unique().tolist()
        hist_options = [f"{code} — {parc_names.get(code, '')}" for code in parc_codes]
        with st.form(key="form_hist_inc"):
            sel_h_idx = st.selectbox("Parc", range(len(hist_options)), format_func=lambda i: hist_options[i], key="inc_hist")
            submitted_hist = st.form_submit_button("Afficher l'historique", type="primary")
        if submitted_hist:
            sel_h = parc_codes[sel_h_idx]
            df_hist = session.sql(f"""
                SELECT
                    CODE_PARC, EAE_SPRINKLEURS, NB_POSTES, NB_TETES,
                    NB_EXTINCTEURS_TOTAL, NB_BAC_A_SABLE,
                    NB_DAI, FLAG_SSI, TYPE_SSI, MARQUE_SSI, DATE_MISE_EN_SERVICE_SSI,
                    NB_DETECTION_CO_NO, NB_PORTE_COMPARTIMENTAGE,
                    NB_EXTRACTEURS, NB_INSUFFLATEURS, NB_COLONNES_SECHES, NB_BAES,
                    TYPE_ALIMENTATION_BAES, NB_TRAPPE_EVACUATION_MOTORISEE,
                    TYPE_TARIFS_ELEC, FLAG_CELLULES_HT, FLAG_GROUPE_ELECTROGENE, FLAG_TGS,
                    CAPACITE_CUVE_FIOUL, DATE_DERNIERE_COMMISSION, AVIS_COMMISSION,
                    DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR,
                    DATE_DEBUT, DATE_FIN, IS_ACTIVE
                FROM S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE
                WHERE CODE_PARC = '{sel_h}' ORDER BY DATE_DEBUT DESC
            """).to_pandas()
            if df_hist.empty:
                st.info("Aucun historique.")
            else:
                st.caption(f"{len(df_hist)} version(s) pour **{sel_h}**")
                st.dataframe(df_hist, use_container_width=True, hide_index=True, column_config={
                    "CODE_PARC": st.column_config.TextColumn("Code Parc"),
                    "EAE_SPRINKLEURS": st.column_config.TextColumn("EAE Sprinklers"),
                    "NB_POSTES": st.column_config.NumberColumn("Postes"),
                    "NB_TETES": st.column_config.NumberColumn("Têtes"),
                    "NB_EXTINCTEURS_TOTAL": st.column_config.NumberColumn("Extincteurs total"),
                    "NB_BAC_A_SABLE": st.column_config.NumberColumn("Bacs à sable"),
                    "NB_DAI": st.column_config.NumberColumn("DAI"),
                    "FLAG_SSI": st.column_config.TextColumn("SSI"),
                    "TYPE_SSI": st.column_config.TextColumn("Type SSI"),
                    "MARQUE_SSI": st.column_config.TextColumn("Marque SSI"),
                    "DATE_MISE_EN_SERVICE_SSI": st.column_config.DateColumn("Date mise en service SSI", format="DD/MM/YYYY"),
                    "NB_DETECTION_CO_NO": st.column_config.NumberColumn("Détection CO-NO"),
                    "NB_PORTE_COMPARTIMENTAGE": st.column_config.NumberColumn("Portes compartimentage"),
                    "NB_EXTRACTEURS": st.column_config.NumberColumn("Extracteurs"),
                    "NB_INSUFFLATEURS": st.column_config.NumberColumn("Insufflateurs"),
                    "NB_COLONNES_SECHES": st.column_config.NumberColumn("Colonnes sèches"),
                    "NB_BAES": st.column_config.NumberColumn("BAES"),
                    "TYPE_ALIMENTATION_BAES": st.column_config.TextColumn("Type Alimentation BAES"),
                    "NB_TRAPPE_EVACUATION_MOTORISEE": st.column_config.NumberColumn("Trappes d'évacuation motorisées"),
                    "TYPE_TARIFS_ELEC": st.column_config.TextColumn("Type de tarifs élec"),
                    "FLAG_CELLULES_HT": st.column_config.TextColumn("Cellules HT"),
                    "FLAG_GROUPE_ELECTROGENE": st.column_config.TextColumn("Groupe électrogène"),
                    "FLAG_TGS": st.column_config.TextColumn("TGS"),
                    "CAPACITE_CUVE_FIOUL": st.column_config.NumberColumn("Capacité cuve fioul (L)"),
                    "DATE_DERNIERE_COMMISSION": st.column_config.DateColumn("Date dernière commission", format="DD/MM/YYYY"),
                    "AVIS_COMMISSION": st.column_config.TextColumn("Avis commission"),
                    "DATE_CREATION": st.column_config.DatetimeColumn("Date création", format="DD/MM/YYYY HH:mm"),
                    "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
                    "DATE_MODIFICATION": st.column_config.DatetimeColumn("Date modification", format="DD/MM/YYYY HH:mm"),
                    "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
                    "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                    "DATE_FIN": st.column_config.TextColumn("Date fin"),
                    "IS_ACTIVE": st.column_config.TextColumn("Actif"),
                })
