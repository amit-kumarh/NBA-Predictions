from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

nbaSeasons = ['2020']
months = ['october-2019', 'november', 'december', 'january', 'february', 'march', 'july', 'august']
timeout = 25

driver = webdriver.Firefox()

for season in nbaSeasons:
    for month in months:    
        url = f"https://www.basketball-reference.com/leagues/NBA_{season}_games-{month}.html"
        driver.get(url)
        element_present = EC.presence_of_element_located((By.ID, "schedule"))
        WebDriverWait(driver, timeout).until(element_present)
        src = driver.page_source
        parser = BeautifulSoup(src, 'lxml')
        table = parser.find("table", attrs = {'id': "schedule"})
        headerlist = ['Team1', '1pts', "Team2", '2pts']
        rows = table.findAll('tr')[1:]
        team_stats = [[td.getText().strip() for td in rows[i].findAll('td')[1:5]] for i in range(len(rows))]
        team_stats = [a for a in team_stats if a != []]
        stats = pd.DataFrame(team_stats, columns=headerlist)
        pd.DataFrame.to_csv(stats, f'./matchups/{month}{season}.csv', mode='a', header=True)

driver.quit()