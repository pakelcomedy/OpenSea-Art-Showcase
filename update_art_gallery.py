import requests

API_KEY = "60c2cea4924d4cf195bff2225eddd514"
LIMIT = 10

def fetch_collections():
    url = "https://api.opensea.io/api/v2/collections"
    params = {
        "order_by": "created_date",
        "limit": LIMIT
    }
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()

def main():
    try:
        collections = fetch_collections()
        
        with open('README.md', 'w') as f:
            f.write("# Digital Art Gallery\n\n")
            f.write("## Trending Collections on OpenSea\n\n")
            for collection in collections['collections']:
                name = collection.get('name', 'Unnamed Collection')
                image_url = collection.get('image_url', '')
                description = collection.get('description', 'No description available.')
                opensea_url = collection.get('opensea_url', '#')
                
                f.write(f"### {name}\n")
                if image_url:
                    f.write(f"![{name}]({image_url})\n\n")
                f.write(f"**Description:** {description}\n\n")
                f.write(f"[OpenSea Link]({opensea_url})\n\n")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err.response.status_code} - {err.response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")

if __name__ == "__main__":
    main()
