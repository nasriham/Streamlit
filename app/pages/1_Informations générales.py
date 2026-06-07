import streamlit as st
from core.queries import (
    get_parks,
    get_villes,
    get_secteurs,
    get_districts,
    get_type,
    get_gestion,
    get_peageur,
    get_flag,
    insert_park,
    update_park,
    delete_park,
    get_history
)
from core.functions import (
    clean_value
)
from datetime import datetime
import pytz
import pandas as pd

user = st.user.user_name

if "message" in st.session_state:
    if st.session_state["message_type"] == "success":
        st.success(st.session_state["message"])
    elif st.session_state["message_type"] == "warning":
        st.warning(st.session_state["message"])

    del st.session_state["message"]
    del st.session_state["message_type"]


# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=120)
with col2:
    st.title("Gestion des parcs - Informations générales")

st.set_page_config(
    page_title="Exploitation des parcs",
    layout="wide"
)
    
# =========================
# 📦 LOAD DATA
# =========================
df_parks = get_parks()
df_villes = get_villes()
df_secteurs = get_secteurs()
df_districts = get_districts()
df_type = get_type()
df_gestion = get_gestion()
df_peageur = get_peageur()
df_flag_fourriere = get_flag()
df_flag_metstation = get_flag()
df_flag_casier_irv = get_flag()

# =========================
# 🔁 DICTIONNAIRES (code -> libellé)
# =========================
ville_dict = dict(zip(df_villes["CODE_VILLE"], df_villes["LIBELLE_VILLE"]))
secteur_dict = dict(zip(df_secteurs["CODE_SECTEUR"], df_secteurs["LIBELLE_SECTEUR"]))
district_dict = dict(zip(df_districts["CODE_DISTRICT"], df_districts["LIBELLE_DISTRICT"]))
type_dict = dict(zip(df_type["CODE_TYPE_PARC"], df_type["LIBELLE_TYPE_PARC"]))
gestion_dict = dict(zip(df_gestion["CODE_GESTION"], df_gestion["LIBELLE_GESTION"]))
peageur_dict = dict(zip(df_peageur["CODE_PEAGEUR"], df_peageur["LIBELLE_PEAGEUR"]))
fourriere_dict = dict(zip(df_flag_fourriere["CODE_FLAG"], df_flag_fourriere["LIBELLE_FLAG"]))
metstation_dict = dict(zip(df_flag_metstation["CODE_FLAG"], df_flag_metstation["LIBELLE_FLAG"]))
casier_irv_dict = dict(zip(df_flag_casier_irv["CODE_FLAG"], df_flag_casier_irv["LIBELLE_FLAG"]))

# =========================
# 🏷 LABELS (code - libellé)
# =========================
ville_labels = {code: f"{lib}" for code, lib in ville_dict.items()}
secteur_labels = {code: f"{lib}" for code, lib in secteur_dict.items()}
district_labels = {code: f"{lib}" for code, lib in district_dict.items()}
type_labels = {code: f"{lib}" for code, lib in type_dict.items()}
gestion_labels = {code: f"{lib}" for code, lib in gestion_dict.items()}
peageur_labels = {code: f"{lib}" for code, lib in peageur_dict.items()}
fourriere_labels = {code: f"{lib}" for code, lib in fourriere_dict.items()}
metstation_labels = {code: f"{lib}" for code, lib in metstation_dict.items()}
casier_irv_labels = {code: f"{lib}" for code, lib in casier_irv_dict.items()}

# =========================
# 👀 TABLE AFFICHAGE
# =========================
df_view = df_parks.copy()

