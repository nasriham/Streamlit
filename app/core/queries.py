from core.db import get_session
import pandas as pd
from core.functions import (
    clean_value
)
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

def get_gestion():
    return session.sql("""
        SELECT CODE_GESTION,
               LIBELLE_GESTION  
        FROM S_REFERENTIEL.T_R_GESTION
    """).to_pandas()

def get_peageur():
    return session.sql("""
        SELECT CODE_PEAGEUR,
               LIBELLE_PEAGEUR  
        FROM S_REFERENTIEL.T_R_PEAGEUR
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
            CODE_GESTION,
            CODE_PEAGEUR,
            NOMBRE_NIVEAU,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            CODE_FLAG_CASIER_IRV,
            SURFACE,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC
        WHERE IS_ACTIVE = 'TRUE'
    """).to_pandas()

def get_parks_exploit():
    return session.sql("""
        SELECT *
        FROM S_REFERENTIEL.T_R_PARC_EXPLOITATION
        WHERE IS_ACTIVE = TRUE
    """).to_pandas()

def get_parks_commercial():
    return session.sql("""
        SELECT
            CODE_PARC,
            CODE_FLAG_HORAIRES,
            CODE_FLAG_ABONNES,
            CODE_FLAG_AMODIES,
            CODE_FLAG_CONVENTION,
            NOM_CREATEUR,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_COMMERCIAL
        WHERE IS_ACTIVE = TRUE
        ORDER BY CODE_PARC
    """).to_pandas()

def get_parks_juridique():
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
        WHERE IS_ACTIVE = TRUE
        ORDER BY CODE_PARC
    """).to_pandas()

def get_parks_incendie():
    return session.sql("""
        SELECT 
            CODE_PARC,
            EAE_SPRINKLEURS,
        	NB_POSTES,
        	NB_TETES,
        	NB_EXTINCTEURS_EAU_PLUS_6_KG,
        	NB_EXTINCTEURS_CO2_2_KG,
        	NB_EXTINCTEURS_CO2_5_KG,
        	NB_EXTINCTEURS_POUDRE_6_KG,
        	NB_EXTINCTEURS_POUDRE_9_KG,
        	NB_EXTINCTEURS_POUDRE_50_KG,
        	NB_EXTINCTEURS_TOTAL,
        	NB_BAC_A_SABLE,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE
        WHERE IS_ACTIVE = TRUE
    """).to_pandas()

def get_parks_divers():
    return session.sql("""
        SELECT 
            CODE_PARC,
            GABARIT_STANDARD,
        	CODE_FLAG_PRESENCE_HUMAINE,
        	NB_ASCENCEURS,
        	NB_PEAGEURS,
        	CODE_FLAG_LAPI,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        FROM S_REFERENTIEL.T_R_PARC_DIVERS
        WHERE IS_ACTIVE = TRUE
    """).to_pandas()
    
# CREATE
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
            CODE_GESTION,
            CODE_PEAGEUR,
            NOMBRE_NIVEAU,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            CODE_FLAG_CASIER_IRV,
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
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, try_to_number(?), 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            '01/01/2222',
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
        row["CODE_GESTION"],
        row["CODE_PEAGEUR"],
        row["NOMBRE_NIVEAU"],
        row["CODE_FLAG_FOURRIERE"],
        row["CODE_FLAG_METSTATION"],
        row["CODE_FLAG_CASIER_IRV"],
        clean_value(row["SURFACE"],"number"),
        row["NOM_CREATEUR"],
        row["NOM_MODIFICATEUR"]
    ]).collect()

def insert_exploit(row: dict, user: str):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_EXPLOITATION (
            CODE_PARC,
            NB_CAPACITE_TOTALE,
            NB_CAPACITE_EXPLOITEE,
            NB_CAPACITE_VL,
            NB_CAPACITE_VL_DT_THERMIQUE,
            NB_CAPACITE_VL_DT_ELECTRIQUE,
            NB_CAPACITE_VL_DT_PMR,
            NB_CAPACITE_VL_DT_PMR_ELECTRIQUE,
            NB_CAPACITE_VL_DT_MOTO,
            NB_CAPACITE_VL_DT_VELO,
            NB_CAPACITE_VL_DT_VELO_CARGO,
            NB_CAPACITE_VL_DT_VELO_AUTRE,
            NB_CAPACITE_VL_DT_AUTRE,
            COMMENTAIRE_AUTRE,
            NB_VOIES_ACCES,
            NB_VOIES_SORTIES,
            NB_ASCENCEUR,
            NB_ESCALIER,
            NB_PORTAIL,
            NB_TRAPPE_EVACUATION_MOTORISEE,
            NB_RIDEAUX_MOTORISEE,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        SELECT
            ?,
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            ?, -- commentaire (texte)
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            '2222-01-01',
            TRUE
    """, [
        row.get("CODE_PARC"),
        clean_value(row.get("NB_CAPACITE_TOTALE","number")),
        clean_value(row.get("NB_CAPACITE_EXPLOITEE","number")),
        clean_value(row.get("NB_CAPACITE_VL","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_THERMIQUE","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_ELECTRIQUE","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_PMR","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_PMR_ELECTRIQUE","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_MOTO","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_VELO","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_VELO_CARGO","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_VELO_AUTRE","number")),
        clean_value(row.get("NB_CAPACITE_VL_DT_AUTRE","number")),
        row.get("COMMENTAIRE_AUTRE"),
        clean_value(row.get("NB_VOIES_ACCES","number")),
        clean_value(row.get("NB_VOIES_SORTIES","number")),
        clean_value(row.get("NB_ASCENCEUR","number")),
        clean_value(row.get("NB_ESCALIER","number")),
        clean_value(row.get("NB_PORTAIL","number")),
        clean_value(row.get("NB_TRAPPE_EVACUATION_MOTORISEE","number")),
        clean_value(row.get("NB_RIDEAUX_MOTORISEE","number")),
        user,
        user
    ]).collect()

