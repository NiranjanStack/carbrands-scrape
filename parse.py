#!/usr/bin/env python

"""parse.py: Returns formatted data in csv"""

__author__      = "Anand Niranjan"

import pandas as pd
import os
from lxml import html
import numpy as np
import datetime

def parse_html(html_file, path):
    """

    :param html_file: html page of car brand
    :param path: location to save csv
    :return: formatted data in csv
    """

    dt = datetime.datetime.now()
    with open(os.path.join(location, html_file), 'r') as file:
        content = file.read()

    tree = html.fromstring(content)

    names = tree.xpath("//ul[@id='divModels']//strong/text()")

    price_xp = tree.xpath("//ul[@id='divModels']//div[@class='font20 margin-top15']/text()")

    price_unit = [p[40:-14] for p in price_xp]

    price_list = [p.split(' ')[0] for p in price_unit]
    unit_list = [p.split(' ')[1] for p in price_unit]

    df = pd.DataFrame(np.column_stack([names, price_list, unit_list]),
                      columns=['name', 'price', 'unit'])
    df['Timestamp'] = dt

    file_name = os.path.join(path, 'car_brands_{}.csv'.format(dt.date()))
    df.to_csv(file_name, mode='a', header=False, index=False)

    return True

if __name__ == "__main__":
    location = r'E:\python_projects\carwale\html'

    save_path = r'E:\python_projects\carwale\parsed_data'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for file in os.listdir(location):
        parse_html(file, save_path)