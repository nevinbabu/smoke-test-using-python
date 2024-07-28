"""Simple smoke test"""
# open webbrowser
# open url
# Capture title to check if its correct webpage
# Enter username
# Enter password
# login
# logout
# close browser
import time
import os
import unittest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
USERNAME = os.getenv("SAUCE_USERNAME")
PASSWD = os.getenv("SAUCE_PASSWD")
URL = "https://www.saucedemo.com/"


class SmokeTest(unittest.TestCase):
    """Smoke test for SauceDemo"""
    driver = None

    @classmethod
    def setUpClass(cls):
        service = Service("chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service)

    def test_1_title(self):
        """Test if the title is correct"""
        print("testing url")
        self.driver.get(URL)
        self.assertIn(self.driver.title, "Swag Labs")

    def test_2_login(self):
        """Test if the login is successfull"""
        print("testing login")
        self.driver.find_element(By.NAME, "user-name").send_keys(USERNAME)
        self.driver.find_element(By.NAME, "password").send_keys(PASSWD)
        self.driver.find_element(By.ID, "login-button").click()

        # Checking if the login was successfull
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'inventory_list'))
        )
        self.assertIn('inventory.html', self.driver.current_url)

    def test_3_logout(self):
        """Test if the logout is successfull"""
        print("testing logout")
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        # self.driver.find_element(By.ID, "logout_sidebar_link").click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-button'))
        )
        self.assertEqual('https://www.saucedemo.com/', self.driver.current_url)

    @classmethod
    def tearDownClass(cls):
        print("tearing down")
        time.sleep(2)
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
