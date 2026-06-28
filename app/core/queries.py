# SQL queries for parking management application
# Co-authored with CoCo
from core.db import get_session
import pandas as pd
from core.functions import (
    clean_value
)

def clean_date(val):
    """Return a date string safe for Snowflake, or None if empty/invalid."""
    if val is None:
        return None
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    s = str(val).strip()
    if s.lower() in ("none", "nat", ""):
        return None
    return s
session = get_session()

# READ
def get_villes():
    return session.sql("""
       SELECT CODE_VILLE,
              CODE_POSTAL || ' - ' || LIBELLE_VILLE AS LIBELLE_VILLE   
        FROM S_REFERENTIEL.T_R_VILLE
    """).to_pandas()

def get_secteurs():
    return session.sql("""
        SELECT CODE_SECTEUR,
               LIBELLE_SECTEUR   
        FROM S_REFERENTIEL.T_R_SECTEUR
    """).to_pandas()

def get_districts():
    return session.sql("""
        SELECT CODE_DISTRICT,
               LIBELLE_DISTRICT   
        FROM S_REFERENTIEL.T_R_DISTRICT
    """).to_pandas()

def get_type():
    return session.sql("""
        SELECT CODE_TYPE_PARC,
               LIBELLE_TYPE_PARC  
        FROM S_REFERENTIEL.T_R_TYPE_PARC
    """).to_pandas()


def get_flag():
    return session.sql("""
        SELECT CODE_FLAG,
               LIBELLE_FLAG  
        FROM S_REFERENTIEL.T_R_FLAG
    """).to_pandas()

def get_nature_juridique():
    return session.sql("""
        SELECT CODE_NATURE_JURIDIQUE,
               LIBELLE_NATURE_JURIDIQUE  
        FROM S_REFERENTIEL.T_R_NATURE_JURIDIQUE
    """).to_pandas()
    
def get_parks():
    return session.sql("""
        SELECT 
            CODE_PARC,
            NOM_PARC,
            ADRESSE_PARC,
            CODE_VILLE,
            CODE_SECTEUR,
            CODE_DISTRICT,
            CODE_TYPE_PARC,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            UPPER(IS_ACTIVE::VARCHAR) AS IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC
        WHERE IS_ACTIVE = 'TRUE'
    """).to_pandas()

def _sync_tables_filles():
    """Synchronise les tables filles avec T_R_PARC : insere une ligne pour chaque parc manquant."""
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_EXPLOITATION (CODE_PARC, NIVEAU, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        SELECT p.CODE_PARC, 'RDC', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE
        FROM S_REFERENTIEL.T_R_PARC p
        WHERE p.IS_ACTIVE = 'TRUE'
          AND p.CODE_PARC NOT IN (SELECT CODE_PARC FROM S_REFERENTIEL.T_R_PARC_EXPLOITATION WHERE IS_ACTIVE = TRUE)
    """).collect()
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_EQUIPEMENT_ACCES (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        SELECT p.CODE_PARC, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, 'TRUE'
        FROM S_REFERENTIEL.T_R_PARC p
        WHERE p.IS_ACTIVE = 'TRUE'
          AND p.CODE_PARC NOT IN (SELECT CODE_PARC FROM S_REFERENTIEL.T_R_EQUIPEMENT_ACCES WHERE IS_ACTIVE = 'TRUE')
    """).collect()
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_JURIDIQUE (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        SELECT p.CODE_PARC, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE
        FROM S_REFERENTIEL.T_R_PARC p
        WHERE p.IS_ACTIVE = 'TRUE'
          AND p.CODE_PARC NOT IN (SELECT CODE_PARC FROM S_REFERENTIEL.T_R_PARC_JURIDIQUE WHERE IS_ACTIVE = TRUE)
    """).collect()
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        SELECT p.CODE_PARC, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'SYSTEM', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE
        FROM S_REFERENTIEL.T_R_PARC p
        WHERE p.IS_ACTIVE = 'TRUE'
          AND p.CODE_PARC NOT IN (SELECT CODE_PARC FROM S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE WHERE IS_ACTIVE = TRUE)
    """).collect()

