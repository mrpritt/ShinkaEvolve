import pandas as pd
import json
from typing import List, Tuple


def split_df_by_category(df: pd.DataFrame) -> Tuple[List[pd.DataFrame], List[str]]:
    """
    Splits the main evolution DataFrame into an 'Overall' DataFrame
    plus individual DataFrames for each Archipelago paradigm.
    """
    extracted_categories = []

    # Bulletproof extraction: check all possible locations
    for _, row in df.iterrows():
        cat = "Any/free"

        # 1. Direct 'category' column from DB schema
        if "category" in df.columns and pd.notna(row["category"]):
            cat = row["category"]
        # 2. Flattened 'target_category' column (from load_programs_to_df json normalization)
        elif "target_category" in df.columns and pd.notna(row["target_category"]):
            cat = row["target_category"]
        # 3. Unflattened 'metadata' column
        elif "metadata" in df.columns:
            meta = row["metadata"]
            if isinstance(meta, str):
                try:
                    meta_dict = json.loads(meta)
                    if isinstance(meta_dict, dict):
                        cat = meta_dict.get("target_category", "Any/free")
                except Exception:
                    pass
            elif isinstance(meta, dict):
                cat = meta.get("target_category", "Any/free")

        extracted_categories.append(cat)

    # Assign our safely resolved categories
    df["extracted_category"] = extracted_categories

    dfs = [df.copy()]
    labels = ["Overall (All Paradigms)"]

    # Get unique paradigms, filtering out the base 'Any/free'
    categories = df["extracted_category"].dropna().unique()

    for cat in categories:
        # VISUAL TRICK: Include Gen 0 in every paradigm's dataframe!
        # This ensures every line on the graph visually branches out from the root seed.
        cat_df = df[(df["extracted_category"] == cat) | (df["generation"] == 0)].copy()

        if not cat_df.empty:
            dfs.append(cat_df)
            labels.append(f"Paradigm: {cat}")

    # Ensure the 'category' column exists for the lineage tree filter
    df["category"] = df["extracted_category"]

    return dfs, labels
