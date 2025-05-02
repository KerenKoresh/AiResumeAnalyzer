
import requests
from bs4 import BeautifulSoup


def extract_job_description_from_linkedin(url: str) -> str:
    """Fetches and extracts job description from a LinkedIn job post URL."""
    headers = {
        "User-Agent": "Mozilla/5.0"  # חשוב כדי שלא ייחסם
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError("Failed to fetch the LinkedIn page.")

    soup = BeautifulSoup(response.text, "html.parser")

    # זו דוגמה בסיסית – כדאי לבדוק את מבנה הדף הספציפי
    description_div = soup.find("div", class_="description__text")
    if not description_div:
        raise ValueError("Could not locate job description on the page.")

    return description_div.get_text(strip=True)