def insert_park_commercial(row, user):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_COMMERCIAL (
            CODE_PARC,
            CODE_FLAG_HORAIRES,
            CODE_FLAG_ABONNES,
            CODE_FLAG_AMODIES,
            CODE_FLAG_CONVENTION,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            '01/01/2222',
            TRUE
        )
    """, [
        row["CODE_PARC"],
        row["CODE_FLAG_HORAIRES"],
        row["CODE_FLAG_ABONNES"],
        row["CODE_FLAG_AMODIES"],
        row["CODE_FLAG_CONVENTION"],
        user,
        user
    ]).collect()

def insert_park_juridique(row, user):
    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_JURIDIQUE (
            CODE_PARC,
            MISE_EN_SERVICE,
            CODE_NATURE_JURIDIQUE,
            SIRET,	
            CODE_FLAG_COPRO,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        VALUES (
            ?, ?, ?, ?, ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            '01/01/2222',
            TRUE
        )
    """, [
        row["CODE_PARC"],
        row["MISE_EN_SERVICE"],
        row["CODE_NATURE_JURIDIQUE"],
        row["SIRET"],
        row["CODE_FLAG_COPRO"],
        user,
        user
    ]).collect()

def insert_incendie(row: dict, user: str):

    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_SECURITE_INCENDIE (
            CODE_PARC,
            EAE_SPRINKLEURS,
            NB_POSTES,
            NB_TETES,
            NB_EXTINCTEURS_EAU_PLUS_6_KG,
            NB_EXTINCTEURS_CO2_2_KG,
            NB_EXTINCTEURS_CO2_5_KG,
            NB_EXTINCTEURS_POUDRE_6_KG,
            NB_EXTINCTEURS_POUDRE_9_KG,
            NB_EXTINCTEURS_POUDRE_50_KG,
            NB_EXTINCTEURS_TOTAL,
            NB_BAC_A_SABLE,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        SELECT
            ?,
            ?,
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            try_to_number(?),
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            '2222-01-01',
            TRUE
    """, [
        row.get("CODE_PARC"),
        row.get("EAE_SPRINKLEURS"),
        clean_value(row.get("NB_POSTES","number")),
        clean_value(row.get("NB_TETES","number")),
        clean_value(row.get("NB_EXTINCTEURS_EAU_PLUS_6_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_CO2_2_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_CO2_5_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_POUDRE_6_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_POUDRE_9_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_POUDRE_50_KG","number")),
        clean_value(row.get("NB_EXTINCTEURS_TOTAL","number")),
        clean_value(row.get("NB_BAC_A_SABLE","number")),
        user,
        user
    ]).collect()

def insert_park_divers(row: dict, user: str):

    session.sql("""
        INSERT INTO S_REFERENTIEL.T_R_PARC_DIVERS (
            CODE_PARC,
            GABARIT_STANDARD,
            CODE_FLAG_PRESENCE_HUMAINE,
            NB_ASCENCEURS,
            NB_PEAGEURS,
            CODE_FLAG_LAPI,
            DATE_CREATION,
            NOM_CREATEUR,
            DATE_MODIFICATION,
            NOM_MODIFICATEUR,
            DATE_DEBUT,
            DATE_FIN,
            IS_ACTIVE
        )
        SELECT
            ?,
            ?,
            ?,
            try_to_number(?),
            try_to_number(?),
            ?,
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            ?,
            CURRENT_TIMESTAMP(),
            '2222-01-01',
            TRUE
    """, [
        row.get("CODE_PARC"),
        row.get("GABARIT_STANDARD"),
        row.get("CODE_FLAG_PRESENCE_HUMAINE"),
        clean_value(row.get("NB_ASCENCEURS","number")),
        clean_value(row.get("NB_PEAGEURS","number")),
        row.get("CODE_FLAG_LAPI"),
        user,
        user
    ]).collect()
    
# UPDATE
def update_park(row):

    # 1. fermer version actuelle
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC
        SET 
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = 'FALSE',
            DATE_MODIFICATION = CURRENT_TIMESTAMP(),
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
            CODE_GESTION,
            CODE_PEAGEUR,
            NOMBRE_NIVEAU,
            CODE_FLAG_FOURRIERE,
            CODE_FLAG_METSTATION,
            CODE_FLAG_CASIER_IRV,
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
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, try_to_number(?), 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            ?, 
            CURRENT_TIMESTAMP(),
            '01/01/2222',
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
        row["CODE_GESTION"],
        row["CODE_PEAGEUR"],
        row["NOMBRE_NIVEAU"],
        row["CODE_FLAG_FOURRIERE"],
        row["CODE_FLAG_METSTATION"],
        row["CODE_FLAG_CASIER_IRV"],
        row["SURFACE"],
        row["NOM_CREATEUR"],
        row["NOM_MODIFICATEUR"]
    ]).collect()

def update_exploit(row: dict, user: str):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_EXPLOITATION
        SET 
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_exploit(row, user)

def update_commercial(row, user):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_COMMERCIAL
        SET 
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_park_commercial(row, user)

def update_juridique(row, user):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_JURIDIQUE
        SET 
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
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
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_incendie(row, user)
    
def update_divers(row, user):

    # 1. close ancienne ligne
    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC_DIVERS
        SET 
            DATE_FIN = CURRENT_TIMESTAMP(),
            IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = ?,
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
        WHERE CODE_PARC = ?
          AND IS_ACTIVE = TRUE
    """, [user, row["CODE_PARC"]]).collect()

    # 2. insert nouvelle version
    insert_park_divers(row, user)
    
