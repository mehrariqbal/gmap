from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

location = 'south end'
item = 'charities'
#url = f"https://www.google.com/maps/search/{item}+in+{location} UK?hl=en".format(item,location)
url = f"https://www.google.com/maps/search/charities+in+southend-UK/@51.5436816,-77.3411665,3z?hl=en&entry=ttu"
service = Service(executable_path=r"C:\\Program Files\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")

option = webdriver.ChromeOptions()
#option.add_argument("--headless")  # Run Chrome in headless mode (without a visible browser window)
#option.add_argument("--lang=en")
chrome_prefs = {"profile.managed_default_content_settings.javascript": 1}
option.add_experimental_option("prefs", chrome_prefs)

driver = webdriver.Chrome(service=service, options=option)
driver.get(url)
print("getting url")

driver.implicitly_wait(10)

panel = driver.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]")
time.sleep(5)
text = "You've reached the end of the list."
print("<--------scrolling the page-------->")

x=0
while True:
    driver.execute_script("arguments[0].scrollTop += arguments[0].scrollHeight;", panel)
    time.sleep(1)
    print('/////////--',x,'--\\\\\\\\', end='',flush=True)
    x +=1
    print('\r', end='', flush=True)
    if text in panel.text:
        break


print("Full Page Loading completed")
page_source = driver.page_source


column_name = ['Name','Review','Type','Address','Region','Postcode','Country','WebAddress','Phone']
df = pd.DataFrame(columns=column_name)

sp = BeautifulSoup(page_source,"html.parser")
        
charity_urls = [a["href"] for a in sp.find_all("a", class_="hfpxzc")]
print("numer of toal charities: ",len(charity_urls))
print("getting data for each charity")
for url in charity_urls:
    driver.get(url)
    time.sleep(1)
    panel2 = driver.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div")
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
    except:
        address = ''

    try:
        WebAddress_a= panel2.find_element(By.XPATH,"//a[@data-item-id='authority']")
        WebAddress = WebAddress_a.get_attribute('aria-label').split(":")[-1]
    except:
        WebAddress=''

    try:
        Phone_a = panel2.find_element(By.XPATH,"//button[@data-tooltip='Copy phone number']")
        Phone = Phone_a.get_attribute('aria-label').split(":")[-1]
    except:
        Phone = ''
        


    print(name,review,Type,address,region,postcode,country,WebAddress,Phone)
    new_row = pd.DataFrame([[name,review,Type,address,region,postcode,country,WebAddress,Phone]],columns=column_name)
    df = pd.concat([df,new_row],ignore_index=True)
    
print("Data sourcig completed. Saving the excel file..")

df.to_excel("charities.xlsx")