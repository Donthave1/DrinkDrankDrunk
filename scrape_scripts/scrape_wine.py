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


def init_browser():
    executable_path = {"executable_path": "/Users/stefa/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_wine_alcohol(wine_name):

    browser = init_browser()

    wine_info = "https://www.wine-searcher.com/find/" + wine_name

    browser.visit(wine_info)
 
    #store the html in a variable called html    
    html = browser.html

    # create a soup object from the html.  This will parse the html we pulled from wine searcher website.
    soup = BeautifulSoup(html, "html.parser")

    sidepanel = soup.find_all(class_='dtlbl sidepanel-text')
    
    text_list = []
    
    for x in sidepanel:
                
        clean_text = x.get_text(strip=True)
        text_list.append(clean_text)
       
       
    return text_list    


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
  #  wine_alcohol = list(db.alcohol.find())

    #test out your theory
    wine_alcohol = ['Chocolate Shop Chocolate Red Wine', 'Luc Belaire Rare Rose', 'Chalk Hill Estate Chardonnay']

              
    for wines in wine_alcohol:

        wine_name = wines["Wine Name"]
        
        wine_search = wine_name.replace(" ", "+")
        sidebar_list = scrape_wine_alcohol(wine_search)

        if not sidebar_list:
            print(f"Wine Not Found: {wine_name}")

        else:
            
            text_search = "Alcohol Content"
            
            search_result =  [s for s in sidebar_list if text_search in s]
            alcohol_range = search_result[0]
            
            alcohol_pct = alcohol_range[15:17]
        
            #Update the MongoDB
            dbquery = {"Wine Name": wine_name}
            update_alc = {"$set" : {"alcohol_percent" : alcohol_pct}}

            col.update_one(dbquery, update_alc)






  
