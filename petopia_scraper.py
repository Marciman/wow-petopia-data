import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://www.wow-petopia.com/"
CATEGORIES = {
    "collector": "Sammler-Pets",
    "rare": "Seltene Pets",
    "looks": "Besondere Optik",
    "elite": "Elite-Pets"
}

def scrape_category(category_id):
    url = urljoin(BASE_URL, f"browse.php?id={category_id}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    pets = []
    for pet in soup.select('.petlisting'):
        # Grundlegende Daten
        pet_data = {
            'name': pet.select_one('.petname a').text.strip(),
            'category': CATEGORIES[category_id],
            'family': pet.select_one('.family').text.strip(),
            'location': pet.select_one('.location').text.strip(),
            'image': urljoin(BASE_URL, pet.select_one('.petimage img')['src'])
        }
        
        # Zusätzliche Felder je nach Kategorie
        if category_id == "elite":
            pet_data['spawn_time'] = pet.select_one('.spawntime').text.strip() if pet.select_one('.spawntime') else "N/A"
            pet_data['taming_notes'] = pet.select_one('.tamingnotes').text.strip() if pet.select_one('.tamingnotes') else ""
        
        pets.append(pet_data)
    
    return pets

def main():
    all_pets = {}
    for category_id in CATEGORIES.keys():
        print(f"Scraping {category_id}...")
        all_pets[category_id] = scrape_category(category_id)
    
    # Als JSON speichern
    with open('petopia_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_pets, f, ensure_ascii=False, indent=2)
    
    print(f"Daten erfolgreich gespeichert! Gesamt: {sum(len(pets) for pets in all_pets.values())} Pets")

if __name__ == "__main__":
    main()