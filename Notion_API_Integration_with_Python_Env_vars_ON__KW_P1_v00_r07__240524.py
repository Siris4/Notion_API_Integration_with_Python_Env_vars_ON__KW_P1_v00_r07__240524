import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from notion_client import Client

# Read Notion API key and page ID from environment variables
notion_api_key = os.environ.get('NOTION_API_KEY_My_Selenium_Notion_Integration')
notion_page_id = os.environ.get('NOTION_PAGE_ID_My_Selenium_Notion_Integration')

# Debug prints to check if environment variables are being retrieved correctly
print("Notion API Key:", notion_api_key)
print("Notion Page ID:", notion_page_id)

if not notion_api_key or not notion_page_id:
    raise ValueError("Environment variables NOTION_API_KEY and NOTION_PAGE_ID must be set")

# Initialize Notion client
notion = Client(auth=notion_api_key)

def test_integration_access():
    try:
        # Fetch the page
        page = notion.pages.retrieve(page_id=notion_page_id)
        print(f"Integration access confirmed. \nPage data:", page)

        # Check if the page has a title
        if 'properties' in page and 'title' in page['properties']:
            title_property = page['properties']['title']
            if title_property['type'] == 'title' and title_property['title']:
                print("Page title:", title_property['title'][0]['text']['content'])
            else:
                print("Page has no title or title format is unexpected")
        else:
            print("Page properties do not include a title")
    except Exception as e:
        print(f"Failed to access page: {e}")

test_integration_access()

# Selenium setup
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Use WebDriver Manager to handle ChromeDriver
try:
    print("Attempting to initialize ChromeDriver with WebDriver Manager")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("ChromeDriver initialized successfully.")
except Exception as e:
    print(f"Failed to initialize ChromeDriver: {e}")
    raise

def scrape_favorites():
    # Replace with the URL of the site with your favorites
    driver.get("https://example.com")

    # Log in if necessary
    # login()

    # Scrape the favorites from the sidebar using XPath
    favorites = []
    try:
        favorite_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'favorite-item')]")
        for element in favorite_elements:
            favorites.append(element.text)
    except Exception as e:
        print(f"Failed to scrape favorites: {e}")

    return favorites

def update_notion(favorites):
    # Fetch the existing page content
    try:
        page = notion.pages.retrieve(page_id=notion_page_id)
        # Clear the existing content
        children = []
        for favorite in favorites:
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "text": [
                        {
                            "type": "text",
                            "text": {
                                "content": favorite
                            }
                        }
                    ]
                }
            })

        # Update the Notion page with the new content
        notion.blocks.children.append(block_id=notion_page_id, children=children)
        print("Notion page updated successfully.")
    except Exception as e:
        print(f"Failed to update Notion page: {e}")

# Main function
def main():
    favorites = scrape_favorites()
    update_notion(favorites)
    driver.quit()

if __name__ == "__main__":
    main()
