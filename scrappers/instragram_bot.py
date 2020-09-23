from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import time

# find who doesn't follow back
# TODO find a safe way to store the password and email
# learn xpath to make the script search more resilient and redable
USERNAME = ""
PASSWORD = ""


def get_names(driver):
    # execute javascript to scroll
    suggestion = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div[2]/div[1]')

    driver.execute_script("arguments[0].scrollIntoView();", suggestion)
    time.sleep(2)

    # scroll to the buttom of the list
    scroll_box = driver.find_element_by_xpath(
        '/html/body/div[4]/div/div/div[2]')

    last_height, height = 0, 1
    while last_height != height:
        last_height = height
        time.sleep(1)
        height = driver.execute_script('''arguments[0].scrollTo(0, arguments[0].scrollHeight);
                             return arguments[0].scrollHeight;''', scroll_box)
        print("height is {}".format(height))

    # get all relevant names
    all_name_links = scroll_box.find_elements_by_tag_name('a')
    names = [link.text for link in all_name_links if link.text != '']

    # click x button to close followers/following
    driver.find_element_by_xpath(
        "/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
    return names


driver = webdriver.Chrome()
driver.get("https://www.instagram.com/")
time.sleep(3)
driver.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(USERNAME)
driver.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(PASSWORD)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
time.sleep(4)

# ignore save screen
driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div/div/div/button').click()
time.sleep(2)

# ignore notification
driver.find_element_by_xpath(
    '/html/body/div[4]/div/div/div/div[3]/button[2]').click()
time.sleep(2)

# click on name
driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a').click()
time.sleep(3)

# following
driver.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()

time.sleep(2)
following_names = get_names(driver)

# use this names for something usefull, for example to compare with the followers
# click on followers and get the list
driver.find_element_by_xpath(
    "//a[@href=\"/vasilis_drettas/followers/\"]").click()
time.sleep(2)
follower_names = get_names(driver)

not_follow_back_names = [
    following for following in following_names if following not in follower_names]

print(not_follow_back_names)
