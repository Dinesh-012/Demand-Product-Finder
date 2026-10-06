"""
Streamlit Dashboard - AI Product Demand Finder
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add parent folder so we can import core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.trends import collect_category_trends, CATEGORY_KEYWORDS
from core.amazon import scrape_bestsellers

st.set_page_config(
    page_title="Demand Product Finder",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI Product Demand Finder")
st.markdown("**States:** Tamil Nadu  •  Kerala  •  Karnataka")
st.markdown("---")

# Sidebar
st.sidebar.header("Controls")
category = st.sidebar.selectbox(
    "Select Category",
    list(CATEGORY_KEYWORDS.keys())
)

show_amazon = st.sidebar.checkbox("Scrape live Amazon Best Sellers", value=True)
max_products = st.sidebar.slider("Amazon products to show", 5, 15, 8)

if st.sidebar.button("Run Analysis", type="primary"):
    with st.spinner("Collecting data..."):

        # 1. Google Trends (sample data for demo)
        trends_df = collect_category_trends(category)

        # 2. Amazon (live)
        amazon_df = pd.DataFrame()
        if show_amazon:
            try:
                amazon_df = scrape_bestsellers(category, max_products=max_products)
            except Exception as e:
                st.error(f"Amazon scraping failed: {e}")

    # Display Results
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Google Trends Interest (State-wise)")
        st.caption("Relative search interest across states (demo data)")
        st.dataframe(trends_df, use_container_width=True)

        # Simple bar chart
        if not trends_df.empty:
            chart_df = trends_df.set_index("keyword")
            st.bar_chart(chart_df)

    with col2:
        st.subheader("Amazon.in Best Sellers (Live)")
        if not amazon_df.empty:
            st.dataframe(
                amazon_df[["rank", "title", "price", "rating"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Amazon data not available")

    st.success("Analysis complete!")

else:
    st.info("← Select a category and click **Run Analysis**")
    st.markdown("""
    ### How it works
    1. **Google Trends** → Shows relative product interest in Tamil Nadu, Kerala & Karnataka
    2. **Amazon Best Sellers** → Live scrape of current top products in the category
    3. Combined view helps identify high-demand products in South India
    """)