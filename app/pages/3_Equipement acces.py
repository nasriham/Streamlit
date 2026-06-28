# Page Equipement et Acces avec onglets et formulaire de modification
# Co-authored with CoCo
import streamlit as st
import pandas as pd
from core.queries import (
    get_parks,
    get_parks_equipements,
    get_peageurs,
    insert_equipement,
    update_equipement
)
from core.functions import (
    show_notification,
    notify
)

user = getattr(st.user, "user_name", "SYSTEM")

show_notification()

st.title("🔧 Équipement & Accès")
st.caption(f"Gestion des équipements et accès des parcs — Connecté : **{user}**")
st.divider()

df = get_parks_equipements()
df_parks_ref = get_parks()
df_peageurs = get_peageurs()

peageur_labels = dict(zip(df_peageurs["CODE_PEAGEUR"], df_peageurs["LIBELLE_PEAGEUR"]))
OUI_NON_OPTIONS = ["", "O", "N"]
OUI_NON_DISPLAY = {"": "Non renseigné", "O": "Oui", "N": "Non"}

tab_search, tab_edit, tab_history = st.tabs([
    "🔍 Rechercher", "✏️ Modifier", "📜 Historique"
])

# ===== CONSULTER =====
with tab_search:
    st.subheader("Équipements par parc")
    search = st.text_input("🔍 Rechercher", key="search_equip")
    if df.empty:
        st.info("Aucune donnée.")
    else:
        display_cols = [c for c in ["NOM_PARC", "NB_VOIES_ENTREES", "NB_VOIES_SORTIES", "NOM_PEAGEUR",
            "NB_LECTEURS_PIETONS", "NB_LECTEURS_METSTATIONS", "NB_CAISSES",
            "NB_BORNES_PEAGE_ENTREES", "FLAG_DOUBLE_ENTREES", "NB_BORNES_PEAGE_SORTIES",
            "FLAG_DOUBLE_SORTIES", "FLAG_LECTURE_PLAQUE", "NB_ASCENSEURS", "MARQUE_ASCENSEURS",
            "DATE_MISE_SERVICE_ASCENSEUR", "NB_ESCALIERS", "NB_PORTAILS", "NB_PORTES_COULISSANTES",
            "NB_RIDEAUX_MOTORISES", "NB_BORNES_IRVE", "FLAG_LOCKERS", "FLAG_GUIDAGE_PLACE",
            "GABARIT_STANDARD", "DATE_CREATION", "NOM_CREATEUR", "DATE_MODIFICATION", "NOM_MODIFICATEUR",
            "DATE_DEBUT", "DATE_FIN", "IS_ACTIVE"] if c in df.columns]
        df_d = df[display_cols].copy()
        if search:
            term = search.lower()
            mask = pd.Series([False] * len(df_d))
            for col in display_cols:
                mask = mask | df_d[col].astype(str).str.lower().str.contains(term, na=False)
            df_d = df_d[mask]
        st.caption(f"{len(df_d)} parc(s)")
        st.dataframe(df_d, use_container_width=True, hide_index=True,
            column_config={
                "NOM_PARC": st.column_config.TextColumn("Nom Parc", width="medium"),
                "NB_VOIES_ENTREES": st.column_config.NumberColumn("Voies entrées"),
                "NB_VOIES_SORTIES": st.column_config.NumberColumn("Voies sorties"),
                "NOM_PEAGEUR": st.column_config.TextColumn("Nom Péageur"),
                "NB_LECTEURS_PIETONS": st.column_config.NumberColumn("Lecteurs piétons"),
                "NB_LECTEURS_METSTATIONS": st.column_config.NumberColumn("Lecteurs Metstations"),
                "NB_CAISSES": st.column_config.NumberColumn("Caisses"),
                "NB_BORNES_PEAGE_ENTREES": st.column_config.NumberColumn("Bornes de Péages entrées"),
                "FLAG_DOUBLE_ENTREES": st.column_config.TextColumn("Double entrées"),
                "NB_BORNES_PEAGE_SORTIES": st.column_config.NumberColumn("Bornes de Péages sorties"),
                "FLAG_DOUBLE_SORTIES": st.column_config.TextColumn("Double Sorties"),
                "FLAG_LECTURE_PLAQUE": st.column_config.TextColumn("Lecture Plaque"),
                "NB_ASCENSEURS": st.column_config.NumberColumn("Ascenseurs"),
                "MARQUE_ASCENSEURS": st.column_config.TextColumn("Marque Ascenseurs"),
                "DATE_MISE_SERVICE_ASCENSEUR": st.column_config.DatetimeColumn("Date mise en service Ascenseur", format="DD/MM/YYYY"),
                "NB_ESCALIERS": st.column_config.NumberColumn("Escalier"),
                "NB_PORTAILS": st.column_config.NumberColumn("Portail"),
                "NB_PORTES_COULISSANTES": st.column_config.NumberColumn("Portes coulissantes"),
                "NB_RIDEAUX_MOTORISES": st.column_config.NumberColumn("Nb rideaux Motorisés"),
                "NB_BORNES_IRVE": st.column_config.NumberColumn("Bornes IRVE"),
                "FLAG_LOCKERS": st.column_config.TextColumn("Lockers"),
                "FLAG_GUIDAGE_PLACE": st.column_config.TextColumn("Guidage à la place"),
                "GABARIT_STANDARD": st.column_config.TextColumn("Gabarit standard"),
                "DATE_CREATION": st.column_config.DatetimeColumn("Date création", format="DD/MM/YYYY HH:mm"),
                "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
                "DATE_MODIFICATION": st.column_config.DatetimeColumn("Date modification", format="DD/MM/YYYY HH:mm"),
                "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
                "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                "DATE_FIN": st.column_config.TextColumn("Date fin"),
                "IS_ACTIVE": st.column_config.TextColumn("Actif"),
            })

