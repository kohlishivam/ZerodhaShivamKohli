#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import requests
import zipfile
import io
import pandas as pd
import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
import redis


URL = 'https://www.bseindia.com/markets/equity/EQReports/Equitydebcopy.aspx'


def file_downloder():
    '''
    Fetches the URL where the zip file is located
    And downloads the zip and stores the file downloaded
    '''
    url = urlopen(URL)
    html = url.read()
    soup = BS(html, "html.parser")
    equity_file = soup.find(id='btnhylZip')
    link = equity_file.get('href', None)
    r = requests.get(link)
    zipfile_csv = zipfile.ZipFile(io.BytesIO(r.content))
    zipfile_csv.extractall()
    return zipfile_csv.namelist()[0]


def save_data(csv_file):
    '''
    Stores the result of the CSV in Redis
    '''
    csv_data = pd.read_csv(csv_file)
    # The required fileds are stored
    csv_data = csv_data[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].copy()
    for index, row in csv_data.iterrows():
        r.hmset(row['SC_CODE'], row.to_dict())
        r.set("equity:"+row['SC_NAME'], row['SC_CODE'])


class Page:
    @cherrypy.expose
    def index(self, search=""):
        '''
        Fetches the top 10 result from the redis and
        renders it to the frontend
        '''
        html_file = env.get_template('index.html')
        self.result = []
        for key in r.scan_iter("equity:*"):
            code = r.get(key)
            self.result.append(r.hgetall(code).copy())
        self.result = self.result[0:10]
        return html_file.render(result=self.result)


if __name__ == '__main__':
    csv_file = file_downloder()
    r = redis.StrictRedis(host="localhost",
        port=6379,
        charset="utf-8",
        decode_responses=True,
        db=1)
    save_data(csv_file)
    env = Environment(loader=FileSystemLoader('media'))
    config = {'global': {'server.socket_host':  '0.0.0.0',
                'server.socket_port':  int(os.environ.get('PORT', '5000'))}}
    cherrypy.quickstart(Page(), config=config)
