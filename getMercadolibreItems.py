from sys import prefix
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import re
import requests
from random import randrange
from PIL import Image
from Screenshot import Screenshot_Clipping


#datos vendedor
item_id = 'MLU478347178'
category_id = 'MLU6330'
seller_id = '493860478'
nombre = 'test2'

#ruta de chrome
driver_path = ''


chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument("no-sandbox");
chrome_options.add_argument("window-size=1920,1080");

#para tener solo la consola
#chrome_options.add_argument("headless");

driver = webdriver.Chrome(driver_path, options=chrome_options)


driver.set_window_position(2000, 0)
driver.maximize_window()
# gives an implicit wait for 20 seconds
driver.implicitly_wait(10)


def _init(url):
    url_array = []
    driver.get(url)

    try:
        l = driver.find_elements(By.CLASS_NAME, "ui-search-link")
    except:
        driver.close()
        print("Error")

    for i in l:
        if "MLU-" in i.get_property('href'):
            url_array.append(i.get_property('href'))

    print('-' * 100)
    try:
        driver.find_element(By.ID, "newCookieDisclaimerButton").click()
    except:
        print('No disclaimer one')


    try:
        driver.find_element(By.CLASS_NAME, "cookie-consent-banner-opt-out__action--key-accept").click()
    except:
        print('No disclaimer two')


    url_array = list(dict.fromkeys(url_array))

    num = 0
    for i in url_array:
        driver.get(i)
        print(
            driver.find_element(
                By.XPATH,
                "/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1"
            ).text)
        folder_name = driver.find_element(
            By.XPATH,
            "/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1"
        ).text
        folder_name = re.sub('[^A-Za-z0-9]+', '', folder_name) + '-' + str(num)
        try:
            ventas = driver.find_element(By.CLASS_NAME, "ui-pdp-subtitle").text
            ventas = int(re.search(r'\d+', ventas).group())
        except:
            ventas = 0
        folder_name = str(ventas) + '-' + folder_name
        prefix = 'C:/Users/Alvi/Desktop/' + nombre
        folder = os.path.join(prefix, folder_name)
        file_name = 'desc.txt'

        os.makedirs(folder, exist_ok=True)

        try:
            obj = Screenshot_Clipping.Screenshot()
            img_loc = obj.full_Screenshot(driver,
                                          save_path=folder,
                                          image_name='ss.png')
        except:
            print('error ss')

        item = driver.find_elements(By.CLASS_NAME,
                                    "andes-table__column--value")
        file = os.path.join(folder, file_name)
        images = driver.find_elements(By.CLASS_NAME,
                                      "ui-pdp-gallery__figure__image")

        for i in images:
            imgnamegen = randrange(1, 100000)
            imgname = str(imgnamegen) + '.jpg'
            imgfile = os.path.join(folder, imgname)
            try:
                img_data = requests.get(i.get_property('src')).content
                with open(imgfile, 'wb') as handler:
                    handler.write(img_data)
            except:
                print('img error')

        num += 1

        with open(file, 'w') as f:
            f.write(driver.find_element(By.CLASS_NAME, "ui-pdp-title").text)
            f.write('\n')
            f.write('precio:')
            f.write(
                driver.find_element(By.CLASS_NAME,
                                    "ui-pdp-price__second-line").text)
            f.write('\n')
            f.write('\n')
            f.write('-' * 100)
            for i in item:
                f.write(i.text)
                f.write('\n')
            f.write('-' * 100)
            f.write('\n')
            f.write(
                driver.find_element(By.CLASS_NAME, "ui-pdp-description").text)



#----------------------------------------------------------------
items_per_page = 51
for i in range(0, 2):
    if i == 0:
        url = 'https://listado.mercadolibre.com.uy/_CustId_'+ seller_id +'?item_id='+ item_id +'&category_id'+ category_id +'&seller_id='+ seller_id +'&client=recoview-selleritems&recos_listing=true'
        _init(url)
    else:
        url = 'https://listado.mercadolibre.com.uy//_Desde_'+ str(items_per_page) +'_CustId_'+ seller_id +'?item_id='+ item_id +'&category_id'+ category_id +'&seller_id='+ seller_id +'&client=recoview-selleritems&recos_listing=true'
        _init(url)

driver.close()

