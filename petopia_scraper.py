import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://www.wow-petopia.com/"
CATEGORIES = {
    "collector": "Collector Pets",
    "rare": "Rare Spawns", 
    "looks": "Unique Looks",
    "elite": "Elite Pets"
}

def scrape_pet_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pet_data = {
        "name": soup.select_one("h1.pet-name").text.strip(),
        "family": soup.select_one(".pet-family").text.strip().replace("Family: ", ""),
        "locations": [],
        "image": urljoin(BASE_URL, soup.select_one(".pet-image img")["src"])
    }
    
    # Spawn-Punkte extrahieren
    for loc in soup.select(".pet-location"):
        pet_data["locations"].append({
            "zone": loc.select_one(".location-zone").text.strip(),
            "coords": loc.select_one(".location-coords").text.strip() if loc.select_one(".location-coords") else "N/A",
            "spawn_time": loc.select_one(".location-spawntime").text.strip() if loc.select_one(".location-spawntime") else "N/A"
        })
    
    return pet_data

def scrape_category(category_id):
    url = f"{BASE_URL}browse.php?id={category_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pets = []
    for link in soup.select(".petlisting a.petname"):
        pet_url = urljoin(BASE_URL, link["href"])
        print(f"Scraping {pet_url}...")
        pets.append(scrape_pet_page(pet_url))
    
    return pets

def main():
    all_pets = {}
    for category_id, category_name in CATEGORIES.items():
        print(f"\n=== Scraping {category_name} ===")
        all_pets[category_id] = scrape_category(category_id)
    
    # Als JSON speichern
    with open('petopia_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_pets, f, ensure_ascii=False, indent=2)
    
    print(f"\nDone! Saved {sum(len(pets) for pets in all_pets.values())} pets")

if __name__ == "__main__":
    main()
