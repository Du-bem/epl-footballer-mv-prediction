# =============================================================
# 02 - DATA CLEANING
# Premier League Player Market Value Prediction
# =============================================================
# This notebook filters raw data to the Premier League,
# aggregates appearances per player per season, applies the
# 900-minute filter, and joins all tables into a master
# dataframe. Goalkeepers are excluded as available performance
# metrics do not adequately capture their contribution.
# =============================================================

import pandas as pd
import numpy as np

DATA_PATH = 'thesis_dataset/'

# ── Reload raw tables ─────────────────────────────────────────
appearances = pd.read_csv(DATA_PATH + 'appearances.csv')
players     = pd.read_csv(DATA_PATH + 'players.csv')
valuations  = pd.read_csv(DATA_PATH + 'player_valuations.csv')
games       = pd.read_csv(DATA_PATH + 'games.csv')

# ── Step 1: Filter to Premier League appearances ──────────────
# competition_id GB1 = English Premier League
pl_appearances = appearances[
    appearances['competition_id'] == 'GB1'
].copy()

pl_appearances['season'] = pd.to_datetime(
    pl_appearances['date']
).dt.year

print(f"PL appearances: {pl_appearances.shape[0]}")
print(f"Seasons: {sorted(pl_appearances['season'].unique())}")

# ── Step 2: Aggregate per player per season ───────────────────
season_stats = pl_appearances.groupby(
    ['player_id', 'season']
).agg(
    goals          = ('goals', 'sum'),
    assists        = ('assists', 'sum'),
    minutes_played = ('minutes_played', 'sum'),
    appearances    = ('appearance_id', 'count')
).reset_index()

# Apply 900-minute minimum filter (~10 full games per season)
season_stats = season_stats[
    season_stats['minutes_played'] >= 900
].reset_index(drop=True)

print(f"\nPlayer-season records (≥900 mins): {season_stats.shape[0]}")

# ── Step 3: Join player profile ───────────────────────────────
players['date_of_birth'] = pd.to_datetime(players['date_of_birth'])
players['birth_year']    = players['date_of_birth'].dt.year

player_profile = players[[
    'player_id', 'birth_year', 'position', 
    'sub_position', 'foot'
]].copy()

df = season_stats.merge(player_profile, on='player_id', how='left')
df['age'] = df['season'] - df['birth_year']

print(f"\nAfter player profile join: {df.shape}")
print(df.isnull().sum())

# ── Step 4: Join target variable (market value) ───────────────
valuations['date']   = pd.to_datetime(valuations['date'])
valuations['season'] = valuations['date'].dt.year

# Take last recorded valuation per player per season
target = valuations.groupby(['player_id', 'season']).agg(
    market_value = ('market_value_in_eur', 'last')
).reset_index()

df = df.merge(target, on=['player_id', 'season'], how='left')

print(f"\nAfter market value join: {df.shape}")
print(f"Missing market values: {df['market_value'].isnull().sum()}")

# ── Step 5: Join club prestige ────────────────────────────────
# total_market_value is null in clubs.csv
# Instead, aggregate player valuations per club per season
club_season_value = valuations.groupby(
    ['current_club_id', 'season']
).agg(
    club_total_value = ('market_value_in_eur', 'sum'),
    player_count     = ('player_id', 'count')
).reset_index()

club_season_value.columns = [
    'club_id', 'season', 'club_total_value', 'player_count'
]

# Filter to PL clubs with at least 8 players
pl_games    = games[games['competition_id'] == 'GB1']
pl_club_ids = set(
    pl_games['home_club_id'].tolist() + 
    pl_games['away_club_id'].tolist()
)

club_season_value = club_season_value[
    (club_season_value['club_id'].isin(pl_club_ids)) &
    (club_season_value['player_count'] >= 8)
]

# Get player's primary club per season
player_club_season = pl_appearances.groupby(
    ['player_id', 'season']
)['player_club_id'].agg(
    lambda x: x.mode()[0]
).reset_index()

player_club_season.columns = ['player_id', 'season', 'club_id']

df = df.merge(player_club_season, on=['player_id', 'season'], how='left')
df = df.merge(
    club_season_value[['club_id', 'season', 'club_total_value']],
    on=['club_id', 'season'],
    how='left'
)

print(f"\nAfter club prestige join: {df.shape}")
print(f"Missing club values: {df['club_total_value'].isnull().sum()}")

# ── Step 6: Drop nulls and goalkeepers ────────────────────────
df = df.dropna(subset=['market_value', 'club_total_value'])
df = df[df['position'] != 'Goalkeeper'].reset_index(drop=True)

# Drop rows with missing foot data (25 rows — 0.6%)
df = df[df['foot'].notna()].reset_index(drop=True)

print(f"\nFinal clean dataset: {df.shape}")
print(df.isnull().sum())

# ── Save clean dataset ────────────────────────────────────────
df.to_csv('thesis_dataset/clean_dataset.csv', index=False)
print("\nSaved: thesis_dataset/clean_dataset.csv")
