import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Enterprise Data Quality System", layout="wide")

st.title("📊 Enterprise Data Quality Monitoring System")

st.write("Upload a CSV file to analyze data quality.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Dataset Preview")
    st.dataframe(df.head())
    st.subheader("📊 Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Total Records", len(df))

    st.subheader("🔎 Data Quality Report")
    st.subheader("📊 Data Quality Report")

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    total_cells = df.size

    quality_score = 100 - ((missing_values + duplicate_rows) / total_cells * 100)

    st.write(f"Missing Values: {missing_values}")
    st.write(f"Duplicate Rows: {duplicate_rows}")
    st.write(f"Data Quality Score: {quality_score:.2f}%")

    st.progress(int(quality_score))
    if quality_score >= 90:
        st.success("✅ Excellent Data Quality")
    elif quality_score >= 70:
        st.warning("⚠️ Good Data Quality")
    else:
        st.error("❌ Poor Data Quality")


    # Missing Values
    missing = df.isnull().sum()

    # Duplicate Rows
    duplicates = df.duplicated().sum()

    # Outlier Detection (Numerical Columns)
    numeric_cols = df.select_dtypes(include=np.number)
    outliers = {}

    for col in numeric_cols.columns:
        Q1 = numeric_cols[col].quantile(0.25)
        Q3 = numeric_cols[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_count = numeric_cols[
            (numeric_cols[col] < (Q1 - 1.5 * IQR)) |
            (numeric_cols[col] > (Q3 + 1.5 * IQR))
        ].shape[0]
        outliers[col] = outlier_count

    # Quality Score
    total_cells = df.shape[0] * df.shape[1]
    total_missing = missing.sum()
    quality_score = round(100 - (total_missing / total_cells) * 100, 2)

    col1, col2, col3 = st.columns(3)

    col1.metric("Duplicate Records", duplicates)
    col2.metric("Total Missing Values", int(total_missing))
    col3.metric("Data Quality Score (%)", quality_score)

    report = pd.DataFrame({
        "Metric": [
            "Duplicate Records",
            "Missing Values",
            "Data Quality Score"],
        "Value": [
            duplicates,
            total_missing,
            quality_score
            ]
        })
    csv = report.to_csv(index=False)
    st.download_button(
        label="📥 Download Quality Report",
        data=csv,
        file_name="data_quality_report.csv",
        mime="text/csv")

    st.subheader("📋 Dataset Profile")
    profile_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Unique Values": [df[col].nunique() for col in df.columns]
        })
    st.dataframe(profile_df)

    st.subheader("📊 Missing Values by Column")
    missing_df = pd.DataFrame({
        "Column": missing.index,
        "Missing Values": missing.values
    })
    st.dataframe(missing_df)
    st.bar_chart(
        missing_df.set_index("Column")
    )



    st.subheader("📊 Outliers by Column")
    st.dataframe(pd.DataFrame(outliers.items(), columns=["Column", "Outlier Count"]))