def get_parks_exploit():
    _sync_tables_filles()
    return session.sql("""
        SELECT
            p.NOM_PARC,
            e.CODE_PARC,
            e.NIVEAU,
            e.NB_CAPACITE_VL_DT_THERMIQUE,
            e.NB_CAPACITE_VL_DT_ELECTRIQUE,
            e.NB_CAPACITE_VL_DT_PMR,
            e.NB_CAPACITE_VL_DT_PMR_ELECTRIQUE,
            e.NB_CAPACITE_VL_DT_MOTO,
            e.NB_CAPACITE_VL_DT_VELO,
            e.NB_CAPACITE_VL_DT_AUTRE,
            e.COMMENTAIRE_AUTRE,
            e.SURFACE,
            e.DATE_CREATION,
            e.NOM_CREATEUR,
            e.DATE_MODIFICATION,
            e.NOM_MODIFICATEUR,
            e.DATE_DEBUT,
            e.DATE_FIN,
            UPPER(e.IS_ACTIVE::VARCHAR) AS IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_EXPLOITATION e
        LEFT JOIN S_REFERENTIEL.T_R_PARC p ON e.CODE_PARC = p.CODE_PARC AND p.IS_ACTIVE = 'TRUE'
        WHERE e.IS_ACTIVE = TRUE
        ORDER BY p.NOM_PARC, e.NIVEAU
    """).to_pandas()

def get_parks_equipements():
    _sync_tables_filles()
    return session.sql("""
        SELECT
            p.NOM_PARC,
            e.CODE_PARC,
            e.NB_VOIES_ENTREES,
            e.NB_VOIES_SORTIES,
            e.NOM_PEAGEUR,
            e.NB_LECTEURS_PIETONS,
            e.NB_LECTEURS_METSTATIONS,
            e.NB_CAISSES,
            e.NB_BORNES_PEAGE_ENTREES,
            e.FLAG_DOUBLE_ENTREES,
            e.NB_BORNES_PEAGE_SORTIES,
            e.FLAG_DOUBLE_SORTIES,
            e.FLAG_LECTURE_PLAQUE,
            e.NB_ASCENSEURS,
            e.MARQUE_ASCENSEURS,
            e.DATE_MISE_SERVICE_ASCENSEUR,
            e.NB_ESCALIERS,
            e.NB_PORTAILS,
            e.NB_PORTES_COULISSANTES,
            e.NB_RIDEAUX_MOTORISES,
            e.NB_BORNES_IRVE,
            e.FLAG_LOCKERS,
            e.FLAG_GUIDAGE_PLACE,
            e.GABARIT_STANDARD,
            e.DATE_CREATION,
            e.NOM_CREATEUR,
            e.DATE_MODIFICATION,
            e.NOM_MODIFICATEUR,
            e.DATE_DEBUT,
            e.DATE_FIN,
            UPPER(e.IS_ACTIVE::VARCHAR) AS IS_ACTIVE
        FROM S_REFERENTIEL.T_R_EQUIPEMENT_ACCES e
        LEFT JOIN S_REFERENTIEL.T_R_PARC p ON e.CODE_PARC = p.CODE_PARC AND p.IS_ACTIVE = 'TRUE'
        WHERE e.IS_ACTIVE = 'TRUE'
        ORDER BY p.NOM_PARC
    """).to_pandas()

def get_parks_juridique():
    _sync_tables_filles()
    return session.sql("""
        SELECT
        p.NOM_PARC,
        j.CODE_PARC,
        j.MISE_EN_SERVICE,
        j.CODE_NATURE_JURIDIQUE,
        j.TYPE_CONVENTION,
        j.NOM_TIERS_ATTENANT,
        j.SIRET,  
        j.CODE_FLAG_COPRO,
        j.NOM_COPRO,
        j.DATE_CREATION,
        j.NOM_CREATEUR,
        j.DATE_MODIFICATION,
        j.NOM_MODIFICATEUR,
        j.DATE_DEBUT,
        j.DATE_FIN,
        UPPER(j.IS_ACTIVE::VARCHAR) AS IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_JURIDIQUE j
        LEFT JOIN S_REFERENTIEL.T_R_PARC p ON j.CODE_PARC = p.CODE_PARC AND p.IS_ACTIVE = 'TRUE'
        WHERE j.IS_ACTIVE = TRUE
        ORDER BY p.NOM_PARC
    """).to_pandas()

