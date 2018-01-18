#!/usr/bin/env python

"""request.py: Extracts pages from carwale.com"""

__author__      = "Anand Niranjan"


import requests
from lxml import html
import urllib.parse
import os
import time
import random


def get_car_data(url):
    """

    :param url: url of website
    :return: html files for all car brands
    """

    response = requests.get(url)
    tree = html.fromstring(response.content)
    brands = tree.xpath("//div[@class='brand-type-container']//a/@href")

    brand_url = []
    for brand in brands:
        new_url = urllib.parse.urljoin(url, brand)
        brand_url.append(new_url)

    save_path = r'E:\python_projects\carwale\html'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for b_url in brand_url:

        time.sleep(random.randint(1,3))
        resp = requests.get(b_url)
        file_name = os.path.join(save_path, (b_url.split('/')[-2]+'.html'))
        with open (file_name, 'w') as file:
            file.write(str(resp.text.encode('UTF-8')))


if __name__ == "__main__":
    carwale = "https://www.carwale.com/new"
    get_car_data(carwale)





