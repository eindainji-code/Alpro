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
#Contoh: query "sl" -> menemukan "Slime"
#query "on" -> menemukan "Laistrygonian", "Nemean Lion"

def linear_search(enemy_list: list, query: str) -> list:
    query_lower = query.lower().strip()
    results = []
 
    for enemy in enemy_list:
        if query_lower in enemy["name"].lower():
            results.append(enemy)
 
    return results

#BINARY SEARCH (pencarian nama persis/exact match)
#Binary Search hanya bisa exact match karena
#bekerja dengan membandingkan nilai tengah list.
#jadi datanya harus diurutkan dulu secara alfabetis

def binary_search(sorted_list: list, query: str) -> dict | None:
    query_lower = query.lower().strip()
    left = 0
    right = len(sorted_list) - 1
 
    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_list[mid]["name"].lower()
 
        if mid_name == query_lower:
            return sorted_list[mid] #Data yang dicari ditemukan
 
        elif mid_name < query_lower:
            left = mid + 1 #Cari di sebelah kiri
 
        else:
            right = mid - 1 #Cari di sebelah kanan
 
    return None #Data yang dicari tidak ditemukan

#INSERTION SORT UNTUK MENGURUTKAN DATA SECARA ALFABETIS
def sort_alphabetically(enemy_list: list) -> list:
    sorted_list = enemy_list.copy()
 
    for i in range(1, len(sorted_list)):
        key = sorted_list[i]
        j = i - 1
 
        while j >= 0 and sorted_list[j]["name"].lower() > key["name"].lower():
            sorted_list[j + 1] = sorted_list[j]
            j -= 1
 
        sorted_list[j + 1] = key
 
    return sorted_list

#TAMPILAN DI LAYAR
TIER_LABEL = {
    "tier_1":    "Tier 1",
    "tier_2":    "Tier 2",
    "tier_3":    "Tier 3",
    "boss":      "Boss",
    "final_boss":"Final Boss"
}
 
def display_enemy(enemy: dict):
    tier = TIER_LABEL.get(enemy["tier"], enemy["tier"])
    print(f"\n  ┌─────────────────────────")
    print(f"  │  {enemy['name']}  [{tier}]")
    print(f"  ├─────────────────────────")
    print(f"  │  HP  : {enemy['hp']}")
    print(f"  │  ATK : {enemy['atk']}")
    print(f"  │  DEF : {enemy['def']}")
    print(f"  └─────────────────────────")
 
 
def display_results(results: list, query: str, algo: str):
    print(f"\n[{algo}] Result \"{query}\":")
 
    if not results:
        print("Enemy not found.")
        return
 
    print(f"  {len(results)} enemy found.")
    for enemy in results:
        display_enemy(enemy)

#FUNGSI UTAMA ENSIKLOPEDIA
def encyclopedia():
    all_enemies   = flatten(enemies)
    sorted_enemies = sort_alphabetically(all_enemies)  #Untuk binary search
 
    print("\n" + "=" * 40)
    print("ENEMY ENCYCLOPEDIA")
    print("=" * 40)
    print("Enter the enemy's name to search.")
    print("Type 'list' to see all enemies.")
    print("Type 'exit' to exit.")
    print("=" * 40)
 
    while True:
        query = input("\nFind enemy").strip()
 
        if query.lower() == "exit":
            print("\nEnter the enemy's name.")
            break
 
        if query.lower() == "list":
            print("\n=== ALL ENEMIES ===")
            for e in sorted_enemies:
                tier = TIER_LABEL.get(e["tier"], e["tier"])
                print(f"  - {e['name']:<20} [{tier}]")
            continue
 
        if not query:
            print("Please enter the enemy's name.")
            continue
 
        #LINEAR SEARCH - partial match
        linear_results = linear_search(all_enemies, query)
        display_results(linear_results, query, "Linear Search")
 
        #BINARY SEARCH - exact match
        binary_result = binary_search(sorted_enemies, query)
        print(f"\n[Binary Search] Result \"{query}\" (exact match):")
        if binary_result:
            display_enemy(binary_result)
        else:
            print("Enemy not found (use full name for binary search).")
 
        time.sleep(0.5)