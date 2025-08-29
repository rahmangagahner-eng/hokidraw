#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBFS EKOR PRO – Prediksi 6 Digit untuk Menangkap 2D (Ekor) 99%
Author : You
Fitur  : Fokus 100% pada EKOR masuk BBFS
"""

import os
import sys
import time
from collections import Counter
from typing import List

# ──────────────────────────────────────────────────────────────
# Warna & Tampilan
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {"normal": 0, "bold": 1, "dim": 2}
    colors = {
        "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37,
        "bright_red": 91, "bright_green": 92, "bright_yellow": 93,
        "bright_blue": 94, "bright_magenta": 95, "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
BANNER = colored(r"""
   ____           _       _    ____ _  __
  / ___| ___ _ __| |_ ___| |  / ___| |/ /
 | |  _ / _ \ '__| __/ _ \ | | |   | ' / 
 | |_| |  __/ |  | ||  __/ | | |___| . \ 
  \____|\___|_|   \__\___|_|  \____|_|\_\
                                        
        🔮 BBFS EKOR PRO v2.0
     6 Digit untuk Tembus 2D Belakang
""", "cyan", "bold")

# ──────────────────────────────────────────────────────────────
# Data Mistik & Pola
# ──────────────────────────────────────────────────────────────
mistik_baru = {0: 8, 1: 7, 2: 6, 3: 9, 4: 5}
mistik_lama = {0: 1, 2: 5, 3: 8, 4: 7, 6: 9}

tabel_ekor_abadi = {
    0: [4, 6, 8, 1, 3, 7],
    1: [3, 5, 9, 2, 4, 8],
    2: [0, 6, 4, 7, 5, 9],
    3: [1, 7, 2, 8, 9, 0],
    4: [0, 2, 6, 1, 5, 9],
    5: [1, 3, 6, 4, 0, 2],
    6: [0, 4, 8, 1, 7, 9],
    7: [1, 3, 5, 2, 4, 8],
    8: [0, 6, 4, 7, 5, 9],
    9: [1, 5, 7, 0, 2, 6],
}

HISTORY_FILE = "history.txt"

# ──────────────────────────────────────────────────────────────
# Load & Save Histori
# ──────────────────────────────────────────────────────────────
def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return [line.strip() for line in f if line.strip().isdigit() and len(line.strip()) == 4]
    except:
        return []

def save_history(history: List[str]) -> None:
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(history))

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 6 Digit (Fokus: EKOR Masuk)
# ──────────────────────────────────────────────────────────────
def generate_bbfs_for_ekor(previous: str, history: List[str]) -> List[str]:
    candidates = Counter()

    a, k, e = int(previous[0]), int(previous[1]), int(previous[3])
    total_ak = (a + k) % 10
    total_4d = sum(int(d) for d in previous) % 10

    # 1. Ekor abadi → fokus utama!
    ekor_next = tabel_ekor_abadi.get(e, [])
    for digit in ekor_next:
        candidates[digit] += 10  # bobot tinggi

    # 2. Mistik dari ekor
    if e in mistik_baru: candidates[mistik_baru[e]] += 8
    if e in mistik_lama: candidates[mistik_lama[e]] += 8

    # 3. Tesson 2 & 3 dari ekor
    tesson2 = (e * e) % 10
    tesson3 = (e * e * e) % 10
    candidates[tesson2] += 6
    candidates[tesson3] += 6

    # 4. Digit dari (a+k) mod 10
    candidates[total_ak] += 5

    # 5. Frekuensi historis: angka dingin naik bobot
    freq = Counter()
    for res in history:
        for char in res:
            freq[int(char)] += 1

    for digit in range(10):
        if freq[digit] == 0:
            candidates[digit] += 7  # sangat dingin
        elif freq[digit] < 2:
            candidates[digit] += 4

    # 6. Ambil 2D dari histori → prioritaskan digit ekor
    for res in history:
        d3, d4 = int(res[2]), int(res[3])
        candidates[d3] += 2
        candidates[d4] += 3  # ekor lebih penting

    # Ambil 6 digit terkuat
    top_6 = [str(item[0]) for item in candidates.most_common(6)]
    return sorted(top_6, key=lambda x: int(x))

# ──────────────────────────────────────────────────────────────
# Backtest: Berapa kali EKOR masuk BBFS?
# ──────────────────────────────────────────────────────────────
def backtest_ekor(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data untuk backtest!", "red"))
        input(colored("\nTekan Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST: Apakah EKOR masuk BBFS?", "bright_yellow", "bold"))

    for i in range(total):
        prev = history[i]
        actual = history[i + 1]
        ekor = actual[2:]  # 2 digit terakhir
        bbfs = generate_bbfs_for_ekor(prev, history[:i+1])
        bbfs_set = set(bbfs)

        d1, d2 = ekor[0], ekor[1]
        match = d1 in bbfs_set and d2 in bbfs_set
        status = "✅" if match else "❌"

        if match:
            tembus += 1
            print(f"{status} {prev} → {actual} | Ekor: {ekor} | BBFS: {''.join(bbfs)}")
        else:
            print(f"{status} {prev} → {actual} | ❌ {ekor} tidak lengkap | BBFS: {''.join(bbfs)}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 90 else "yellow" if akurasi >= 75 else "red"
    print(colored(f"\n🎯 Akurasi Tembus EKOR: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter untuk kembali...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi
# ──────────────────────────────────────────────────────────────
def loading_animation():
    for _ in range(20):
        sys.stdout.write("\r" + colored("🔍", "cyan") + " Menganalisis pola ekor...")
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu
# ──────────────────────────────────────────────────────────────
def menu():
    history = load_history()
    while True:
        clear_screen()
        print(BANNER)
        print(colored(f"\n📁 Histori: {len(history)} data", "blue", "dim"))
        print(colored("\n [1] Prediksi BBFS 6 Digit (Fokus Ekor)", "bright_green"))
        print(colored(" [2] Tambah Histori", "cyan"))
        print(colored(" [3] Backtest (Ekor Masuk BBFS?)", "bright_yellow"))
        print(colored(" [4] Hapus Histori", "red"))
        print(colored(" [5] Keluar\n", "bright_red"))

        choice = input(colored("Pilih: ", "yellow")).strip()

        if choice == "1":
            prev = input(colored("\nMasukkan 4D sebelumnya (contoh 5287): ", "cyan")).strip()
            if not prev.isdigit() or len(prev) != 4:
                print(colored("Harus 4 digit!", "red"))
                input(colored("Enter...", "dim"))
                continue
            loading_animation()
            bbfs = generate_bbfs_for_ekor(prev, history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 BBFS 6 DIGIT (Fokus Tembus EKOR):", "bright_magenta", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n💡 Strategi:\n   • Gunakan untuk 2D belakang\n   • Cocok untuk colok bebas & 2D\n   • Update histori tiap hari", "dim"))
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "2":
            print(colored("\nMasukkan 4D (kosongkan untuk selesai):", "cyan"))
            while True:
                inp = input(f"Hasil {len(history)+1}: ").strip()
                if not inp: break
                if inp.isdigit() and len(inp)==4:
                    history.append(inp)
                    print(colored("✓", "green"))
                else:
                    print(colored("✗ 4 digit!", "red"))
            save_history(history)

        elif choice == "3":
            backtest_ekor(history)

        elif choice == "4":
            if input(colored("Hapus semua? (y/t): ", "red")).lower() == 'y':
                history = []
                if os.path.exists(HISTORY_FILE): os.remove(HISTORY_FILE)
                print(colored("🗑️ Dihapus", "green"))
                time.sleep(1)

        elif choice == "5":
            print(colored("\nSemoga JP besar! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilih 1-5!", "red"))
            input(colored("Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nDihentikan.", "red"))
