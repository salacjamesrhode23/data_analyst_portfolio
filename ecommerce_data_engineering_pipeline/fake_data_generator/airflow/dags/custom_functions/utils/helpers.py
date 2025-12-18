import random
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

# -----------------------------
# Helper Functions
# -----------------------------
def random_number() -> str:
    """Return a random 12-digit order or payment number."""
    return f"#{random.randint(100_000_000_000, 999_999_999_999)}"


def normalize_columns(data: Dict[str, Any], exclude: Optional[List[str]] = None) -> Dict[str, Any]:
    """Return a dictionary excluding specified keys."""
    if exclude is None:
        exclude = []
    return {k: v for k, v in data.items() if k not in exclude}


def dataframe_to_lookup(df: pd.DataFrame, key_col: str) -> Dict[Any, Dict[str, Any]]:
    """Convert a DataFrame to a lookup dict using one column as key."""
    return {
        row[key_col]: normalize_columns(row.to_dict(), exclude=[key_col])
        for _, row in df.iterrows()
    }
