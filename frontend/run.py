import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import openrouteservice

# Load the DataFrame
df = pd.read_csv('/home/jabez/Documents/week_8/Logistic-optimization-Delivery-drivers-location-optimisation-with-Causal-Inference-/data/df_concatenated.csv')

df_random_subset = df.sample(n=5, random_state=1)  # random_state ensures reproducibility

# Title of the app
st.title('Car Journey Story')

# Create a Folium map
map = folium.Map(location=[37.7749, -122.4194], zoom_start=5)

# Initialize OpenRouteService client
ors_client = openrouteservice.Client(key='')

# Iterate through each row in the DataFrame and plot the start and end locations
for index, row in df_random_subset.iterrows():
    start_coords = [row['lat_org'], row['lon_org']]
    end_coords = [row['lat_des'], row['lon_des']]
    
    # Add marker for start location
    folium.Marker(
        start_coords, 
        tooltip=f"Vehicle {row['order_id']} Start", 
        icon=folium.Icon(color='green')
    ).add_to(map)
    
    # Add marker for end location
    folium.Marker(
        end_coords, 
        tooltip=f"Vehicle {row['order_id']} End", 
        icon=folium.Icon(color='red')
    ).add_to(map)
    
    # Get the route between the start and end locations
    coords = (start_coords[::-1], end_coords[::-1])  # Reverse order for ORS (lon, lat)
    try:
        route = ors_client.directions(coordinates=coords, profile='driving-car', format='geojson')
        route_geometry = route['features'][0]['geometry']['coordinates']
        
        # Convert route coordinates to folium format
        folium_route_coords = [(coord[1], coord[0]) for coord in route_geometry]
        
        # Add the route as a polyline on the map
        folium.PolyLine(folium_route_coords, color='blue', weight=2.5, opacity=1).add_to(map)
    except Exception as e:
        st.error(f"Error fetching route for vehicle {row['order_id']}: {e}")

# Display the map in the Streamlit app
st_folium(map, width=700, height=500)
