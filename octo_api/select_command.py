import requests

from octo_api_test import OCTOPRINT_URL, headers

data = {
    "command": "select",
    "print": True
}

filename = 'biyikliairpodsholder.gcode'

response = requests.post(f"{OCTOPRINT_URL}/api/files/local/{filename}", json=data, headers=headers)

if response.status_code == 204:
    print("Print job started successfully")
else:
    print("Failed to start print job")

