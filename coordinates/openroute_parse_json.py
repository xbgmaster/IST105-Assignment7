import json
import requests
import os
import sys

# ==============================================
# Step 5: Geocode Addresses
# ==============================================
def geocode_address(address, geocode_api, key):
    url = f"{geocode_api}api_key={key}&text={address}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if json_data["features"]:
            coords = json_data["features"][0]["geometry"]["coordinates"]
            print(f"Geocoded coordinates for '{address}': {coords}") 
            if -90 <= coords[1] <= 90 and -180 <= coords[0] <= 180:
                return coords
            else:
                print(f"Error: Invalid coordinates for address '{address}'")
                return None
        else:
            print(f"Error: No results found for address '{address}'")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None