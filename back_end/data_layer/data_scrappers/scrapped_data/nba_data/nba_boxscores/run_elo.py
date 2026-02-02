import pandas as pd
import math
from pathlib import Path
import numpy as np
from datetime import datetime
import unicodedata
import os

# =========================
# CONFIGURATION
# =========================
DATA_DIR = Path("./unified")
OUTPUT_DIR = Path("./elo_output")
OUTPUT_DIR.mkdir(exist_ok=True)

RESULTS_DIR = OUTPUT_DIR / "results"
HISTORY_DIR = OUTPUT_DIR / "history"
LOGS_DIR = OUTPUT_DIR / "logs"

RESULTS_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

print(f"Output will be saved to: {OUTPUT_DIR}")

# NBA PRIORS (more balanced)
NBA_TEAM_PRIORS = {
    'BOS': 1600, 'DEN': 1600, 'OKC': 1580, 'MIN': 1580, 'MIL': 1590,
    'PHI': 1580, 'LAC': 1570, 'NYK': 1570, 'DAL': 1570, 'PHO': 1560,
    'CLE': 1550, 'ORL': 1540, 'IND': 1540, 'LAL': 1530, 'GSW': 1520,
    'SAC': 1520, 'MIA': 1520, 'NOP': 1510, 'ATL': 1500, 'CHI': 1500,
    'SAS': 1510, 'HOU': 1490, 'MEM': 1490, 'UTA': 1480, 'BRK': 1480,
    'TOR': 1470, 'POR': 1460, 'CHO': 1450, 'DET': 1440, 'WAS': 1430
}

SUPERSTAR_PRIORS = {
    'Nikola Jokic': 1850, 'Giannis Antetokounmpo': 1820, 'Luka Doncic': 1820,
    'Jayson Tatum': 1780, 'Shai Gilgeous-Alexander': 1800, 'Joel Embiid': 1780,
    'Anthony Edwards': 1760, 'Stephen Curry': 1750, 'Kevin Durant': 1750,
    'LeBron James': 1730, 'Devin Booker': 1720, 'Kawhi Leonard': 1720,
    'Damian Lillard': 1710, 'Donovan Mitchell': 1710, 'Anthony Davis': 1720,
    'Victor Wembanyama': 1750,  # High but realistic for a rookie sensation
    'Ja Morant': 1700, 'Zion Williamson': 1670, 'Paolo Banchero': 1680,
    'Chet Holmgren': 1680, 'Jaren Jackson Jr.': 1670, 'Jaylen Brown': 1680,
    'Bam Adebayo': 1660, 'Domantas Sabonis': 1660, 'DeAaron Fox': 1660,
    'Kyrie Irving': 1700, 'James Harden': 1690, 'Karl-Anthony Towns': 1680,
    'Trae Young': 1690, 'Jalen Brunson': 1690, 'Tyrese Haliburton': 1720,
}

# Base values
INITIAL_TEAM_ELO = 1500
INITIAL_PLAYER_ELO = 1500
SEASON_REGRESSION = 0.75  # More regression for stability
HOME_ADVANTAGE = 100
TEAM_K = 16  # Lower K for more stability
PLAYER_K = 10  # Lower K for more stability
MIN_MINUTES = 10

# =========================
# HELPER FUNCTIONS
# =========================
def normalize_name(name):
    if pd.isna(name):
        return ""
    name = str(name).strip()
    name = ' '.join(name.split())
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    
    corrections = {
        'Nikola Jokić': 'Nikola Jokic', 'Luka Dončić': 'Luka Doncic',
        'Bogdan Bogdanović': 'Bogdan Bogdanovic', 'Dāvis Bertāns': 'Davis Bertans',
        'Kristaps Porziņģis': 'Kristaps Porzingis', 'Jonas Valančiūnas': 'Jonas Valanciunas',
        'Nikola Vučević': 'Nikola Vucevic', 'Goran Dragić': 'Goran Dragic',
        'Dario Šarić': 'Dario Saric', 'Alperen Şengün': 'Alperen Sengun',
    }
    return corrections.get(name, name)

