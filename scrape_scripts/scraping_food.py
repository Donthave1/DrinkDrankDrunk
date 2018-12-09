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
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_wine_food(wine_name):

    browser = init_browser()

    wine_info = "https://www.wine-searcher.com/find/" + wine_name

    browser.visit(wine_info)
 
    #store the html in a variable called html    
    html = browser.html

    # create a soup object from the html.  This will parse the html we pulled from wine searcher website.
    soup = BeautifulSoup(html, "html.parser")

    sidepanel = soup.find_all(class_='sidepanel-text')
    
    text_list = []
    
    for x in sidepanel:
                
        clean_text = x.get_text(strip=True)
        text_list.append(clean_text)
       
       
    return text_list    

client = MongoClient("mongodb://localhost:27017/")

with client:
    #connect to the Mongo DB
    db = client.winedata
    col = db.food

    #Create a list of the alcohol collection that is in Mongo
    wines = list(db.food.find())
    # test wines = ["Chateau Mouton Rothschild", "Chateau lafite"]

              
    for wine in wines:

        wine_name = wines["Wine Name"]
        
        wine_search = wine.replace(" ", "+")
        sidebar_list = scrape_wine_food(wine_search)

        if not sidebar_list:
            print(f"Wine Not Found: {wine_name}")

        else:
            
            text_search = "Food Suggestion"
            
            search_result =  [s for s in sidebar_list if text_search in s]

            food_pairing = search_result [0]


            
        
            #Update the MongoDB
            dbquery = {"Wine Name": wine_name}
            update_food = {"$set" : {"Food Suggestion" : food_pairing}}

            col.update_one(dbquery, update_food)