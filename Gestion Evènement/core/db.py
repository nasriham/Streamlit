import streamlit as st

# -- Snowflake connection singleton --
conn = st.connection("snowflake")

SCHEMA = "DB_REFERENTIEL_DEV.S_REFERENTIEL_EVENEMENT"


def run_dml(query: str):
    """Execute DML (INSERT/UPDATE/DELETE) via Snowpark session."""
    session = conn.session()
    session.sql(query).collect()


def run_query(query: str, ttl: int = 0):
    """Execute SELECT query and return DataFrame."""
    return conn.query(query, ttl=ttl)
