from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='http://127.0.0.1:8000/login']")
        login.click()
        time.sleep(1)
        email=driver.find_element(By.CSS_SELECTOR,"input#email[name='email']")
        email.send_keys("midhujh27@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input#password[name='password']")
        password.send_keys("Midhu1.jayan")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        submit = driver.find_element(By.CSS_SELECTOR, "button#login")
        submit.click()
        time.sleep(1)
        lang = driver.find_element(By.CSS_SELECTOR, "select.goog-te-combo")
        lang.click()
        time.sleep(1)
        lang_select = driver.find_element(By.CSS_SELECTOR, "option[value='hi']")
        lang_select.click()
        time.sleep(3)
        lang_en = driver.find_element(By.CSS_SELECTOR, "option[value='en']")
        lang_en.click()
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(3)
        loc = driver.find_element(By.CSS_SELECTOR, "h5.card-title#locate_station")
        loc.click()
        time.sleep(2)
        loc_toggle = driver.find_element(By.CSS_SELECTOR, "label.toggle-label[for='toggle']")
        loc_toggle.click()
        time.sleep(2)
        loc_btn = driver.find_element(By.CSS_SELECTOR, "button#btn-find")
        loc_btn.click()
        time.sleep(5)
        bk_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='goBack()']")
        bk_btn.click()
        time.sleep(5)
        crime_status = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/listcrime/']")
        crime_status.click()
        time.sleep(5)
        sug_adv_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/func_app/advocate_detail/58/")]/button[text()="Suggest Advocates"]')))
        sug_adv_button.click()
        time.sleep(2)
        back_btn = driver.find_element(By.CSS_SELECTOR,"button[onclick='goBack()']")
        back_btn.click()
        time.sleep(2)
        view_documents_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/evidence_crime_report/58/")]//button[text()="View Documents"]')))
        view_documents_button.click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        view_doc = driver.find_element(By.CSS_SELECTOR, "a#btn-final.btn.btn-primary")
        view_doc.click()
        
        view_doc.send_keys(Keys.CONTROL + Keys.RETURN)
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        # Navigate to the desired URL
        driver.get("http://127.0.0.1:8000/evidence_crime_report/58/")
        time.sleep(2)
    
        log = driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/logout/'")
        log.click()
        time.sleep(2)
        
        
        


    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()