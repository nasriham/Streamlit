"""Toutes les requêtes SQL centralisées."""

from core.db import run_query, run_dml, SCHEMA


# ===== EVENEMENTS =====

def get_evenements():
    return run_query(f"""
        SELECT
            e.CODE_EVENEMENT,
            e.TITRE_EVENEMENT,
            e.CODE_TYPE_EVENEMENT,
            t.LIBELLE_TYPE_EVENEMENT AS TYPE_EVENEMENT,
            t.CATEGORIE,
            e.CODE_DESCRIPTION,
            COALESCE(d.LIBELLE_DESCRIPTION, e.DESCRIPTION_AUTRE) AS DESCRIPTION,
            e.CODE_LIEU,
            l.LIBELLE_LIEU AS LIEU,
            l.VILLE,
            e.CODE_IMPACT,
            i.LIBELLE_IMPACT AS IMPACT,
            i.NIVEAU_SEVERITE,
            e.DATE_DEBUT,
            e.DATE_FIN,
            e.IS_JOURNEE_PARTIELLE,
            e.CRENEAU,
            e.IS_PLACES_IMPACTEES,
            e.NB_PLACES_IMPACTEES,
            e.FERMETURE_TOTALE,
            e.IS_PISTES_IMPACTEES,
            e.NB_PISTES_ENTREE_FERMEES,
            e.NB_PISTES_SORTIE_FERMEES,
            e.TYPE_TRAVAUX,
            e.CONTACT_INTERNE,
            e.CONTACT_EXTERNE,
            e.IS_TRAVAUX_PHASES,
            e.COMMENTAIRE,
            e.NOM_CREATEUR,
            e.NOM_MODIFICATEUR,
            e.DATE_CREATION,
            e.DATE_MODIFICATION
        FROM {SCHEMA}.T_BASE_EVENEMENT e
        LEFT JOIN {SCHEMA}.T_TYPE_EVENEMENT t ON e.CODE_TYPE_EVENEMENT = t.CODE_TYPE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_DESCRIPTION_EVENEMENT d ON e.CODE_DESCRIPTION = d.CODE_DESCRIPTION
        LEFT JOIN {SCHEMA}.T_LIEU_EVENEMENT l ON e.CODE_LIEU = l.CODE_LIEU
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.IS_ACTIVE = TRUE
        ORDER BY e.DATE_DEBUT DESC
    """)


def get_ref_types():
    return run_query(
        f"SELECT CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX FROM {SCHEMA}.T_TYPE_EVENEMENT WHERE IS_ACTIVE = TRUE ORDER BY CATEGORIE, LIBELLE_TYPE_EVENEMENT",
        ttl=60
    )


def insert_type_evenement(libelle: str, categorie: str, is_travaux: bool = False):
    """Insert a new event type and return its code."""
    libelle_sql = libelle.replace("'", "''")
    run_dml(f"""
        INSERT INTO {SCHEMA}.T_TYPE_EVENEMENT (CODE_TYPE_EVENEMENT, LIBELLE_TYPE_EVENEMENT, CATEGORIE, IS_TRAVAUX, IS_ACTIVE)
        SELECT COALESCE(MAX(CODE_TYPE_EVENEMENT), 0) + 1, '{libelle_sql}', '{categorie}', {is_travaux}, TRUE
        FROM {SCHEMA}.T_TYPE_EVENEMENT
    """)
    df = run_query(f"SELECT MAX(CODE_TYPE_EVENEMENT) AS CODE FROM {SCHEMA}.T_TYPE_EVENEMENT WHERE LIBELLE_TYPE_EVENEMENT = '{libelle_sql}'")
    return int(df.iloc[0]["CODE"])