df_view["VILLE"] = df_view["CODE_VILLE"].map(ville_labels)
df_view["SECTEUR"] = df_view["CODE_SECTEUR"].map(secteur_labels)
df_view["DISTRICT"] = df_view["CODE_DISTRICT"].map(district_labels)
df_view["TYPE"] = df_view["CODE_TYPE_PARC"].map(type_labels)
df_view["GESTION"] = df_view["CODE_GESTION"].map(gestion_labels)
df_view["PEAGEUR"] = df_view["CODE_PEAGEUR"].map(peageur_labels)
df_view["FOURRIERE"] = df_view["CODE_FLAG_FOURRIERE"].map(fourriere_labels)
df_view["METSTATION"] = df_view["CODE_FLAG_METSTATION"].map(metstation_labels)
df_view["CASIER IRV"] = df_view["CODE_FLAG_CASIER_IRV"].map(casier_irv_labels)

st.subheader("📊 Liste des parcs")

event = st.dataframe(
    df_view[["CODE_PARC", "NOM_PARC", "ADRESSE_PARC", "VILLE", "SECTEUR", "DISTRICT", "TYPE", "GESTION", "PEAGEUR", "NOMBRE_NIVEAU", "FOURRIERE", "METSTATION", "CASIER IRV", "SURFACE"]],
    use_container_width=True,
    selection_mode="single-row",
    on_select="rerun"
)

# =========================
# 🎯 SELECTION LIGNE
# =========================
if event.selection.rows:
    selected_row = df_parks.iloc[event.selection.rows[0]]

    st.subheader("✏️ Modifier un parc")

    if st.button("📜 Voir historique"):
        st.session_state["history_code_parc"] = selected_row["CODE_PARC"]
        
    # =========================
    # 🧾 FORMULAIRE EDIT (2 COLONNES)
    # =========================
    
    col1, col2 = st.columns(2)
    
    with col1:
        nom = st.text_input("Nom parc", value=selected_row["NOM_PARC"])
        adresse = st.text_input("Adresse", value=selected_row["ADRESSE_PARC"])

        ville_options = {v: k for k, v in ville_labels.items()} 
        default_ville = ville_labels[selected_row["CODE_VILLE"]]
        
        ville = st.selectbox(
            "Ville",
            list(ville_options.keys()),
            index=list(ville_options.keys()).index(default_ville)
        )
        code_ville = ville_options[ville]

        secteur_options = {v: k for k, v in secteur_labels.items()}
        default_secteur = secteur_labels[selected_row["CODE_SECTEUR"]]
    
        secteur = st.selectbox(
            "Secteur",
            list(secteur_options.keys()),
            index=list(secteur_options.keys()).index(default_secteur)
        )
        code_secteur = secteur_options[secteur]

        district_options = {v: k for k, v in district_labels.items()}
        default_district = district_labels[selected_row["CODE_DISTRICT"]]
        
        district = st.selectbox(
            "District",
            list(district_options.keys()),
            index=list(district_options.keys()).index(default_district)
        )
        code_district = district_options[district]

        type_options = {v: k for k, v in type_labels.items()} 
        default_type = type_labels[selected_row["CODE_TYPE_PARC"]]
        
        type = st.selectbox(
            "Type de parc",
            list(type_options.keys()),
            index=list(type_options.keys()).index(default_type)
        )
        code_type = type_options[type]
    
    
    with col2:
        
        gestion_options = {v: k for k, v in gestion_labels.items()} 
        default_gestion = gestion_labels[selected_row["CODE_GESTION"]]
        
        gestion = st.selectbox(
            "Gestion",
            list(gestion_options.keys()),
            index=list(gestion_options.keys()).index(default_gestion)
        )
        code_gestion = gestion_options[gestion]

        peageur_options = {v: k for k, v in peageur_labels.items()} 
        default_peageur = peageur_labels[selected_row["CODE_PEAGEUR"]]
        
        peageur = st.selectbox(
            "Péageur",
            list(peageur_options.keys()),
            index=list(peageur_options.keys()).index(default_peageur)
        )
        code_peageur = peageur_options[peageur]
    
        nombre_niveau = st.number_input(
            "Nombre de niveau",
            value=selected_row["NOMBRE_NIVEAU"]
        )

        fourriere_options = {v: k for k, v in fourriere_labels.items()} 
        default_fourriere = fourriere_labels[selected_row["CODE_FLAG_FOURRIERE"]]
        
        fourriere = st.selectbox(
            "Fourrière",
            list(fourriere_options.keys()),
            index=list(fourriere_options.keys()).index(default_fourriere)
        )
        code_fourriere = fourriere_options[fourriere]

        metstation_options = {v: k for k, v in metstation_labels.items()} 
        default_metstation = metstation_labels[selected_row["CODE_FLAG_METSTATION"]]
        
        metstation = st.selectbox(
            "Metstation",
            list(metstation_options.keys()),
            index=list(metstation_options.keys()).index(default_metstation)
        )
        code_metstation = metstation_options[metstation]

        casier_irv_options = {v: k for k, v in casier_irv_labels.items()} 
        default_casier_irv = casier_irv_labels[selected_row["CODE_FLAG_CASIER_IRV"]]
        
        casier_irv = st.selectbox(
            "Casier IRV",
            list(casier_irv_options.keys()),
            index=list(casier_irv_options.keys()).index(default_casier_irv)
        )
        code_casier_irv = casier_irv_options[casier_irv]
    
        surface = st.text_input(
            "Surface",
            value=clean_value(selected_row["SURFACE"],"number")
        )

        surface=clean_value(surface,"number")
        
    # =========================
    # 💾 UPDATE
    # =========================
    if st.button("💾 Mettre à jour"):
        update_park({
            "CODE_PARC": selected_row["CODE_PARC"],
            "NOM_PARC": nom,
            "ADRESSE_PARC": adresse,
            "CODE_VILLE": code_ville,
            "CODE_SECTEUR": code_secteur,
            "CODE_DISTRICT": code_district,
            "CODE_TYPE_PARC": code_type,
            "CODE_GESTION": code_gestion,
            "CODE_PEAGEUR": code_peageur,
            "NOMBRE_NIVEAU": nombre_niveau,
            "CODE_FLAG_FOURRIERE": code_fourriere,
            "CODE_FLAG_METSTATION": code_metstation,
            "CODE_FLAG_CASIER_IRV": code_casier_irv,
            "SURFACE": surface,
            "NOM_CREATEUR": user,
            "NOM_MODIFICATEUR": user,
            "DATE_MODIFICATION": datetime.now(pytz.timezone("Europe/Paris"))
        })

        st.session_state["message"] = "Parc mis à jour ✅"
        st.session_state["message_type"] = "success"
        st.rerun()


