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

Now that we have the categoires the winning Teams had in common, we now will build our algorithm that will determine which of these stats above in combination lead to the most ammount of correct predicition for the team winning.

Example: Home Batting Average > Away Batting Average and Home ERA > Away ERA

To accomplish this, I started by programaticlly testing each stat one by one and adding another stat to the list and would continue testing each combination to get the winning percentage. 

I soon then realised that this method is not testing each possible combination of stats, as it's running sequentually. '

So if Batting Average was at the Beginning of the testing and ERA was at the end, these two stats would never be tested indendently with eachother.

So I updated my code to get every possible combination of stats that were passed, then run the prediction tests to see which unique algorithms would result in a win.

I took the number of times the algorithm predicted a team would win, then compared it againt the actual result of the game. I compared the total number of times the algorithm was correct in predicting the winning team vs how many totals were predicted to win, and that gave me the winning percentage for the algorithm.

Note: The API's I used all had historical data which helped in running the testing over a series of time.

From there, I picked the top algorithm which picked the correct winning team the highest percentage of times and implented that into my daily running MLB Game Predictor.

The secert sauce as of right now (*Pending more stats being included in the algorithm testing*) is:

*Note: In situations where a lower stat is better such as strike out percentage the has already been factored in when using the greater than operator.*

Home Strike Out % > Away Strike Out% and Home Slugging % > Away Slugging % and Home ERA > Away ERA and Home Homeruns/9 Against > Away Homeruns/9 Against and Home OBP Against > Away OBP Against: 

71.95% Win Rate (Total Wins Predicted: 328, Predicted Actual Wins: 236)

