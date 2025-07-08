import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="SKU Priority Highlighter", layout="wide")
st.title(" SKU Priority Highlighter (Dot Matrix Compatible)")

# Load master priority list (must be in same GitHub repo for Streamlit Cloud)
priority_df = pd.read_excel("Final Priority List.xlsx")
priority_df.iloc[:, 0] = priority_df.iloc[:, 0].astype(str).str.strip()
priority_skus = set(priority_df.iloc[:, 0])

# File uploader for indent
uploaded_file = st.file_uploader("Upload Loading Indent Excel", type=["xlsx"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Clean up Material column
        df["Material"] = df["Material"].astype(str).str.strip()

        # Add marker column for priority SKUs
        df["Priority"] = df["Material"].apply(lambda x: "***" if x in priority_skus else "")

        # Save to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Prioritized Indent")

        # Offer for download
        st.success(" File processed. Priority SKUs marked with ***")
        st.download_button(
            label=" Download Indent (Dot Matrix Compatible)",
            data=output.getvalue(),
            file_name="Prioritized_Indent_DotMatrix.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f" Error processing file: {e}")
