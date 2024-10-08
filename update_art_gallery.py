import requests
import os
import time

def is_image_valid(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Image URL validation failed: {e}")
        return False

def fetch_trending_collections(retries=3, delay=5):
    url = "https://api.opensea.io/api/v2/collections?limit=5&offset=0"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": os.getenv("OPENSEA_API_KEY")  # Fetch the API key from environment variables
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            collections = data.get("collections", [])
            if collections:
                return collections
            else:
                print("No collections found in the response.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        
        print(f"Retrying... ({attempt + 1}/{retries})")
        time.sleep(delay)
    
    return []

def main():
    collections = fetch_trending_collections()
    
    if not collections:
        print("No collections found after retries.")
        return
    
    # Markdown content generation
    markdown_content = """\
<div align="center">

# Digital Art Gallery

## Trending Collections on OpenSea

| Collection Name                       | Image                                                                                     | Description                       | OpenSea Link                                                                                          |
|---------------------------------------|-------------------------------------------------------------------------------------------|-----------------------------------|--------------------------------------------------------------------------------------------------------|"""

    for collection in collections:
        collection_name = collection.get("name", "")
        image_url = collection.get("image_url", "")
        description = collection.get("description", "")
        opensea_link = collection.get("opensea_url", "")

        if is_image_valid(image_url):
            if len(collection_name) > 15:
                collection_name_summary = f"<details><summary>{collection_name[:15]}...</summary>{collection_name}</details>"
            else:
                collection_name_summary = collection_name

            if len(description) > 30:
                description = f"<details><summary>{description[:30]}...</summary>{description}</details>"
            
            # Constructing each row in the table
            markdown_content += f"\n| **{collection_name_summary}** | ![Image]({image_url}?w=200&auto=format) | {description} | <details><summary>Link</summary>[{collection_name}]({opensea_link})</details> |"

    markdown_content += "\n\n</div>"
    
    # Writing to README.md
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)
    
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
