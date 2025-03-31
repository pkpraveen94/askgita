import streamlit as st
import requests
import folium
from geopy.distance import geodesic
from folium.plugins import PolyLineTextPath
from streamlit_folium import folium_static

# Define the API key (replace with your actual key)
api_key = "AIzaSyDxN9MpYQa1o4pZanoUlRBZBDqrC-veu9U"

# Precinct data
precincts = {
    "001": {"name": "Harbins A", "address": "3550 New Hope Road, Dacula, GA 30019", "coords": [34.0310, -83.9008]},
    "002": {"name": "Rockbridge A", "address": "3150 Spain Road, Snellville, GA 30039", "coords": [33.8090, -84.0382]},
    "003": {"name": "Dacula", "address": "202 Hebron Church Road NE, Dacula, GA 30019", "coords": [33.9925, -83.8974]},
    "004": {"name": "Suwanee A", "address": "361 Main Street, Suwanee, GA 30024", "coords": [34.0515, -84.0713]},
    "005": {"name": "Baycreek A", "address": "555 Grayson Parkway, Grayson, GA 30017", "coords": [33.8945, -83.9630]},
    "006": {"name": "Goodwins A", "address": "1570 Lawrenceville Suwanee Road, Lawrenceville, GA 30043", "coords": [33.9876, -84.0769]},
    "007": {"name": "Duluth A", "address": "3167 Main Street NW, Duluth, GA 30096", "coords": [34.0020, -84.1446]},
    "008": {"name": "Duncans A", "address": "4404 Braselton Highway, Hoschton, GA 30548", "coords": [34.0992, -83.7854]},
    "009": {"name": "Picketts A", "address": "2723 N Bogan Road, Buford, GA 30519", "coords": [34.1275, -83.9833]},
    "010": {"name": "Cates A", "address": "2428 Main Street East, Snellville, GA 30078", "coords": [33.8573, -84.0199]}
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
    
    for number, data in precincts.items():
        folium.Marker(
            location=data["coords"],
            popup=f"<strong style='color:black;'>{'Precinct ' + number + ' - ' + data['name']}</strong><br>{data['address']}",  # Make precinct number and name bold and black
            icon=folium.Icon(color='red', icon='flag')
        ).add_to(precinct_map)
    
    return precinct_map

# Function to create a map showing nearby places and distances
def create_places_map(places_data, center_location, precinct_name, zoom_start=12):
    map_ = folium.Map(location=center_location, zoom_start=zoom_start)
    
    # Adding marker for the precinct location
    folium.Marker(
        location=center_location,
        popup=f"<strong>{precinct_name}</strong> - Precinct Location",
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(map_)
    
    distances = []
    if places_data and 'results' in places_data:
        # Collecting all places and calculating distances
        for place in places_data['results']:
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            place_location = (lat, lng)
            distance_km = geodesic(center_location, place_location).km
            distance_miles = distance_km * 0.621371
            
            distances.append({
                'place': place,
                'distance_miles': distance_miles,
                'location': (lat, lng),
                'address': place.get('vicinity', 'Address not available')  # Getting address
            })
        
        # Sorting places based on the distance from the precinct
        distances.sort(key=lambda x: x['distance_miles'])
        
        # Adding markers for all nearby places (without lines)
        for place_data in distances:
            lat, lng = place_data['location']
            distance_miles = place_data['distance_miles']
            address = place_data['address']
            
            # Modified popup content to make Distance, Address, and Place Name headings bold and black
            folium.Marker(
                location=[lat, lng],
                popup=f"<strong style='color:black;'>{place_data['place']['name']}</strong><br>"
                      f"<strong style='color:black;'>Distance:</strong> {distance_miles:.2f} miles<br>"
                      f"<strong style='color:black;'>Address:</strong> {address}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_)
        
        # Drawing lines to the nearest 5 places
        for place_data in distances[:5]:
            lat, lng = place_data['location']
            folium.PolyLine(
                locations=[center_location, (lat, lng)],
                color="blue", 
                weight=2.5, 
                opacity=1
            ).add_to(map_)
    
    return map_

# Streamlit app structure
def main():
    st.markdown("<h2>BallotDA - Discovering Nearby Places Around Precinct Locations</h2>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-size:20px;'>Select a Precinct Number</h3>", unsafe_allow_html=True)  # Adjusted size to match the previous one
    
    # Creating and displaying the precinct map
    precinct_map = create_precinct_map()
    folium_static(precinct_map)
    
    st.markdown("---")
    st.markdown("<h3>Discover Nearby Places</h3>", unsafe_allow_html=True)
    
    # Selectbox for precinct
    selected_precinct = st.selectbox("Select a Precinct Number", list(precincts.keys()))
    
    # Selectbox for place type (single selection)
    selected_place_type = st.selectbox(
        "Select a Place Type", 
        options=["church", "school", "library", "community_center"],
        index=0  # Default to 'church'
    )

    if selected_precinct:
        precinct_data = precincts[selected_precinct]
        lat, lng = precinct_data["coords"]
        location = f"{lat},{lng}"
        radius = 32186  # Set the search radius
        
        # Fetch places data for selected place type
        places_data = fetch_places_data(api_key, location, radius, [selected_place_type])
        
        if places_data:
            st.success(f"📍 Showing results near {precinct_data['name']} - {precinct_data['address']}")
            places_map = create_places_map(places_data, [lat, lng], precinct_data['name'])
            folium_static(places_map)

if __name__ == "__main__":
    main()