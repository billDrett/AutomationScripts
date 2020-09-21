from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary  # Adds chromedriver binary to path

from datetime import datetime
import random
import re

# Randomly choose between up,down,left,right to play the 2048 game


def randomKeyGenerator(body_element):
    rand_num = random.randint(0, 3)
    if rand_num == 0:
        return body_element.send_keys(Keys.UP)
    elif rand_num == 1:
        return body_element.send_keys(Keys.DOWN)
    elif rand_num == 2:
        return body_element.send_keys(Keys.LEFT)
    else:
        return body_element.send_keys(Keys.RIGHT)


driver = webdriver.Chrome()
driver.get("https://play2048.co/")
body_element = driver.find_element_by_tag_name('body')

random.seed(datetime.now())
while len(driver.find_elements_by_class_name("game-over")) == 0:
    randomKeyGenerator(body_element)

# sometimes the current score has two values, only the first is important
current_score = driver.find_elements_by_class_name("score-container")[0]
current_score = current_score.text.split()[0]
best_score = driver.find_elements_by_class_name("best-container")[0].text
print("current score is {}, best score is {}".format(
    current_score, best_score))
