import requests
import json
import sys

# ==============================================
# Step 3: Create Variables for API Request
# ==============================================
directions_api = "https://api.openrouteservice.org/v2/directions/driving-car"
geocode_api = "https://api.openrouteservice.org/geocode/search?"
key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImY3YmEyNjM1NzNlNTQ2ODk5NDUwY2ExMzliZGE3ZTEwIiwiaCI6Im11cm11cjY0In0="  
# ==============================================
# Step 5: Geocode Addresses
# ==============================================
def geocode_address(address):
    url = f"{geocode_api}api_key={key}&text={address}"
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        if json_data["features"]:
            coords = json_data["features"][0]["geometry"]["coordinates"]
            print(f"Geocoded coordinates for '{address}': {coords}")  # Debugging
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


# ==============================================
# Step 4 + Step 6 + Step 7 (Console version)
# ==============================================
while True:
    orig = input("Starting Location: ")
    if orig.lower() in ("quit", "q"):
        break
    dest = input("Destination: ")
    if dest.lower() in ("quit", "q"):
        break

    # Step 6: Geocode both
    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        print("Unable to geocode one or both addresses. Please try again.\n")
        continue

    # Construct JSON body
    body = {"coordinates": [orig_coords, dest_coords]}
    headers = {"Authorization": key, "Content-Type": "application/json"}

    # Make POST request
    response = requests.post(directions_api, headers=headers, json=body)
    json_data = response.json()
    print(json_data)  # Debugging

    # Step 7: Parse and display trip info
    if response.status_code == 200:
        if 'routes' in json_data and json_data['routes']:
            route = json_data['routes'][0]
            if 'segments' in route and route['segments']:
                segment = route['segments'][0]
                print("\nAPI Status: Successful route call.\n")
                print("=============================================")
                print(f"Directions from {orig} to {dest}")

                duration = segment.get('duration', 'N/A')
                distance = segment.get('distance', 'N/A')

                print(f"Trip Duration: {duration} seconds")
                print(f"Distance: {distance} meters")
                print("=============================================")

                if 'steps' in segment:
                    for step in segment['steps']:
                        instruction = step.get('instruction', 'N/A')
                        step_distance = step.get('distance', 'N/A')
                        print(f"{instruction} ({step_distance} meters)")
                else:
                    print("No step-by-step directions available.")
                print("=============================================\n")
            else:
                print("Error: No segments found in the route.")
        else:
            print("Error: No routes found in the response.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# ==============================================
# Django Integration (command-line arguments)
# ==============================================
if len(sys.argv) == 3:
    orig = sys.argv[1]
    dest = sys.argv[2]

    orig_coords = geocode_address(orig)
    dest_coords = geocode_address(dest)

    if not orig_coords or not dest_coords:
        print(json.dumps({"error": "Unable to geocode one or both addresses"}))
        sys.exit(1)

    body = {"coordinates": [orig_coords, dest_coords]}
    headers = {"Authorization": key, "Content-Type": "application/json"}

    response = requests.post(directions_api, headers=headers, json=body)
    json_data = response.json()

    if response.status_code == 200 and 'routes' in json_data and json_data['routes']:
        route = json_data['routes'][0]
        if 'segments' in route and route['segments']:
            segment = route['segments'][0]

            result = {
                "origin": orig,
                "destination": dest,
                "duration": segment.get("duration"),
                "distance": segment.get("distance"),
                "steps": segment.get("steps", [])
            }

            print(json.dumps(result))
            sys.exit(0)

    print(json.dumps({"error": "No valid route found"}))
    sys.exit(1)

