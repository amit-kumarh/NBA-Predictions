from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd

nbaSeasons = ['2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2010-11', '2009-10']
months = ['1', '2', '3', '4', '5', '6', '7']
seasonNames = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', '2011', '2010']
monthnames = ['', 'october', 'november', 'december', 'january', 'february', 'march', 'april']
timeout = 25

driver = webdriver.Firefox()

for season in nbaSeasons:
    for month in months:    
        url = f"https://www.nba.com/stats/teams/advanced/?sort=W&dir=-1&Season={season}&SeasonType=Regular%20Season&Month={month}"
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
        seasonname = seasonNames[nbaSeasons.index(season)]
        pd.DataFrame.to_csv(stats, f'./stats/{monthnames[int(month)]}{seasonname}.csv', mode='a', header=True)


driver.quit()