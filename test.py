import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from Car import Car


base_url = "https://www.leboncoin.fr/recherche?category=2&price=10000-15000&u_car_brand=MERCEDES-BENZ&sort=price&order=asc"
if len(sys.argv) > 1:
    base_url = sys.argv[1]
else:
    base_url = input("Lien de recherche leboncoin : ")
    
nb_pages = 2
limit=10

def getCars(driver):
    cars = []
    for page in range(1, nb_pages + 1):
        url = f"{base_url}&page={page}" if page > 1 else base_url
        print(f"Connexion page {page}/{nb_pages} : {url}")
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        annonces = soup.find_all("article", attrs={"data-test-id": "ad"})
        if not annonces:
            print(f"Aucune annonce trouvée sur la page {page}.")
        else:
            print(f"Nombre d'annonces trouvées sur la page {page} : {len(annonces)}")
            for annonce in annonces:
                lien_element = annonce.find("a", class_="absolute inset-0")
                if lien_element:
                    car = Car()
                    car.set_link("https://www.leboncoin.fr" + lien_element.get("href"))
                    cars.append(car)
    return cars

def recuperer_infos(driver, car):
    driver.get(car.get_link())
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Trouver la balise contenant le prix
    prix_element = soup.find("div", {"data-qa-id": "adview_price"})
    if prix_element:
        prix_text = prix_element.find("p", class_="text-headline-2")
        if prix_text:
            car.set_price(prix_text.text.strip())
            
    # Trouver la cote
    cote_container = soup.find("h2", class_="text-headline-2", string="Le bon prix L’argus™")
    if cote_container:
        cote_container = cote_container.find_parent("div")
        if cote_container:
            cote_container = cote_container.find_parent("div")
            if cote_container:
                cote_divs = cote_container.find_all("div", class_="bottom-lg text-body-1 absolute font-bold whitespace-nowrap")
                if len(cote_divs) >= 2:
                    car.set_coteMin(cote_divs[0].text.strip())
                    car.set_coteMax(cote_divs[1].text.strip())

# Lancement du navigateur
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0 Safari/537.36")
driver = webdriver.Chrome(options=options)

# Récupération des annonces
res_cars = getCars(driver)
## res_cars = res_cars[:5] 

valid = 0
# Récupération des prix
for i in range(0,len(res_cars)):
    print(f"Annonce {i+1}/{len(res_cars)}")
    recuperer_infos(driver, res_cars[i])
    if res_cars[i].isValid():
        valid += 1
        if valid == limit:
            break

# Afficher les voitures
for car in res_cars:
    if car.isValid():
        print(car)

driver.quit()
