from Functions.Initialize import Initialize
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, NoSuchWindowException, \
    TimeoutException
from selenium.webdriver.ie.options import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as OpcionesChrome
from selenium.webdriver.support.ui import Select
import pytest
import json
import time
import re
import os
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException

Scenario = {}
GlobalDay = time.strftime(Initialize.DateFormat)
GlobalHour = time.strftime(Initialize.HourFormat)


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

    def tear_down(self):
        print("The driver is closed")
        self.driver.quit()

    def xpath_element(self, XPATH):
        elements = self.driver.find_element_by_xpath(XPATH)
        print("Xpath_Element: Element used " + XPATH)
        return elements

    def _xpath_element(self, XPATH):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, XPATH)))
            elements = self.driver.find_element_by_xpath(XPATH)
            print(u"Waiting for element...: Item was displayed " + XPATH)
            return elements

        except TimeoutException:
            print(u"Waiting for element...: Element not present " + XPATH)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Waiting for element: Element not present " + XPATH)
            Functions.tearDown(self)

    def _id_element(self, ID):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, ID)))
            elements = self.driver.find_element_by_id(ID)
            print(u"Wait element: Item was displayed " + ID)
            return elements

        except TimeoutException:
            print(u"Wait element: Element not present " + ID)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Wait element: Element not present " + ID)
            Functions.tearDown(self)

    def name_element(self, name):
        elements = self.driver.find_element_by_name(name)
        print("Xpath_Elements: The element was used " + name)
        return elements

    def _name_element(self, name):
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.ID, name)))
            elements = self.driver.find_element_by_id(name)
            print(u"Wait element: Item was displayed " + name)
            return elements

        except TimeoutException:
            print(u"Wait element: Element not present " + name)
            Functions.tearDown(self)
        except NoSuchElementException:
            print(u"Wait element: Element not present " + name)
            Functions.tearDown(self)

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

    def get_elements(self, entity, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    elements = self.driver.find_element_by_id(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "name":
                    elements = self.driver.find_element_by_name(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "xpath":
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)
                    elements = self.driver.find_element_by_xpath(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "link":
                    elements = self.driver.find_element_by_partial_link_text(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "css":
                    elements = self.driver.find_element_by_css_selector(self.json_ValueToFind)

                print("get_elements: " + self.json_ValueToFind)
                return elements

            except NoSuchElementException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: Element not present: " + self.json_ValueToFind)
                Functions.tearDown(self)

    def get_text(self, entity, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, entity)

        if Get_Entity is None:
            print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    elements = self.driver.find_element_by_id(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "name":
                    elements = self.driver.find_element_by_name(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "xpath":
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)
                    elements = self.driver.find_element_by_xpath(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "link":
                    elements = self.driver.find_element_by_partial_link_text(self.json_ValueToFind)

                if self.json_GetFieldBy.lower() == "css":
                    elements = self.driver.find_element_by_css_selector(self.json_ValueToFind)

                print("get_text: " + self.json_ValueToFind)
                print("Text Value : " + elements.text)
                return elements.text

            except NoSuchElementException:
                print("get_text: Element not found: " + self.json_ValueToFind)
                Functions.tearDown(self)
            except TimeoutException:
                print("get_text: Element not found: " + self.json_ValueToFind)
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
        WebDriverWait(driver, 30).until(lambda driver: page_state == 'complete')
        assert page_state == 'complete', "Upload was not completed"

    def wait(self, timeLoad=8):
        print("Wait: Start (" + str(timeLoad) + ")")
        try:
            totalWait = 0
            while (totalWait < timeLoad):
                # print("Cargando ... intento: " + str(totalWait))
                time.sleep(1)
                totalWait = totalWait + 1
        finally:
            print("Wait: load finished ... ")

    def wait_element(self, locator, MyTextElement=None):
        Get_Entity = Functions.get_entity(self, locator)
        wait = WebDriverWait(self.driver, 10, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])

        if Get_Entity is None:
            return print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.ID, self.json_ValueToFind)))
                    print(u"Wait element: the item was displayed. " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.NAME, self.json_ValueToFind)))
                    print(u"Wait element: the item was displayed. " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait = WebDriverWait(self.driver, 20)
                    if MyTextElement is not None:
                        self.json_ValueToFind = self.json_ValueToFind.format(MyTextElement)
                        print(self.json_ValueToFind)

                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.XPATH, self.json_ValueToFind)))
                    # wait.until(EC.((By.XPATH, self.json_ValueToFind)))
                    print(u"Wait element: the item was displayed." + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    print(u"Wait element: the item was displayed. " + locator)
                    return True

            except TimeoutException:
                print(u"Wait element: Not present " + locator)
                Functions.tearDown(self)
            except NoSuchElementException:
                print(u"Wait element: Not present " + locator)
                Functions.tearDown(self)

    def check_element(self, locator):
        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            print("The value was not found in the defined Json")
        else:
            try:
                if self.json_GetFieldBy.lower() == "id":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.ID, self.json_ValueToFind)))
                    print(u"check_element: the item was displayed " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "name":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.NAME, self.json_ValueToFind)))
                    print(u"check_element: the item was displayed " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "xpath":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.XPATH, self.json_ValueToFind)))
                    print(u"check_element: the item was displayed " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "link":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                    print(u"check_element: the item was displayed " + locator)
                    return True

                if self.json_GetFieldBy.lower() == "css":
                    wait = WebDriverWait(self.driver, 20)
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.json_ValueToFind)))
                    print(u"check_element: the item was displayed " + locator)
                    return True

            except NoSuchElementException:
                print("get_text: Element not found: " + self.json_ValueToFind)
                return False
            except TimeoutException:
                print("get_text: Element not found: " + self.json_ValueToFind)
                return False

    def assert_text(self, locator, TEXTO):

        Get_Entity = Functions.get_entity(self, locator)

        if Get_Entity is None:
            print("The value was not found in the defined Json")
        else:
            if self.json_GetFieldBy.lower() == "id":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.ID, self.json_ValueToFind)))
                ObjText = self.driver.find_element_by_id(self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "name":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.NAME, self.json_ValueToFind)))
                ObjText = self.driver.find_element_by_name(self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "xpath":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.XPATH, self.json_ValueToFind)))
                ObjText = self.driver.find_element_by_xpath(self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "link":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, self.json_ValueToFind)))
                ObjText = self.driver.find_element_by_partial_link_text(self.json_ValueToFind).text

            if self.json_GetFieldBy.lower() == "css":
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, self.json_ValueToFind)))
                ObjText = self.driver.find_element_by_css_selector(self.json_ValueToFind).text

        print("Verify Text: the value displayed in: " + locator + " is: " + ObjText + " the expected is: " + TEXTO)
        assert TEXTO == ObjText, "Compared values do not match"

    ##############   -=_CAPTURA DE PANTALLA_=-   #############################
    ##########################################################################

    def hora_Actual(self):
        self.hora = time.strftime(Initialize.HourFormat)  # formato 24 horas
        return self.hora

    def crear_path(self):
        dia = time.strftime("%d-%m-%Y")  # formato aaaa/mm/dd
        GeneralPath = Initialize.Path_Evidencias
        DriverTest = Initialize.NAVEGADOR
        TestCase = self.__class__.__name__
        horaAct = globalHour
        x = re.search("Context", TestCase)
        if (x):
            path = f"{GeneralPath}/{dia}/{DriverTest}/{horaAct}/"
        else:
            path = f"{GeneralPath}/{dia}/{TestCase}/{DriverTest}/{horaAct}/"

        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def Screenshot(self, TestCase="ScreenShot"):
        PATH = Functions.crear_path(self)
        img = f'{PATH}/{TestCase}_(' + str(Functions.hora_Actual(self)) + ')' + '.png'
        self.driver.get_screenshot_as_file(img)
        print(img)
        return img
