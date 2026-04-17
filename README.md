# EPL Player Market Value Prediction

Machine learning project analysing and predicting player market values in the English Premier League using Transfermarkt data (2012–2025).

## Overview

- 3,819 player-season observations (≥900 minutes, outfield players)  
- Objective: identify key drivers of market value  

## Models

- Ridge Regression (performance only)  
- Ridge Regression (performance + contextual)  
- Random Forest (full model)  

**Best model:** Random Forest (R² = 0.589, RMSE = 0.665)

## Key Findings

- Contextual factors outweigh performance metrics  
- Club value (prestige) is the strongest predictor  
- Age shows a non-linear (peak-age) effect  
- Opponent-weighted contributions do not improve predictions  

## Methodology

- Log-transformed target (market value in EUR)  
- Temporal split (train: 2012–2022, test: 2023–2024)  
- Metrics: R², RMSE  

## Tools

Python (pandas, NumPy, scikit-learn), Matplotlib, Seaborn, JupyterLab  

## Limitations

- Subjective valuations (Transfermarkt)  
- Limited defensive metrics  
- Single-league focus  

## Author

Chidubem Cy-Bartczak  
BSc Data Science Dissertation Project  
