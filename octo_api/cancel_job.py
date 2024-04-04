import requests

from octo_api_test import OCTOPRINT_URL, headers


data = {
    "command": "cancel"
}


response = requests.post(f"{OCTOPRINT_URL}/api/job", json=data, headers=headers)
print(response.content)
if response.status_code == 204:
    print("Print job canceled successfully")
else:
    print("Failed to cancel print job")

