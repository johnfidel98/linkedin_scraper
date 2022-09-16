from selenium import webdriver
from decouple import config
from linkedin_scraper import Person, actions


driver = webdriver.Chrome('chromedriver.exe') 
actions.login(driver, config('email'), config('password'))

#iggy = Person("https://www.linkedin.com/in/pawan-kumar-sharma-b179621bb", driver=driver)
Anirudra = Person("https://in.linkedin.com/in/anirudra-choudhury-109635b1", driver=driver)
print()
