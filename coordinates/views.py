import os
import subprocess
import json
from django.shortcuts import render
import requests
from coordinates.openroute_parse_json import geocode_address

directions_api = "https://api.openrouteservice.org/v2/directions/driving-car"
geocode_api = "https://api.openrouteservice.org/geocode/search?"
key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImY3YmEyNjM1NzNlNTQ2ODk5NDUwY2ExMzliZGE3ZTEwIiwiaCI6Im11cm11cjY0In0="  

def directions_view(request):
    if request.method == "POST":
        origin = request.POST.get("origin")
        destination = request.POST.get("destination")

        origin_coords = geocode_address(origin, geocode_api, key)
        destination_coords = geocode_address(destination, geocode_api, key)

        if not origin_coords or not destination_coords:
            return render(request, "directions_form.html", {
                "error": "Unable to geocode one or both addresses. Please try again."
            })

        body = {"coordinates": [origin_coords, destination_coords]}
        headers = {"Authorization": key, "Content-Type": "application/json"}

        response = requests.post(directions_api, headers=headers, json=body)
        json_data = response.json()

        if response.status_code == 200 and 'routes' in json_data and json_data['routes']:
            route = json_data['routes'][0]
            if 'segments' in route and route['segments']:
                segment = route['segments'][0]

                result = {
                    "origin": origin,
                    "destination": destination,
                    "duration": segment.get("duration", "N/A"),
                    "distance": segment.get("distance", "N/A"),
                    "steps": segment.get("steps", [])
                }

                return render(request, "directions_result.html", {"result": result})

        return render(request, "directions_result.html", {
            "result": {"error": "No valid route found."}
        })

    return render(request, "directions_form.html")
