import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Define the API key (replace with your actual key)
api_key = "AIzaSyDxN9MpYQa1o4pZanoUlRBZBDqrC-veu9U"

# Function to fetch data from the Google Places API
def fetch_places_data(api_key, location, radius, place_types):
    """Fetch data from Google Places API for selected place types."""
    if not place_types:
        return None  

    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": location,  
        "radius": radius,  
        "types": "|".join(place_types),  
        "key": api_key  
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data: {response.status_code}")
        return None

# Function to create a map and add markers for the selected place types
def create_map(places_data, center_location, zoom_start=12):
    """Creates a folium map and adds markers for the selected place types."""
    map_ = folium.Map(location=center_location, zoom_start=zoom_start)
    
    if places_data and 'results' in places_data:
        for place in places_data['results']:
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            
            # Determine the correct place type
            place_type = "Unknown"
            for type_ in place['types']:
                if type_ in ["library", "community_center", "school", "auditorium"]:
                    place_type = type_.replace("_", " ").title()
                    break
            
            # Add marker with label
            folium.Marker(
                location=[lat, lng],
                popup=f"<strong>{place['name']}</strong><br>{place['vicinity']}<br>Type: {place_type}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_)
    
    return map_

# Streamlit app structure
def main():
    """Main function for Streamlit app."""
    st.title("BalletDA - Suitable Indoor Locations for Voting")

    latitude, longitude = 33.8570, -84.3350
    location = f"{latitude},{longitude}"
    radius = 80467  # 50 miles in meters
    place_types_options = ["library", "community_center", "auditorium", "school"]

    # Initialize session state for selection control
    if "selected_types" not in st.session_state:
        st.session_state.selected_types = []
    
    if "selection_made" not in st.session_state:
        st.session_state.selection_made = False

    # Show the radius and location info
    st.write(f"🔍 Searching for voting places around **Atlanta (Brookhaven)**, within a **{radius / 1609.34:.2f} miles** radius.")

    # If selection hasn't been made, show the dropdown
    if not st.session_state.selection_made:
        selected_types = st.multiselect("Select Place Types", place_types_options, default=[])
        
        if selected_types:
            st.session_state.selected_types = selected_types
            st.session_state.selection_made = True  
            st.rerun()  # Hide the dropdown and refresh the page

    # If selection is made, display Reset button and show current selection
    else:
        selected_types = st.session_state.selected_types
        st.success(f"✅ Showing results for: **{', '.join(selected_types)}**")
        
        if st.button("🔄 Select Another Place Type"):
            st.session_state.selection_made = False  # Show dropdown again
            st.session_state.selected_types = []
            st.rerun()

    # If no types are selected, show a message
    if not selected_types:
        st.warning("⚠️ Please select at least one place type to display locations.")
        return

    # Fetch data and generate the map
    places_data = fetch_places_data(api_key, location, radius, selected_types)
    
    if places_data:
        map_ = create_map(places_data, [latitude, longitude])
        folium_static(map_)

if __name__ == "__main__":
    main()



#ASK GITA CODE

# import streamlit as st
# import requests
# from gtts import gTTS
# import os

# # API URL
# url = "https://2owawgyt71.execute-api.us-east-1.amazonaws.com/dev/blog-generation"

# # App Title
# st.set_page_config(page_title="Ask Gita - Spiritual Insights", layout="centered", page_icon="🙏")
# st.title("🙏 Ask Gita - Spiritual Insights")

# # Background and Styling
# st.markdown(
#     """
#     <style>
#         html, body, [class*="css"] {
#             background-color: white !important;
#             color: black !important;
#             font-family: Arial, sans-serif;
#         }
#         .stTextInput input {
#             background-color: #f9f9f9;
#             color: black;
#             border: 1px solid #ccc;
#         }
#         .stButton button {
#             background-color: #007bff;
#             color: white;
#             font-weight: bold;
#             border-radius: 5px;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Introduction section
# st.markdown(""" 
# ### Welcome to Ask Gita
# 🙏 Dive deep into the wisdom of the Bhagavad Gita. Ask your questions and uncover spiritual insights to guide your journey.
# """)

# # Input section
# question = st.text_input("What spiritual question is on your mind today?")

# # Variable to store answer status
# guidance_answer = None

# # Submit button for asking question
# if st.button("Ask Gita for Guidance"):
#     if question:
#         try:
#             # Send the question directly without modifying the prompt
#             response = requests.post(url, json={"blog_topic": question})
            
#             if response.status_code == 200:
#                 data = response.json()

#                 # Extract the 'places_content' from the response
#                 guidance_answer = data.get("places_content", None)
                
#                 if guidance_answer:
#                     st.success("Here's the wisdom we found for you:")
#                     st.write(guidance_answer)
#                 else:
#                     st.warning("No guidance found for your question, but keep seeking!")
#             else:
#                 st.error(f"Failed to retrieve guidance. Server responded with status code: {response.status_code}")
#         except requests.exceptions.RequestException as e:
#             st.error(f"An error occurred while making the request: {e}")
#         except Exception as e:
#             st.error(f"An unexpected error occurred: {e}")
#     else:
#         st.warning("Please enter a question before seeking guidance.")

# # Only show the "Hear the Guidance" button if there's an answer
# if guidance_answer:
#     if st.button("🎧 Hear the Guidance"):
#         # Convert text to speech (voice note)
#         tts = gTTS(text=guidance_answer, lang='en')
#         tts.save("answer.mp3")
        
#         # Play the voice note
#         st.audio("answer.mp3")
        
#         # Optionally delete the audio file after use
#         os.remove("answer.mp3")

# # Footer with two-hand worship symbol
# st.markdown(""" 
# ---
# <div style="text-align: center;">
#     🙌 Powered by Ask Gita | Spiritual Guidance for Everyone 🙌
# </div>
# """, unsafe_allow_html=True)
