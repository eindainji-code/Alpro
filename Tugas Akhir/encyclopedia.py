import json
import time
import os

with open("data/enemies.json", "r") as f:
    enemies = json.load(f)

def flatten(data: dict) -> list:
    #Mengubah nested enemies.json menjadi list flat agar mudah di search dan di sort
    result = []
    for tier, enemy_dict in data.items():
        for name, stats in enemy_dict.items():
            entry = {
                "name": name,
                "tier": tier,
                "hp": stats["hp"],
                "atk": stats["atk"],
                "def": stats["def"]
            }
            result.append(entry)
    return result

#LINEAR SEARCH (pencarian sebagian nama/partial match)

def linear_search(enemy_list: list, query: str) -> list:
    query_lower = query.lower().strip()
    results = []
 
    for enemy in enemy_list:
        if query_lower in enemy["name"].lower():  # partial match
            results.append(enemy)
 
    return results

#BINARY SEARCH (pencarian nama persis/exact match)