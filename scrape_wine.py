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

#################################################
#Pymongo Setup
#################################################

client = MongoClient("mongodb://localhost:27017/")


def init_browser():
    executable_path = {"executable_path": "/Users/stefa/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#def scrape():
    
    #Create the dictionary that will store the scraped wine data
   # wine_alc_data = {}

    #alcohol_content = scrape_wine_alcohol()

   # wine_data['alcohol'] = alcohol_content

    #return wine_data


def scrape_wine_alcohol(wine_name):

    #This function scrapes the Wine Searcher website for the alcohol content

    browser = init_browser()

    #for now, use one wine - make into a loop later

    #wine_brand = "kendall+jackson+chardonnay"

    #wine_alc_data = {}
      
    # visit https://www.wine-searcher.com/ and find the specific brand
    wine_info = "https://www.wine-searcher.com/find/" + wine_name
    browser.visit(wine_info)
    
    #store the html in a variable called html    
    html = browser.html

    # create a soup object from the html.  This will parse the html we pulled from wine searcher website.
    soup = BeautifulSoup(html, "html.parser")
   
    #Get the latest article posted on the site.  The list_text class has the headline,
    # date, and a blurb about the article - "a teaser"
    
    sidepanel = soup.find_all(class_='dtlbl sidepanel-text')

    text_list = []
    
    for x in sidepanel:
                
        clean_text = x.get_text(strip=True)
        text_list.append(clean_text)
       
       
    return text_list    

### MAIN     

with client:

    db = client.winedata

   # wine_alcohol = list(db.alcohol.find())
   #temporary list just to test 
    wine_alcohol = ["Brancaia Tre", "Elderton Shiraz"]
   
    wine_alc_data = {}
     
    for name in wine_alcohol:
        
        wine_search = name.replace(" ", "+")
        sidebar_list = scrape_wine_alcohol(wine_search)
        
        text_search = "Alcohol Content"
        search_result =  [s for s in sidebar_list if text_search in s]
        alcohol_range = search_result[0]
        
        alcohol_pct = alcohol_range[15:17]
        #print(alcohol_pct)
      

        wine_alc_data["Wine Name"] = name
        wine_alc_data["alcohol_percent"] =  alcohol_pct

    print(wine_alc_data)






  
