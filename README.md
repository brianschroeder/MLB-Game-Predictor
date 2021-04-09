# MLB Game Predictor - Baseball Data Science Tools

## Author Brian Schroeder

## Overview
The goal of this project was to gather data from previous games and years, create a program to gather the most common stats that effected a Teams Winning Percentage, and
predict future games based off a model that was created from the data gained from the historical analysis.

## Findings

The stats that effected a Baseball Teams ability to win is split into two categories: Hitting and Pitching. Any Baseball fan knows the game, knows you can't have one without the other. 

(Exluding the obvious stats such as runs and RBIs)

Hitting VS opposing Team Stats 

1. Lower Ammount of Strikeouts
2. Lower Amount of Batters Left on Base
3. Higher Batting Average
4. Higher On Base Percentage
5. Higher OPS
6. Higher Slugging Percentage
7. Higher Amount of Homeruns Per at bat

Pitching VS opposing Teams Stats (Lower is better in most cases in Pitching)

1. Lower on Base Percentage
2. Lower Hits allowed
3. Lower HomeRuns Per 9 innings
4. Lower ERA
5. WHIP
6. Base on Balls
7. Stolen Base Percentage (Interesting)

#### The first script created was the Common_Winning_Stats_Analyzer.py

The goal of this script is to determine which categories such as a Teams Batting Average and ERA effect the outcome of the Game the most. This script has been designed
to look at data over a range of time and output what stat categories helped the Winning team the most. This helps in creating a model for predicting the games winner 
based off of the players that are starting for the team and how the stats they lead in will give a certain team an advantage in Winning.

#### Synopsis
    This program gets the Winner for each game on a specific date and outputs the Stats they were leading in.
    The Output will be the total number of Games that category was higher for the Winning Team vs the losing team.

### By having all the categories that effected and helped the Winning Team, I was then able to created the algorithm that is the most efficient in predicating the Winning Team.
