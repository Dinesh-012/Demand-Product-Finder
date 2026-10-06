"""
Simple demand scoring: combines Google Trends interest + Amazon Best Sellers rank.
"""

import pandas as pd
from typing import Dict


def calculate_demand_score(trends_df: pd.DataFrame, amazon_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a combined view.
    For demo we show Trends scores side-by-side with Amazon top products.
    """
    # Trends summary (average interest per state)
    trends_summary = trends_df.set_index("keyword")

    # Amazon products
    amazon_clean = amazon_df.copy()
    amazon_clean["demand_note"] = amazon_clean["rank"].apply(
        lambda r: "High (Top 5)" if r <= 5 else "Medium" if r <= 10 else "Lower"
    )

    return amazon_clean, trends_summary


def print_combined_report(category: str, trends_df: pd.DataFrame, amazon_df: pd.DataFrame):
    print(f"\n{'='*60}")
    print(f"DEMAND REPORT → {category}")
    print(f"{'='*60}")

    print("\n Google Trends Interest (Sample data for demo)")
    print(trends_df.to_string(index=False))

    print("\n Amazon Best Sellers (Live scraped)")
    if not amazon_df.empty:
        print(amazon_df[["rank", "title", "price", "rating"]].to_string(index=False))
    else:
        print("No Amazon data")