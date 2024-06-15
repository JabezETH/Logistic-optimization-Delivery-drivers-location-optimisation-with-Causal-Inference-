import requests
from math import radians, cos, sin, sqrt, atan2


# Function to get holiday name for a specific date
def get_holiday_name(row):
    year = str(row['st_year'])
    month = str(row['st_month'])
    day = str(row['st_date'])
    api_key = ''
    url = f'https://calendarific.com/api/v2/holidays?&api_key={api_key}&country=NG&year={year}&month={month}&day={day}'
    response = requests.get(url)
    data = response.json()
    
    try:
        # Check if 'holidays' key exists and it's not empty
        if 'holidays' in data['response'] and data['response']['holidays']:
            holiday_name = data['response']['holidays'][0]['name']
        else:
            holiday_name = "No holiday"
    except (KeyError, IndexError):
        # Handle KeyError (if 'response' or 'name' key is missing) or IndexError (if 'holidays' list is empty)
        holiday_name = "No holiday"
    
    return holiday_name


def determine_weekday_or_weekend(date):
    if date.weekday() < 5:  # Weekday is 0-4, Monday to Friday
        return 'Weekday'
    else:  # Weekend is 5-6, Saturday and Sunday
        return 'Weekend'
    
    
# Haversine function to calculate the distance between two points
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

# Function to calculate speed
def calculate_speed(row):
    distance = haversine(row['lat_org'], row['lon_org'], row['lat_des'], row['lon_des'])
    time_diff = (row['trip_end_time'] - row['trip_start_time']).total_seconds() / 3600  # Convert time difference to hours
    # Debugging output
    # print(f"Start: ({row['lat_org']}, {row['lon_org']}), End: ({row['lat_des']}, {row['lon_des']})")
    # print(f"Distance: {distance:.2f} km, Time difference: {time_diff:.2f} hours")
    
    if time_diff == 0:
        return 0  # To handle division by zero
    speed = distance / time_diff  # Speed in km/h
    return speed