def get_ref_descriptions(code_type: int = None):
    where = f"WHERE IS_ACTIVE = TRUE AND CODE_TYPE_EVENEMENT = {code_type}" if code_type else "WHERE IS_ACTIVE = TRUE"
    return run_query(
        f"SELECT CODE_DESCRIPTION, LIBELLE_DESCRIPTION, CODE_TYPE_EVENEMENT FROM {SCHEMA}.T_DESCRIPTION_EVENEMENT {where} ORDER BY LIBELLE_DESCRIPTION",
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
        SELECT CODE_PARC, NOM_PARC, CAPACITE, NB_PISTES_ENTREE, NB_PISTES_SORTIE
        FROM {SCHEMA}.T_PARKING
        WHERE IS_ACTIVE = TRUE
        ORDER BY NOM_PARC
    """, ttl=60)


def get_parcs_evenement(code_evt: int):
    return run_query(f"SELECT CODE_PARC, NOM_PARC FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}")


def get_max_code_evenement():
    df = run_query(f"SELECT COALESCE(MAX(CODE_EVENEMENT), 0) AS CODE FROM {SCHEMA}.T_BASE_EVENEMENT")
    return int(df.iloc[0]["CODE"])


# ===== PHASES DE TRAVAUX =====

def get_phases_travaux(code_evt: int):
    return run_query(f"""
        SELECT CODE_PHASE, NUMERO_PHASE, DATE_DEBUT, DATE_FIN, NB_PLACES_IMPACTEES, COMMENTAIRE
        FROM {SCHEMA}.T_PHASE_TRAVAUX
        WHERE CODE_EVENEMENT = {code_evt}
        ORDER BY NUMERO_PHASE
    """)


def insert_phase_travaux(code_evt: int, numero: int, date_debut: str, date_fin: str, nb_places: int, commentaire: str):
    commentaire_sql = commentaire.replace("'", "''") if commentaire else ""
    run_dml(f"""
        INSERT INTO {SCHEMA}.T_PHASE_TRAVAUX
        (CODE_EVENEMENT, NUMERO_PHASE, DATE_DEBUT, DATE_FIN, NB_PLACES_IMPACTEES, COMMENTAIRE)
        VALUES ({code_evt}, {numero}, '{date_debut}', '{date_fin}', {nb_places if nb_places else 'NULL'}, '{commentaire_sql}')
    """)


def delete_phases_travaux(code_evt: int):
    run_dml(f"DELETE FROM {SCHEMA}.T_PHASE_TRAVAUX WHERE CODE_EVENEMENT = {code_evt}")


# ===== CRUD EVENEMENTS =====

def insert_evenement(titre, code_type, code_description, description_autre, code_lieu, code_impact,
                     timestamp_debut, timestamp_fin_sql, is_journee_partielle, creneau,
                     is_places_impactees, nb_places_impactees, fermeture_totale,
                     is_pistes_impactees, nb_pistes_entree, nb_pistes_sortie,
                     type_travaux, contact_interne, contact_externe, is_travaux_phases,
                     commentaire, user):
    titre_sql = titre.replace("'", "''")
    commentaire_sql = commentaire.replace("'", "''") if commentaire else ""
    description_autre_sql = f"'{description_autre.replace(chr(39), chr(39)+chr(39))}'" if description_autre else "NULL"
    code_desc_sql = code_description if code_description else "NULL"
    code_lieu_sql = code_lieu if code_lieu else "NULL"
    code_impact_sql = code_impact if code_impact else "NULL"
    creneau_sql = f"'{creneau}'" if creneau else "NULL"
    type_travaux_sql = f"'{type_travaux}'" if type_travaux else "NULL"
    contact_interne_sql = f"'{contact_interne.replace(chr(39), chr(39)+chr(39))}'" if contact_interne else "NULL"
    contact_externe_sql = f"'{contact_externe.replace(chr(39), chr(39)+chr(39))}'" if contact_externe else "NULL"

    run_dml(f"""
        INSERT INTO {SCHEMA}.T_BASE_EVENEMENT
        (CODE_EVENEMENT, TITRE_EVENEMENT, CODE_TYPE_EVENEMENT, CODE_DESCRIPTION, DESCRIPTION_AUTRE,
         CODE_LIEU, CODE_IMPACT, DATE_DEBUT, DATE_FIN,
         IS_JOURNEE_PARTIELLE, CRENEAU,
         IS_PLACES_IMPACTEES, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
         IS_PISTES_IMPACTEES, NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
         TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
         COMMENTAIRE, NOM_CREATEUR, DATE_CREATION, IS_ACTIVE)
        VALUES (
            {SCHEMA}.SEQ_EVENEMENT.NEXTVAL,
            '{titre_sql}',
            {code_type},
            {code_desc_sql},
            {description_autre_sql},
            {code_lieu_sql},
            {code_impact_sql},
            '{timestamp_debut}',
            {timestamp_fin_sql},
            {is_journee_partielle},
            {creneau_sql},
            {is_places_impactees},
            {nb_places_impactees if nb_places_impactees else 'NULL'},
            {fermeture_totale},
            {is_pistes_impactees},
            {nb_pistes_entree if nb_pistes_entree else 'NULL'},
            {nb_pistes_sortie if nb_pistes_sortie else 'NULL'},
            {type_travaux_sql},
            {contact_interne_sql},
            {contact_externe_sql},
            {is_travaux_phases},
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
    run_dml(f"DELETE FROM {SCHEMA}.T_PHASE_TRAVAUX WHERE CODE_EVENEMENT = {code_evt}")


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
        SELECT CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE, DESCRIPTION,
               LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
               IS_JOURNEE_PARTIELLE, CRENEAU, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
               NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
               TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
               COMMENTAIRE, PARKINGS_IMPACTES, IS_ACTIVE, MODIFIE_PAR, ACTION,
               DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE
        FROM {SCHEMA}.T_HISTORIQUE_EVENEMENT
        {where_clause}
        ORDER BY DATE_DEBUT_VALIDITE DESC
    """)


def get_historique_complet():
    return run_query(f"""
        SELECT CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE, DESCRIPTION,
               LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
               IS_JOURNEE_PARTIELLE, CRENEAU, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
               NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
               TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
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
        (CODE_EVENEMENT, TITRE_EVENEMENT, TYPE_EVENEMENT, CATEGORIE, DESCRIPTION,
         LIEU, VILLE, IMPACT, NIVEAU_SEVERITE, DATE_DEBUT, DATE_FIN,
         IS_JOURNEE_PARTIELLE, CRENEAU, NB_PLACES_IMPACTEES, FERMETURE_TOTALE,
         NB_PISTES_ENTREE_FERMEES, NB_PISTES_SORTIE_FERMEES,
         TYPE_TRAVAUX, CONTACT_INTERNE, CONTACT_EXTERNE, IS_TRAVAUX_PHASES,
         COMMENTAIRE, PARKINGS_IMPACTES,
         IS_ACTIVE, MODIFIE_PAR, ACTION, DATE_DEBUT_VALIDITE, DATE_FIN_VALIDITE)
        SELECT
            e.CODE_EVENEMENT,
            e.TITRE_EVENEMENT,
            t.LIBELLE_TYPE_EVENEMENT,
            t.CATEGORIE,
            COALESCE(d.LIBELLE_DESCRIPTION, e.DESCRIPTION_AUTRE),
            l.LIBELLE_LIEU,
            l.VILLE,
            i.LIBELLE_IMPACT,
            i.NIVEAU_SEVERITE,
            e.DATE_DEBUT,
            e.DATE_FIN,
            e.IS_JOURNEE_PARTIELLE,
            e.CRENEAU,
            e.NB_PLACES_IMPACTEES,
            e.FERMETURE_TOTALE,
            e.NB_PISTES_ENTREE_FERMEES,
            e.NB_PISTES_SORTIE_FERMEES,
            e.TYPE_TRAVAUX,
            e.CONTACT_INTERNE,
            e.CONTACT_EXTERNE,
            e.IS_TRAVAUX_PHASES,
            e.COMMENTAIRE,
            (SELECT LISTAGG(NOM_PARC, ', ') FROM {SCHEMA}.T_EVENEMENT_PARC WHERE CODE_EVENEMENT = {code_evt}),
            CASE WHEN e.IS_ACTIVE = TRUE THEN 1 ELSE 0 END,
            '{user}',
            '{action}',
            CURRENT_TIMESTAMP(),
            NULL
        FROM {SCHEMA}.T_BASE_EVENEMENT e
        LEFT JOIN {SCHEMA}.T_TYPE_EVENEMENT t ON e.CODE_TYPE_EVENEMENT = t.CODE_TYPE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_DESCRIPTION_EVENEMENT d ON e.CODE_DESCRIPTION = d.CODE_DESCRIPTION
        LEFT JOIN {SCHEMA}.T_LIEU_EVENEMENT l ON e.CODE_LIEU = l.CODE_LIEU
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.CODE_EVENEMENT = {code_evt}
    """)


def close_all_snapshots(code_evt: int):
    """Close all open snapshots for a deleted event."""
    run_dml(f"""
        UPDATE {SCHEMA}.T_HISTORIQUE_EVENEMENT
        SET DATE_FIN_VALIDITE = CURRENT_TIMESTAMP()
        WHERE CODE_EVENEMENT = {code_evt} AND DATE_FIN_VALIDITE IS NULL
    """)


# ===== OCCUPATION / IMPACT PAR PARKING =====

def get_evenements_par_parking():
    """Get events grouped by impacted parking with places info."""
    return run_query(f"""
        SELECT
            ep.NOM_PARC AS PARKING,
            ep.CODE_PARC,
            p.CAPACITE,
            e.CODE_EVENEMENT,
            e.TITRE_EVENEMENT,
            t.LIBELLE_TYPE_EVENEMENT AS TYPE_EVENEMENT,
            t.CATEGORIE,
            i.LIBELLE_IMPACT AS IMPACT,
            i.NIVEAU_SEVERITE,
            e.DATE_DEBUT,
            e.DATE_FIN,
            e.NB_PLACES_IMPACTEES,
            e.FERMETURE_TOTALE,
            e.IS_ACTIVE
        FROM {SCHEMA}.T_EVENEMENT_PARC ep
        JOIN {SCHEMA}.T_BASE_EVENEMENT e ON ep.CODE_EVENEMENT = e.CODE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_PARKING p ON ep.CODE_PARC = p.CODE_PARC
        LEFT JOIN {SCHEMA}.T_TYPE_EVENEMENT t ON e.CODE_TYPE_EVENEMENT = t.CODE_TYPE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.IS_ACTIVE = TRUE
        ORDER BY ep.NOM_PARC, e.DATE_DEBUT DESC
    """)


def get_stats_par_parking():
    """Get event count, max severity, and places impact per parking."""
    return run_query(f"""
        SELECT
            ep.NOM_PARC AS PARKING,
            p.CAPACITE,
            COUNT(DISTINCT ep.CODE_EVENEMENT) AS NB_EVENEMENTS,
            MAX(i.NIVEAU_SEVERITE) AS SEVERITE_MAX,
            SUM(CASE WHEN e.FERMETURE_TOTALE = TRUE THEN p.CAPACITE ELSE COALESCE(e.NB_PLACES_IMPACTEES, 0) END) AS TOTAL_PLACES_IMPACTEES,
            MIN(e.DATE_DEBUT) AS PREMIER_EVENEMENT,
            MAX(e.DATE_DEBUT) AS DERNIER_EVENEMENT
        FROM {SCHEMA}.T_EVENEMENT_PARC ep
        JOIN {SCHEMA}.T_BASE_EVENEMENT e ON ep.CODE_EVENEMENT = e.CODE_EVENEMENT
        LEFT JOIN {SCHEMA}.T_PARKING p ON ep.CODE_PARC = p.CODE_PARC
        LEFT JOIN {SCHEMA}.T_IMPACT_EVENEMENT i ON e.CODE_IMPACT = i.CODE_IMPACT
        WHERE e.IS_ACTIVE = TRUE
        GROUP BY ep.NOM_PARC, p.CAPACITE
        ORDER BY NB_EVENEMENTS DESC
    """)
