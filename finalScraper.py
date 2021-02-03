from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def scrapeStats():
    timeout = 25
    driver = webdriver.Chrome()

    url = "https://www.nba.com/stats/teams/advanced/?sort=W_PCT&dir=-1&Season=2020-21&SeasonType=Regular%20Season&LastNGames=10"
    driver.get(url)
    element_present = EC.presence_of_element_located((By.XPATH, r"/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]"))
    WebDriverWait(driver, timeout).until(element_present)
    src = driver.page_source
    parser = BeautifulSoup(src, 'lxml')
    table = parser.find("div", attrs = {'class': "nba-stat-table"})
    headers = table.findAll('th')
    headerlist = [h.text.strip() for h in headers[1:]]
    headerlist = [a for a in headerlist if not 'RANK' in a]
    headerlist = headerlist[:-2]
    rows = table.findAll('tr')[1:]
    team_stats = [[td.getText().strip() for td in rows[i].findAll('td')[1:]] for i in range(len(rows))]
    team_stats = team_stats[:30]
    stats = pd.DataFrame(team_stats, columns=headerlist)
    driver.quit()
    return stats
    

def scrapeMatchups():
    timeout = 25
    driver = webdriver.Firefox()

    url = ""
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
    return stats

def merge(stats):
    today = datetime.datetime.now()
    matchups = pd.read_csv(f'./games/{today.month}{today.day}.csv')
    stats['TEAM'].replace("LA Clippers", "Los Angeles Clippers", inplace=True)


    # Mergings the results and stats datasets, adding a prefix depending on which teams stats are being used
    df = matchups.merge(stats.add_prefix('Team1'), how='left', left_on=['Team1'], 
                        right_on=['Team1TEAM']).drop(['Team1TEAM'],
                                                    axis=1).merge(stats.add_prefix('Team2'), 
                                                                                how='left', left_on=['Team2'], 
                                                                                right_on=['Team2TEAM']).drop(['Team2TEAM'],axis=1)
    return df                                                                                
