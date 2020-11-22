# import modules
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars = {}

    # Scraping the most recent article data
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='image_and_description_container')

    for result in results:
        title_block = soup.find_all('div', class_= 'content_title')
        paragraph_block = soup.find('div', class_='article_teaser_body')
        
    mars["title"] = title_block[1].text
    mars["paragraph"] = paragraph_block.text

        # Scraping the feauture image
    feature_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(feature_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    image_results = soup.find('div',class_="carousel_container")
    url_string = image_results.article["style"].\
    strip("background-image: url").\
    strip("(").strip(");").strip("''")
    url_string

    mars["feature_image"] = f"https://www.jpl.nasa.gov{url_string}"

    # Scraping the facts table
    facts_url = "https://space-facts.com/mars/"

    # Use Pandas to scrape the table containing facts about Mars
    tables = pd.read_html(facts_url)
    # Convert the data to an HTML Table string
        
    mars_table = tables[0]
    mars_table = mars_table.rename({0: "", 1: "Data"}, axis =1).set_index("")

    #export as a html file
    mars_table.to_html("templates/mars_facts.html")

    # Scraping the hemisphere images

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Obtain high resolution images of each of Mars hemispheres
    results = soup.find_all('div',class_="item")
    url_list = []
    title = []
    for result in results:
        url_list.append(result.a['href'])
        title.append(result.h3.text)
        
    click_list = ["https://astrogeology.usgs.gov" + url for url in url_list]

    img_urls = []
    for site in click_list:
        browser.visit(site)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url = soup.find("div", class_ = "downloads").li.a["href"]
        img_urls.append(img_url)
    img_urls

    mars["hemispheres"] = []
    for url, name in zip(img_urls, title):
        mars["hemispheres"].append({"title":name,"img_url":url})

    return mars