def expected_score(r_a, r_b):
    return 1 / (1 + 10 ** ((r_b - r_a) / 400))

def margin_multiplier(diff):
    return math.log(abs(diff) + 1)

def parse_minutes(m):
    if isinstance(m, str) and ":" in m:
        mm, ss = m.split(":")
        return float(mm) + float(ss) / 60
    return float(m)

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    with open(LOGS_DIR / "elo_calculation.log", 'a') as f:
        f.write(log_message + '\n')
    print(message)

# =========================
# MAIN EXECUTION
# =========================
def main():
    write_log("="*60)
    write_log("NBA ELO RATING SYSTEM")
    write_log("="*60)
    
    # Load data
    write_log("Loading data...")
    basic = pd.read_csv(DATA_DIR / "basic_boxscore.csv")
    advanced = pd.read_csv(DATA_DIR / "advanced_boxscore.csv")
    four = pd.read_csv(DATA_DIR / "four_factors.csv")
    
    # Normalize names
    basic['player'] = basic['player'].apply(normalize_name)
    if 'player' in advanced.columns:
        advanced['player'] = advanced['player'].apply(normalize_name)
    
    # Extract season
    if 'game_date' in basic.columns:
        basic['game_date'] = pd.to_datetime(basic['game_date'], errors='coerce')
        basic['season'] = basic['game_date'].apply(
            lambda x: x.year if not pd.isna(x) and x.month >= 10 else x.year - 1 if not pd.isna(x) else 2024
        )
    else:
        basic['season'] = 2024
    
    # Prepare minutes
    if 'mp' in basic.columns:
        basic["minutes"] = basic["mp"].apply(parse_minutes)
    elif 'minutes' in basic.columns:
        basic["minutes"] = basic["minutes"].apply(parse_minutes)
    
    # Points column
    points_col = next((col for col in ['pts', 'points', 'PTS', 'Points'] if col in basic.columns), 'pts')
    basic = basic.rename(columns={points_col: 'points'})
    
    # Team points
    team_points = (
        basic.groupby(["game_id", "team", "home_team", "away_team", "season"])
        .agg(points=("points", "sum"))
        .reset_index()
    )
    points_pivot = team_points.pivot(index="game_id", columns="team", values="points")
    
    # Four factors
    column_mapping = {'eFG%': 'efg_pct', 'TOV%': 'tov_pct', 'ORB%': 'orb_pct', 'FT/FGA': 'ft_rate', 'pace': 'pace'}
    four = four.rename(columns=column_mapping)
    for col in ['efg_pct', 'tov_pct', 'orb_pct', 'ft_rate', 'pace']:
        if col not in four.columns:
            four[col] = 100 if col == 'pace' else 0.0
    
    ff_agg = four.groupby(["game_id", "team"]).agg({
        "efg_pct": "mean", "tov_pct": "mean", "orb_pct": "mean", 
        "ft_rate": "mean", "pace": "mean"
    }).reset_index()
    ff_pivot = ff_agg.set_index(['game_id', 'team'])
    
    # Player data
    if 'bpm' not in advanced.columns:
        advanced['bpm'] = 0
    if 'plus_minus' not in advanced.columns and 'pm' in advanced.columns:
        advanced['plus_minus'] = advanced['pm']
    
    merge_cols = ["game_id", "player", "team"]
    advanced_cols = [col for col in ["bpm", "plus_minus", "pm"] if col in advanced.columns]
    
    players = basic.merge(
        advanced[merge_cols + advanced_cols],
        on=merge_cols,
        how="left"
    )
    players["bpm"] = players["bpm"].fillna(0)
    players["plus_minus"] = players["plus_minus"].fillna(0)
    
    # Initialize Elo
    team_elo = {team: NBA_TEAM_PRIORS.get(team, INITIAL_TEAM_ELO) for team in team_points['team'].unique()}
    player_elo = {}
    for player in players['player'].unique():
        player_elo[player] = SUPERSTAR_PRIORS.get(player, INITIAL_PLAYER_ELO)
    
    # History tracking
    team_history = []
    player_history = []
    current_season = None
    
    # Process games
    game_ids = sorted(players['game_id'].unique())
    total_games = len(game_ids)
    write_log(f"Processing {total_games} games...")
    
    for idx, game_id in enumerate(game_ids):
        if idx % 500 == 0 and idx > 0:
            write_log(f"Processed {idx}/{total_games} games...")
        
        gp = players[players['game_id'] == game_id]
        if gp.empty:
            continue
            
        season = gp["season"].iloc[0]
        
        # Season transition
        if season != current_season and current_season is not None:
            write_log(f"Season change: {current_season} -> {season}")
            for t in team_elo:
                prior = NBA_TEAM_PRIORS.get(t, INITIAL_TEAM_ELO)
                team_elo[t] = prior + (team_elo[t] - prior) * SEASON_REGRESSION
            for p in player_elo:
                prior = SUPERSTAR_PRIORS.get(p, INITIAL_PLAYER_ELO)
                player_elo[p] = prior + (player_elo[p] - prior) * SEASON_REGRESSION
        current_season = season
        
        teams = gp["team"].unique()
        if len(teams) != 2:
            continue
        
        home = gp["home_team"].iloc[0]
        away = gp["away_team"].iloc[0]
        
        # Get actual score
        if game_id in points_pivot.index:
            try:
                actual_diff = points_pivot.loc[game_id, home] - points_pivot.loc[game_id, away]
            except:
                actual_diff = 0
        else:
            actual_diff = 0
        
        # Get four factors
        ff_margin = 0
        try:
            home_data = ff_pivot.loc[(game_id, home)]
            away_data = ff_pivot.loc[(game_id, away)]
            efg = home_data["efg_pct"] - away_data["efg_pct"]
            tov = away_data["tov_pct"] - home_data["tov_pct"]
            orb = home_data["orb_pct"] - away_data["orb_pct"]
            ftr = home_data["ft_rate"] - away_data["ft_rate"]
            home_pace = home_data["pace"]
            ff_margin = (0.4 * efg + 0.25 * tov + 0.2 * orb + 0.15 * ftr) * home_pace / 100
        except:
            ff_margin = 0
        
        # Team Elo update
        home_rating = team_elo[home] + HOME_ADVANTAGE
        away_rating = team_elo[away]
        exp_home = expected_score(home_rating, away_rating)
        score_home = 1 if actual_diff > 0 else 0.5 if actual_diff == 0 else 0
        
        # Use blended margin
        blended_diff = 0.7 * actual_diff + 0.3 * ff_margin
        delta = TEAM_K * (score_home - exp_home) * margin_multiplier(abs(blended_diff))
        
        team_elo[home] += delta
        team_elo[away] -= delta
        
        team_history.append([game_id, home, team_elo[home], season])
        team_history.append([game_id, away, team_elo[away], season])
        
        # Player Elo update
        gp_filtered = gp[gp["minutes"] >= MIN_MINUTES].copy()
        if gp_filtered.empty:
            continue
        
        # Calculate player impact
        gp_filtered["pm_per_min"] = gp_filtered["plus_minus"] / gp_filtered["minutes"].clip(lower=0.1)
        gp_filtered["opp_elo"] = gp_filtered["team"].apply(
            lambda t: team_elo[away] if t == home else team_elo[home]
        )
        gp_filtered["pm_adj"] = gp_filtered["pm_per_min"] * (gp_filtered["opp_elo"] / 1500)
        
        # Normalize metrics
        for col in ['pm_adj', 'bpm']:
            std_val = gp_filtered[col].std()
            mean_val = gp_filtered[col].mean()
            if std_val > 0:
                gp_filtered[f"{col}_z"] = (gp_filtered[col] - mean_val) / std_val
            else:
                gp_filtered[f"{col}_z"] = 0
        
        # Combine metrics
        gp_filtered["impact"] = 0.6 * gp_filtered["pm_adj_z"] + 0.4 * gp_filtered["bpm_z"]
        
        # Update player Elo
        total_minutes = gp_filtered["minutes"].sum()
        for _, row in gp_filtered.iterrows():
            pid = row["player"]
            minutes_played = row["minutes"]
            
            # Weight by minutes played
            weight = (minutes_played / total_minutes) ** 0.7
            
            # Cap impact to prevent extreme changes
            capped_impact = max(-2, min(2, row["impact"]))
            
            player_elo[pid] += PLAYER_K * weight * capped_impact
            
            # Keep within reasonable bounds
            player_elo[pid] = max(1200, min(2000, player_elo[pid]))
            
            player_history.append([game_id, pid, player_elo[pid], season])
    
    # Final adjustments
    write_log("\nApplying final adjustments...")
    
    # Save results
    write_log("Saving results...")
    
    # Team Elo
    team_elo_df = pd.DataFrame(list(team_elo.items()), columns=["team", "elo"])
    team_elo_df = team_elo_df.sort_values("elo", ascending=False)
    team_elo_df['rank'] = range(1, len(team_elo_df) + 1)
    team_elo_df.to_csv(RESULTS_DIR / "team_elo_final.csv", index=False)
    
    # Player Elo
    player_elo_df = pd.DataFrame(list(player_elo.items()), columns=["player", "elo"])
    player_elo_df = player_elo_df.sort_values("elo", ascending=False)
    player_elo_df['rank'] = range(1, len(player_elo_df) + 1)
    player_elo_df.to_csv(RESULTS_DIR / "player_elo_final.csv", index=False)
    
    # Save top players
    top_players = player_elo_df.head(20)
    top_players.to_csv(RESULTS_DIR / "top_20_players.csv", index=False)
    
    # Save history
    if team_history:
        team_hist_df = pd.DataFrame(team_history, columns=["game_id", "team", "elo", "season"])
        team_hist_df.to_csv(HISTORY_DIR / "team_elo_history.csv", index=False)
    
    if player_history:
        player_hist_df = pd.DataFrame(player_history, columns=["game_id", "player", "elo", "season"])
        player_hist_df.to_csv(HISTORY_DIR / "player_elo_history.csv", index=False)
    
    # Create summary
    write_log("\n" + "="*60)
    write_log("RESULTS SUMMARY")
    write_log("="*60)
    
    write_log(f"\nTop 5 Teams:")
    for i, row in team_elo_df.head().iterrows():
        write_log(f"  {row['rank']:2d}. {row['team']}: {row['elo']:.1f}")
    
    write_log(f"\nTop 10 Players:")
    for i, row in player_elo_df.head(10).iterrows():
        write_log(f"  {row['rank']:2d}. {row['player']}: {row['elo']:.1f}")
    
    # Check specific players
    key_players = ['Victor Wembanyama', 'Nikola Jokic', 'Giannis Antetokounmpo', 
                   'LeBron James', 'Stephen Curry', 'Anthony Davis']
    
    write_log(f"\nKey Player Rankings:")
    for player in key_players:
        if player in player_elo:
            rank = player_elo_df[player_elo_df['player'] == player]['rank'].iloc[0]
            elo = player_elo[player]
            write_log(f"  {player}: {elo:.1f} (Rank: {rank})")
    
    write_log(f"\nSan Antonio Spurs:")
    if 'SAS' in team_elo:
        rank = team_elo_df[team_elo_df['team'] == 'SAS']['rank'].iloc[0]
        write_log(f"  Elo: {team_elo['SAS']:.1f} (Rank: {rank}/{len(team_elo_df)})")
    
    write_log(f"\nAll files saved to: {OUTPUT_DIR}")
    write_log("="*60)
    write_log("ELO CALCULATION COMPLETE!")
    write_log("="*60)

if __name__ == "__main__":
    main()