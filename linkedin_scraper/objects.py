from dataclasses import dataclass

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from . import constants as c


@dataclass
class Contact:
    name: str = None
    occupation: str = None
    url: str = None


@dataclass
class Skill:
    name: str = None
    endorsements: int = None


@dataclass
class Institution:
    institution_name: str = None


@dataclass
class Experience(Institution):
    position_title: str = None
    duration: str = None


@dataclass
class Education(Institution):
    from_date: str = None
    to_date: str = None
    degree: str = None


@dataclass
class Interest:
    title = None


@dataclass
class Scraper:
    driver: Chrome = None

    def is_signed_in(self):
        try:
            self.driver.find_element(By.ID, c.VERIFY_LOGIN_ID)
            return True
        except:
            pass
        return False

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME,"class_name")
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element(By.XPATH,"tag_name")
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element(By.XPATH,"tag_name")
            return elem.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element__(cls, *args):
        for elem in args:
            if elem:
                return elem[0]
