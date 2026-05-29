"""Toutes les requêtes SQL centralisées."""

from core.db import run_query, run_dml, SCHEMA, SCHEMA_GOLD


# ===== EVENEMENTS =====

def get_evenements():
    return run_query(f"""
        SELECT
            e.CODE_EVENEMENT,
            e.TITRE_EVENEMENT,
            e.CODE_TYPE_EVENEMENT,
            t.LIBELLE_TYPE_EVENEMENT AS TYPE_EVENEMENT,
            t.CATEGORIE,
            e.CODE_LIEU,
            l.LIBELLE_LIEU AS LIEU,
            l.VILLE,
            e.CODE_IMPACT,
            i.LIBELLE_IMPACT AS IMPACT,
            i.NIVEAU_SEVERITE,
            e.DATE_DEBUT,
            e.DATE_FIN,
            e.COMMENTAIRE,
            e.NOM_CREATEUR,
            e.NOM_MODIFICATEUR,
            e.DATE_CREATION,
            e.DATE_MODIFICATION
        FROM {SCHEMA}.T_BASE_EVENEMENT e
        LEFT JOIN {SCHEMA}.T_TYPE_EVENEMENT t ON e.CODE_TYPE_EVENEMENT = t.CODE_TYPE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_LIEU_EVENEMENT l ON e.CODE_LIEU = l.CODE_LIEU
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.IS_ACTIVE = TRUE
        ORDER BY e.DATE_DEBUT DESC
    """)


def get_ref_types():
    return run_query(
        f"SELECT CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE FROM {SCHEMA}.T_TYPE_EVENEMENT WHERE IS_ACTIVE = TRUE ORDER BY CATEGORIE, LIBELLE_TYPE_EVENEMENT",
        ttl=60
    )


def get_ref_lieux():
    return run_query(
        f"SELECT CODE_LIEU, LIBELLE_LIEU, VILLE FROM {SCHEMA}.T_LIEU_EVENEMENT WHERE IS_ACTIVE = TRUE ORDER BY VILLE, LIBELLE_LIEU",
        ttl=60
    )


def get_ref_impacts():
    return run_query(
        f"SELECT CODE_IMPACT, LIBELLE_IMPACT, NIVEAU_SEVERITE FROM {SCHEMA}.T_IMPACT_EVENEMENT WHERE IS_ACTIVE = TRUE ORDER BY NIVEAU_SEVERITE",
        ttl=60
    )


def get_parkings():
    return run_query(f"""
        SELECT DISTINCT PHNUM AS CODE_PARC, PHNAME AS NOM_PARC
        FROM {SCHEMA_GOLD}.DIM_TERMINAL
        ORDER BY PHNAME
    """, ttl=60)


def get_parcs_evenement(code_evt: int):
    return run_query(f"SELECT CODE_PARC, NOM_PARC FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}")


def get_max_code_evenement():
    df = run_query(f"SELECT MAX(CODE_EVENEMENT) AS CODE FROM {SCHEMA}.T_BASE_EVENEMENT")
    return int(df.iloc[0]["CODE"])


# ===== CRUD EVENEMENTS =====

def insert_evenement(titre, code_type, code_lieu, code_impact, timestamp_debut, timestamp_fin_sql, commentaire, user):
    titre_sql = titre.replace("'", "''")
    commentaire_sql = commentaire.replace("'", "''") if commentaire else ""
    run_dml(f"""
        INSERT INTO {SCHEMA}.T_BASE_EVENEMENT
        (CODE_EVENEMENT, TITRE_EVENEMENT, CODE_TYPE_EVENEMENT, CODE_LIEU, CODE_IMPACT, DATE_DEBUT, DATE_FIN, COMMENTAIRE, NOM_CREATEUR, DATE_CREATION, IS_ACTIVE)
        VALUES (
            {SCHEMA}.SEQ_EVENEMENT.NEXTVAL,
            '{titre_sql}',
            {code_type},
            {code_lieu},
            {code_impact},
            '{timestamp_debut}',
            {timestamp_fin_sql},
            '{commentaire_sql}',
            '{user}',
            CURRENT_TIMESTAMP(),
            TRUE
        )
    """)


def update_evenement(code_evt: int, set_parts: list, user: str):
    set_parts.append(f"NOM_MODIFICATEUR = '{user}'")
    set_parts.append("DATE_MODIFICATION = CURRENT_TIMESTAMP()")
    run_dml(f"""
        UPDATE {SCHEMA}.T_BASE_EVENEMENT SET
            {', '.join(set_parts)}
        WHERE CODE_EVENEMENT = {code_evt}
    """)


def delete_evenement(code_evt: int, user: str):
    run_dml(f"""
        UPDATE {SCHEMA}.T_BASE_EVENEMENT
        SET IS_ACTIVE = FALSE,
            NOM_MODIFICATEUR = '{user}',
            DATE_MODIFICATION = CURRENT_TIMESTAMP()
        WHERE CODE_EVENEMENT = {code_evt}
    """)
    run_dml(f"DELETE FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}")


# ===== PARKINGS ASSOCIES =====

