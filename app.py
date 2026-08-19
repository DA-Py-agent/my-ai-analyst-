import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Setup Page
st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI Data Analyst (Final Version)")

# 2. Sidebar for API Key
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Paste your Google API Key (AQ...):", type="password")
    st.info("Make sure you enabled the 'Generative Language API' in Google Cloud.")

# 3. File Uploader
uploaded_file = st.file_uploader("Step 1: Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the data
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview:")
    st.dataframe(df.head()) 

    # 4. Question Input
    user_question = st.text_input("Step 2: Ask a question about your data")

    if st.button("Analyze"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar!")
        else:
            try:
                # Configure AI with the 'rest' transport (best for new AQ keys)
                genai.configure(api_key=api_key, transport='rest')
                
                # We use Gemini 1.5 Flash - it's fast and reliable
                model = genai.GenerativeModel('gemini-1.5-flash')

                # Prepare the data summary for the AI
                data_summary = f"The dataset has these columns: {list(df.columns)}. Here is a sample:\n{df.head().to_string()}"
                
                prompt = f"""
                You are a professional data analyst. 
                Data Details: {data_summary}
                User Question: '{user_question}'
                
                Answer the question clearly based on the data provided.
                """

                with st.spinner("Analyzing..."):
                    response = model.generate_content(prompt)
                    st.success(response.text)

            except Exception as e:
                # If there's an error, show a helpful message
                if "404" in str(e):
                    st.error("Error 404: The AI model wasn't found. Make sure you clicked 'ENABLE' on the Gemini API page in Google Cloud.")
                else:
                    st.error(f"Something went wrong: {e}")
else:
    st.info("Please upload a CSV file to get started.")
