from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time
import re

#TODO think what functionality should belong here and what at the individial script level. Maybe separate them based on the page.
# profile page, friend page etc
class InstagramBot:
    def __init__(self, driver, username, password):
        self.username = username
        self.password = password
        self.driver = driver
        driver.get("https://www.instagram.com/")
        time.sleep(3)

    def find_not_follow_back_people(self):
        self.go_to_personal_profile()
        follower_names, following_names = self.find_followers_and_followies()
        not_follow_back_names = [
            following for following in following_names if following not in follower_names]
        return not_follow_back_names

    #private methods
    def go_to_personal_profile(self):
        self.login_to_profile()
        self.click_profile_pic()

    def login_to_profile(self):
        self.add_credintials()
        self.dismiss_notifications()

    def add_credintials(self):
        self.driver.find_element_by_xpath(
            '//input[@name=\"username\"]').send_keys(self.username)
        self.driver.find_element_by_xpath(
            '//input[@name=\"password\"]').send_keys(self.password)
        self.driver.find_element_by_xpath(
            '//*[contains(text(),"Log In")]').click()
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
