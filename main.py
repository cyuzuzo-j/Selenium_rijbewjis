import os
import sys
import time

from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from datetime import datetime
from selenium.webdriver.edge.options import Options
frequency = 1500  # Set Frequency To 2500 Hertz
duration = 500  # Set Duration To 1000 ms == 1 second

today = datetime.now()
naam = ""
voornaam = ""
Adres = ""
Postcode = ""
Gemeente = ""
Geboortedatum = ""
Rijksregisternummer = ""
Telefoon = ""
Email = ""
examencentrum = "Haasroden"
ModelHuidigVRB = "36 Maanden (36M)"
eersteVRB = ""
huidigVRB = ""
VRBgeldigtot = ""
afspraak_url = "https://extranet.autoveiligheid.be/Afspraken_EC/MaakAfspraakECStap1Persoon.asp?Nieuw=1&menu=1&Id=243365697"

BESCHIKBAAR_VANAF = 5
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def check_riba():
    try:
        try:
            opt = Options()
            driver = webdriver.Edge(options = opt,service=EdgeService(EdgeChromiumDriverManager().install()))
        except Exception as e:
            print('failed',e )
            time.sleep(10)
            check_riba()

        driver.get(afspraak_url)
        driver.find_element(By.XPATH, '//*[@id="bodyDiv"]/main/div/div/div[2]/div/div[2]/a').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="rijksregisterNr"]').send_keys(Rijksregisternummer)
        driver.find_element(By.XPATH,'//*[@id="emailAdres"]').send_keys(Email)
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="bodyDiv"]/main/div/div/div[3]/div/div[2]/button').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="bodyDiv"]/main/div[1]/div[3]/div/div[2]/a').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="ec1024"]/div/span').click()
        #driver.find_element(By.XPATH,'//*[@id="ec1005"]/div/span').click()
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="PartialDiv"]/div[1]/div[2]').click()
        driver.execute_script('''
            var elem = arguments[0];
            var value = arguments[1];
            elem.value = value;
        ''', driver.find_element(By.XPATH, '//*[@id="inputFilter_StartDate"]'), f'{ today.day}/{ today.month }/{today.year}')
        time.sleep(2)
        driver.find_element(By.XPATH,'//*[@id="filterCollapse"]/div/div/input').click()

        time.sleep(6)
        try:
            data = driver.find_element(By.XPATH,'//*[@id="timeSelectCollapse"]/div[2]/ol/li/ol/li[1]/span').text
            month = data.split('/')[1]
            print(month)
            if (0<int(month) <= today.month + 3 and data.split('/')[0][0] != 'P'):
                print(f"affbesckibaar {data.split('/')[0]}/{month}")

                for i in range(50):
                    playsound("i-did-it-message-tone.mp3")
                    time.sleep(duration / 3000)
                time.sleep(50000)
            else:
                print("niks beschikbaar")
        except:
            print("EROR")

        driver.close()

    except Exception as e:
        print("crashed",e)
        time.sleep(500)
        driver.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        try:
            print("started")
            check_riba()
            time.sleep(60 * 5)

        except:
            time.sleep(60 * 10)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
