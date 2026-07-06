import requests
from bs4 import BeautifulSoup
import json
import re
import os

URL = "https://leagueoflegends.fandom.com/wiki/Essence_Emporium"
OUTPUT_FILE = os.path.join("data", "chromas.json")

def scrape():
    resp = requests.get(URL)
    soup = BeautifulSoup(resp.text, "html.parser")

    # The chroma table is usually inside a div with class "tabbertab" and title "Chromas"
    # It may be multiple tables (one per event). We'll grab the latest one.
    chroma_tables = soup.select("table.wikitable.sortable")

    chromas = []
    for table in chroma_tables:
        for row in table.select("tr")[1:]:  # skip header
            cols = row.find_all("td")
            if len(cols) < 4:
                continue
            # Typical columns: Champion, Skin, Chroma Name, Image (then possibly others)
            champion = cols[0].get_text(strip=True)
            skin = cols[1].get_text(strip=True)
            name = cols[2].get_text(strip=True)
            img_tag = cols[3].find("img")
            image_url = img_tag["src"] if img_tag else ""
            # Fix relative URLs
            if image_url and image_url.startswith("/"):
                image_url = "https://leagueoflegends.fandom.com" + image_url

            chromas.append({
                "champion": champion,
                "skin": skin,
                "name": name,
                "image": image_url
            })

    # If no chromas found, keep old data (don't overwrite with empty list)
    if not chromas:
        print("Warning: No chromas found – keeping existing data.")
        return

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chromas, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(chromas)} chromas.")

if __name__ == "__main__":
    scrape()