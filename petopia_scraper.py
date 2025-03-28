import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.wow-petopia.com/"
CATEGORIES = ["collector", "rare", "looks", "elite"]

def scrape_pets():
    all_pets = []
    
    for category in CATEGORIES:
        url = f"{BASE_URL}browse.php?id={category}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for pet in soup.select('.petlisting'):
            pet_data = {
                "name": pet.select_one('.petname a').text.strip(),
                "category": category,
                "family": pet.select_one('.family').text.strip(),
                "zone": pet.select_one('.location').text.strip(),
                "image": BASE_URL + pet.select_one('.petimage img')['src'].lstrip('/')
            }
            
            if category == "elite":
                spawn = pet.select_one('.spawntime')
                pet_data["spawn_time"] = spawn.text.strip() if spawn else "N/A"
            
            all_pets.append(pet_data)
    
    return all_pets

if __name__ == "__main__":
    pets = scrape_pets()
    with open('petopia_data.json', 'w', encoding='utf-8') as f:
        json.dump(pets, f, ensure_ascii=False, indent=2)
