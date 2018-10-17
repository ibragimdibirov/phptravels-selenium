import time

import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# *****************************************************************************
# Unit test suite
# *****************************************************************************
class AssignTest(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1366,788")
    cls.email = "EMAIL-HERE"
    cls.password = "PASSWORD-HERE"
    cls.url="http://www.phptravels.net"
    cls.driver = webdriver.Chrome(chrome_options=options)
    cls.wait = WebDriverWait(cls.driver, 10)


  @classmethod
  def tearDownClass(cls):
    cls.driver.quit()

  def test1_login_bad_password(self):
    ##########################
    # I - Test bad password login #
    ##########################
    self.driver.get("http://www.phptravels.net/login")
    time.sleep(5)
    email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    email.clear()
    email.send_keys(self.email)
    password = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
    password.clear()
    password.send_keys("wrongpassword")
    login = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login.click()
    time.sleep(5)
    assert len(self.driver.find_elements_by_xpath("//div[text()='Invalid Email or Password']")) != 0

  def test2_login(self):
    ##########################
    # I - Test good credentials login #
    ##########################
    self.driver.get("http://www.phptravels.net/login")
    time.sleep(5)
    email = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    email.clear()
    email.send_keys(self.email)
    password = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))
    password.clear()
    password.send_keys(self.password)
    login = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
    login.click()
    time.sleep(5)
    assert self.driver.title == 'My Account'

  def search(self, hotel_city, check_in_date, check_out_date, travelers_count):
    ##########################
    # I - Helper Search #
    ##########################
    self.driver.get("http://www.phptravels.net/login")
    home = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='container']//a[text()='Home']")))
    home.click()
    hotel = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'hotelsearch locationlisthotels')]")))
    hotel.click()
    actions = ActionChains(self.driver)
    actions.send_keys(hotel_city).perform()
    result = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select2-result-label')]//span")))
    result.click()
    time.sleep(5)
    check_in = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='HOTELS']//input[@placeholder='Check in']")))
    check_in.send_keys(check_in_date)
    check_out = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='HOTELS']//input[@placeholder='Check out']")))
    check_out.send_keys(check_out_date)
    travelers = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='HOTELS']//input[@id='travellersInput']")))
    travelers.clear()
    travelers.send_keys(travelers_count)
    search = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'search-button')]//button")))
    search.click()
    time.sleep(5)

  def test3_search_case_1(self):
    ##########################
    # I - Test Search #
    ##########################
    self.search("Montreal", "20/10/2018", "30/10/2018", "2 Adult 0 Child")
    assert self.driver.title == 'Search Results'

  def test3_search_case_2(self):
    ##########################
    # I - Test Search #
    ##########################
    self.search("Montreal", "20/10/2018", "5/10/2018", "2 Adult 0 Child")
    assert self.driver.title == 'Search Results'

  def test3_search_case_3(self):
    ##########################
    # I - Test Search #
    ##########################
    self.search("Montreal", "20/10/2018", "30/10/2018", "0 Adult 0 Child")
    assert self.driver.title == 'Search Results'

if __name__ == "__main__":
  unittest.main()
