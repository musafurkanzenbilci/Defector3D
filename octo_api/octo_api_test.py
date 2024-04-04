OCTOPRINT_URL = "http://localhost:5000"
API_KEY = ""
if not API_KEY:
    print("PLEASE ADD YOUR API KEY IN octo_api_test.py")

headers = {
    "X-Api-Key": API_KEY,
}

# Retrieve printer status
if __name__ == '__main__':
    import requests
    response = requests.get(f"{OCTOPRINT_URL}/api/printer", headers=headers)
    if response.status_code == 200:
        print("Printer status:", response.json())
    else:
        print("Failed to retrieve printer status")

