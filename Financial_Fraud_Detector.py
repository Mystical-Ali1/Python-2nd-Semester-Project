import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Transaction Scanner", layout="wide")
st.title("💳 Smart Transaction Scanner")

uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # === Preprocessing ===
    df['Amount'] = df['Amount'].astype(float)
    df['Time'] = pd.to_timedelta(df['Time'], unit='s')
    df['Hour'] = df['Time'].dt.components.hours
    df.fillna(0, inplace=True)

    # === Fraud Detection ===
    def detect_fraud(row):
        if row['Amount'] > 2000:
            return 1
        if row['Hour'] < 6 or row['Hour'] > 22:
            return 1
        return 0

    df['Fraud_Risk'] = df.apply(detect_fraud, axis=1)

    # === Dashboard Outputs ===
    st.subheader("📊 Overview")
    st.write(df.head())

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Amount Distribution")
        fig, ax = plt.subplots()
        ax.hist(df['Amount'], bins=50, color='skyblue')
        ax.set_xlabel("Amount")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col2:
        st.subheader("Transactions by Hour")
        fig, ax = plt.subplots()
        df['Hour'].value_counts().sort_index().plot(kind='bar', color='orange', ax=ax)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Count")
        st.pyplot(fig)

    st.subheader("🚨 Fraud Risk Summary")
    fig, ax = plt.subplots()
    df['Fraud_Risk'].value_counts().plot(kind='bar', color=['green', 'red'], ax=ax)
    ax.set_xticklabels(['Not Fraud', 'Potential Fraud'], rotation=0)
    ax.set_ylabel("Transaction Count")
    st.pyplot(fig)

    # === Export Labeled File ===
    st.download_button("Download Labeled CSV", df.to_csv(index=False), "labeled_transactions.csv", "text/csv")
