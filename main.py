from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import requests
from bs4 import BeautifulSoup
import lxml

#ALL CONDITIONS FOR THE SEARCH
LOCATION_WHERE_TO_TRAVEL = "Krabi"
COUNTRY = "Thailand"
CHECK_IN = "2023-02-01"
CHECK_OUT = "2023-02-20"
GUESTS = "1"
SUPERHOST = "&superhost=true"
MAX_PRICE_PER_DAY = "20"
MIN_BEDS = "1"

all_location_names_list = []
price_per_night_list = []
links_list = []


google_form_url = "https://forms.gle/y4YC5ScsxVFSUcgV7"
air_bnb_url = f"https://de.airbnb.com/s/{LOCATION_WHERE_TO_TRAVEL}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=april&flexible_trip_dates%5B%5D=march&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&checkin={CHECK_IN}&checkout={CHECK_OUT}&adults={GUESTS}&source=structured_search_input_header&query={LOCATION_WHERE_TO_TRAVEL}%20{COUNTRY}&amenities%5B%5D=4&room_types%5B%5D=Entire%20home%2Fapt&room_types%5B%5D=Private%20room&room_types%5B%5D=Hotel%20room&price_max={MAX_PRICE_PER_DAY}&min_beds={MIN_BEDS}{SUPERHOST}"

chrome_driver_path = "/Applications/chromedriver"

s = Service(chrome_driver_path)

class AirBnbFinder:
    def __init__(self):
        self.driver = self.driver = webdriver.Chrome(service=s)
        self.wait = WebDriverWait(self.driver, 60)    
        
    def get_airbnb_data(self):
            
        #Getting data from airbnb
        response = requests.get(air_bnb_url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_location_names = soup.find_all("span", class_="ts5gl90 tl3qa0j t1nzedvd dir dir-ltr")
        price_per_night = soup.select("div._1jo4hgw span._tyxjp1")
        links = soup.select("div.cm4lcvy.dir.dir-ltr a.l8au1ct.dir.dir-ltr")
    
        for i in range(len(all_location_names)):
            all_location_names_list.append(all_location_names[i].text)
            price_per_night_list.append(price_per_night[i].text)
            links_list.append(f"https://de.airbnb.com{links[i]['href']}")
    
    def post_in_googleforms(self):   
        self.driver.get(google_form_url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)   
        
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.KHxj8b.tL9Q4c")))
        
        for i in range(len(all_location_names_list)):
            time.sleep(1)
            input_boxes = self.driver.find_elements(By.CSS_SELECTOR, "textarea.KHxj8b.tL9Q4c")  
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.KHxj8b.tL9Q4c")))
            input_boxes[0].send_keys(f"{LOCATION_WHERE_TO_TRAVEL},{COUNTRY}")
            input_boxes[1].send_keys(all_location_names_list[i])
            input_boxes[2].send_keys(price_per_night_list[i])
            input_boxes[3].send_keys(links_list[i])
            self.driver.find_element(By.CSS_SELECTOR, "div.lRwqcd div.uArJ5e.UQuaGc.Y5sE8d.VkkpIf.NqnGTe").click()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "div.c2gzEf a").click()
        self.driver.quit()
bot = AirBnbFinder()
bot.get_airbnb_data()
bot.post_in_googleforms()
    
    