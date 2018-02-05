#!/usr/bin/env python

"""
request.py: Extracts pages from carwale.com
2/5/2018 : Added Logger
"""

__author__      = "Anand Niranjan"


import requests
from lxml import html
import urllib.parse
import os
import time
import random
import logging
import datetime

save_path = r'E:\python_projects\carwale\html'
log_path = r'E:\python_projects\carwale\logs'
dt = datetime.datetime.now()
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename= os.path.join(log_path, 'request_{}.log'.format(dt.date())),
    level=logging.INFO)

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

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for b_url in brand_url:
        time_sec = random.randint(1,3)
        time.sleep(time_sec)
        resp = requests.get(b_url)
        file_name = os.path.join(save_path, (b_url.split('/')[-2]+'.html'))
        with open (file_name, 'w') as file:
            logging.info("Extracting {} after {} second(s).".format(file_name, time_sec))
            file.write(str(resp.text.encode('UTF-8')))


if __name__ == "__main__":
    carwale = "https://www.carwale.com/new"
    get_car_data(carwale)





