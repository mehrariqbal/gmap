from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

location = 'south end'
item = 'charities'
#url = f"https://www.google.com/maps/search/{item}+in+{location} UK?hl=en".format(item,location)
url = f"https://www.google.com/maps/place/A+Better+Start+Southend/@51.5435842,0.7125057,17z/data=!3m1!4b1!4m6!3m5!1s0x47d8d946e05feaad:0x312c9d9d9c245b79!8m2!3d51.5435842!4d0.7125057!16s%2Fg%2F11fxx25jq1?authuser=0&hl=en&entry=ttu"
#chrom_driver_path = "C:\\Program Files\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=r"C:\\Program Files\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

option = webdriver.ChromeOptions()
#option.add_argument("--headless")  # Run Chrome in headless mode (without a visible browser window)
option.add_argument("--lang=en")
driver = webdriver.Chrome(service=service, options=option)
driver.get(url)

panel2 = driver.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div")
time.sleep(5)

#panel2 = panel.find_element(By.CLASS_NAME,"")
try:
    name = panel2.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1").text
except Exception as e:
    name = ''
try:
    review = panel2.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]").text
except:
    review = ''
try:
    Type = panel2.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/span").text
except:
    Type = ''
try:
    address_button = panel2.find_element(By.XPATH, "//button[@data-item-id='address']")
    address_full_a = address_button.get_attribute('aria-label').split(":")[-1]
    address_full_b = address_full_a.split(",")
    address = ','.join(address_full_b[:-2])
    region = address_full_b[-2].split(" ")[1]
    postcode = ' '.join(address_full_b[-2].split(" ")[2:])
    country = address_full_b[-1]
    #address_full = panel2.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]").text.split(',')
    # address = ','.join(address_full[:-2])[:-1]
    # postcode = ' '.join(address_full[-2].split(" ")[2:])
    # country = address_full[-1]
except:
    address = ''
    region
    postcode = ''
    ountry = ''

try:
    WebAddress_a= panel2.find_element(By.XPATH,"//a[@data-item-id='authority']")
    WebAddress = WebAddress_a.get_attribute('aria-label').split(":")[-1]
except:
    WebAddress='error'

try:
    Phone_a = panel2.find_element(By.XPATH,"//button[@data-tooltip='Copy phone number']")
    Phone = Phone_a.get_attribute('aria-label').split(":")[-1]
except:
    Phone = 'error'
    


print(name,review,Type,address,region,postcode,country,WebAddress,Phone)



#time.sleep(10)
# x = 0
# while True:
#     driver.execute_script("arguments[0].scrollTop += 100;", panel)
#     x+=1
#     time.sleep(1)
#     print(x)
#     if x> 200:
#         break

#driver.execute_script("arguments[0].scrollTop += 1000;", panel)
