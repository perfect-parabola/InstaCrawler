from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def InitChorme():
    file = open('ChromeCrawler/settings.json')
    settings = json.loads(file.read())
    executable_path = settings.get('DriverPath')
    try:
        return webdriver.Chrome(executable_path=executable_path)
    except:
        print('[Error]wrong chrome driver path')

class ChromeInstaCrawler():

    def __init__(self):
        self.driver = InitChorme()

    def close_alarm_setting(self): #close alarm modal when login
        driver = self.driver
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "나중에 하기")]'))
        )
        element.click()
        # self.driver = driver

    def login(self, username, password): #login to Instagram
        driver = self.driver
        InstaLoginUrl = "https://www.instagram.com/accounts/login/?source=auth_switcher"
        driver.get(InstaLoginUrl)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'username'))
            )
            driver.find_element_by_name('username').send_keys(username)
            driver.find_element_by_name('password').send_keys(password)
            driver.find_element_by_xpath("//button[@type='submit']").click()
            self.close_alarm_setting()
        except:
            print("[ERROR]login_unable")

    def search(self, q): #search for the query manually
        driver = self.driver
        driver.find_element_by_xpath("//input[@placeholder='검색']").send_keys(q)
        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fuqBx']/a"))
            )
            elements[0].click()
        except:
            print("[ERROR]search_unable")

    def search_by_url(self, q): #search for the query by url
        driver = self.driver
        url_path="https://www.instagram.com/explore/tags/"+q+"/"
        driver.get(url_path)





