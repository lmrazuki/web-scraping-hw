# import modules
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)