def get_parks_incendie():
    _sync_tables_filles()
    return session.sql("""
        SELECT 
            p.NOM_PARC,
            i.CODE_PARC,
            i.EAE_SPRINKLEURS,
            i.NB_POSTES,
            i.NB_TETES,
            i.NB_EXTINCTEURS_TOTAL,
            i.NB_BAC_A_SABLE,
            i.NB_DAI,
            i.FLAG_SSI,
            i.TYPE_SSI,
            i.MARQUE_SSI,
            i.DATE_MISE_EN_SERVICE_SSI,
            i.NB_DETECTION_CO_NO,
            i.NB_PORTE_COMPARTIMENTAGE,
            i.NB_EXTRACTEURS,
            i.NB_INSUFFLATEURS,
            i.NB_COLONNES_SECHES,
            i.NB_BAES,
            i.TYPE_ALIMENTATION_BAES,
            i.NB_TRAPPE_EVACUATION_MOTORISEE,
            i.TYPE_TARIFS_ELEC,
            i.FLAG_CELLULES_HT,
            i.FLAG_GROUPE_ELECTROGENE,
            i.FLAG_TGS,
            i.CAPACITE_CUVE_FIOUL,
            i.DATE_DERNIERE_COMMISSION,
            i.AVIS_COMMISSION,
            i.DATE_CREATION,
            i.NOM_CREATEUR,
            i.DATE_MODIFICATION,
            i.NOM_MODIFICATEUR,
            i.DATE_DEBUT,
            i.DATE_FIN,
            UPPER(i.IS_ACTIVE::VARCHAR) AS IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE i
        LEFT JOIN S_REFERENTIEL.T_R_PARC p ON i.CODE_PARC = p.CODE_PARC AND p.IS_ACTIVE = 'TRUE'
        WHERE i.IS_ACTIVE = TRUE
        ORDER BY p.NOM_PARC
    """).to_pandas()

def get_peageurs():
    return session.sql("""
        SELECT CODE_PEAGEUR, LIBELLE_PEAGEUR
        FROM S_REFERENTIEL.T_R_PEAGEUR
    """).to_pandas()

def park_code_exists(code_parc: str) -> bool:
    result = session.sql("""
        SELECT COUNT(*) AS CNT
        FROM S_REFERENTIEL.T_R_PARC
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = 'TRUE'
    """, [code_parc]).to_pandas()
    return int(result["CNT"].iloc[0]) > 0

