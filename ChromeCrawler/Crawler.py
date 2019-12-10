from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ImageHandler.Handler import DownloadImage, PathMaker
import json, time

def InitChorme():
    file = open('ChromeCrawler/settings.json')
    settings = json.loads(file.read())
    executable_path = settings.get('DriverPath')
    try:
        return webdriver.Chrome(executable_path=executable_path)
    except:
        print('[Error]wrong chrome driver path')

class ChromeInstaCrawler():

    ImageRowClassName = 'Nnq7C'
    CntImg = 0
    last_image_src = ""

    def __init__(self):
        self.driver = InitChorme()

    def CloseAlarmSetting(self): #close alarm modal when login
        driver = self.driver
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "나중에 하기")]'))
        )
        element.click()
        # self.driver = driver

    def Login(self, username, password): #login to Instagram
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
            self.CloseAlarmSetting()
        except:
            print("[ERROR]login_unable")

    def Search(self, q): #search for the query manually
        driver = self.driver
        driver.find_element_by_xpath("//input[@placeholder='검색']").send_keys(q)
        try:
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fuqBx']/a"))
            )
            elements[0].click()
        except:
            print("[ERROR]search_unable")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, self.ImageRowClassName))
            )
        except:
            print("[ERROR]no_searched_images")
        self.q = q

    def SearchByUrl(self, q): #search for the query by url
        driver = self.driver
        url_path="https://www.instagram.com/explore/tags/"+q+"/"
        driver.get(url_path)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, self.ImageRowClassName))
            )
        except:
            print("[ERROR]no_searched_images")
        self.q = q

    def MakeImagePath(self):
        path = "data/" + self.q + "/"
        path = PathMaker(path)
        self.path = path

    def DownloadImages(self):
        driver = self.driver
        path = self.path

        download = False
        if not self.last_image_src:
            download = True

        elements = driver.find_elements_by_class_name(self.ImageRowClassName)

        for element in elements:
            imgs = element.find_elements_by_tag_name('img')

            for img in imgs:
                src = img.get_attribute('src')
                if download:
                    DownloadImage(src, path=path)
                    self.CntImg +=1
                    print(str(self.CntImg)+" completed")
                    self.last_image_src = src
                else:
                    if self.last_image_src == src:
                        download = True

    def Scroller(self, y = "document.body.scrollHeight"):
        driver = self.driver
        driver.execute_script("window.scrollTo(0,"+y+");")
        time.sleep(1)

    def execute(self, username, password, query, maxcnt):
        self.Login(username, password)
        self.SearchByUrl(query)
        self.MakeImagePath()
        while self.CntImg <maxcnt:
            self.DownloadImages()
            self.Scroller()




