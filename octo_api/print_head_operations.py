import requests

from octo_api_test import OCTOPRINT_URL, headers

data = {
    "command": "home",
    "axes": ['x', 'y']
}

response = requests.post(f"{OCTOPRINT_URL}/api/printer/printhead", json=data, headers=headers)

if response.status_code == 204:
    print("Successful")
else:
    print("Failed")

