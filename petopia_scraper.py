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
        
        for pet in soup.select('.petlisting'):
            name = pet.select_one('.petname a')
            family = pet.select_one('.family')
            location = pet.select_one('.location')
            image = pet.select_one('.petimage img')
            
            if not all([name, family, location, image]):
                continue
                
            pet_data = {
                "name": name.text.strip(),
                "family": family.text.strip(),
                "zone": location.text.strip(),
                "image": urljoin(BASE_URL, image['src'])
            }
            
            if category == "elite":
                spawn = pet.select_one('.spawntime')
                pet_data["spawn_time"] = spawn.text.strip() if spawn else "N/A"
            
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
