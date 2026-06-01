import json
import os
import screen as s

def load_players(fpath = "data/player.json"): #Memuat semua data pemain dari file JSON
    if not os.path.exists(fpath):
        print("File player.json tidak ditemukan.")
        return []
    
    with open(fpath, "r") as f:
        players = json.load(f)

    return players

#===================================================
#ALGORITMA SORTING = INSERTION SORT (Untuk data kecil)
#Mengurutkan pemain berdasarkan floor tertinggi yang dicapai
#Jika floor sama, pemain dengan level karakter lebih tinggi akan
#Menempati peringkat lebih atas
#Jika masih sama, pemain dengan EXP lebih tinggi menang
#===================================================

def lb_insertion(players: list) -> list:

    """
    Mengurutkan list pemain menggunakan insertion sort
    Kriteria utama: floor (descending)
    Kriteria kedua: character_level (descending)
    Kriteria ketiga: exp (descending)
    """
    sorted_pl = players.copy() #Menyalin list asli agar tidak termodifikasi

    for i in range (1, len(sorted_pl)):
        key = sorted_pl[i]
        j = i - 1

        #Bandingkan ketiga kriteria sekaligus
        while j >= 0 and _compare(sorted_pl[j], key) < 0:
            sorted_pl[j + 1] = sorted_pl[j]
            j -= 1

        sorted_pl[j + 1] = key

    return sorted_pl

def _compare(a: dict, b: dict) -> int:
    """
    Fungsi untuk membandingkan dua pemain
    Mengembalikan nilai positif jika a > b (a lebih tinggi di leaderboard).
    Mengembalikan nilai negatif jika a < b
    Mengembalikan 0 jika setara
    """

    #Kriteria utama: floor
    if a.get("floor", 1) != b.get("floor", 1):
        return a.get("floor", 1) - b.get("floor", 1)
    
    #Kriteria kedua: level karakter
    if a.get("character_level", 1) != b.get("character_level", 1):
        return a.get("character_level", 1) - b.get("character_level", 1)
    
    #Kriteria ketiga: EXP
    if a.get("exp", 0) != b.get("exp", 0):
        return a.get("exp", 0) - b.get("exp", 0)

    if a.get("name", "") < b.get("name", ""):
        return 1

    if a.get("name", "") > b.get("name", ""):
        return -1

    return 0

#ALGORITMA MERGE SORT: UNTUK DATA LEBIH BESAR AGAR LEBIH EFISIEN

def merge_lb(players: list) -> list:
    if len(players) <= 1:
        return players.copy()
 
    mid = len(players) // 2
    left = merge_lb(players[:mid])
    right = merge_lb(players[mid:])
 
    return _merge(left, right)
 
 
def _merge(left: list, right: list) -> list:
    result = []
    i = j = 0
 
    while i < len(left) and j < len(right):
        if _compare(left[i], right[j]) >= 0:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
 
    result.extend(left[i:])
    result.extend(right[j:])
    return result

#MENAMPILKAN LEADERBOARD DI TERMINAL

def display_lb(players: list, merge_sort: bool = False):
    if not players:
        print("Player data isn't available.")
        return
    
    if merge_sort:
        sorted_pl = merge_lb(players)
        algo_name = "Merge Sort"
    else:
        sorted_pl = lb_insertion(players)
        algo_name = "Insertion Sort"

    print("\n" + "=" * 62)
    print(f"{'LEADERBOARD':^62}")
    print(f"{'(Sorted with ' + algo_name + ')':^62}")
    print("=" * 62)
    print(
    f"{'TITLE':<10}"
    f"{'RANK':<6}"
    f"{'NAMA':<13}"
    f"{'CLASS':<13}"
    f"{'FLOOR':<9}"
    f"{'LVL':<7}"
    f"{'EXP':<7}"
)
    print("-" * 62)

    best_pl = {1: "GOAT", 2: "AMAZING", 3: "NICE"}

    for rank, player in enumerate(sorted_pl, start=1):
        best = best_pl.get(rank, "  ")
        print(
            f"{best:<10}"
            f"{rank:<6}"
            f"{player.get('name', '?'):<13}"
            f"{player.get('class', '?'):<13}"
            f"{player.get('floor', 1):<9}"
            f"{player.get('character_level', 1):<7}"
            f"{player.get('exp', 0):<7}"
        )

    print("=" * 62)