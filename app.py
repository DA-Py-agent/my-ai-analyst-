import streamlit as st
import pandas as pd
import google.generativeai as genai

# Setup
st.set_page_config(page_title="AI Data Analyst (Multi-Format)", layout="wide")
st.title("📊 AI Data Analyst")
st.subheader("I can read CSV and Excel files!")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Paste your Google API Key:", type="password")

# 1. Flexible File Uploader (Accepts CSV and Excel)
uploaded_file = st.file_uploader("Upload your data file (CSV or Excel)", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 2. Check the file extension and read accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # This handles .xlsx and .xls files
            df = pd.read_excel(uploaded_file)

        st.write("### Data Preview:", df.head())
        user_question = st.text_input("Ask a question about this data:")

        if st.button("Analyze"):
            if not api_key:
                st.error("Please enter your API Key in the sidebar!")
            else:
                try:
                    # 3. Configure AI (Using transport='rest' for stability)
                    genai.configure(api_key=api_key, transport='rest')
                    
                    # Using Gemini 1.5 Flash
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    # Create data context for the AI
                    data_summary = f"Columns: {list(df.columns)}. Data Sample:\n{df.head().to_string()}"
                    prompt = f"You are a data analyst. Data: {data_summary}\n\nQuestion: {user_question}"

                    with st.spinner("Analyzing your data..."):
                        response = model.generate_content(prompt)
                        st.success(response.text)

                except Exception as e:
                    st.error(f"AI Error: {e}")
    
    except Exception as e:
        st.error(f"File Loading Error: {e}. Make sure the file isn't corrupted.")

else:
    st.info("Waiting for a CSV or Excel file...")
