import requests
from bs4 import BeautifulSoup
import re

SEARCH_TERM = "Jennifer lawrence"
IMGUR_URL = "https://imgur.com/search?q={}".format(SEARCH_TERM)


def find_list_of_pics(search_term):
    response = requests.get(IMGUR_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    div_of_images = soup.find("div", {"class": "cards"})
    all_pics = div_of_images.findAll("img")
    return ["https:{}".format(pic["src"]) for pic in all_pics]


def find_file_name(img_url):
    return re.findall('\w+\.\w+$', img_url)


# TODO make it work with async io. Maybe to do a comparision with requests on the speed
# TODO add command line argument for the output path and search term
# TODO use a package install to add all dependencies instead of manually using pip install
if __name__ == '__main__':
    img_urls = find_list_of_pics(SEARCH_TERM)

    imgs_reposnse = [(requests.get(img), find_file_name(img))
                     for img in img_urls]
    for res, name in imgs_reposnse:
        res.raise_for_status()
        output = open(name[0], "wb")
        output.write(res.content)
        output.close()
