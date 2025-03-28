import json

def convert_to_lua():
    with open('petopia_data.json', 'r', encoding='utf-8') as f:
        pets = json.load(f)
    
    lua_output = """-- Auto-generated pet data
HRT_Data = {
    pets = {
"""
    
    for pet in pets:
        lua_output += f"""        {{
            name = "{pet['name']}",
            category = "{pet['category']}",
            family = "{pet['family']}",
            zone = "{pet['zone']}",
            image = "{pet['image']}","""
        
        if 'spawn_time' in pet:
            lua_output += f"""
            spawn_time = "{pet['spawn_time']}","""
        
        lua_output += """
        },
"""
    
    lua_output += """    }
}
return HRT_Data
"""
    
    with open('HRT_Data.lua', 'w', encoding='utf-8') as f:
        f.write(lua_output)

if __name__ == "__main__":
    convert_to_lua()
