from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
from instagram_bot import InstagramBot

# Script to find who doest follow you back
# TODO find a safe way to store the password and email
USERNAME = ""
PASSWORD = ""

driver = webdriver.Chrome()

instagram_bot = InstagramBot(driver, USERNAME, PASSWORD)
print(instagram_bot.find_not_follow_back_people())