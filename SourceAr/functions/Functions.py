from selenium.webdriver.common.keys import Keys
from SourceAr.Functions.Initialize import Initialize
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.ie.options import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as OpcionesChrome
import pytest
import json
import time
import re
import os
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.select import Select

global_day = time.strftime(Initialize.date_format)
global_hour = time.strftime(Initialize.hour_format)


class Functions(Initialize):

    def open_browser(self, challenge="", url=Initialize.url, browser=Initialize.browser):
        print("Root: " + Initialize.basedir)
        self.Windows = {}
        print("----------------")
        print(browser)
        print("---------------")

        if browser == ("IExplorer"):
            caps = DesiredCapabilities.INTERNETEXPLORER.copy()
            caps["platform"] = "WINDOWS"
            caps["browserName"] = "internet explorer"
            caps["ignoreZoomSetting"] = True
            caps["requireWindowFocus"] = True
            caps["nativeEvents"] = True
            self.driver = webdriver.Ie(Initialize.basedir + "\\drivers\\IEDriverServer.exe", caps)
            # self.driver.implicitly_wait(10)
            self.driver.maximize_window()
            self.driver.get(url[challenge])
            self.Windows = {'Principal': self.driver.window_handles[0]}
            print(self.Windows)
            return self.driver

        if browser == ("CHROME"):
            options = OpcionesChrome()
            options.add_argument('start-maximized')
            options.add_argument('ignore-certificate-errors')
            self.driver = webdriver.Chrome(executable_path=Initialize.basedir + "\\drivers\\chromedriver.exe",
                                           options=options)
            self.driver.get(url[challenge])
            self.Windows = {'Principal': self.driver.window_handles[0]}
            return self.driver

        if browser == ("FIREFOX"):
            self.driver = webdriver.Firefox()
            self.driver.accept_untrusted_certs = True
            self.driver.maximize_window()
            self.driver.get(url[challenge])
            self.Windows = {'Principal': self.driver.window_handles[0]}
            return self.driver

        if browser == ("OPERA"):
            options = OpcionesChrome()
            options.add_argument('start-maximized')
            options.add_argument('ignore-certificate-errors')
            self.driver = webdriver.Chrome(executable_path=Initialize.basedir + "\\drivers\\operadriver.exe",
                                           options=options)
            self.driver.get(url[challenge])
            self.Windows = {'Principal': self.driver.window_handles[0]}
            return self.driver

    def tearDown(self):
        print("The driver is closed")
        self.driver.quit()

    def get_api_endpoint(self, endpoint):
        return Initialize.api_endpoint[endpoint]

    def get_json_file(self, directory, file):
        json_path = Initialize.Json + "/" + directory + "/" + file + '.json'
        try:
            with open(json_path, "r") as read_file:
                self.json_strings = json.loads(read_file.read())
                print("get_json_file: " + json_path)
        except FileNotFoundError:
            self.json_strings = False
            pytest.skip(u"get_json_file: File not found " + file)
            Functions.tearDown(self)

    def get_entity(self, entity):
        if self.json_strings is False:
            print("Define the DOM for this test")
        else:
            try:
                self.json_ValueToFind = self.json_strings[entity]["ValueToFind"]
                self.json_GetFieldBy = self.json_strings[entity]["GetFieldBy"]
                print(self.json_ValueToFind)
                print(self.json_GetFieldBy)
                return True

            except KeyError:
                pytest.skip(u"get_entity: Key not found " + entity)
                # self.driver.close()
                Functions.tearDown(self)
                return None

    def get_elements(self, entity, my_text_element=None):
        get_entity = Functions.get_entity(self, entity)
        wait = WebDriverWait(self.driver, 30, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                 ElementClickInterceptedException, ElementNotInteractableException])

        if get_entity is None:
            print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.ID, self.json_ValueToFind)))
                    elements = self.driver.find_element_by_id(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "name":
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.NAME, self.json_ValueToFind)))
                    elements = self.driver.find_element_by_name(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "xpath":
                    if my_text_element is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(my_text_element)
                    # wait.until(EC.invisibility_of_element_located((By.XPATH, "//body/div[6]/div[1]/div[1]/img[1]")))
                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.XPATH, self.json_ValueToFind)))
                    elements = self.driver.find_element_by_xpath(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "link":
                    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, self.json_ValueToFind)))
                    elements = self.driver.find_element_by_link_text(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "css":
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.json_ValueToFind)))
                    elements = self.driver.find_element_by_css_selector(self.json_ValueToFind)

                return elements

            except NoSuchElementException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except ElementClickInterceptedException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except ElementNotInteractableException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def get_select_elements(self, entity):
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    select = Select(self.driver.find_element_by_id(self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "name":
                    select = Select(self.driver.find_element_by_name(self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "xpath":
                    select = Select(self.driver.find_element_by_xpath(self.json_ValueToFind))

                if self.json_GetFieldBy.lower() == "link":
                    select = Select(self.driver.find_element_by_partial_link_text(self.json_ValueToFind))

                print("get_select_elements: " + self.json_ValueToFind)
                return select

            except NoSuchElementException:
                print("Element not found: " + self.json_ValueToFind)
                Functions.tearDown(self)

            except TimeoutException:
                print("Element not found: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def select_by_text(self, entity, text):
        Functions.get_select_elements(self, entity).select_by_visible_text(text)

    def send_key_text(self, entity, text):
        Functions.get_elements(self, entity).clear()
        Functions.get_elements(self, entity).send_keys(text)

    def page_has_loaded(self):
        driver = self.driver
        print("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = driver.execute_script('return document.readyState;')
        yield
        WebDriverWait(driver, 30).until(lambda driver_control: page_state == 'complete')
        assert page_state == 'complete', "Upload was not completed"

    def current_time(self):
        self.time = time.strftime(Initialize.HourFormat)  # formato 24 horas
        return self.time

    def create_path(self):
        day = time.strftime("%d-%m-%Y")  # formato aaaa/mm/dd
        general_path = Initialize.path_evidences
        driver_test = Initialize.browser
        test_case = self.__class__.__name__
        current_time = global_hour
        x = re.search("Context", test_case)
        if x:
            path = f"{general_path}/{day}/{driver_test}/{current_time}/"
        else:
            path = f"{general_path}/{day}/{test_case}/{driver_test}/{current_time}/"

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def screen_shot(self, test_case="screenshot"):
        path = Functions.create_path(self)
        img = f'{path}/{test_case}_(' + str(Functions.current_time(self)) + ')' + '.png'
        self.driver.get_screenshot_as_file(img)
        print(img)
        return img

    def select_option(self, select, text):
        select_objet = Select(select)
        nuevo = select.find_elements_by_tag_name("option")
        self.flag_selection = False
        for option in nuevo:
            if option.get_attribute("value") == str(text):
                option.click()
                self.flag_selection = True

        return self.flag_selection

    def scroll_to(self, locator):
        get_entity = Functions.get_entity(self, locator)
        wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException,
                                                 ElementClickInterceptedException])
        if get_entity is None:
            return print("Json value not found")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.ID, self.json_ValueToFind)))
                    locator_ = self.driver.find_element(By.ID, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", locator_)
                    print(u"scroll_to: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.XPATH, self.json_ValueToFind)))
                    locator_ = self.driver.find_element(By.XPATH, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", locator_)
                    print(u"scroll_to: " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, self.json_ValueToFind)))
                    locator_ = self.driver.find_element(By.PARTIAL_LINK_TEXT, self.json_ValueToFind)
                    self.driver.execute_script("arguments[0].scrollIntoView();", locator_)
                    print(u"scroll_to: " + locator)
                    return True

            except NoSuchElementException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except ElementClickInterceptedException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def send_especific_keys(self, element, key):
        if key == 'Enter':
            Functions.get_elements(self, element).send_keys(Keys.ENTER)
        if key == 'Tab':
            Functions.get_elements(self, element).send_keys(Keys.TAB)
        if key == 'Space':
            Functions.get_elements(self, element).send_keys(Keys.SPACE)


