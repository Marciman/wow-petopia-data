import json

with open('petopia_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lua_output = """-- Auto-generated pet data
HRT_Data = {
    pets = {
"""

for category, pets in data.items():
    for pet in pets:
        lua_output += f"""        {{
            name = "{pet['name']}",
            family = "{pet['family']}",
            category = "{category}",
            image = "{pet['image']}",
            locations = {{\n"""
        
        for loc in pet["locations"]:
            lua_output += f"""                {{
                    zone = "{loc['zone']}",
                    coords = "{loc['coords']}",
                    spawn_time = "{loc['spawn_time']}"
                }},\n"""
        
        lua_output += "            }\n        },\n"

lua_output += """    }
}
return HRT_Data
"""

with open('HRT_Data.lua', 'w', encoding='utf-8') as f:
    f.write(lua_output)
