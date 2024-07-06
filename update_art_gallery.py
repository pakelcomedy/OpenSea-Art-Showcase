import requests
from datetime import datetime

# Function to fetch trending NFT collections from OpenSea
def fetch_trending_collections():
    url = "https://api.opensea.io/api/v2/collections"
    headers = {
        "Accept": "application/json",
        "X-API-KEY": "60c2cea4924d4cf195bff2225eddd514"  # Replace with your actual API key
    }
    params = {
        "order_by": "created_date",
        "limit": 5  # Fetching the top 5 trending collections
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        collections_data = response.json().get("collections", [])
        return collections_data
    else:
        print(f"Failed to fetch collections. Status code: {response.status_code}")
        return None

# Function to format collections data in Markdown with HTML centering tags
def format_collections_markdown(collections):
    if not collections:
        return ""

    markdown_content = "# <div align=\"center\">Digital Art Gallery</div>\n\n"
    markdown_content += "## <div align=\"center\">Trending Collections on OpenSea</div>\n\n"
    markdown_content += "<div align=\"center\">\n\n"
    markdown_content += "| Collection Name | Image | Description | OpenSea Link |\n"
    markdown_content += "|-----------------|-------|-------------|--------------|\n"

    for collection in collections:
        collection_name = collection.get("name", "Unknown")
        image_url = collection.get("image_url", "")
        description = collection.get("description", "No description available.")
        opensea_url = collection.get("opensea_url", "")

        markdown_content += f"| {collection_name} | ![Image]({image_url}) | {description} | [{opensea_url}]({opensea_url}) |\n"

    markdown_content += "\n</div>\n"

    return markdown_content

# Function to update README.md with formatted collections data
def update_readme_with_collections(markdown_content):
    with open("README.md", "w", encoding="utf-8") as readme_file:
        readme_file.write(markdown_content)

    print("README.md updated successfully.")

# Main function to fetch collections, format Markdown, and update README.md
def main():
    trending_collections = fetch_trending_collections()
    if trending_collections:
        markdown_content = format_collections_markdown(trending_collections)
        update_readme_with_collections(markdown_content)

if __name__ == "__main__":
    main()