#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars

import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #using bs to write it into html
    html_news = browser.html
    soup_news = bs(html_news,"html.parser")

    # # Printing news title and paragraph
    news_title = soup_news.find("div", class_="content_title").text
    news_paragraph = soup_news.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Teaser Paragraph: {news_paragraph}")


    # # Getting featured image from the home page
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html_image = browser.html
    soup_image = bs(html_image, "html.parser")

    image = soup_image.find("article", class_="carousel_item")["style"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)


    # # Mars weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html_twitter = browser.html
    soup_twitter = bs(html_twitter, "html.parser")

    mars_weather = soup_twitter.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    print(mars_weather)


    # # Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    html_facts = browser.html

    read_facts = pd.read_html(facts_url)
    facts_df = pd.DataFrame(read_facts[0])
    mars_facts = facts_df.to_html(header = False, index = False)
    print(mars_facts)

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html_hemi = browser.html
    soup_hemi = bs(html_hemi, "html.parser")

    mars_hemisphere = []

    products = soup_hemi.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html_image = browser.html
        soup_image = bs(html_image, "html.parser")
        downloads = soup_image.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    return mars_hemisphere