# DELETE
def delete_park(code_parc, user):

    session.sql("""
        UPDATE S_REFERENTIEL.T_R_PARC
        SET 
            IS_ACTIVE = FALSE,
            DATE_FIN = CURRENT_TIMESTAMP(),
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

def get_history_commercial():
    return session.sql("""
        SELECT
        CODE_PARC,
        CODE_FLAG_HORAIRES,
        CODE_FLAG_ABONNES,
        CODE_FLAG_AMODIES,
        CODE_FLAG_CONVENTION,
        NOM_CREATEUR,
        NOM_MODIFICATEUR,
        DATE_DEBUT,
        DATE_FIN,
        IS_ACTIVE
    FROM S_REFERENTIEL.T_R_PARC_COMMERCIAL
    ORDER BY CODE_PARC, DATE_DEBUT DESC
    """, ).to_pandas()

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

def get_history_divers():
    return session.sql("""
        SELECT
        CODE_PARC,
        GABARIT_STANDARD,
        CODE_FLAG_PRESENCE_HUMAINE,
        NB_ASCENCEURS,	
        NB_PEAGEURS,
        CODE_FLAG_LAPI,
        NOM_CREATEUR,
        NOM_MODIFICATEUR,
        DATE_DEBUT,
        DATE_FIN,
        IS_ACTIVE
    FROM S_REFERENTIEL.T_R_PARC_DIVERS
    ORDER BY CODE_PARC, DATE_DEBUT DESC
    """).to_pandas()
