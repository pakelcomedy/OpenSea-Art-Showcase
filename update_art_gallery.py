import os
import requests

def is_image_valid(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def fetch_trending_collections():
    url = "https://api.opensea.io/api/v2/collections?limit=5&offset=0"
    api_key = os.getenv('OPENSEA_API_KEY')
    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get("collections", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def main():
    collections = fetch_trending_collections()
    
    if not collections:
        print("No collections found.")
        return
    
    # Markdown content generation
    markdown_content = """\
<div align="center">

# Digital Art Gallery

## Trending Collections on OpenSea

| Collection Name                             | Image                                                                                     | Description              | OpenSea Link                                                                                          |
|---------------------------------------------|-------------------------------------------------------------------------------------------|--------------------------|--------------------------------------------------------------------------------------------------------|"""

    for collection in collections:
        collection_name = collection.get("name", "")
        image_url = collection.get("image_url", "")
        description = collection.get("description", "")
        opensea_link = collection.get("opensea_url", "")

        if len(collection_name) > 15:
            collection_name_summary = f"<details><summary>{collection_name}</summary>"
        else:
            collection_name_summary = collection_name
        
        # Check if image URL is valid
        if is_image_valid(image_url):
            # Constructing each row in the table
            markdown_content += f"\n| **{collection_name_summary}** | ![Image]({image_url}?w=200&auto=format) | {description} | <details><summary>Link</summary>[{collection_name}]({opensea_link})</details> |"
        else:
            print(f"Skipping {collection_name} due to invalid image URL: {image_url}")

    markdown_content += "\n\n</div>"
    
    # Writing to README.md
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)
    
    print("README.md updated successfully.")

if __name__ == "__main__":
    main()
