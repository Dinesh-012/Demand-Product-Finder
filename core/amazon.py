"""
Amazon.in Bestsellers scraper (MVP version)
Scrapes top products from major category Best Sellers pages.
"""

import time
import pandas as pd
from typing import List, Dict
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
# from playwright_stealth import stealth_sync

# Amazon Best Sellers category URLs (India)
CATEGORY_URLS = {
    "Electronics": "https://www.amazon.in/gp/bestsellers/electronics",
    "Home & Kitchen Appliances": "https://www.amazon.in/gp/bestsellers/kitchen",
    "Beauty Products": "https://www.amazon.in/gp/bestsellers/beauty",
}


def scrape_bestsellers(category: str, max_products: int = 12) -> pd.DataFrame:
    if category not in CATEGORY_URLS:
        raise ValueError(f"Unknown category: {category}")

    url = CATEGORY_URLS[category]
    products = []
    seen_titles = set()

    print(f"\nScraping Amazon Bestsellers → {category}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        try:
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            time.sleep(4)

            items = page.query_selector_all("div.zg-grid-general-faceout, div#gridItemRoot")

            for i, item in enumerate(items):
                if len(products) >= max_products:
                    break
                try:
                    title_el = item.query_selector("div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1, a.a-link-normal span div")
                    title = title_el.inner_text().strip() if title_el else "N/A"

                    if title in seen_titles or title == "N/A":
                        continue
                    seen_titles.add(title)

                    price_el = item.query_selector("span._cDEzb_p13n-sc-price_3mJ9Z, span.p13n-sc-price")
                    price = price_el.inner_text().strip() if price_el else "N/A"

                    rating_el = item.query_selector("span.a-icon-alt")
                    rating = rating_el.inner_text().split()[0] if rating_el else "N/A"

                    products.append({
                        "rank": len(products) + 1,
                        "title": title[:120],
                        "price": price,
                        "rating": rating,
                        "category": category
                    })
                except Exception:
                    continue

        except Exception as e:
            print(f"Error while scraping {category}: {e}")
        finally:
            browser.close()

    df = pd.DataFrame(products)
    print(f"  Collected {len(df)} unique products")
    return df


def scrape_all_categories(categories: List[str] = None) -> Dict[str, pd.DataFrame]:
    if categories is None:
        categories = list(CATEGORY_URLS.keys())

    result = {}
    for cat in categories:
        result[cat] = scrape_bestsellers(cat)
        time.sleep(2)
    return result


if __name__ == "__main__":
    print("Testing Amazon Bestsellers scraper...")
    df = scrape_bestsellers("Electronics", max_products=8)
    print("\nResult:")
    if not df.empty:
        print(df[["rank", "title", "price", "rating"]].to_string(index=False))
    else:
        print("No products collected. Amazon may be blocking. We will handle fallback next.")