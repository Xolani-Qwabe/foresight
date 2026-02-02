import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ---------------- CONFIG ----------------
BASE_DIR = "nba_rosters"
WAIT_SECONDS = 3
# --------------------------------------

NBA_TEAMS = {
    "ATL": "atl/atlanta-hawks",
    "BOS": "bos/boston-celtics",
    "BKN": "bkn/brooklyn-nets",
    "CHA": "cha/charlotte-hornets",
    "CHI": "chi/chicago-bulls",
    "CLE": "cle/cleveland-cavaliers",
    "DAL": "dal/dallas-mavericks",
    "DEN": "den/denver-nuggets",
    "DET": "det/detroit-pistons",
    "GSW": "gs/golden-state-warriors",
    "HOU": "hou/houston-rockets",
    "IND": "ind/indiana-pacers",
    "LAC": "lac/la-clippers",
    "LAL": "lal/los-angeles-lakers",
    "MEM": "mem/memphis-grizzlies",
    "MIA": "mia/miami-heat",
    "MIL": "mil/milwaukee-bucks",
    "MIN": "min/minnesota-timberwolves",
    "NOP": "no/new-orleans-pelicans",
    "NYK": "ny/new-york-knicks",
    "OKC": "okc/oklahoma-city-thunder",
    "ORL": "orl/orlando-magic",
    "PHI": "phi/philadelphia-76ers",
    "PHX": "phx/phoenix-suns",
    "POR": "por/portland-trail-blazers",
    "SAC": "sac/sacramento-kings",
    "SAS": "sa/san-antonio-spurs",
    "TOR": "tor/toronto-raptors",
    "UTA": "utah/utah-jazz",
    "WAS": "wsh/washington-wizards"
}

def slugify(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "_")
        .replace(".", "")
        .replace("'", "")
    )

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def scrape_team_roster(driver, team_code, team_path):
    url = f"https://www.espn.com/nba/team/roster/_/name/{team_path}"
    print(f"Scraping {team_code} -> {url}")

    driver.get(url)
    time.sleep(WAIT_SECONDS)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    team_name_tag = soup.find("h1")
    team_name = team_name_tag.text.strip() if team_name_tag else team_code
    team_slug = slugify(team_name)

    team_dir = os.path.join(BASE_DIR, team_slug)
    os.makedirs(team_dir, exist_ok=True)

    roster_table = soup.find("table")
    if not roster_table:
        print(f"Roster table not found for {team_name}")
        return []

    players = []

    # ✅ FIXED LOOP
    for row in roster_table.select("tbody tr"):
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        img = cols[0].find("img")
        name_link = cols[1].find("a")

        if not img or not name_link:
            continue

        img_url = img.get("src")
        player_name = name_link.text.strip()

        if not img_url or "/i/headshots/nba/players/" not in img_url:
            continue

        filename = f"{slugify(player_name)}.png"
        file_path = os.path.join(team_dir, filename)

        players.append({
            "team": team_name,
            "player": player_name,
            "image_url": img_url,
            "file_path": file_path
        })

    # download images
    for p in players:
        if not os.path.exists(p["file_path"]):
            try:
                r = requests.get(p["image_url"], timeout=10)
                r.raise_for_status()
                with open(p["file_path"], "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"Failed {p['player']}: {e}")

    # save team CSV
    pd.DataFrame(players).to_csv(
        os.path.join(team_dir, "roster_images.csv"),
        index=False
    )

    print(f"Saved {len(players)} players for {team_name}")
    return players

def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    driver = get_driver()

    all_players = []

    try:
        for code, path in NBA_TEAMS.items():
            players = scrape_team_roster(driver, code, path)
            all_players.extend(players)
            time.sleep(2)
    finally:
        driver.quit()

    # save master CSV
    df = pd.DataFrame(all_players)
    df.to_csv(os.path.join(BASE_DIR, "all_nba_rosters.csv"), index=False)

    print("\nDONE")
    print(f"Total players scraped: {len(df)}")

if __name__ == "__main__":
    main()
