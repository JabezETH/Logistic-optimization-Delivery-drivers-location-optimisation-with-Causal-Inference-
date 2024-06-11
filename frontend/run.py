import streamlit as st
import folium
from streamlit_folium import st_folium

# Title of the app
st.title('Car Journey Story')

# Sidebar for user inputs
st.sidebar.header('Journey Details')

# Input fields for start and end locations
start_location = st.sidebar.text_input('Start Location', 'Start Point')
end_location = st.sidebar.text_input('End Location', 'End Point')

# Input field for waypoints
waypoints = st.sidebar.text_area('Waypoints (separate by comma)', 'Waypoint1, Waypoint2')

# Function to get coordinates for locations (using some geocoding service, here we mock it)
def get_coordinates(location):
    # Mock coordinates (normally you would use an API to get these)
    locations = {
        'Start Point': [37.7749, -122.4194],
        'Waypoint1': [37.8044, -122.2711],
        'Waypoint2': [37.7749, -122.4194],
        'End Point': [34.0522, -118.2437]
    }
    return locations.get(location, [0, 0])

# Get coordinates for start, end, and waypoints
start_coords = get_coordinates(start_location)
end_coords = get_coordinates(end_location)
waypoint_list = waypoints.split(', ')
waypoint_coords = [get_coordinates(point.strip()) for point in waypoint_list]

# Create a Folium map
map = folium.Map(location=start_coords, zoom_start=10)

# Add markers for start, waypoints, and end locations
folium.Marker(start_coords, tooltip=start_location, icon=folium.Icon(color='green')).add_to(map)
for waypoint, coord in zip(waypoint_list, waypoint_coords):
    folium.Marker(coord, tooltip=waypoint, icon=folium.Icon(color='blue')).add_to(map)
folium.Marker(end_coords, tooltip=end_location, icon=folium.Icon(color='red')).add_to(map)

# Add a line connecting the points
points = [start_coords] + waypoint_coords + [end_coords]
folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(map)

# Display the map in the Streamlit app
st_folium(map, width=700, height=500)
