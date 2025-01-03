# Import necessary libraries
import streamlit as st
import requests

# API URL
url = "https://2owawgyt71.execute-api.us-east-1.amazonaws.com/dev/blog-generation"

# App Title
st.set_page_config(page_title="Ask Gita - Spiritual Insights", layout="centered", page_icon="🙏")
st.title("🙏 Ask Gita - Spiritual Insights")

# Background and Styling
st.markdown(
    """
    <style>
        html, body, [class*="css"] {
            background-color: white !important;
            color: black !important;
            font-family: Arial, sans-serif;
        }
        .stTextInput input {
            background-color: #f9f9f9;
            color: black;
            border: 1px solid #ccc;
        }
        .stButton button {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Introduction section
st.markdown("""
### Welcome to Ask Gita
🙏 Dive deep into the wisdom of the Bhagavad Gita. Ask your questions and uncover spiritual insights to guide your journey.
""")

# Input section
question = st.text_input("What spiritual question is on your mind today?")

# Submit button
if st.button("Seek Guidance"):
    if question:
        try:
            # Make a request to the API
            response = requests.post(url, json={"question": question})
            
            if response.status_code == 200:
                data = response.json()
                st.success("Here's the wisdom we found for you:")
                st.write(data.get("answer", "No answer found, but keep seeking!"))
            else:
                st.error("Failed to retrieve guidance. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question before seeking guidance.")

# Footer with two-hand worship symbol
st.markdown("""
---
<div style="text-align: center;">
    🙌 Powered by Ask Gita | Spiritual Guidance for Everyone 🙌
</div>
""", unsafe_allow_html=True)

