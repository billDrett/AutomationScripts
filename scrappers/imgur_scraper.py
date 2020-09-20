import requests
from bs4 import BeautifulSoup
import re
import sys
import os

# Script to retrieve all pictures based on a search term from imgur


def find_list_of_pics(search_term):
    imgur_url = "https://imgur.com/search?q={}".format(search_term)
    response = requests.get(imgur_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    div_of_images = soup.find("div", {"class": "cards"})
    all_pics = div_of_images.findAll("img")
    return ["https:{}".format(pic["src"]) for pic in all_pics]


def find_file_name(img_url):
    return re.findall('\w+\.\w+$', img_url)


# TODO make it work with async io. Maybe to do a comparision with requests on the speed
# TODO use a package install to add all dependencies instead of manually using pip install
if __name__ == '__main__':
    if(len(sys.argv) != 3):
        sys.exit('''To run please provide the search term and output path
                ./imgur_scraper.py <search_term> <output_path>''')

    # extract command line arguments
    search_term = sys.argv[1]
    output_path = sys.argv[2]
    if not os.path.isdir(output_path):
        sys.exit("output path is not a directory")

    img_urls = find_list_of_pics(search_term)
    imgs_response = [(requests.get(img), find_file_name(img))
                     for img in img_urls]
    for res, name in imgs_response:
        if res.status_code != requests.codes.ok:
            print("Warning request failed for ulr {}".format(res.url))
            continue

        file_name = "{}/{}".format(output_path, name[0])
        with open(file_name, 'wb') as out_file:
            out_file.write(res.content)
