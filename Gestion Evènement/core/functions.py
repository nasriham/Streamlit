"""Fonctions métier : recherche, logging, user."""

import streamlit as st
import pandas as pd

from core.db import run_query
from core.queries import insert_snapshot


def get_current_user() -> str:
    """Get the real connected Snowflake user (not the service account)."""
    try:
        user = st.context.headers.get("Sf-Context-Current-User", None)
        if user:
            return user
    except Exception:
        pass
    try:
        if hasattr(st, "user") and st.user.user_name:
            return st.user.user_name
    except Exception:
        pass
    df = run_query("SELECT CURRENT_USER() AS USERNAME")
    return df.iloc[0]["USERNAME"]


def search_evenements(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Filter events by search term across multiple columns."""
    if not search_term:
        return df
    term = search_term.lower()
    mask = df["TITRE_EVENEMENT"].str.lower().str.contains(term, na=False)
    mask = mask | df["CODE_EVENEMENT"].astype(str).str.contains(term, na=False)
    for col in ["TYPE_EVENEMENT", "CATEGORIE", "DESCRIPTION", "LIEU", "VILLE", "IMPACT"]:
        if col in df.columns:
            mask = mask | df[col].str.lower().str.contains(term, na=False)
    return df[mask]


def log_modification(code_evt: int, action: str, user: str):
    """Log a full snapshot of the event in history."""
    insert_snapshot(code_evt, action, user)


def show_notification():
    """Display pending notification if any."""
    if "notification" in st.session_state:
        notif = st.session_state.pop("notification")
        if notif["type"] == "success":
            st.success(notif["message"])
        elif notif["type"] == "error":
            st.error(notif["message"])
        elif notif["type"] == "warning":
            st.warning(notif["message"])


def notify(message: str, notif_type: str = "success"):
    """Set a notification to be displayed after rerun."""
    st.session_state["notification"] = {"type": notif_type, "message": message}
