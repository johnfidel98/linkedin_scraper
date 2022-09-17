import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .objects import Experience, Education, Scraper, Interest, Contact, Skill
import os
from linkedin_scraper import selectors


class Person(Scraper):

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        skills=None,
        interests=None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.also_viewed_urls = []
        self.contacts = contacts or []
        self.skills = skills or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)
    
    def add_skill(self, interest):
        self.skills.append(interest)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")
            x = input("please verify the capcha then press any key to continue...")
            self.scrape_not_logged_in(close_on_complete=close_on_complete)

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME,"button").click()
        except Exception as e:
            pass

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.__TOP_CARD,
                )
            )
        )

        self.name = root.find_element(By.CLASS_NAME, selectors.NAME).text.strip()

        # get about
        try:
            see_more = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#about + div + div.ph5 button"))
            )
            driver.execute_script("arguments[0].click();", see_more)

            about = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "#about + div + div.ph5",
                    )
                )
            )
        except:
            about = None
        if about:
            self.add_about(about.text.strip())

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

        # get experience
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/5));"
        )

        ## todo Click SEE MORE
        """
        try:
            see_more_experience = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        '#experience + div + div.pvs-list__outer-container div.pvs-list__footer-wrapper a',
                    )
                )
            )
            driver.execute_script("arguments[0].click();", see_more_experience)
            in_enperience = True
        except:
            in_enperience = False
        """

        try:
            exp = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "experience"))
            )
        except:
            exp = None

        if exp is not None:
            for position in driver.find_elements(By.CSS_SELECTOR, "#experience + div + div.pvs-list__outer-container li.artdeco-list__item"):
                position_title = position.find_element(By.CSS_SELECTOR,"span.mr1").text.strip()

                try:
                    company = position.find_element(By.CSS_SELECTOR,"span.t-14").text.strip()
                    duration = position.find_element(By.CSS_SELECTOR,"span.t-14.t-black--light").text.strip()
                except:
                    company, duration = None, None

                experience = Experience(
                    position_title=position_title,
                    duration=duration
                )
                experience.institution_name = company
                self.add_experience(experience)

        # get location
        location = driver.find_element(By.CSS_SELECTOR, "div.pb2:has(> span.text-body-small) span.text-body-small").text
        self.add_location(location)

        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get education
        ## Click SEE MORE
        # self._click_see_more_by_class_name("pv-education-section__see-more")
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "education"))
            )
            edu = driver.find_element(By.ID,"education")
        except:
            edu = None
        if edu:
            for school in edu.find_elements(By.CSS_SELECTOR,
                "#education + div + div.pvs-list__outer-container li.artdeco-list__item"
            ):
                university = school.find_element(By.CSS_SELECTOR,
                    "span.mr1"
                ).text.strip()

                try:
                    degree = school.find_element(By.CSS_SELECTOR,"span.t-14").text.strip()
                    times = (
                        school.find_element(By.CSS_SELECTOR,"span.t-14.t-black--light").text.strip().split('-')
                    )
                    from_date, to_date = (times.split(" ")[0], times.split(" ")[2])
                except:
                    degree = None
                    from_date, to_date = (None, None)
                education = Education(
                    from_date=from_date, to_date=to_date, degree=degree
                )
                education.institution_name = university
                self.add_education(education)

        # get interest
        try:

            interests = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        "#interests + div + div div.pvs-list__outer-container li.artdeco-list__item",
                    )
                )
            )
            for interestElement in interests:
                interest = Interest(
                    interestElement.find_element(By.CSS_SELECTOR,"span.mr1").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get skills
        try:
            skills = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "skills"))
            )
        except:
            skills = None
        if skills:
            for skill_block in driver.find_elements(By.CSS_SELECTOR, "#skills + div + div div.pvs-entity"):
                skill_name = skill_block.find_element(By.CSS_SELECTOR, "span.mr1").text.strip()

                try:
                    endorsements = skill_block.find_element(By.CSS_SELECTOR, "li:last-child .t-14").text.strip()
                except:
                    endorsements = None
                skill = Skill(
                    name=skill_name, endorsements=endorsements
                )
                self.add_skill(skill)

        if close_on_complete:
            driver.quit()

    def scrape_not_logged_in(self, close_on_complete=True, retry_limit=10):
        driver = self.driver
        retry_times = 0
        while self.is_signed_in() and retry_times <= retry_limit:
            page = driver.get(self.linkedin_url)
            retry_times = retry_times + 1

        # get name
        self.name = driver.find_element(By.CLASS_NAME,
            "top-card-layout__title"
        ).text.strip()

        # get experience
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "experience"))
            )
            exp = driver.find_element(By.CLASS_NAME,"experience")
        except:
            exp = None

        if exp is not None:
            for position in exp.find_elements(By.CLASS_NAME,
                "experience-item__contents"
            ):
                position_title = position.find_element(By.CLASS_NAME,
                    "experience-item__title"
                ).text.strip()
                company = position.find_element(By.CLASS_NAME,
                    "experience-item__subtitle"
                ).text.strip()

                try:
                    times = position.find_element(By.CLASS_NAME,
                        "experience-item__duration"
                    )
                    from_date = times.find_element(By.CLASS_NAME,
                        "date-range__start-date"
                    ).text.strip()
                    try:
                        to_date = times.find_element(By.CLASS_NAME,
                            "date-range__end-date"
                        ).text.strip()
                    except:
                        to_date = "Present"
                    duration = position.find_element(By.CLASS_NAME,
                        "date-range__duration"
                    ).text.strip()
                    location = position.find_element(By.CLASS_NAME,
                        "experience-item__location"
                    ).text.strip()
                except:
                    from_date, to_date, duration, location = (None, None, None, None)

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                )
                experience.institution_name = company
                self.add_experience(experience)
        driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

        # get education
        edu = driver.find_element(By.CLASS_NAME,"education__list")
        for school in edu.find_elements(By.CLASS_NAME,"result-card"):
            university = school.find_element(By.CLASS_NAME,
                "result-card__title"
            ).text.strip()
            degree = school.find_element(By.CLASS_NAME,
                "education__item--degree-info"
            ).text.strip()
            try:
                times = school.find_element(By.CLASS_NAME,"date-range")
                from_date = times.find_element(By.CLASS_NAME,
                    "date-range__start-date"
                ).text.strip()
                to_date = times.find_element(By.CLASS_NAME,
                    "date-range__end-date"
                ).text.strip()
            except:
                from_date, to_date = (None, None)
            education = Education(from_date=from_date, to_date=to_date, degree=degree)

            education.institution_name = university
            self.add_education(education)

        if close_on_complete:
            driver.close()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return "{name}\n\nAbout\n{about}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nInterest\n{int}\n\nSkills\n{skil}".format(
            name=self.name,
            about=self.about,
            exp=self.experiences,
            edu=self.educations,
            int=self.interests,
            skil=self.skills,
        )
