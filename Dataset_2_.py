from selenium import webdriver
from bs4 import BeautifulSoup
from html_table_extractor.extractor import Extractor
from io import StringIO
import csv
import re
import time
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox()
driver.implicitly_wait(30)


def scrape_day(raceDay):
    web_link = f"https://racing.appledaily.com.hk/race-day/bet-result?raceDay={raceDay}"

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.select('.race-day-bet__content')[0]
    content_title = content.select('.race-day-bet__content__title')[0].text.strip()
    race_date = content.find(attrs={"value": raceDay}).text.strip()
    race_card_names = content.select('.race_name_card')
    #content_tables = content.select('.race-day-bet__content__table')
    content_small_tables = content.select('.small-3')
    content_big_tables = content.select('.small-6')


    race_sub_titles = []
    for race_card_name in race_card_names:
        race_card_name = re.split('\n\s+\n', re.sub('\n\s+\xa0', ' ', race_card_name.text.strip()))

        race_card_csv = ''
        for item in race_card_name:
            race_card_csv = race_card_csv + f'"{str(item).strip()}",'
        race_sub_titles.append(race_card_csv)


    main_tables = []
    for content_big_table in content_big_tables:
        content_big_table = Extractor(content_big_table).parse().return_list()
        content_big_table = str(content_big_table).replace(r'\n', '')
        content_big_table = re.sub('\s+', '', content_big_table)
        string_io = StringIO()
        csv.writer(string_io, delimiter=',', quoting=csv.QUOTE_ALL).writerows(eval(content_big_table.split()[0]))
        content_big_table = string_io.getvalue().replace('\r\n', ',')
        main_tables.append(content_big_table)


    i = 0
    for content_table in content_small_tables:
        content_table = Extractor(content_table).parse().return_list()
        content_table = str(content_table).replace(r'\n', '')
        content_table = re.sub('\s+', '', content_table)
        string_io = StringIO()
        csv.writer(string_io, delimiter=',', quoting=csv.QUOTE_ALL).writerows(eval(content_table.split()[0]))
        content_table = string_io.getvalue().replace('\r\n', ',')

        match_csv = f'"{content_title}", "{web_link}", "{race_date}", {race_sub_titles[i]} {content_table} {main_tables[i]}\n'
        with open(f'csv/{race_date[:4]}.csv', 'a') as f:
            f.write(match_csv)

        i = i + 1


def scrape_year(first_race_day):
    driver.get(f"https://racing.appledaily.com.hk/race-day/bet-result?raceDay={first_race_day}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.select('.race-day-bet__content')[0]
    content_selector = content.select('.race-day-bet__content__selector')[0]
    selector_options = content_selector.find_all('option')

    for selector_option in selector_options:
        race_day = selector_option['value']
        if not race_day  == '-1':
            try:
                driver.find_element_by_xpath(
                    f'/html/body/div[2]/div[3]/div[1]/div/div[3]/div[2]/div/select/option[{selector_options.index(selector_option)+1}]').click()
                driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div/div[3]/div[3]/div[2]/div[1]/table/tbody')
                time.sleep(5)
                driver.find_element_by_css_selector('.race-day-bet__content__title')
                driver.find_element_by_css_selector('.race-day-bet__content')
                scrape_day(race_day)
            except Exception as e:
                print(f'{e}\t error at race_day {race_day}')
                pass

scrape_year(2373)

driver.quit()


#all the years to scrape
#2687  -------->2019-2020
#2597
#2373
#2285

#2197
#2114
#2031
#1948
#1865  -------->2011-2012
