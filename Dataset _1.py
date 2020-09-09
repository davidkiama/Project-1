#Importing the libraries
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd


class loop_through:
    def __init__(self):
        self.driver = webdriver.Chrome()

        start = 1783
        end = 2687

        master_list = []

        for page_number in range(start, end):
            url = (
                f"https://racing.appledaily.com.hk/race-day/bet-result?raceDay={page_number}"
            )
            self.driver.get(url)
            sleep(3)

            try:
                tournament_link = self.driver.find_element_by_xpath(
                    "//*[@id='app']/div[3]/div[1]/div/div[3]/div[3]/div[2]/div[3]/a"
                ).get_attribute('href')
            except:
                print(f'error at {page_number}   ')
                continue

            self.driver.get(
                tournament_link)  #Visit the link that has the matchdays

            race_days = self.driver.find_elements_by_xpath(
                "//*[@id='app']/div[3]/div[1]/div/div[3]/div[2]/div[2]/a")

            for race_day in race_days:
                race_day.click()
                sleep(3)

                # Values conctenated with the row
                web_link = self.driver.current_url

                title = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'race-day-race__content__title')]"
                ).text

                subtitle = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'race-day-race__content__subtitle')]"
                ).text

                total_games = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'race-day-race__content__subtitle')][2]/span[1]"
                ).text

                venue = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'race-day-race__content__subtitle')][2]/span[2]"
                ).text

                index = self.driver.find_element_by_xpath(
                    "//div[contains(@class, 'race-day-race__content__subtitle')][2]/div[1]"
                ).text

                time = self.driver.find_element_by_xpath(
                    "//*[@id='app']/div[3]/div[1]/div/div[3]/div[1]/div/div[3]/div"
                ).text

                ticket = self.driver.find_element_by_xpath(
                    "//*[@id='app']/div[3]/div[1]/div/div[4]/div/div[1]/table/tfoot/tr[1]/td"
                ).text

                speeds = self.driver.find_element_by_xpath(
                    "//*[@id='app']/div[3]/div[1]/div/div[4]/div/div[1]/table/tfoot/tr[2]/td"
                ).text

                # Getting the rows from the table
                soup = bs(self.driver.page_source, 'html.parser')
                table = soup.find("tbody")
                table_rows = table.findAll('tr')

                for results in table_rows:
                    rows = [row.text.strip() for row in results.findAll('td')]

                    complete_row = [
                        web_link, title, subtitle, total_games, venue, index,
                        time, ticket, speeds
                    ]
                    combined_row = rows + complete_row
                    master_list.append(combined_row)

            df = pd.DataFrame(master_list)

            df.to_excel(f'Dataset{page_number}.xlsx', engine='xlsxwriter')


loop_through()
