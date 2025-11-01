import os
import subprocess
import json
from django.shortcuts import render

def directions_view(request):
    if request.method == "POST":
        orig = request.POST.get("origin")
        dest = request.POST.get("destination")

       
        script_path = os.path.join(os.path.dirname(__file__), "09_openroute_parse_json.py")

     
        process = subprocess.run(
            ["python3", script_path, orig, dest],
            capture_output=True,
            text=True
        )

    
        if process.returncode == 0:
            try:
                result = json.loads(process.stdout)
            except json.JSONDecodeError:
                result = {"error": "Is not possible to read the output information of the script."}
        else:
            result = {"error": process.stderr}

        return render(request, "directions_result.html", {"result": result})

    return render(request, "directions_form.html")

