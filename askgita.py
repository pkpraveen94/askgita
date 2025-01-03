import streamlit as st
import requests
from gtts import gTTS
import os

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

# Submit button for asking question
if st.button("Seek Guidance"):
    if question:
        try:
            # Send the question as "blog_topic" (matching the expected data format)
            response = requests.post(url, json={"blog_topic": question})
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer found, but keep seeking!")
                
                st.success("Here's the wisdom we found for you:")
                st.write(answer)

                # Display button for hearing the guidance
                if st.button("🎧 Hear the Guidance"):
                    # Convert text to speech (voice note)
                    tts = gTTS(text=answer, lang='en')
                    tts.save("answer.mp3")
                    
                    # Play the voice note
                    st.audio("answer.mp3")
                    
                    # Optionally delete the audio file after use
                    os.remove("answer.mp3")
                
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
