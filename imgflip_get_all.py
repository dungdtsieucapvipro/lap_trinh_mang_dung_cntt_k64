import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# Function to use Playwright for extracting details from the dynamic page
def lay_chi_tiet(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()

        # Visit the URL
        page.goto(url, timeout=0)  # Increase timeout and wait for network idle

        title = page.query_selector("h1").inner_text()
        image = page.query_selector("img.mm-img").get_attribute("src")

        print(f"{title}: https://imgflip.com{image}")

        # Close the browser
        browser.close()

# Function to scrape initial page for links and call lay_chi_tiet for each link
def scrape_and_extract_details(page):
    # Make a request to the page
    print(f'Get meme list from page: https://imgflip.com/memetemplates?page={page}')
    response = requests.get(f'https://imgflip.com/memetemplates?page={page}')

    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the relevant links
        danh_sach_A = soup.findAll("a", class_="mt-caption")

        for tag_a in danh_sach_A:
            # Construct the full URL
            full_href = 'https://imgflip.com' + tag_a['href']
            print(f"Processing URL: {full_href}")
            # Call the Playwright function to scrape details from the dynamic page
            lay_chi_tiet(full_href)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Execute the scraping function
for i in range(1, 1000):
    scrape_and_extract_details(i)