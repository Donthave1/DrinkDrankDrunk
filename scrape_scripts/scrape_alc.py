# Scrape the Wine Searcher website for alcohol content

#Import dependencies

from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
import tweepy
import json
import pprint
import pandas as pd
import time 


def init_browser():
    executable_path = {"executable_path": "/Users/stefa/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_wine_alcohol(soup):
 
    span = soup.find("span", class_="prodAlcoholPercent_percent")
    pct = [span.text][0]

    print(pct)           
    return pct


### MAIN     

#################################################
#Pymongo Setup
#################################################

client = MongoClient("mongodb://localhost:27017/")

with client:
    #connect to the Mongo DB
    db = client.winedata
    col = db.alcohol

    #Create a list of the alcohol collection that is in Mongo
    wine_alcohol = list(db.alcohol.find())

    #Use splinter to get the html on the wine page
    browser = init_browser()

    url = "https://www.wine.com/search/"
    
    test_list = ["Falernia Syrah Reserva", "Dierberg Chardonnay"]
              
    for wine in test_list:

        wine_search = wine.replace(" ", "%20")

        search_url = url + wine_search + "/0"
       
        browser.visit(search_url)
       
        html = browser.html

        # create a soup object from the html.  This will parse the html we pulled from wine searcher website.
        soup = BeautifulSoup(html, "html.parser")

        #find the first wine in the list and then visit that link
        wine_link = soup.find("a", class_="prodItemInfo_link").get("href")

        full_wine_link = "https://www.wine.com" + wine_link

        print(full_wine_link)

        browser.visit(full_wine_link)
    
        html = browser.html

        soup = BeautifulSoup(html, "html.parser")

        alc_percent = scrape_wine_alcohol(soup)

        if not alc_percent:
            print(f"Wine Not Found: {wine}")

        else:
            
            print(alc_percent)
        
            #Update the MongoDB
            dbquery = {"Wine Name": wine}
            update_alc = {"$set" : {"alcohol_percent" : alc_percent}}

            col.update_one(dbquery, update_alc)

    




  
