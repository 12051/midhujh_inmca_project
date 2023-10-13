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
        activity = driver.find_element(By.CSS_SELECTOR, "a#activity")
        activity.click()
        time.sleep(1)
        reportcrime = driver.find_element(By.CSS_SELECTOR, "a#reportcrime")
        reportcrime.click()
        time.sleep(1)
        slt = driver.find_element(By.CSS_SELECTOR, "select#crimeCategory")
        slt.click()
        time.sleep(1)
        slt_human = driver.find_element(By.CSS_SELECTOR, "option[value='off_doc']")
        slt_human.click()
        time.sleep(1)
        chk = driver.find_element(By.CSS_SELECTOR, "label[for='termsCheckbox']")
        chk.click()
        time.sleep(1)
        sub = driver.find_element(By.CSS_SELECTOR, "button[onclick='redirectToPage()']")
        sub.click()
        time.sleep(1)
        aadh=driver.find_element(By.CSS_SELECTOR,"input#ano[type='text']")
        aadh.send_keys("987605479087")
        time.sleep(1)
        aadh=driver.find_element(By.CSS_SELECTOR,"input#email[type='email']")
        aadh.send_keys("midhujh27@gmail.com")
        time.sleep(1)
        rad=driver.find_element(By.CSS_SELECTOR,"input[type='radio'][name='threat'][value='Yes']")
        rad.click()
        time.sleep(1)
        des=driver.find_element(By.CSS_SELECTOR,"textarea#descri")
        des.send_keys("Manu Joseph, Phone: 9999999999, On 11-10-2023, I discovered a potentially forged document while reviewing SSLC Certificates. The document exhibited suspicious alterations, including questionable signatures and discrepancies in dates.")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        file_path = 'C:\\Users\\Midhu J H\\Downloads\\user.jpg'
        evi_image_input = driver.find_element(By.CSS_SELECTOR, "input#id_evidence_image[type='file']")
        evi_image_input.send_keys(file_path)
        time.sleep(3)
        btn=driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
        btn.click()
        time.sleep(3)
        log = driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/logout/'")
        log.click()
        time.sleep(2)
        login2=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='http://127.0.0.1:8000/login']")
        login2.click()
        time.sleep(1)
        email=driver.find_element(By.CSS_SELECTOR,"input#email[name='email']")
        email.send_keys("kanjirappallylawenforcement@gmail.com")
        password=driver.find_element(By.CSS_SELECTOR,"input#password[name='password']")
        password.send_keys("Midhu1.jayan")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        submit = driver.find_element(By.CSS_SELECTOR, "button#login")
        submit.click()
        time.sleep(1)
        activity2 = driver.find_element(By.CSS_SELECTOR, "a.nav-link#activity[data-toggle='dropdown']")
        activity2.click()
        time.sleep(1)
        managecrime = driver.find_element(By.CSS_SELECTOR, "a#managecrime[href='/law_page']")
        managecrime .click()
        time.sleep(1)
        btndetails = driver.find_element(By.CSS_SELECTOR, "a[href='/view_crime/37'] > button.btn.btn-light.edit-button")
        btndetails .click()
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(3)
        file_path_ = 'C:\\Users\\Midhu J H\\Downloads\\Report_9.pdf'
        file_in = driver.find_element(By.CSS_SELECTOR, "input[type='file'][name='document_arrest'][id='id_document_arrest']")
        file_in.send_keys(file_path_)
        time.sleep(5)
        btnupl = driver.find_element(By.CSS_SELECTOR, "button#charge-arrest")
        btnupl.click()
        time.sleep(2)
        activity3 = driver.find_element(By.CSS_SELECTOR, "a.nav-link#acti[data-toggle='dropdown']")
        activity3.click()
        time.sleep(1)
        managecrimestatus = driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href='/law_page']")
        managecrimestatus.click()
        time.sleep(2)
        log2 = driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/logout/']")
        log2.click()
        time.sleep(2)
        
        
        
        
        
        
        
        
        
        
        


        

    # Add more test methods as needed

if __name__ == '__main__':
    import unittest
    unittest.main()