def insert_park(row):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC (
            CODE_PARC,
            NOM_PARC,
            ADRESSE_PARC,
            CODE_VILLE,
            CODE_SECTEUR,
            CODE_DISTRICT,
            CODE_TYPE_PARC,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NULL,
            'TRUE'
        )
    """, [
        row["CODE_PARC"],
        row["NOM_PARC"],
        row["ADRESSE_PARC"],
        row["CODE_VILLE"],
        row["CODE_SECTEUR"],
        row["CODE_DISTRICT"],
        row["CODE_TYPE_PARC"],
        row["CODE_FLAG_FOURRIERE"],
        row["CODE_FLAG_METSTATION"],
        row["NOM_CREATEUR"],
        row["NOM_MODIFICATEUR"]
    ]).collect()

    # Initialisation automatique des tables filles
    code = row["CODE_PARC"]
    createur = row["NOM_CREATEUR"]

    # Exploitation (avec niveau RDC par defaut)
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_EXPLOITATION (CODE_PARC, NIVEAU, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        VALUES (?, 'RDC', CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE)
    """, [code, createur, createur]).collect()

    # Equipement & Acces
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_EQUIPEMENT_ACCES (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        VALUES (?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, 'TRUE')
    """, [code, createur, createur]).collect()

    # Juridique
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_JURIDIQUE (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        VALUES (?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE)
    """, [code, createur, createur]).collect()

    # Securite incendie
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE (CODE_PARC, DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR, DATE_DEBUT, DATE_FIN, IS_ACTIVE)
        VALUES (?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, TRUE)
    """, [code, createur, createur]).collect()

def insert_exploit(row: dict, user: str):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_EXPLOITATION (
            CODE_PARC,
            NIVEAU,
            NB_CAPACITE_VL_DT_THERMIQUE,
            NB_CAPACITE_VL_DT_ELECTRIQUE,
            NB_CAPACITE_VL_DT_PMR,
            NB_CAPACITE_VL_DT_PMR_ELECTRIQUE,
            NB_CAPACITE_VL_DT_MOTO,
            NB_CAPACITE_VL_DT_VELO,
            NB_CAPACITE_VL_DT_AUTRE,
            COMMENTAIRE_AUTRE,
            SURFACE,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NULL,
            TRUE
        )
    """, [
        row.get("CODE_PARC"),
        row.get("NIVEAU"),
        row.get("NB_CAPACITE_VL_DT_THERMIQUE"),
        row.get("NB_CAPACITE_VL_DT_ELECTRIQUE"),
        row.get("NB_CAPACITE_VL_DT_PMR"),
        row.get("NB_CAPACITE_VL_DT_PMR_ELECTRIQUE"),
        row.get("NB_CAPACITE_VL_DT_MOTO"),
        row.get("NB_CAPACITE_VL_DT_VELO"),
        row.get("NB_CAPACITE_VL_DT_AUTRE"),
        row.get("COMMENTAIRE_AUTRE"),
        row.get("SURFACE"),
        user,
        user
    ]).collect()

