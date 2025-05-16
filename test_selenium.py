from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Create web driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

#Open website
driver.get("https://edition.cnn.com/")

#Finding element on website
try:
    menu_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/header/div/nav/div/div/div[1]/div[1]/button[1]'))
    )
    menu_button.click()

    topic_header = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/header/div/nav/div/div/div[2]/div/nav[2]/ul/li[3]/a'))
    )
    topic_header.click()

    news_topic = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section[3]/section[1]/div/section/div/div/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/div/div/div[1]/a[2]'))
    )
    news_topic.click()

except Exception as e:
    print(f"Error details: {e}")


