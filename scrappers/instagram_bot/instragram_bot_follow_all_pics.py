from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import re

# find who doesn't follow back
# TODO find a safe way to store the password and email
# learn xpath to make the script search more resilient and redable
USERNAME = ""
PASSWORD = ""


class InstagramBot:
    def __init__(self, driver, username, password):
        self.username = username
        self.password = password
        self.driver = driver

    def find_not_follow_back_people(self):
        self.go_to_personal_profile()
        follower_names, following_names = self.find_followers_and_followies()
        not_follow_back_names = [
            following for following in following_names if following not in follower_names]
        return not_follow_back_names
    def search_and_follow(self, search_name):
        self.driver()
    #private methods
    def go_to_personal_profile(self):
        self.go_to_default_screen()
        self.click_profile_pic()

    def go_to_default_screen(self):
        self.add_credintials()
        self.dismiss_notifications()

    def add_credintials(self):
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[@id="loginForm"]/div/div[3]/button').click()
        time.sleep(4)

    def dismiss_notifications(self):
        # ignore save screen
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(2)

        # ignore notification screen
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)

    def ignore_notification_screen(self):
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        time.sleep(2)

    def click_profile_pic(self):
        # click on name
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()
        time.sleep(3)

    def find_followers_and_followies(self):
        # following
        self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()

        time.sleep(2)
        following_names = self.get_names_from_scrollbox()

        # followers
        self.driver.find_element_by_xpath(
            "//a[@href=\"/vasilis_drettas/followers/\"]").click()
        time.sleep(2)
        follower_names = self.get_names_from_scrollbox()

        return follower_names, following_names

    def get_names_from_scrollbox(self):
        # execute javascript to scroll
        suggestion = self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[2]/div[1]')

        self.driver.execute_script(
            "arguments[0].scrollIntoView();", suggestion)
        time.sleep(2)

        # scroll to the buttom of the list
        scroll_box = self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[2]')

        last_height, height = 0, 1
        while last_height != height:
            last_height = height
            time.sleep(1)
            height = self.driver.execute_script('''arguments[0].scrollTo(0, arguments[0].scrollHeight);
                                return arguments[0].scrollHeight;''', scroll_box)
            print("height is {}".format(height))

        # get all relevant names
        all_name_links = scroll_box.find_elements_by_tag_name('a')
        names = [link.text for link in all_name_links if link.text != '']

        # click x button to close followers/following
        self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
        return names


driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")
time.sleep(3)

instagram_bot = InstagramBot(driver, USERNAME, PASSWORD)
instagram_bot.go_to_default_screen()
print(instagram_bot.find_not_follow_back_people()())

#when you are at a persons page like all their pics
driver.get('https://www.instagram.com/someone/')
time.sleep(3)

#scroll to the buttom of all the pics
last_height, height = 0, 1
while last_height != height:
    last_height = height
    time.sleep(1)
    height = driver.execute_script('''window.scrollBy(0,document.body.scrollHeight)
                    return document.body.scrollHeight;''')
    print("height is {}".format(height))

#get every page
all_links_tags = driver.find_elements_by_tag_name('a')
all_urls = [url.get_attribute('href') for url in all_links_tags]
photo_urls = []
for photo_url in all_urls:
    #photo urls start have a url /p/
    founded = re.findall('/p/\w+/$', photo_url)
    
    if len(founded) > 0:
        photo_urls.append(photo_url)
#go to every page and like
for photo_url in photo_urls :
    driver.get(photo_url)
    time.sleep(2)
    # like an open picture
    try:
        driver.find_element_by_xpath('//*[@aria-label=\"Like\"]').click()
    except Exception:
        #probably already liked, skip
        print('probably already liked')

driver.get('https://www.instagram.com/someone/')



