import json

with open('petopia_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lua_output = """-- Automatisch generierte Pet-Daten
HRT_Data = {
    categories = {
        "collector", "rare", "looks", "elite"
    },
    pets = {
"""

for category, pets in data.items():
    for pet in pets:
        lua_output += f"        {{\n"
        lua_output += f"            name = \"{pet['name']}\",\n"
        lua_output += f"            category = \"{pet['category']}\",\n"
        lua_output += f"            family = \"{pet['family']}\",\n"
        lua_output += f"            zone = \"{pet['location']}\",\n"
        lua_output += f"            image = \"{pet['image']}\",\n"
        
        if 'spawn_time' in pet:
            lua_output += f"            spawn_time = \"{pet['spawn_time']}\",\n"
        if 'taming_notes' in pet:
            lua_output += f"            notes = \"{pet['taming_notes']}\",\n"
        
        lua_output += "        },\n"

lua_output += """    }
}
return HRT_Data
"""

with open('HRT_Data.lua', 'w', encoding='utf-8') as f:
    f.write(lua_output)