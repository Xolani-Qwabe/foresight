import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

SEASON = 2025  # Change to 2026 when the season page exists
BASE = "https://www.basketball-reference.com"
BOX_BASE = f"{BASE}/boxscores"
OUT = Path("data")
OUT.mkdir(exist_ok=True)

CHECKPOINT = OUT / "completed_games.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (NBA data scraper)"
}

REQUEST_DELAY = 3  # seconds between each game

# ============================================================
# UTILITIES
# ============================================================

def flatten_columns(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[1] if c[1] else c[0] for c in df.columns]
    return df

def normalize_player_schema(df):
    df = flatten_columns(df)

    if "Starters" in df.columns:
        df = df.rename(columns={"Starters": "player"})
    elif "Player" in df.columns:
        df = df.rename(columns={"Player": "player"})
    elif "Unnamed: 0" in df.columns:
        df = df.rename(columns={"Unnamed: 0": "player"})

    if "-additional" in df.columns:
        df = df.rename(columns={"-additional": "player_id"})

    return df

def split_players_and_team(df):
    df["player"] = df["player"].astype(str)

    team = df[df["player"] == "Team Totals"]
    players = df[(~df["player"].str.contains("Did Not", na=False)) &
                 (df["player"] != "Team Totals")]
    return players, team

# ============================================================
# SEASON DISCOVERY
# ============================================================

def get_season_game_ids(season):
    url = f"{BASE}/leagues/NBA_{season}_games.html"
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    game_ids = set()
    # Grab all boxscore links directly
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/boxscores/") and href.endswith(".html"):
            gid = href.split("/")[-1].replace(".html", "")
            game_ids.add(gid)

    if not game_ids:
        print("⚠️ No game IDs found! Check the season page URL or HTML structure.")

    return sorted(game_ids)

# ============================================================
# CHECKPOINTING
# ============================================================

def load_completed():
    if CHECKPOINT.exists():
        return set(pd.read_csv(CHECKPOINT)["game_id"])
    return set()

def save_completed(game_id):
    df = pd.DataFrame([[game_id]], columns=["game_id"])
    df.to_csv(CHECKPOINT, mode="a", header=not CHECKPOINT.exists(), index=False)

# ============================================================
# SCRAPERS
# ============================================================

def scrape_quarters(game_id):
    url = f"{BOX_BASE}/{game_id}.html"
    tables = pd.read_html(url)
    q = tables[0]
    q["game_id"] = game_id
    q.to_csv(OUT / f"{game_id}_quarters.csv", index=False)
    print(f"✔ Quarters: {game_id}")

def scrape_boxscores(game_id):
    url = f"{BOX_BASE}/{game_id}.html"
    tables = pd.read_html(url)

    basic_players, basic_team = [], []
    adv_players, adv_team = [], []

    for df in tables:
        df = normalize_player_schema(df)

        if "TS%" in df.columns:  # Advanced stats
            p, t = split_players_and_team(df)
            adv_players.append(p)
            adv_team.append(t)
        elif "FG" in df.columns and "PTS" in df.columns:  # Basic stats
            p, t = split_players_and_team(df)
            basic_players.append(p)
            basic_team.append(t)

    if adv_players:
        pd.concat(adv_players).assign(game_id=game_id).to_csv(
            OUT / f"{game_id}_advanced_players.csv", index=False
        )
        pd.concat(adv_team).assign(game_id=game_id).to_csv(
            OUT / f"{game_id}_advanced_team.csv", index=False
        )

    if basic_players:
        pd.concat(basic_players).assign(game_id=game_id).to_csv(
            OUT / f"{game_id}_basic_players.csv", index=False
        )
        pd.concat(basic_team).assign(game_id=game_id).to_csv(
            OUT / f"{game_id}_basic_team.csv", index=False
        )

    print(f"✔ Boxscores: {game_id}")

def scrape_game(game_id):
    scrape_quarters(game_id)
    scrape_boxscores(game_id)

# ============================================================
# MAIN
# ============================================================

def main():
    print(f"Discovering NBA {SEASON} games...")
    all_games = get_season_game_ids(SEASON)
    completed = load_completed()
    pending = [g for g in all_games if g not in completed]

    print(f"Total games: {len(all_games)}")
    print(f"Remaining: {len(pending)}")

    for i, gid in enumerate(pending, 1):
        try:
            print(f"[{i}/{len(pending)}] Scraping {gid}")
            scrape_game(gid)
            save_completed(gid)
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(f"FAILED {gid}: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