# =========================
# 🗑 HISTORIQUE
# =========================
if "history_code_parc" in st.session_state:

    df_history = get_history(st.session_state["history_code_parc"])
    df_histo = df_history.copy()

    df_histo["CODE_VILLE"] = df_histo["CODE_VILLE"].map(ville_labels)
    df_histo["CODE_SECTEUR"] = df_histo["CODE_SECTEUR"].map(secteur_labels)
    df_histo["CODE_DISTRICT"] = df_histo["CODE_DISTRICT"].map(district_labels)
    df_histo["CODE_TYPE_PARC"] = df_histo["CODE_TYPE_PARC"].map(type_labels)
    df_histo["CODE_GESTION"] = df_histo["CODE_GESTION"].map(gestion_labels)
    df_histo["CODE_PEAGEUR"] = df_histo["CODE_PEAGEUR"].map(peageur_labels)
    df_histo["CODE_FLAG_FOURRIERE"] = df_histo["CODE_FLAG_FOURRIERE"].map(fourriere_labels)
    df_histo["CODE_FLAG_METSTATION"] = df_histo["CODE_FLAG_METSTATION"].map(metstation_labels)
    df_histo["CODE_FLAG_CASIER_IRV"] = df_histo["CODE_FLAG_CASIER_IRV"].map(casier_irv_labels)

    st.markdown("### 📊 Historique des versions")

    st.dataframe(
        df_histo.style.apply(
            lambda x: ["background-color: #d4fcd4" if x.IS_ACTIVE else "" for _ in x],
            axis=1
        )
    )

    if st.button("❌ Fermer historique"):
        del st.session_state["history_code_parc"]
        st.rerun()
        