def insert_park_juridique(row, user):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_JURIDIQUE (
            CODE_PARC,
            MISE_EN_SERVICE,
            CODE_NATURE_JURIDIQUE,
            TYPE_CONVENTION,
            NOM_TIERS_ATTENANT,
            SIRET,  
            CODE_FLAG_COPRO,
            NOM_COPRO,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?, 
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?, 
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NULL,
            TRUE
        )
    """, [
        row["CODE_PARC"],
        row.get("MISE_EN_SERVICE"),
        row.get("CODE_NATURE_JURIDIQUE"),
        row.get("TYPE_CONVENTION"),
        row.get("NOM_TIERS_ATTENANT"),
        row.get("SIRET"),
        row.get("CODE_FLAG_COPRO"),
        row.get("NOM_COPRO"),
        user,
        user
    ]).collect()

def insert_incendie(row: dict, user: str):
    date_ssi = clean_date(row.get("DATE_MISE_EN_SERVICE_SSI"))
    date_comm = clean_date(row.get("DATE_DERNIERE_COMMISSION"))

    date_ssi_sql = f"'{date_ssi}'" if date_ssi else "NULL"
    date_comm_sql = f"'{date_comm}'" if date_comm else "NULL"

    session.sql(f"""
        INSERT INTO S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE (
            CODE_PARC,
            EAE_SPRINKLEURS,
            NB_POSTES,
            NB_TETES,
            NB_EXTINCTEURS_TOTAL,
            NB_BAC_A_SABLE,
            NB_DAI,
            FLAG_SSI,
            TYPE_SSI,
            MARQUE_SSI,
            DATE_MISE_EN_SERVICE_SSI,
            NB_DETECTION_CO_NO,
            NB_PORTE_COMPARTIMENTAGE,
            NB_EXTRACTEURS,
            NB_INSUFFLATEURS,
            NB_COLONNES_SECHES,
            NB_BAES,
            TYPE_ALIMENTATION_BAES,
            NB_TRAPPE_EVACUATION_MOTORISEE,
            TYPE_TARIFS_ELEC,
            FLAG_CELLULES_HT,
            FLAG_GROUPE_ELECTROGENE,
            FLAG_TGS,
            CAPACITE_CUVE_FIOUL,
            DATE_DERNIERE_COMMISSION,
            AVIS_COMMISSION,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        SELECT
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            {date_ssi_sql}, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, {date_comm_sql}, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NULL,
            TRUE
    """, [
        row.get("CODE_PARC"),
        row.get("EAE_SPRINKLEURS"),
        clean_value(row.get("NB_POSTES"), "int"),
        clean_value(row.get("NB_TETES"), "int"),
        clean_value(row.get("NB_EXTINCTEURS_TOTAL"), "int"),
        clean_value(row.get("NB_BAC_A_SABLE"), "int"),
        clean_value(row.get("NB_DAI"), "int"),
        row.get("FLAG_SSI"),
        row.get("TYPE_SSI"),
        row.get("MARQUE_SSI"),
        clean_value(row.get("NB_DETECTION_CO_NO"), "int"),
        clean_value(row.get("NB_PORTE_COMPARTIMENTAGE"), "int"),
        clean_value(row.get("NB_EXTRACTEURS"), "int"),
        clean_value(row.get("NB_INSUFFLATEURS"), "int"),
        clean_value(row.get("NB_COLONNES_SECHES"), "int"),
        clean_value(row.get("NB_BAES"), "int"),
        row.get("TYPE_ALIMENTATION_BAES"),
        clean_value(row.get("NB_TRAPPE_EVACUATION_MOTORISEE"), "int"),
        row.get("TYPE_TARIFS_ELEC"),
        row.get("FLAG_CELLULES_HT"),
        row.get("FLAG_GROUPE_ELECTROGENE"),
        row.get("FLAG_TGS"),
        clean_value(row.get("CAPACITE_CUVE_FIOUL"), "int"),
        row.get("AVIS_COMMISSION"),
        user,
        user
    ]).collect()

def update_park(row):

    # 1. fermer version actuelle
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC
        SET 
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            IS_ACTIVE = 'FALSE',
            DATE_MODIFICATION = CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NOM_MODIFICATEUR = ?
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = 'TRUE'
    """, [
        row["NOM_MODIFICATEUR"],
        row["CODE_PARC"]
    ]).collect()

    # 2. insérer nouvelle version

    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC (
            CODE_PARC,
            NOM_PARC,
            ADRESSE_PARC,
            CODE_VILLE,
            CODE_SECTEUR,
            CODE_DISTRICT,
            CODE_TYPE_PARC,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ,
            NULL,
            'TRUE'
        )
    """, [
        row["CODE_PARC"],
        row["NOM_PARC"],
        row["ADRESSE_PARC"],
        row["CODE_VILLE"],
        row["CODE_SECTEUR"],
        row["CODE_DISTRICT"],
        row["CODE_TYPE_PARC"],
        row["CODE_FLAG_FOURRIERE"],
        row["CODE_FLAG_METSTATION"],
        row["NOM_CREATEUR"],
        row["NOM_MODIFICATEUR"]
    ]).collect()

def update_exploit(row: dict, user: str):

    # 1. close ancienne ligne (utilise ANCIEN_NIVEAU si disponible, sinon NIVEAU)
    ancien_niveau = row.get("ANCIEN_NIVEAU") or row.get("NIVEAU")
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_EXPLOITATION
        SET 
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ
        WHERE CODE_PARC = ?
          AND NIVEAU = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"], ancien_niveau]).collect()

    # 2. insert nouvelle version
    insert_exploit(row, user)


def update_juridique(row, user):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_JURIDIQUE
        SET 
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_park_juridique(row, user)

def update_incendie(row: dict, user: str):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE
        SET 
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_incendie(row, user)
    
# DELETE
def delete_park(code_parc, user):

    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC
        SET 
            IS_ACTIVE = 'FALSE',
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            NOM_MODIFICATEUR = ?
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = 'TRUE'
    """, [user, code_parc]).collect()

