import time
import re
import os
import unicodedata
import hashlib
import csv
import random
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# ============================================================
# CONFIG
# ============================================================

SEASON_YEAR = 2026
BASE_DIR = "/home/thabi/projects/data_scrapper/nba_2025_26_boxscores"
CHECKPOINT_FILE = os.path.join(BASE_DIR, "checkpoint.csv")

RESTART_DRIVER_EVERY = 25
MAX_RETRIES = 4

# ---------------- DATE CONTROL ----------------
START_DATE_STR = "2026-01-01"   # inclusive
END_DATE_STR   = "2026-01-20"   # inclusive

START_DATE = datetime.strptime(START_DATE_STR, "%Y-%m-%d").date()
END_DATE   = datetime.strptime(END_DATE_STR, "%Y-%m-%d").date()
# ---------------------------------------------

MONTHS = [
    "", "-october", "-november", "-december",
    "-january", "-february", "-march", "-april",
    "-may", "-june"
]

os.makedirs(BASE_DIR, exist_ok=True)

if not os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["game_id"])

# ============================================================
# DRIVER
# ============================================================

def get_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=Service(), options=options)
    driver.set_page_load_timeout(30)
    return driver

driver = get_driver()

# ============================================================
# CHECKPOINTING
# ============================================================

def load_completed_games():
    with open(CHECKPOINT_FILE, "r") as f:
        return {
            row[0] for row in csv.reader(f)
            if row and row[0] != "game_id"
        }

def mark_game_complete(game_id):
    with open(CHECKPOINT_FILE, "a", newline="") as f:
        csv.writer(f).writerow([game_id])

# ============================================================
# HELPERS
# ============================================================

def safe_get(url):
    global driver
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            driver.get(url)
            time.sleep(random.uniform(2, 3))
            return True
        except WebDriverException:
            try:
                driver.quit()
            except:
                pass
            time.sleep(5 * attempt)
            driver = get_driver()
    return False

def sanitize(col):
    col = unicodedata.normalize("NFKD", str(col)).lower()
    col = re.sub(r"\s+", "_", col)
    col = re.sub(r"[^a-z0-9_]", "", col)
    return col if not col[0].isdigit() else f"c_{col}"

def extract_game_date_from_url(url):
    try:
        return datetime.strptime(
            url.split("/")[-1][:8], "%Y%m%d"
        ).date()
    except:
        return None

def get_resume_date(completed_games):
    dates = []
    for gid in completed_games:
        try:
            dates.append(datetime.strptime(gid[:8], "%Y%m%d").date())
        except:
            pass
    return max(dates) + timedelta(days=1) if dates else START_DATE

def extract_tables():
    tables = []
    for t in driver.find_elements(By.TAG_NAME, "table"):
        tid = t.get_attribute("id")
        if tid and tid.startswith("box-"):
            tables.append((t.get_attribute("outerHTML"), tid))
    return tables

def extract_home_away_teams():
    teams = []
    for t in driver.find_elements(By.CSS_SELECTOR, "table[id^='box-']"):
        m = re.search(r"box-([A-Z]{3})", t.get_attribute("id"))
        if m and m.group(1) not in teams:
            teams.append(m.group(1))
    return teams if len(teams) >= 2 else ("UNK", "UNK")

def make_player_uid(player, team):
    return hashlib.sha1(f"{player}_{team}_{SEASON_YEAR}".encode()).hexdigest()

# ============================================================
# TABLE SAVE
# ============================================================

def save_table(html, table_id, game_id, game_date, away, home):
    df = pd.read_html(StringIO(html))[0]

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join(filter(None, map(str, c))) for c in df.columns]

    df.columns = [sanitize(c) for c in df.columns]

    player_col = next((c for c in df.columns if "player" in c), None)
    if not player_col:
        return

    df[player_col] = df[player_col].astype(str).str.replace(r"[*†‡§]", "", regex=True)
    df = df[df[player_col].str.strip() != ""]

    team = re.search(r"box-([A-Z]{3})", table_id).group(1)

    df["player_uid"] = df[player_col].apply(lambda p: make_player_uid(p, team))
    df["team"] = team
    df["opponent"] = away if team == home else home
    df["game_id"] = game_id
    df["game_date"] = game_date

    out_dir = os.path.join(BASE_DIR, "tables", table_id)
    os.makedirs(out_dir, exist_ok=True)
    df.to_csv(os.path.join(out_dir, f"{game_id}.csv"), index=False)

# ============================================================
# SCHEDULE SCRAPE
# ============================================================

box_score_links = []

for m in MONTHS:
    safe_get(
        f"https://www.basketball-reference.com/leagues/NBA_{SEASON_YEAR}_games{m}.html"
    )
    for l in driver.find_elements(By.PARTIAL_LINK_TEXT, "Box Score"):
        box_score_links.append(l.get_attribute("href"))

box_score_links = sorted(set(box_score_links))

completed_games = load_completed_games()
resume_date = get_resume_date(completed_games)

print(f"Resuming from: {resume_date}")
print(f"Stopping at:   {END_DATE}")

# ============================================================
# MAIN LOOP
# ============================================================

for i, url in enumerate(box_score_links, 1):
    game_date = extract_game_date_from_url(url)
    if not game_date:
        continue

    if game_date < resume_date or game_date > END_DATE:
        continue

    game_id = url.split("/")[-1].replace(".html", "")
    if game_id in completed_games:
        continue

    if i % RESTART_DRIVER_EVERY == 0:
        driver.quit()
        driver = get_driver()

    if not safe_get(url):
        continue

    away, home = extract_home_away_teams()

    for html, tid in extract_tables():
        if "basic" in tid:
            save_table(html, tid, game_id, game_date, away, home)

    mark_game_complete(game_id)
    time.sleep(random.uniform(1, 2))

driver.quit()
print("SCRAPE COMPLETE")