# =========================
# ➕ CREATE
# =========================
st.subheader("➕ Ajouter un parc")

col1, col2 = st.columns(2)

# =========================
# COLONNE 1
# =========================
with col1:

    code_parc = st.text_input("Code parc")
    nom = st.text_input("Nom parc")
    adresse = st.text_input("Adresse")

    ville_options = {v: k for k, v in ville_labels.items()}
    ville = st.selectbox("Ville", list(ville_options.keys()))
    code_ville = ville_options[ville]

    secteur_options = {v: k for k, v in secteur_labels.items()}
    secteur = st.selectbox("Secteur", list(secteur_options.keys()))
    code_secteur = secteur_options[secteur]

    district_options = {v: k for k, v in district_labels.items()}
    district = st.selectbox("District", list(district_options.keys()))
    code_district = district_options[district]

    type_options = {v: k for k, v in type_labels.items()}
    type_parc = st.selectbox("Type de parc", list(type_options.keys()))
    code_type = type_options[type_parc]


# =========================
# COLONNE 2
# =========================
with col2:

    gestion_options = {v: k for k, v in gestion_labels.items()}
    gestion = st.selectbox("Gestion", list(gestion_options.keys()))
    code_gestion = gestion_options[gestion]

    peageur_options = {v: k for k, v in peageur_labels.items()}
    peageur = st.selectbox("Péageur", list(peageur_options.keys()))
    code_peageur = peageur_options[peageur]

    nombre_niveau = st.number_input("Nombre de niveau", value=0,key="create_nombre_niveau")

    fourriere_options = {v: k for k, v in fourriere_labels.items()}
    fourriere = st.selectbox("Fourrière", list(fourriere_options.keys()))
    code_fourriere = fourriere_options[fourriere]

    metstation_options = {v: k for k, v in metstation_labels.items()}
    metstation = st.selectbox("Metstation", list(metstation_options.keys()))
    code_metstation = metstation_options[metstation]

    casier_irv_options = {v: k for k, v in casier_irv_labels.items()}
    casier_irv = st.selectbox("Casier IRV", list(casier_irv_options.keys()), key="create_casier_irv")
    code_casier_irv = casier_irv_options[casier_irv]

    surface = st.text_input( "Surface", value=0)
    surface=clean_value(surface,"number")

if st.button("➕ Créer le parc"):

    insert_park({
        "CODE_PARC": code_parc,
        "NOM_PARC": nom,
        "ADRESSE_PARC": adresse,
        "CODE_VILLE": code_ville,
        "CODE_SECTEUR": code_secteur,
        "CODE_DISTRICT": code_district,
        "CODE_TYPE_PARC": code_type,
        "CODE_GESTION": code_gestion,
        "CODE_PEAGEUR": code_peageur,
        "NOMBRE_NIVEAU": nombre_niveau,
        "CODE_FLAG_FOURRIERE": code_fourriere,
        "CODE_FLAG_METSTATION": code_metstation,
        "CODE_FLAG_CASIER_IRV": code_casier_irv,
        "SURFACE": surface,
        "NOM_CREATEUR": user,
        "NOM_MODIFICATEUR": user,
        "DATE_CREATION": datetime.now(pytz.timezone("Europe/Paris"))
    })

    st.session_state["message"] = "Parc créé ✅"
    st.session_state["message_type"] = "success"
    st.rerun()

# =========================
# 🗑 DELETE
# =========================
st.subheader("🗑️ Suppression")

to_delete = st.selectbox(
    "Sélectionner un parc",
    df_parks["CODE_PARC"]
)

if st.button("Supprimer"):
    delete_park(to_delete,user)
    st.session_state["message"] = "Parc supprimé"
    st.session_state["message_type"] = "warning"
    st.rerun()
