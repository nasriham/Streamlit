import math
import pandas as pd

def clean_value(x, dtype="str"):
    # NULL universel
    if x is None:
        return None

    # pandas NA
    if pd.isna(x):
        return None

    # float NaN
    if isinstance(x, float) and math.isnan(x):
        return None

    # string dirty values
    if isinstance(x, str) and x.strip().lower() in ["", "none", "nan"]:
        return None

    # cast numeric
    if dtype == "number":
        try:
            val = float(x)
            if math.isnan(val):
                return None
            return x
        except:
            return None

    if dtype == "int":
        try:
            return int(float(x))
        except:
            return None

    if dtype == "str":
        return str(x)

    return x

def normalize(v):
    if pd.isna(v):
        return None
    return v

def has_changed(old, new):
    old_dict = old.to_dict()
    new_dict = new.to_dict()

    for col in old_dict:
        if col in [
            "DATE_CREATION", "DATE_MODIFICATION",
            "DATE_DEBUT", "DATE_FIN",
            "IS_ACTIVE", "NOM_CREATEUR", "NOM_MODIFICATEUR"
        ]:
            continue

        if normalize(old_dict[col]) != normalize(new_dict[col]):
            return True

    return False