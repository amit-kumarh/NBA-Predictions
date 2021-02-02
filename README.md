NBA-Predictions
=======
# NBA-Predictions
Python scripts that use ML to predict the results of NBA games

bbref.py - scrapes every matchup from basketballreference.com for seasons 2009-2019 through 2018-2019. Skips 2011-2012 due to lockout
bbref2020.py - scrapes matchups for 2020, different file because season not played in normal months

nbaadv.py - scrapes every monthly advanced stats from stats.nba.com for seasons 2009-2019 through 2018-2019. Skips 2011-2012 due to lockout
nbaadv.py - scrapes monthly advanced stats for 2020, different file because season not played in normal months

merging.py - merges matchups with the two team's monthly stats into one CSV file

final.csv - dataset used for training model. One line per matchup, each line has winner and advanced stats for each team.
final_data.csv - final.csv with team names and scores in each matchup

finalScraper.py - contains functions to scrape advanced stats for every team's last 10 games, and merge that with the matchups for the day. Also contains an unfinished function that will scrape the day's matchups so those don't have to be input manuall, but I was unable to find a source that publishes daily matchups in a table that matchups the wording used in the rest of the scripts (Full team name is used, as in "Boston Celtics". ESPN and such only say "Boston")

model.py - contains functions that train model, and a main function that calls on finalScraper.py to get a dataset of matchups and uses the SVM classifier model to predict the winner. Writes output to a file in the ./results folder 

Given that finalScraper.py is unfinished, as of now it pulls the day's matchups from ./games/{month}{day}.csv (As in Feb. 2 would be 22.csv).






