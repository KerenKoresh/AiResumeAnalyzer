from playwright.sync_api import sync_playwright


def extract_job_description_from_linkedin(url: str) -> str:
    """Fetches and extracts job description from a LinkedIn job post URL using Playwright."""
    with sync_playwright() as p:
        # Start the browser and open a new page
        browser = p.chromium.launch(headless=True)  # 'headless=True' means no GUI
        page = browser.new_page()

        # Go to the LinkedIn job post
        page.goto(url)

        # Wait for the description to be loaded
        page.wait_for_selector('div.description__text')

        # Extract the job description
        description = page.query_selector('div.description__text').inner_text()

        browser.close()

        return description.strip()