# ===== MODIFIER =====
with tab_edit:
    st.subheader("Modifier les équipements")
    if df.empty:
        st.info("Aucune donnée à modifier.")
    else:
        mode = st.radio("Mode de saisie", ["Formulaire", "Grille (type Excel)"], horizontal=True, key="eq_mode")

        if mode == "Formulaire":
            mod_options = [str(row.get('NOM_PARC') or row['CODE_PARC']) for _, row in df.iterrows()]
            sel_mod_idx = st.selectbox("Sélectionner un parc", range(len(mod_options)),
                                        format_func=lambda i: mod_options[i], key="eq_mod_select")
            sel = df.iloc[sel_mod_idx]
            pk = sel["CODE_PARC"]

            st.divider()
            with st.form(key=f"form_eq_{pk}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("Parc", value=pk, disabled=True)
                    voies_e = st.number_input("Voies entrées", min_value=0, value=int(sel["NB_VOIES_ENTREES"]) if pd.notna(sel.get("NB_VOIES_ENTREES")) else 0)
                    voies_s = st.number_input("Voies sorties", min_value=0, value=int(sel["NB_VOIES_SORTIES"]) if pd.notna(sel.get("NB_VOIES_SORTIES")) else 0)
                    peageur_options_form = list(peageur_labels.values())
                    current_peageur = sel.get("NOM_PEAGEUR") or ""
                    peageur_idx = peageur_options_form.index(current_peageur) if current_peageur in peageur_options_form else 0
                    peageur = st.selectbox("Péageur", peageur_options_form, index=peageur_idx, key="eq_peageur")
                    lect_piet = st.number_input("Lecteurs piétons", min_value=0, value=int(sel["NB_LECTEURS_PIETONS"]) if pd.notna(sel.get("NB_LECTEURS_PIETONS")) else 0)
                    lect_met = st.number_input("Lecteurs Metstation", min_value=0, value=int(sel["NB_LECTEURS_METSTATIONS"]) if pd.notna(sel.get("NB_LECTEURS_METSTATIONS")) else 0)
                    caisses = st.number_input("Caisses", min_value=0, value=int(sel["NB_CAISSES"]) if pd.notna(sel.get("NB_CAISSES")) else 0)
                    bornes_e = st.number_input("Bornes péage entrées", min_value=0, value=int(sel["NB_BORNES_PEAGE_ENTREES"]) if pd.notna(sel.get("NB_BORNES_PEAGE_ENTREES")) else 0)
                    cur_double_e = sel.get("FLAG_DOUBLE_ENTREES") or ""
                    double_e_idx = OUI_NON_OPTIONS.index(cur_double_e) if cur_double_e in OUI_NON_OPTIONS else 0
                    double_e = st.selectbox("Double entrées", OUI_NON_OPTIONS, index=double_e_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="eq_double_e")
                    bornes_s = st.number_input("Bornes péage sorties", min_value=0, value=int(sel["NB_BORNES_PEAGE_SORTIES"]) if pd.notna(sel.get("NB_BORNES_PEAGE_SORTIES")) else 0)
                    cur_double_s = sel.get("FLAG_DOUBLE_SORTIES") or ""
                    double_s_idx = OUI_NON_OPTIONS.index(cur_double_s) if cur_double_s in OUI_NON_OPTIONS else 0
                    double_s = st.selectbox("Double sorties", OUI_NON_OPTIONS, index=double_s_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="eq_double_s")
                with col2:
                    cur_plaque = sel.get("FLAG_LECTURE_PLAQUE") or ""
                    plaque_idx = OUI_NON_OPTIONS.index(cur_plaque) if cur_plaque in OUI_NON_OPTIONS else 0
                    lect_plaque = st.selectbox("Lecture plaque", OUI_NON_OPTIONS, index=plaque_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="eq_plaque")
                    ascenseurs = st.number_input("Ascenseurs", min_value=0, value=int(sel["NB_ASCENSEURS"]) if pd.notna(sel.get("NB_ASCENSEURS")) else 0)
                    marque_asc = st.text_input("Marque ascenseurs", value=sel.get("MARQUE_ASCENSEURS") or "")
                    date_asc = st.date_input("Date mise en service ascenseur", value=sel.get("DATE_MISE_SERVICE_ASCENSEUR") if pd.notna(sel.get("DATE_MISE_SERVICE_ASCENSEUR")) else None)
                    escaliers = st.number_input("Escaliers", min_value=0, value=int(sel["NB_ESCALIERS"]) if pd.notna(sel.get("NB_ESCALIERS")) else 0)
                    portails = st.number_input("Portails", min_value=0, value=int(sel["NB_PORTAILS"]) if pd.notna(sel.get("NB_PORTAILS")) else 0)
                    portes_c = st.number_input("Portes coulissantes", min_value=0, value=int(sel["NB_PORTES_COULISSANTES"]) if pd.notna(sel.get("NB_PORTES_COULISSANTES")) else 0)
                    rideaux = st.number_input("Rideaux motorisés", min_value=0, value=int(sel["NB_RIDEAUX_MOTORISES"]) if pd.notna(sel.get("NB_RIDEAUX_MOTORISES")) else 0)
                    bornes_irve = st.number_input("Bornes IRVE", min_value=0, value=int(sel["NB_BORNES_IRVE"]) if pd.notna(sel.get("NB_BORNES_IRVE")) else 0)
                    cur_lockers = sel.get("FLAG_LOCKERS") or ""
                    lockers_idx = OUI_NON_OPTIONS.index(cur_lockers) if cur_lockers in OUI_NON_OPTIONS else 0
                    lockers = st.selectbox("Lockers", OUI_NON_OPTIONS, index=lockers_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="eq_lockers")
                    cur_guidage = sel.get("FLAG_GUIDAGE_PLACE") or ""
                    guidage_idx = OUI_NON_OPTIONS.index(cur_guidage) if cur_guidage in OUI_NON_OPTIONS else 0
                    guidage = st.selectbox("Guidage à la place", OUI_NON_OPTIONS, index=guidage_idx, format_func=lambda x: OUI_NON_DISPLAY[x], key="eq_guidage")
                    gabarit = st.text_input("Gabarit standard", value=sel.get("GABARIT_STANDARD") or "")
                submitted = st.form_submit_button("Mettre à jour", type="primary")

            if submitted:
                update_equipement({
                    "CODE_PARC": pk, "NB_VOIES_ENTREES": voies_e, "NB_VOIES_SORTIES": voies_s,
                    "NOM_PEAGEUR": peageur, "NB_LECTEURS_PIETONS": lect_piet, "NB_LECTEURS_METSTATIONS": lect_met,
                    "NB_CAISSES": caisses, "NB_BORNES_PEAGE_ENTREES": bornes_e, "FLAG_DOUBLE_ENTREES": double_e,
                    "NB_BORNES_PEAGE_SORTIES": bornes_s, "FLAG_DOUBLE_SORTIES": double_s, "FLAG_LECTURE_PLAQUE": lect_plaque,
                    "NB_ASCENSEURS": ascenseurs, "MARQUE_ASCENSEURS": marque_asc, "DATE_MISE_SERVICE_ASCENSEUR": str(date_asc) if date_asc else None,
                    "NB_ESCALIERS": escaliers, "NB_PORTAILS": portails, "NB_PORTES_COULISSANTES": portes_c,
                    "NB_RIDEAUX_MOTORISES": rideaux, "NB_BORNES_IRVE": bornes_irve, "FLAG_LOCKERS": lockers,
                    "FLAG_GUIDAGE_PLACE": guidage, "GABARIT_STANDARD": gabarit,
                }, user)
                notify("✅ Équipement mis à jour", "success")
                st.rerun()

        else:
            # ===== MODE GRILLE (type Excel) =====
            st.info("Modifiez directement les cellules ci-dessous puis cliquez sur **Enregistrer les modifications**.")

            st.markdown("""
            <style>
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
                "CODE_PARC", "NOM_PARC", "NB_VOIES_ENTREES", "NB_VOIES_SORTIES",
                "NOM_PEAGEUR", "NB_LECTEURS_PIETONS", "NB_LECTEURS_METSTATIONS",
                "NB_CAISSES", "NB_BORNES_PEAGE_ENTREES", "FLAG_DOUBLE_ENTREES",
                "NB_BORNES_PEAGE_SORTIES", "FLAG_DOUBLE_SORTIES", "FLAG_LECTURE_PLAQUE",
                "NB_ASCENSEURS", "MARQUE_ASCENSEURS", "DATE_MISE_SERVICE_ASCENSEUR",
                "NB_ESCALIERS", "NB_PORTAILS", "NB_PORTES_COULISSANTES",
                "NB_RIDEAUX_MOTORISES", "NB_BORNES_IRVE",
                "FLAG_LOCKERS", "FLAG_GUIDAGE_PLACE", "GABARIT_STANDARD"
            ]
            available_grid_cols = [c for c in GRID_COLS if c in df.columns]
            df_grid = df[available_grid_cols].copy()

            flag_cols = [c for c in df_grid.columns if c.startswith("FLAG_")]
            flag_map_display = {"O": "Oui", "N": "Non"}
            flag_map_store = {"Oui": "O", "Non": "N"}
            for col in flag_cols:
                df_grid[col] = df_grid[col].map(flag_map_display)

            num_cols = [c for c in df_grid.columns if c.startswith("NB_")]

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
            column_config["NOM_PEAGEUR"] = st.column_config.SelectboxColumn(
                "Péageur ▾",
                options=list(peageur_labels.values()),
                required=False
            )
            column_config["DATE_MISE_SERVICE_ASCENSEUR"] = st.column_config.DateColumn(
                "Date MES Ascenseur",
                format="DD/MM/YYYY"
            )

            edited_df = st.data_editor(
                df_grid,
                column_config=column_config,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                key="eq_grid_editor"
            )

            if st.button("Enregistrer les modifications", type="primary", key="btn_save_eq_grid"):
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
                        def safe_int_eq(val):
                            if pd.notna(val):
                                try:
                                    return int(val)
                                except (ValueError, TypeError):
                                    pass
                            return 0

                        update_equipement({
                            "CODE_PARC": edited_row["CODE_PARC"],
                            "NB_VOIES_ENTREES": safe_int_eq(edited_row.get("NB_VOIES_ENTREES")),
                            "NB_VOIES_SORTIES": safe_int_eq(edited_row.get("NB_VOIES_SORTIES")),
                            "NOM_PEAGEUR": edited_row.get("NOM_PEAGEUR"),
                            "NB_LECTEURS_PIETONS": safe_int_eq(edited_row.get("NB_LECTEURS_PIETONS")),
                            "NB_LECTEURS_METSTATIONS": safe_int_eq(edited_row.get("NB_LECTEURS_METSTATIONS")),
                            "NB_CAISSES": safe_int_eq(edited_row.get("NB_CAISSES")),
                            "NB_BORNES_PEAGE_ENTREES": safe_int_eq(edited_row.get("NB_BORNES_PEAGE_ENTREES")),
                            "FLAG_DOUBLE_ENTREES": flag_map_store.get(edited_row.get("FLAG_DOUBLE_ENTREES")),
                            "NB_BORNES_PEAGE_SORTIES": safe_int_eq(edited_row.get("NB_BORNES_PEAGE_SORTIES")),
                            "FLAG_DOUBLE_SORTIES": flag_map_store.get(edited_row.get("FLAG_DOUBLE_SORTIES")),
                            "FLAG_LECTURE_PLAQUE": flag_map_store.get(edited_row.get("FLAG_LECTURE_PLAQUE")),
                            "NB_ASCENSEURS": safe_int_eq(edited_row.get("NB_ASCENSEURS")),
                            "MARQUE_ASCENSEURS": edited_row.get("MARQUE_ASCENSEURS"),
                            "DATE_MISE_SERVICE_ASCENSEUR": edited_row.get("DATE_MISE_SERVICE_ASCENSEUR") if pd.notna(edited_row.get("DATE_MISE_SERVICE_ASCENSEUR")) else None,
                            "NB_ESCALIERS": safe_int_eq(edited_row.get("NB_ESCALIERS")),
                            "NB_PORTAILS": safe_int_eq(edited_row.get("NB_PORTAILS")),
                            "NB_PORTES_COULISSANTES": safe_int_eq(edited_row.get("NB_PORTES_COULISSANTES")),
                            "NB_RIDEAUX_MOTORISES": safe_int_eq(edited_row.get("NB_RIDEAUX_MOTORISES")),
                            "NB_BORNES_IRVE": safe_int_eq(edited_row.get("NB_BORNES_IRVE")),
                            "FLAG_LOCKERS": flag_map_store.get(edited_row.get("FLAG_LOCKERS")),
                            "FLAG_GUIDAGE_PLACE": flag_map_store.get(edited_row.get("FLAG_GUIDAGE_PLACE")),
                            "GABARIT_STANDARD": edited_row.get("GABARIT_STANDARD"),
                        }, user)
                        changes_count += 1
                if changes_count > 0:
                    notify(f"✅ {changes_count} parc(s) mis à jour", "success")
                    st.rerun()
                else:
                    st.info("Aucune modification détectée.")

# ===== HISTORIQUE =====
with tab_history:
    @st.fragment
    def show_history_equip():
        st.subheader("Historique")
        if df.empty:
            st.info("Aucune donnée.")
        else:
            parc_codes = df["CODE_PARC"].unique().tolist()
            parc_names_ref = df_parks_ref.set_index("CODE_PARC")["NOM_PARC"].to_dict()
            hist_options = [f"{code} — {parc_names_ref.get(code, '')}" for code in parc_codes]
            with st.form(key="form_hist_equip"):
                sel_h_idx = st.selectbox("Parc", range(len(hist_options)), format_func=lambda i: hist_options[i], key="eq_hist")
                submitted_hist = st.form_submit_button("Afficher l'historique", type="primary")
            if submitted_hist:
                sel_h = parc_codes[sel_h_idx]
                from core.db import get_session
                session = get_session()
                df_hist = session.sql(f"""
                    SELECT CODE_PARC, NB_VOIES_ENTREES, NB_VOIES_SORTIES, NOM_PEAGEUR,
                           NB_LECTEURS_PIETONS, NB_LECTEURS_METSTATIONS, NB_CAISSES,
                           NB_BORNES_PEAGE_ENTREES, FLAG_DOUBLE_ENTREES,
                           NB_BORNES_PEAGE_SORTIES, FLAG_DOUBLE_SORTIES, FLAG_LECTURE_PLAQUE,
                           NB_ASCENSEURS, MARQUE_ASCENSEURS, DATE_MISE_SERVICE_ASCENSEUR,
                           NB_ESCALIERS, NB_PORTAILS, NB_PORTES_COULISSANTES,
                           NB_RIDEAUX_MOTORISES, NB_BORNES_IRVE, FLAG_LOCKERS,
                           FLAG_GUIDAGE_PLACE, GABARIT_STANDARD,
                           DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR,
                           DATE_DEBUT, DATE_FIN, IS_ACTIVE
                    FROM S_REFERENTIEL.T_R_EQUIPEMENT_ACCES
                    WHERE CODE_PARC = '{sel_h}' ORDER BY DATE_DEBUT DESC
                """).to_pandas()
                if df_hist.empty:
                    st.info("Aucun historique.")
                else:
                    st.caption(f"{len(df_hist)} version(s) pour **{sel_h}**")
                    st.dataframe(df_hist, use_container_width=True, hide_index=True, column_config={
                        "CODE_PARC": st.column_config.TextColumn("Code Parc"),
                        "NB_VOIES_ENTREES": st.column_config.NumberColumn("Voies entrées"),
                        "NB_VOIES_SORTIES": st.column_config.NumberColumn("Voies sorties"),
                        "NOM_PEAGEUR": st.column_config.TextColumn("Nom Péageur"),
                        "NB_LECTEURS_PIETONS": st.column_config.NumberColumn("Lecteurs piétons"),
                        "NB_LECTEURS_METSTATIONS": st.column_config.NumberColumn("Lecteurs Metstations"),
                        "NB_CAISSES": st.column_config.NumberColumn("Caisses"),
                        "NB_BORNES_PEAGE_ENTREES": st.column_config.NumberColumn("Bornes de Péages entrées"),
                        "FLAG_DOUBLE_ENTREES": st.column_config.TextColumn("Double entrées"),
                        "NB_BORNES_PEAGE_SORTIES": st.column_config.NumberColumn("Bornes de Péages sorties"),
                        "FLAG_DOUBLE_SORTIES": st.column_config.TextColumn("Double Sorties"),
                        "FLAG_LECTURE_PLAQUE": st.column_config.TextColumn("Lecture Plaque"),
                        "NB_ASCENSEURS": st.column_config.NumberColumn("Ascenseurs"),
                        "MARQUE_ASCENSEURS": st.column_config.TextColumn("Marque Ascenseurs"),
                        "DATE_MISE_SERVICE_ASCENSEUR": st.column_config.DateColumn("Date mise en service Ascenseur", format="DD/MM/YYYY"),
                        "NB_ESCALIERS": st.column_config.NumberColumn("Escalier"),
                        "NB_PORTAILS": st.column_config.NumberColumn("Portail"),
                        "NB_PORTES_COULISSANTES": st.column_config.NumberColumn("Portes coulissantes"),
                        "NB_RIDEAUX_MOTORISES": st.column_config.NumberColumn("Nb rideaux Motorisés"),
                        "NB_BORNES_IRVE": st.column_config.NumberColumn("Bornes IRVE"),
                        "FLAG_LOCKERS": st.column_config.TextColumn("Lockers"),
                        "FLAG_GUIDAGE_PLACE": st.column_config.TextColumn("Guidage à la place"),
                        "GABARIT_STANDARD": st.column_config.TextColumn("Gabarit standard"),
                        "DATE_CREATION": st.column_config.DatetimeColumn("Date création", format="DD/MM/YYYY HH:mm"),
                        "NOM_CREATEUR": st.column_config.TextColumn("Créateur"),
                        "DATE_MODIFICATION": st.column_config.DatetimeColumn("Date modification", format="DD/MM/YYYY HH:mm"),
                        "NOM_MODIFICATEUR": st.column_config.TextColumn("Modificateur"),
                        "DATE_DEBUT": st.column_config.DatetimeColumn("Date début", format="DD/MM/YYYY HH:mm"),
                        "DATE_FIN": st.column_config.TextColumn("Date fin"),
                        "IS_ACTIVE": st.column_config.TextColumn("Actif"),
                    })

    show_history_equip()
