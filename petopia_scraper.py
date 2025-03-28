import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://www.wow-petopia.com/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def scrape_category(category):
    url = f"{BASE_URL}browse.php?id={category}"
    print(f"Scraping {url}...")

    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        pets = []

        for row in soup.select('tr'):
            name_cell = row.select_one("td.name .pettablename a")
            zone_cell = row.select_one("td.zone")

            if not all([name_cell, zone_cell]):
                continue

            name = name_cell.text.strip()
            zone = zone_cell.text.strip()

            pet_data = {
                "name": name,
                "family": "Unknown",  # Optional: später ergänzen
                "zone": zone,
                "image": urljoin(BASE_URL, name_cell['href'])  # Link zur Detailseite
            }

            if category == "elite":
                pet_data["spawn_time"] = "N/A"  # Optional: kann verbessert werden

            pets.append(pet_data)

        return pets

    except Exception as e:
        print(f"Error scraping {category}: {str(e)}")
        return []

def main():
    categories = {
        "collector": scrape_category("collector"),
        "rare": scrape_category("rare"),
        "looks": scrape_category("looks"),
        "elite": scrape_category("elite")
    }

    with open('petopia_data.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)

    total_pets = sum(len(pets) for pets in categories.values())
    print(f"Successfully scraped {total_pets} pets")

if __name__ == "__main__":
    main()
