from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)  # Set headless=True for headless mode
    page = browser.new_page()
    page.goto("https://imgflip.com/memegenerator/Distracted-Boyfriend", timeout=0)  # Wait until the network is idle
    title = page.query_selector("h1").inner_text()
    image = page.query_selector("img.mm-img").get_attribute("src")

    print(f"{title}: https://imgflip.com{image}")
    browser.close()

with sync_playwright() as playwright:
    run(playwright)