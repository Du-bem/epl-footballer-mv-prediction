# =============================================================
# 01 - DATA LOADING
# Premier League Player Market Value Prediction
# =============================================================
# This notebook loads all raw CSV files from the Transfermarkt
# dataset and performs an initial inspection of each table.
# =============================================================

import pandas as pd

DATA_PATH = 'thesis_dataset/'

# ── Load all tables ──────────────────────────────────────────
appearances   = pd.read_csv(DATA_PATH + 'appearances.csv')
club_games    = pd.read_csv(DATA_PATH + 'club_games.csv')
clubs         = pd.read_csv(DATA_PATH + 'clubs.csv')
competitions  = pd.read_csv(DATA_PATH + 'competitions.csv')
games         = pd.read_csv(DATA_PATH + 'games.csv')
players       = pd.read_csv(DATA_PATH + 'players.csv')
valuations    = pd.read_csv(DATA_PATH + 'player_valuations.csv')
transfers     = pd.read_csv(DATA_PATH + 'transfers.csv')

# ── Shape inspection ─────────────────────────────────────────
tables = {
    'appearances':  appearances,
    'club_games':   club_games,
    'clubs':        clubs,
    'competitions': competitions,
    'games':        games,
    'players':      players,
    'valuations':   valuations,
    'transfers':    transfers,
}

for name, df in tables.items():
    print(f"\n{'='*40}")
    print(f"TABLE: {name.upper()}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

# ── Null inspection ──────────────────────────────────────────
print("\n\n── NULL COUNTS PER TABLE ──")
for name, df in tables.items():
    print(f"\n{name.upper()}")
    print(df.isnull().sum())

# ── Key table previews ───────────────────────────────────────
print("\n\n── APPEARANCES PREVIEW ──")
print(appearances.head(3))

print("\n── VALUATIONS PREVIEW ──")
print(valuations.head(3))

print("\n── PLAYERS PREVIEW ──")
print(players.head(3))

# ── Confirm Premier League competition ID ────────────────────
print("\n\n── PREMIER LEAGUE COMPETITION ──")
print(competitions[competitions['name'] == 'premier-league'])

# ── Date range of Premier League appearances ─────────────────
pl_apps = appearances[appearances['competition_id'] == 'GB1']
print(f"\nPL Appearances: {pl_apps.shape[0]}")
print(f"Date range: {pl_apps['date'].min()} → {pl_apps['date'].max()}")
