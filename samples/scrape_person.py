import os
from linkedin_scraper import Person, actions
from selenium import webdriver
# driver = webdriver.Chrome("../chromedriver")
driver = webdriver.Chrome(executable_path='/Users/sushil/Documents/exec/chromedriver/chromedriver')

email = "pawan1995219@gmail.com"
password = "pawansharma999"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
person = Person("https://www.linkedin.com/in/pawan-kumar-sharma-b179621bb", driver=driver)
print(person)
