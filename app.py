import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI Data Analyst Dashboard")

# Sidebar for API Key
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    st.info("Get a free key at: aistudio.google.com")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # File Uploader
    uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=['csv', 'xlsx'])

    if uploaded_file:
        # Load Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Data Loaded Successfully!")
        
        # Show Data Preview (Power BI Style)
        with st.expander("👁️ View Raw Data"):
            st.dataframe(df.head())

        # Chat Interface
        st.subheader("🤖 Ask your Data a Question")
        user_question = st.text_input("e.g., Summarize this data or Ask for a specific chart")

        if user_question:
            # Simple AI prompt to analyze data columns
            prompt = f"Here are the columns in my dataset: {list(df.columns)}. My question is: {user_question}. Please provide a helpful summary or analysis."
            response = model.generate_content(prompt)
            st.write("### AI Insight:")
            st.write(response.text)

            # Auto-Visualization Logic (Basic)
            st.subheader("📈 Visual Analysis")
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 1:
                fig = px.bar(df, x=df.columns[0], y=numeric_cols[0], title="Automatic Insight Chart")
                st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")
