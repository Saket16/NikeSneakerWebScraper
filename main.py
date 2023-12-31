from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

chrome_driver_path = r"C:\Users\saket\Downloads\chromedriver-win64\chromedriver.exe"

# Create a Service object with the path to the ChromeDriver executable
chrome_service = Service(chrome_driver_path)

# Use the Service object when creating the Chrome WebDriver
driver = webdriver.Chrome(service=chrome_service)
#driver = webdriver.Chrome("chromedriver.exe")
#driver = webdriver.Chrome(r"C:\Users\saket\Downloads\chromedriver-win64\chromedriver.exe")
#"C:\Users\saket\Downloads\chromedriver-win64\chromedriver.exe"
models = []
prices = []
driver.get('https://www.nike.com/w/mens-shoes-nik1zy7ok')
unique_items = set()
for page_number in range(1, 30):
   # time.sleep(.5)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    for element in soup.findAll('div', attrs={'class': 'product-card__body'}):
        model = element.find('div', attrs={'class': 'product-card__title'})
        price = element.find('div', attrs={'class': 'product-price'})
        if model is not None and price is not None:
            item_text = f"{model.text} - {price.text}"
            if item_text not in unique_items:
                unique_items.add(item_text)
                models.append(model.text)
                prices.append(price.text)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
df = pd.DataFrame({'Product Name': models, 'Price': prices})
df.to_csv('sneakers.csv', index=False, encoding='utf-8')
driver.quit()