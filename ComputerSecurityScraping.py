# import libraries
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

class ComputerSecurityScraping:
    eu_pattern_list = ['EU-US', 'EFTA', 'Swiss-US', 'Privacy Shield', 'EU-U.S.', 'Swiss-U.S.', 'EEA']
    dnt_pattern_list = ['DNT', 'Do Not Track', 'Do-Not-Track', 'do not allow tracking']
    gdpr_pattern_list = ['GDPR', 'Control Information', 'Manage information', 'Delete Information', 'Manage Your Data', 'Delete Your Data', 'control information', 'manage your data', 'update your information', 'restrict access', 'control who sees what', 'choices about how your data is collected', 'Data subject rights', 'right to be forgotten', 'Lawful bases of personal data processing', 'right to complain', 'retention periods']
    cali_pattern_list = ['California Online Privacy', 'California privacy', 'California Privacy', 'CalOPPA']
    eu_pattern = re.compile('|'.join(eu_pattern_list))
    dnt_pattern = re.compile('|'.join(dnt_pattern_list))
    gdpr_pattern = re.compile('|'.join(gdpr_pattern_list))
    cali_pattern = re.compile('|'.join(cali_pattern_list))
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
            cali_list = []
            num_links = 0
            exception = False
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
            if num_links == 0:
                continue

            for i in range(num_links):
                # navigate to link
                try:
                    link[i].click()
                    break
                except (exceptions.StaleElementReferenceException, exceptions.ElementClickInterceptedException, exceptions.WebDriverException, exceptions.ElementNotInteractableException) as e:
                    print(url + ' ' + str(e))
                    exception = True
                    continue

            if exception:
                continue

            print(url + ' ' + str(num_links))

            page_source = driver.execute_script("return document.documentElement.innerHTML;")

            soup = BeautifulSoup(page_source, 'html.parser')

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

            p = soup.find_all('p', text=self.cali_pattern)
            if len(p):
                cali_list.append(p)
            div = soup.find_all('div', text=self.cali_pattern)
            if len(div):
                cali_list.append(div)
            a = soup.find_all('a', text=self.cali_pattern)
            if len(a):
                cali_list.append(a)
            li = soup.find_all('li', text=self.cali_pattern)
            if len(li):
                cali_list.append(li)
            h2 = soup.find_all('h2', text=self.cali_pattern)
            if len(h2):
                cali_list.append(h2)

            self.dict[url] = {'EU-US Privacy Shield': eu_list, 'DNT': dnt_list, 'GDPR': gdpr_list, 'CalOPPA': cali_list}
        driver.close()
        self.write_to_table()
        self.graph_info()

    def write_to_table(self):
        with open('privacy_policy_info.csv', 'w', newline='') as csvfile:
            fieldnames = ['URL', 'EU-US Privacy Shield', 'Do Not Track', 'GDPR', 'CalOPPA']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.dict.keys():
                writer.writerow({'URL': item, 'EU-US Privacy Shield': self.dict[item]['EU-US Privacy Shield'], 'Do Not Track': self.dict[item]['DNT'], 'GDPR': self.dict[item]['GDPR'], 'CalOPPA': self.dict[item]['CalOPPA']})

    def graph_info(self):
        total_urls = 0
        gdpr_total = 0
        cali_total = 0
        dnt_total = 0
        eu_total = 0

        for key in self.dict.keys():
            total_urls = total_urls + 1
            if len(self.dict[key]['EU-US Privacy Shield']) != 0:
                eu_total = eu_total + 1
            if len(self.dict[key]['DNT']) != 0:
                dnt_total = dnt_total + 1
            if len(self.dict[key]['GDPR']) != 0:
                gdpr_total = gdpr_total + 1
            if len(self.dict[key]['CalOPPA']) != 0:
                cali_total = cali_total + 1

        objects = ('EU-US Privacy Shield', 'Do Not Track', 'GDPR', 'CalOPPA')
        y_pos = np.arange(len(objects))
        performance = [eu_total, dnt_total, gdpr_total, cali_total]

        plt.bar(y_pos, performance, align='center', alpha=1)
        plt.xticks(y_pos, objects)
        plt.ylabel('Amount of Privacy Policies')
        plt.title('Privacy Protocols Among Top Domains')

        plt.show()

if __name__ == '__main__':
    urls = []
    my_filtered_csv = pd.read_csv('url_list.csv', usecols=['URL'])
    for row in my_filtered_csv['URL']:
        urls.append('https://' + row)
    scrape = ComputerSecurityScraping(urls)
    scrape.scrapePages()