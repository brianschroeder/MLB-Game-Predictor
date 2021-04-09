# MLB Game Predictor - Baseball Data Science Tools

## Author Brian Schroeder

## Overview
The goal of this project is to gather data from previous games and years, create a program to gather the most common stats that effected a Teams Winning Percentage, and
predict future games based off a model that was created from the data gained from the historical analysis.

## Findings

First I needed to get the Data for the most common stats that the Winning Teams had in common over a period of time.

I wrote a program to get each game that was played over a time period, got the winnner of the game, retrieved each catgory the team beat the losing team in and put that data into a table and grouped it by that stat (Example Batting Average.) Then, I was able to determine which stats were present the most amound the winning teams.

The stats that effected a Baseball Teams ability to win is split into two categories: Hitting and Pitching. Any Baseball fan knows the game, knows you can't have one without the other. 

*Exluding the obvious stats such as runs and RBIs*

**Stats the Winning Teams had in Common after the Victory**

Hitting VS opposing Team Stats 

1. Lower Amount of Strikeouts
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
5. Lower WHIP
6. Lower Base on Balls
7. Lower Stolen Base Percentage (Interesting)

