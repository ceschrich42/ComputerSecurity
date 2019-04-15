# import libraries
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re

class ComputerSecurityScraping:
    eu_pattern_list = ['EU-US', 'EFTA', 'Swiss-US', 'Privacy Shield', 'EU-U.S.', 'Swiss-U.S.']
    dnt_pattern_list = ['DNT', 'Do Not Track', 'Do-Not-Track']
    gdpr_pattern_list = ['GDPR', 'EEA' 'Control Information', 'Manage information', 'Delete Information', 'Manage Your Data', 'Delete Your Data', 'control information', 'manage your data', 'update your information']
    eu_pattern = re.compile('|'.join(eu_pattern_list))
    dnt_pattern = re.compile('|'.join(dnt_pattern_list))
    gdpr_pattern = re.compile('|'.join(gdpr_pattern_list))

    privacy_list = ['Privacy', 'privacy', 'PRIVACY']

    def __init__(self, urls):
        self.urls = urls
        self.dict = {}

    def scrapePages(self):
        driver = webdriver.Firefox()
        driver.implicitly_wait(5)
        for url in self.urls:
            eu_list = []
            dnt_list = []
            gdpr_list = []
            num_links = 0
            try:
                driver.get(url)
            except (exceptions.StaleElementReferenceException, exceptions.ElementClickInterceptedException, exceptions.WebDriverException, exceptions.ElementNotInteractableException) as e:
                print(url + ' ' + str(e))
                continue

            for privacy in self.privacy_list:
                temp = driver.find_elements_by_partial_link_text(privacy)
                if len(temp):
                    link = temp
                    num_links = len(temp)
                    break


            for i in range(num_links):
                # navigate to link
                try:
                    link[i].click()
                    break
                except (exceptions.StaleElementReferenceException, exceptions.ElementClickInterceptedException, exceptions.WebDriverException, exceptions.ElementNotInteractableException) as e:
                    print(url + ' ' + str(e))
                    continue

            print(url + ' ' + str(num_links))

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            p = soup.find_all('p', text=self.eu_pattern)
            if len(p):
                eu_list.append(p)
            div = soup.find_all('div', text=self.eu_pattern)
            if len(div):
                eu_list.append(div)
            a = soup.find_all('a', text=self.eu_pattern)
            if len(a):
                eu_list.append(a)
            li = soup.find_all('li', text=self.eu_pattern)
            if len(li):
                eu_list.append(li)
            h2 = soup.find_all('h2', text=self.eu_pattern)
            if len(h2):
                eu_list.append(h2)

            print(eu_list)

            p = soup.find_all('p', text=self.dnt_pattern)
            if len(p):
                dnt_list.append(p)
            div = soup.find_all('div', text=self.dnt_pattern)
            if len(div):
                dnt_list.append(div)
            a = soup.find_all('a', text=self.dnt_pattern)
            if len(a):
                dnt_list.append(a)
            li = soup.find_all('li', text=self.dnt_pattern)
            if len(li):
                dnt_list.append(li)
            h2 = soup.find_all('h2', text=self.dnt_pattern)
            if len(h2):
                dnt_list.append(h2)

            print(dnt_list)

            p = soup.find_all('p', text=self.gdpr_pattern)
            if len(p):
                gdpr_list.append(p)
            div = soup.find_all('div', text=self.gdpr_pattern)
            if len(div):
                gdpr_list.append(div)
            a = soup.find_all('a', text=self.gdpr_pattern)
            if len(a):
                gdpr_list.append(a)
            li = soup.find_all('li', text=self.gdpr_pattern)
            if len(li):
                gdpr_list.append(li)
            h2 = soup.find_all('h2', text=self.gdpr_pattern)
            if len(h2):
                gdpr_list.append(h2)

            print(gdpr_list)

            self.dict[url] = {'EU-US Privacy Shield': eu_list, 'DNT': dnt_list, 'GDPR': gdpr_list}
        driver.close()
        self.write_to_table()

    def write_to_table(self):
        with open('privacy_policy_info.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'EU-US Privacy Shield', 'Do Not Track', 'GDPR']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.dict.keys():
                writer.writerow({'URL': item, 'EU-US Privacy Shield': self.dict[item]['EU-US Privacy Shield'], 'Do Not Track': self.dict[item]['DNT'], 'GDPR': self.dict[item]['GDPR']})


if __name__ == '__main__':
    urls = []
    my_filtered_csv = pd.read_csv('url_list.csv', usecols=['URL'])
    i = 0
    for row in my_filtered_csv['URL']:
        if i == 150:
            break
        urls.append('https://' + row)
        i = i+1
    scrape = ComputerSecurityScraping(urls)
    scrape.scrapePages()