def insert_parc_evenement(code_evt: int, code_parc: int, nom_parc: str):
    run_dml(f"""
        INSERT INTO {SCHEMA}.T_EVENEMENT_PARC (CODE_EVENEMENT, CODE_PARC, NOM_PARC)
        VALUES ({code_evt}, {code_parc}, '{nom_parc.replace("'", "''")}')
    """)


def delete_parcs_evenement(code_evt: int):
    run_dml(f"DELETE FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}")


# ===== HISTORIQUE =====

def get_historique(code_evt: int = None):
    where_clause = f"WHERE CODE_EVENEMENT = {code_evt}" if code_evt else ""
    return run_query(f"""
        SELECT CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE,
               LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
               COMMENTAIRE, PARKINGS_IMPACTES, IS_ACTIVE, MODIFIE_PAR, ACTION,
               DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE
        FROM {SCHEMA}.T_HISTORIQUE_EVENEMENT
        {where_clause}
        ORDER BY DATE_DEBUT_VALIDITE DESC
    """)


def get_historique_complet():
    return run_query(f"""
        SELECT CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE,
               LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
               COMMENTAIRE, PARKINGS_IMPACTES, IS_ACTIVE, MODIFIE_PAR, ACTION,
               DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE
        FROM {SCHEMA}.T_HISTORIQUE_EVENEMENT
        ORDER BY DATE_DEBUT_VALIDITE DESC
    """)


def insert_snapshot(code_evt: int, action: str, user: str):
    """Insert a full snapshot of the event into history and close the previous one."""
    # Close previous active snapshot
    run_dml(f"""
        UPDATE {SCHEMA}.T_HISTORIQUE_EVENEMENT
        SET DATE_FIN_VALIDITE = CURRENT_TIMESTAMP(), IS_ACTIVE = 0
        WHERE CODE_EVENEMENT = {code_evt} AND DATE_FIN_VALIDITE IS NULL
    """)
    # Insert new snapshot with current state
    run_dml(f"""
        INSERT INTO {SCHEMA}.T_HISTORIQUE_EVENEMENT
        (CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE, LIEU, VILLE,
         IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN, COMMENTAIRE, PARKINGS_IMPACTES,
         IS_ACTIVE, MODIFIE_PAR, ACTION, DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE)
        SELECT
            e.CODE_EVENEMENT,
            e.TITRE_EVENEMENT,
            t.LIBELLE_TYPE_EVENEMENT,
            t.CATEGORIE,
            l.LIBELLE_LIEU,
            l.VILLE,
            i.LIBELLE_IMPACT,
            i.NIVEAU_SEVERITE,
            e.DATE_DEBUT,
            e.DATE_FIN,
            e.COMMENTAIRE,
            (SELECT LISTAGG(NOM_PARC, ', ') FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}),
            CASE WHEN e.IS_ACTIVE = TRUE THEN 1 ELSE 0 END,
            '{user}',
            '{action}',
            CURRENT_TIMESTAMP(),
            NULL
        FROM {SCHEMA}.T_BASE_EVENEMENT e
        LEFT JOIN {SCHEMA}.T_TYPE_EVENEMENT t ON e.CODE_TYPE_EVENEMENT = t.CODE_TYPE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_LIEU_EVENEMENT l ON e.CODE_LIEU = l.CODE_LIEU
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.CODE_EVENEMENT = {code_evt}
    """)


def close_all_snapshots(code_evt: int):
    """Close all open snapshots for a deleted event (set DATE_FIN_VALIDITE)."""
    run_dml(f"""
        UPDATE {SCHEMA}.T_HISTORIQUE_EVENEMENT
        SET DATE_FIN_VALIDITE = CURRENT_TIMESTAMP()
        WHERE CODE_EVENEMENT = {code_evt} AND DATE_FIN_VALIDITE IS NULL
    """)


# ===== OCCUPATION / TRAFIC =====

def get_occupation_data():
    return run_query(f"""
        SELECT
            DATE_JOUR, TRANCHE_HORAIRE, PARKING_HOUSE_NUM, PARKING_HOUSE_NAME,
            NB_ENTREES, NB_SORTIES, VARIATION_OCCUPATION, NB_EVENEMENTS_TOTAL
        FROM {SCHEMA_GOLD}.KPI_OCCUPATION_HORAIRE
        ORDER BY DATE_JOUR DESC, TRANCHE_HORAIRE
    """, ttl=300)


def get_trafic_summary():
    return run_query(f"""
        SELECT
            PARKING_HOUSE_NAME, PARKING_HOUSE_NUM,
            COUNT(*) AS NB_MOUVEMENTS,
            COUNT(CASE WHEN EVENT_TYPE = 187 THEN 1 END) AS TOTAL_ENTREES,
            COUNT(CASE WHEN EVENT_TYPE = 186 THEN 1 END) AS TOTAL_SORTIES,
            MIN(EVENT_TIME) AS PREMIERE_ACTIVITE,
            MAX(EVENT_TIME) AS DERNIERE_ACTIVITE
        FROM {SCHEMA_GOLD}.FCT_TRAFIC
        WHERE EVENT_TYPE IN (186, 187)
        GROUP BY PARKING_HOUSE_NAME, PARKING_HOUSE_NUM
        ORDER BY NB_MOUVEMENTS DESC
    """, ttl=300)