# HISTORY
def get_history(code_parc):
    return session.sql("""
        SELECT *
        FROM S_REFERENTIEL.T_R_PARC
        WHERE CODE_PARC = ?
        ORDER BY DATE_DEBUT DESC
    """, [code_parc]).to_pandas()

def get_history_juridique():
    return session.sql("""
        SELECT
        CODE_PARC,
        MISE_EN_SERVICE,
        CODE_NATURE_JURIDIQUE,
        SIRET,	
        CODE_FLAG_COPRO,
        NOM_CREATEUR,
        NOM_MODIFICATEUR,
        DATE_DEBUT,
        DATE_FIN,
        IS_ACTIVE
    FROM S_REFERENTIEL.T_R_PARC_JURIDIQUE
    ORDER BY CODE_PARC, DATE_DEBUT DESC
    """, ).to_pandas()

# =============================================
def insert_equipement(row, user):
    date_asc = clean_date(row.get("DATE_MISE_SERVICE_ASCENSEUR"))
    date_asc_sql = f"'{date_asc}'" if date_asc else "NULL"

    session.sql(f"""
        INSERT INTO S_REFERENTIEL.T_R_EQUIPEMENT_ACCES (
            CODE_PARC, NB_VOIES_ENTREES, NB_VOIES_SORTIES, NOM_PEAGEUR,
            NB_LECTEURS_PIETONS, NB_LECTEURS_METSTATIONS, NB_CAISSES,
            NB_BORNES_PEAGE_ENTREES, FLAG_DOUBLE_ENTREES, NB_BORNES_PEAGE_SORTIES,
            FLAG_DOUBLE_SORTIES, FLAG_LECTURE_PLAQUE, NB_ASCENSEURS,
            MARQUE_ASCENSEURS, DATE_MISE_SERVICE_ASCENSEUR, NB_ESCALIERS,
            NB_PORTAILS, NB_PORTES_COULISSANTES, NB_RIDEAUX_MOTORISES,
            NB_BORNES_IRVE, FLAG_LOCKERS, FLAG_GUIDAGE_PLACE, GABARIT_STANDARD,
            DATE_CREATION, NOM_CREATEUR, DATE_MODIFICATION, NOM_MODIFICATEUR,
            DATE_DEBUT, DATE_FIN, IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, {date_asc_sql}, ?, ?, ?, ?, ?, ?, ?, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?, CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, ?,
            CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, NULL, 'TRUE'
        )
    """, [
        row.get("CODE_PARC"),
        row.get("NB_VOIES_ENTREES"),
        row.get("NB_VOIES_SORTIES"),
        row.get("NOM_PEAGEUR"),
        row.get("NB_LECTEURS_PIETONS"),
        row.get("NB_LECTEURS_METSTATIONS"),
        row.get("NB_CAISSES"),
        row.get("NB_BORNES_PEAGE_ENTREES"),
        row.get("FLAG_DOUBLE_ENTREES"),
        row.get("NB_BORNES_PEAGE_SORTIES"),
        row.get("FLAG_DOUBLE_SORTIES"),
        row.get("FLAG_LECTURE_PLAQUE"),
        row.get("NB_ASCENSEURS"),
        row.get("MARQUE_ASCENSEURS"),
        row.get("NB_ESCALIERS"),
        row.get("NB_PORTAILS"),
        row.get("NB_PORTES_COULISSANTES"),
        row.get("NB_RIDEAUX_MOTORISES"),
        row.get("NB_BORNES_IRVE"),
        row.get("FLAG_LOCKERS"),
        row.get("FLAG_GUIDAGE_PLACE"),
        row.get("GABARIT_STANDARD"),
        user,
        user
    ]).collect()


def update_equipement(row, user):
    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_EQUIPEMENT_ACCES
        SET 
            DATE_FIN = TO_VARCHAR(CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ, 'YYYY-MM-DD HH24:MI:SS'),
            IS_ACTIVE = 'FALSE',
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CONVERT_TIMEZONE('Europe/Paris', CURRENT_TIMESTAMP())::TIMESTAMP_NTZ
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = 'TRUE'
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_equipement(row, user)
