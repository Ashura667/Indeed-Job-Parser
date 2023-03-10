import cloudscraper, re
import bs4
import json
def indeed_parser():
    scraper = cloudscraper.create_scraper(delay=10)  # returns a CloudScraper instance
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    donnée = scraper.get("https://fr.indeed.com/jobs?q=développeur%20web").text

    soup = bs4.BeautifulSoup(donnée, "lxml")
    website = soup.find_all('body')
    x = []

    for element in website:
        ulList = element.find_all('li')
        for li in ulList:
            if 'class="cardOutline' in str(li):
                # print(li)

                nommetier = re.search("« (.*?) »", str(li)).group(1)
                Companyname = re.search(r'<span class="companyName">(.*?)<', str(li)).group(1)
                CompanyLocation = soup.find("div", class_="companyLocation").text
                Salary = []
                try:
                    for element in re.findall(r'</path></svg>(.*?)<', str(li)):
                        if len(element) > 1:
                            Salary.append(element)
                except:
                    pass
                poster = ""
                for element in re.findall(r'</span>(.*?)</span>', str(li)):
                    if "Offre" in element or "Recrutement" in element or "Derniere" in element or "Aujourd'hui" in element or 'jour' in element:
                        poster = element
                x.append([{'nom': nommetier, 'Entreprise': Companyname, 'Localisation': CompanyLocation,
                           'Caractéristique': " ".join(Salary), "Date de poste": poster}])
                print(nommetier, Companyname, CompanyLocation, " ".join(Salary), poster)
    with open('indeed.json', 'a', encoding='utf8') as f:
        fichier = json.dumps(x, ensure_ascii=False, indent=4)
        f.write(fichier)

if __name__ == '__main__':
    indeed_parser()
