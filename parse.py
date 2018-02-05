#!/usr/bin/env python

"""parse.py: Returns formatted data in csv"""

__author__      = "Anand Niranjan"

import pandas as pd
import os
from lxml import html
import numpy as np
import datetime
from pymongo import MongoClient
import json
import logging

dt = datetime.datetime.now()
log_path = r'E:\python_projects\carwale\logs'
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename= os.path.join(log_path, 'parse_{}.log'.format(dt.date())),
    level=logging.INFO)

client = MongoClient()
db = client.db1
collection = db.Carwale

def parse_html(html_location, path):
    """

    :param html_location: html page of car brand
    :param path: location to save csv
    :return: formatted data in csv
    """

    for hfile in os.listdir(html_location):

        with open(os.path.join(location, hfile), 'r') as f:
            content = f.read()

        tree = html.fromstring(content)

        names = tree.xpath("//ul[@id='divModels']//strong/text()")

        price_xp = tree.xpath("//ul[@id='divModels']//div[@class='font20 margin-top15']/text()")

        price_unit = [p[40:-14] for p in price_xp]

        price_list = [float(p.split(' ')[0]) for p in price_unit]
        unit_list = [p.split(' ')[1] for p in price_unit]

        brand = tree.xpath("//h1[@class='font30 text-black']/text()")[0].replace(' Cars','')

        df = pd.DataFrame(np.column_stack([names, price_list, unit_list]),
                          columns=['name', 'price', 'unit'])
        df['price'] = df['price'].apply(pd.to_numeric, errors='ignore')
        df['brand'] = brand
        df['Timestamp'] = dt


        file_name = os.path.join(path, 'car_brands_{}.csv'.format(dt.date()))
        logging.info('Writing {} data to {}'.format(brand, file_name))
        df.to_csv(file_name, mode='a', header=False, index=False)

        to_mongo(df)

    return True

def to_mongo(dataframe):
    """

    :param dataframe:
    :return:
    """
    # docs = json.loads(dataframe.T.to_json(date_format='iso')).values()
    # db.Carwale.insert(docs)
    logging.info("Inserting to Mongo Collection: Carwale")
    db.Carwale.insert_many(dataframe.to_dict('records'))

    return True


if __name__ == "__main__":

    location = r'E:\python_projects\carwale\html'

    save_path = r'E:\python_projects\carwale\parsed_data'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    parse_html(location, save_path)