"""
Google Trends collector for Tamil Nadu, Kerala, Karnataka.

NOTE (Deadline mode):
Real Google Trends scraping is currently blocked in headless mode.
This module returns realistic sample data so the full pipeline
(scoring + dashboard) can be demonstrated to recruiters.
The structure is ready for a real scraper later.
"""

import pandas as pd
from typing import List, Dict

STATE_GEO = {
    "Tamil Nadu": "IN-TN",
    "Kerala": "IN-KL",
    "Karnataka": "IN-KA",
}

CATEGORY_KEYWORDS = {
    "Electronics": ["smartphone", "laptop", "wireless earbuds", "smartwatch"],
    "Home & Kitchen Appliances": ["air cooler", "mixer grinder", "induction cooktop", "refrigerator"],
    "Beauty Products": ["face serum", "sunscreen", "hair oil", "lipstick"],
}

# Realistic sample data (based on typical South India patterns)
SAMPLE_DATA = {
    "Electronics": {
        "smartphone": {"Tamil Nadu": 92, "Kerala": 78, "Karnataka": 88},
        "laptop": {"Tamil Nadu": 85, "Kerala": 70, "Karnataka": 95},
        "wireless earbuds": {"Tamil Nadu": 88, "Kerala": 82, "Karnataka": 90},
        "smartwatch": {"Tamil Nadu": 75, "Kerala": 68, "Karnataka": 80},
    },
    "Home & Kitchen Appliances": {
        "air cooler": {"Tamil Nadu": 95, "Kerala": 60, "Karnataka": 85},
        "mixer grinder": {"Tamil Nadu": 90, "Kerala": 88, "Karnataka": 82},
        "induction cooktop": {"Tamil Nadu": 80, "Kerala": 75, "Karnataka": 70},
        "refrigerator": {"Tamil Nadu": 78, "Kerala": 72, "Karnataka": 85},
    },
    "Beauty Products": {
        "face serum": {"Tamil Nadu": 88, "Kerala": 85, "Karnataka": 90},
        "sunscreen": {"Tamil Nadu": 92, "Kerala": 90, "Karnataka": 88},
        "hair oil": {"Tamil Nadu": 95, "Kerala": 93, "Karnataka": 80},
        "lipstick": {"Tamil Nadu": 70, "Kerala": 75, "Karnataka": 82},
    },
}


def collect_category_trends(category: str) -> pd.DataFrame:
    if category not in SAMPLE_DATA:
        raise ValueError(f"Unknown category: {category}")

    rows = []
    for keyword, scores in SAMPLE_DATA[category].items():
        row = {"keyword": keyword, **scores}
        rows.append(row)

    return pd.DataFrame(rows)


def collect_all_trends(categories: List[str] = None) -> Dict[str, pd.DataFrame]:
    if categories is None:
        categories = list(SAMPLE_DATA.keys())

    return {cat: collect_category_trends(cat) for cat in categories}


if __name__ == "__main__":
    print("Google Trends collector (Demo / Sample data mode)")
    print("=" * 50)
    for cat in SAMPLE_DATA:
        print(f"\nCategory: {cat}")
        df = collect_category_trends(cat)
        print(df.to_string(index=False))