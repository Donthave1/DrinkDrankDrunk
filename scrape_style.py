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
    db = client.stef_wine_type
    col = db.wine_type

    #Create a list of the alcohol collection that is in Mongo
    wine_list= list(db.wine_type.find())

    #test out your theory
    #wine_list = ['Yalumba Antique Reserve Tawny Port ']

              
    for wines in wine_list:

        wine_name = wines["brand_name"]
        
        wine_search = wine_name.replace(" ", "+")
        sidebar_list = scrape_wine_alcohol(wine_search)

        if not sidebar_list:
            print(f"Wine Not Found: {wines}")

        else:
            
            text_search = "Wine Style"
            
            search_result =  [s for s in sidebar_list if text_search in s]

            if search_result:
                wine_style_full = search_result[0]
                wine_style = wine_style_full[10:]
                print(wine_style)

                #Update the MongoDB
                dbquery = {"brand_name": wines}
                update_style = {"$set" : {"wine_style" : wine_style}}

                col.update_one(dbquery, update_style)

            else:
                print(f"Wine Style Not Found: {wines}")   
        
            

    




  
