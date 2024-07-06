import requests

def fetch_artwork():
    url = "https://api.opensea.io/api/v1/assets"
    params = {
        "order_direction": "desc",
        "offset": "0",
        "limit": "10"
    }
    api_key = "60c2cea4924d4cf195bff2225eddd514"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }
    
    print("Making request to OpenSea API with headers:", headers)
    try:
        response = requests.get(url, headers=headers, params=params)
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        print("Response headers:", response.headers)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("success") == False:
            print("Request was unsuccessful. Please check the endpoint, API key, and parameters.")
        else:
            return response_data.get("assets", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 403:
            print("Access denied. Check your API key and ensure it has the necessary permissions.")
        elif response.status_code == 401:
            print("Unauthorized access. Ensure your API key is correct.")
        elif response.status_code == 404:
            print("Endpoint not found. Verify the URL and parameters.")
        else:
            print(f"An error occurred: {response.status_code}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Example usage
artworks = fetch_artwork()
print(artworks)
