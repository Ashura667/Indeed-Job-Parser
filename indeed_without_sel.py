import cloudscraper, re
import bs4
import json
scraper = cloudscraper.create_scraper(delay=10)  # returns a CloudScraper instance
# Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
donnée = scraper.get("https://fr.indeed.com/jobs?q=développeur%20web&l=&from=searchOnHP").text
#nom_entreprise = re.findall(r'"company":"(.*?)"', scraper.get("https://fr.indeed.com/jobs?q=développeur%20web&l=&from=searchOnHP").text)

#lieu = re.findall(r'class="companyLocation">(.*?)<', scraper.get("https://fr.indeed.com/jobs?q=développeur%20web&l=&from=searchOnHP").text)
#salaire = re.findall(r'clip-rule="evenodd"></path></svg>(.*?)<', scraper.get("https://fr.indeed.com/jobs?q=développeur%20web&l=&from=searchOnHP").text)

#for i in range(len(nom_metier)):
#    print(nom_metier[i] + " " + nom_entreprise[i] + " " + lieu[i] + " " + salaire[i])
soup =   bs4.BeautifulSoup(donnée, "lxml")
w3schollsList = soup.find_all('body')
x = []

for w3scholl in w3schollsList:
    ulList = w3scholl.find_all('li')
    for li in ulList:
        if 'class="cardOutline' in str(li):
                #print(li)

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
                    if "Offre publiée" in element or "Recrutement" in element or "Derniere" in element:
                        poster = element
                x.append([{'nom':nommetier, 'Entreprise':Companyname, 'Localisation' :CompanyLocation,  'Caractéristique':" ".join(Salary), "Date de poste":poster}])
                print(nommetier, Companyname, CompanyLocation, " ".join(Salary), poster)
with open('indeed.json', 'a', encoding='utf8') as f:
    f.write(json.dumps(x, indent=4))



with open('indeed.html', 'w') as f:
    f.write(scraper.get("https://fr.indeed.com/jobs?q=développeur%20web&l=&from=searchOnHP").text)