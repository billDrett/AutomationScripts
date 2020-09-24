from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import re
from instagram_bot import InstagramBot
# Given a person url like all his/hers pictures
# TODO find a safe way to store the password and email

USERNAME = ""
PASSWORD = ""
PERSON_URL = "https://www.instagram.com/someone/"

def scroll_to_buttom_of_screen_and_get_pics_url(driver):
    photo_urls = set()
    last_height, height = 0, 1
    while last_height != height:
        last_height = height
        height = driver.execute_script('''window.scrollBy(0,document.body.scrollHeight)
                        return document.body.scrollHeight;''')
        time.sleep(1)
        print("height is {}".format(height))
        #must retrieve all photos while scrolling because the photos can disappear while scrolling down
        photo_urls.update(get_all_pics_of_profile(driver))
    return photo_urls

def get_all_pics_of_profile(driver):
    all_links_tags = driver.find_elements_by_tag_name('a')
    all_urls = [url.get_attribute('href') for url in all_links_tags]
    photo_urls = []
    for photo_url in all_urls:
        #photo urls start have a url /p/
        founded = re.findall('/p/\w+', photo_url)
        
        if len(founded) > 0:
            photo_urls.append(photo_url)
    return photo_urls

def like_all_photos(driver, photos_url):
    for photo_url in photo_urls :
        driver.get(photo_url)
        time.sleep(2)
        # like an open picture
        try:
            driver.find_element_by_xpath('//*[@aria-label=\"Like\"]').click()
        except Exception:
            #probably already liked, skip
            print('probably already liked')


driver = webdriver.Chrome()

instagram_bot = InstagramBot(driver, USERNAME, PASSWORD)
instagram_bot.login_to_profile()

#when you are at a persons page like all their pics
driver.get(PERSON_URL)
time.sleep(2)

photo_urls = scroll_to_buttom_of_screen_and_get_pics_url(driver)
like_all_photos(driver, photo_urls)



