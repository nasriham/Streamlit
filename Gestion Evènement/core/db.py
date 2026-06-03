import streamlit as st

# -- Snowflake connection singleton --
conn = st.connection("snowflake")


def get_session():
    """Get Snowpark session."""
    return conn.session()


# -- Détection dynamique de l'environnement --
session = get_session()
current_db = session.get_current_database()

if "DEV" in current_db:
    ENV = "DEV"
elif "QUA" in current_db:
    ENV = "QUA"
elif "PPD" in current_db:
    ENV = "PPD"
else:
    ENV = "PROD"

# Schema dynamique selon l'environnement
SCHEMA = f"{current_db}.S_REFERENTIEL"


def run_dml(query: str):
    """Execute DML (INSERT/UPDATE/DELETE) via Snowpark session."""
    session.sql(query).collect()


def run_query(query: str, ttl: int = 0):
    """Execute SELECT query and return DataFrame."""
    return conn.query(query, ttl=ttl)
