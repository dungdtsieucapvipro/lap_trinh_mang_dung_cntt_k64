from playwright.sync_api import sync_playwright

def lay_chi_tiet(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Wait for the content to load (optional depending on website)
        page.wait_for_timeout(3000)  # Better: wait for specific elements instead

        # Extract the title and image src
        title = page.query_selector("h1").inner_text()
        image = page.query_selector("img.mm-img").get_attribute("src")

        print(f"{title}: https:{image}")

        browser.close()


lay_chi_tiet("https://imgflip.com/memegenerator/Distracted-Boyfriend")