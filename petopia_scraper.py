import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.wow-petopia.com/"

def scrape_pets():
    categories = {
        "collector": [],
        "rare": [],
        "looks": [],
        "elite": []
    }

    for category in categories.keys():
        url = f"{BASE_URL}browse.php?id={category}"
        print(f"Scraping {url}...")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            pets = soup.select('.petlisting')
            
            for pet in pets:
                pet_data = {
                    "name": pet.select_one('.petname a').get_text(strip=True),
                    "family": pet.select_one('.family').get_text(strip=True),
                    "zone": pet.select_one('.location').get_text(strip=True),
                    "image": BASE_URL + pet.select_one('.petimage img')['src'].lstrip('/')
                }
                
                if category == "elite":
                    spawn = pet.select_one('.spawntime')
                    pet_data["spawn_time"] = spawn.get_text(strip=True) if spawn else "N/A"
                
                categories[category].append(pet_data)
                
        except Exception as e:
            print(f"Error scraping {category}: {str(e)}")
    
    return categories

if __name__ == "__main__":
    pet_data = scrape_pets()
    with open('petopia_data.json', 'w', encoding='utf-8') as f:
        json.dump(pet_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {sum(len(v) for v in pet_data.values())} pets")
