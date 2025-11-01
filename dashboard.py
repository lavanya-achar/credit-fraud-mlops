import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ----------------------------------------
# 🌐 Page Configuration
# ----------------------------------------
st.set_page_config(page_title="Credit Fraud Detection Dashboard", layout="wide")

st.title("💳 Credit Fraud Detection Dashboard")
st.markdown("""
This dashboard helps visualize transaction patterns and detect potential frauds 
using an AI-powered backend API.
""")

# ----------------------------------------
# ⚙️ Sidebar - API URL
# ----------------------------------------
api_url = st.sidebar.text_input("🔗 Backend API URL", "http://127.0.0.1:8000/predict")

# ----------------------------------------
# 📂 File Upload
# ----------------------------------------
uploaded_file = st.file_uploader("📂 Upload Transaction Data (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### 📊 Uploaded Dataset Preview", df.head())

    # ----------------------------------------
    # 🧠 Data Check
    # ----------------------------------------
    required_cols = ["Amount", "Time"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"❌ The dataset must include columns: {', '.join(required_cols)}")
    else:
        # ----------------------------------------
        # 📈 Exploratory Insights
        # ----------------------------------------
        st.write("### 🔍 Exploratory Insights")
        col1, col2 = st.columns(2)

        # 🟩 Chart 1 – Average Transaction Amount by Category
        with col1:
            if "Class" in df.columns:
                df["Transaction Type"] = df["Class"].map({0: "Legitimate", 1: "Fraudulent"})
                avg_amount = df.groupby("Transaction Type")["Amount"].mean().reset_index()

                fig1 = px.bar(
                    avg_amount,
                    x="Transaction Type",
                    y="Amount",
                    color="Transaction Type",
                    color_discrete_map={"Legitimate": "#00CC96", "Fraudulent": "#EF553B"},
                    text_auto=".2f",
                    title="💰 Average Transaction Amount by Category",
                )
                fig1.update_traces(texttemplate="₹%{y:,.2f}", textposition="outside")
                fig1.update_layout(
                    yaxis_title="Average Amount (₹)",
                    xaxis_title="Transaction Type",
                    showlegend=False
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.warning("⚠️ 'Class' column not found — skipping category-wise comparison.")

        # 🟦 Chart 2 – Transaction Amount Trend Over Time (by Hour of Day)
        with col2:
            if "Time" in df.columns:
                df["Hour of Day"] = (df["Time"] / 3600) % 24  # Convert seconds → hours
                hourly_trend = df.groupby("Hour of Day")["Amount"].sum().reset_index()

                fig2 = px.line(
                    hourly_trend,
                    x="Hour of Day",
                    y="Amount",
                    title="📈 Transaction Amount Trend by Hour of Day",
                    markers=True,
                    color_discrete_sequence=["#636EFA"]
                )
                fig2.update_layout(
                    xaxis_title="Hour of Day (0–24)",
                    yaxis_title="Total Transaction Amount (₹)",
                    xaxis=dict(tickmode='linear', tick0=0, dtick=2)
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("⚠️ 'Time' column not found — skipping time trend chart.")

        # ----------------------------------------
        # 🚀 Fraud Prediction Section
        # ----------------------------------------
        st.markdown("---")
        st.write("## 🔍 Fraud Detection")

        if st.button("🚀 Predict Fraudulent Transactions"):
            try:
                # Drop 'Class' column before prediction if it exists
                if "Class" in df.columns:
                    df = df.drop("Class", axis=1)

                # ✅ Keep only the first 30 columns (as model was trained on 30 features)
                df = df.iloc[:, :30]

                # Prepare data for backend
                records = [{"features": row.tolist()} for _, row in df.iterrows()]
                response = requests.post(api_url, json=records)

                # Handle API Response
                if response.status_code == 200:
                    preds = response.json().get("predictions", [])
                    if preds:
                        df["Prediction"] = preds
                        df["Prediction Label"] = df["Prediction"].map({0: "Legitimate", 1: "Fraudulent"})

                        st.success("✅ Prediction Complete!")
                        st.write("### 🧾 Prediction Results")
                        st.dataframe(df)

                        # 🥧 Visualization – Fraud vs Non-Fraud
                        fraud_count = df["Prediction Label"].value_counts().reset_index()
                        fraud_count.columns = ["Prediction", "Count"]

                        pie = px.pie(
                            fraud_count,
                            names="Prediction",
                            values="Count",
                            title="🧭 Predicted Fraud vs Legitimate Transactions",
                            color_discrete_sequence=["#00CC96", "#EF553B"]
                        )
                        st.plotly_chart(pie, use_container_width=True)

                        # 📥 Download Predictions
                        st.download_button(
                            label="📥 Download Predictions as CSV",
                            data=df.to_csv(index=False).encode("utf-8"),
                            file_name="fraud_predictions.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ No predictions returned from API.")
                else:
                    st.error(f"❌ API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

else:
    st.info("⬆️ Please upload a CSV file to begin analysis.")
