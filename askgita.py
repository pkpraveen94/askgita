import streamlit as st
import requests
import folium
from geopy.distance import geodesic
from folium.plugins import PolyLineTextPath
from streamlit_folium import folium_static

# Define the API key (replace with your actual key)
api_key = "AIzaSyDxN9MpYQa1o4pZanoUlRBZBDqrC-veu9U"

# Sample Precincts in Gwinnett County
precincts = {
    "Duluth Precinct": [34.0020, -84.1446],
    "Lawrenceville Precinct": [33.9560, -83.9879],
    "Norcross Precinct": [33.9412, -84.2135]
}

# Function to fetch data from the Google Places API
def fetch_places_data(api_key, location, radius, place_types):
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

# Function to create a map with precincts
def create_precinct_map():
    precinct_map = folium.Map(location=[33.9614, -84.0235], zoom_start=9)
    
    for name, coords in precincts.items():
        folium.Marker(
            location=coords,
            popup=name,
            icon=folium.Icon(color='red', icon='flag')
        ).add_to(precinct_map)
    
    return precinct_map

# Function to create a map showing public places near a selected precinct and the distance
def create_places_map(places_data, center_location, precinct_name, zoom_start=12):
    map_ = folium.Map(location=center_location, zoom_start=zoom_start)
    
    # Add the precinct marker with red color
    folium.Marker(
        location=center_location,
        popup=f"<strong>{precinct_name}</strong> - Precinct Location",
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(map_)
    
    # List to store distances from the precinct to each place
    distances = []
    
    if places_data and 'results' in places_data:
        for place in places_data['results']:
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            
            # Calculate the distance from the precinct to the place
            place_location = (lat, lng)
            precinct_location = tuple(center_location)
            distance_km = geodesic(precinct_location, place_location).km  # Distance in kilometers
            distance_miles = distance_km * 0.621371  # Convert kilometers to miles
            
            distances.append({
                'place': place,
                'distance_miles': distance_miles,
                'location': (lat, lng)
            })
        
        # Sort the distances to get the nearest places
        distances.sort(key=lambda x: x['distance_miles'])
        
        # Show all places with markers
        for place in places_data['results']:
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            place_type = place['types'][0].replace("_", " ").title()
            
            # Add the distance directly inside the address in the popup
            distance_miles = geodesic(center_location, (lat, lng)).miles
            address_with_distance = f"{place['vicinity']}<br><strong>Distance: {distance_miles:.2f} miles</strong>"
            
            # Create a marker for the place
            folium.Marker(
                location=[lat, lng],
                popup=f"<strong>{place['name']}</strong><br>{address_with_distance}<br>Type: {place_type}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_)
        
        # Draw lines and show miles for the first 5 nearest places
        for i in range(min(5, len(distances))):
            place = distances[i]['place']
            distance_miles = distances[i]['distance_miles']
            lat, lng = distances[i]['location']
            
            # Create a line from the precinct to the place
            line = folium.PolyLine(
                locations=[center_location, (lat, lng)],
                color="blue", 
                weight=2.5, 
                opacity=1
            ).add_to(map_)
            
            # Add text along the polyline for distance (miles) in the middle of the line
            PolyLineTextPath(line, f"{distance_miles:.2f} miles", offset=5).add_to(map_)
    
    return map_

# Streamlit app structure
def main():
    st.markdown("<h2>BalletDA - Discovering Nearby Places Around Precinct Locations</h2>", unsafe_allow_html=True)
    st.markdown("<h3>Gwinnett County Map - Precinct Locations</h3>", unsafe_allow_html=True)
    
    # Create and display the precinct map
    precinct_map = create_precinct_map()
    folium_static(precinct_map)
    
    st.markdown("---")
    st.markdown("<h3>Nearby Public Places</h3>", unsafe_allow_html=True)
    
    selected_precinct = st.selectbox("Select a Precinct", list(precincts.keys()))
    
    if selected_precinct:
        lat, lng = precincts[selected_precinct]
        location = f"{lat},{lng}"
        radius = 32186  # 20 miles
        place_types = ["library", "community_center", "auditorium", "school"]
        
        places_data = fetch_places_data(api_key, location, radius, place_types)
        
        if places_data:
            st.success(f"📍 Showing results near {selected_precinct}")
            places_map = create_places_map(places_data, [lat, lng], selected_precinct)
            folium_static(places_map)

if __name__ == "__main__":
    main()