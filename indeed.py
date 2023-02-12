import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import re
Liste = []
def requete(page):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    driver = webdriver.Chrome()
    driver.get("https://fr.indeed.com/jobs?q=front+end&l=France&vjk=457455ba15cbff93&start="+str(page) +"0")
    for i in range(1, 16):
        job = driver.find_element(By.CSS_SELECTOR, '#mosaic-provider-jobcards > ul > li:nth-child('+str(i)+')')
        try:
            test = driver.find_element(By.CSS_SELECTOR, "#mosaic-provider-jobcards > ul > li:nth-child("+str(i)+") > div > div.slider_container.css-g7s71f.eu4oa1w0 > div > div.slider_item.css-kyg8or.eu4oa1w0 > div > table.jobCard_mainContent.big6_visualChanges > tbody > tr > td")
            value = str(test.get_attribute("innerHTML"))
            #print(i, "https://fr.indeed.com"+re.search('href="(.*?)"', value).group(1).replace("amp;", ""))
            Liste.append(job.text + "\nURL : https://fr.indeed.com" + re.search('href="(.*?)"', value).group(1).replace("amp;", ""))



        except:
            pass


for i in range(1, 10):
    requete(i)
    with open("indeed.txt", "w", encoding='utf8') as f:
        f.write("\n\n\n".join(Liste))
        f.close()
    Liste = []

