# Project 2: Wine Recommendation Application

![alt text](https://media1.tenor.com/images/46a4614de9b8c2a340bf076e9675b414/tenor.gif?itemid=5405668)

# [Got Wine?](https://whatwine.herokuapp.com/)

By **Team DrinkDrankDrunk**


Edward Chen, Peter Liu, Stefanie Huckleberry, Yolanda Shi  
  


## Wine Suggestion App. Proposal

### Goal 
Want to go on a hot, romantic date, but you only got 30 more minutes to buy a drink? Want to show your significant other how classy you are, but you have no clue about wine? Worry no more! Come to our site and find the perfect choice of wine that will fit to your food, your budget, and your need! Our application is dedicated to help you find the perfect wine that fulfills your requirements and also provides you with information about the choice we suggested! If you are not satisfy with our choice, then go find your own :)!!! Please do not forget to read our No Refund Guarantee Police.
 
## Tools
**Python:** (Library: Pandas, Flask, SQLAlchemy)  
**JavaScript:** (Library: Plotly, Gulp, nmp)   
**Database:** MangoDB  
**HTML/CSS** 

### A prototype of our dataset object :
	
```{  
<--Expected to be on our first data sets-->  
wineName:  
	wineType:  
	year:  
	vineyard:  
	price:  
	professionalReview:  
<--Following Data may need a more scraping-->  
	consumerReview:  
	recommendFoodPairing:  
<--Things that we may consider to add→  
	taste: (acidity/dry/sweet etc.)  
	brandSummary:  
}  
```

## Contents

**Home Page (Ed)**  
	- Form for the user to submit some criteria  
	- Make a selection based on Budget or Drunkenness Level or Food Paring?  

**Budget Selection (Pete)**  
- Price vs. Professional or Consumer Review scatter plot page.  
- Based on the main types of wine (Merlot, Cabernet Sauv, Pinot, Chardonnay, Sauvignon Blanc)  
- Each dot is a brand  
- When user click on the brand dot, leads to the brand profile page(see below)  

**Drunkenness Level (Stef)**  
- Rank the wine type based on the average alcohol content (eg. Dangerous/wasted/tipsy/relax/ Grape Juice)  
- Based on the user’s selection, display a bar chart that shows the alcohol content per brand under that type.  
- Clicking on the brand name will lead to the profile page.  

**Food Pairing (Yo)**  
- Some options such as meat/ veggie/ soup/ salad/ pasta etc.  
- Select the food option and display a pie chart that will show percentage of each type of wine that pairs well with the food type. Selecting the type of wine will display all brands of that wine type that pairs well with the food.  

**Brand Profile (Ed)**  
- A conclusion page that tells you the taste of the wine, and probably a summary of the wine, where it is from etc.   
- Should also display the alcohol content, pricing, and food pairing so the user can get all information about the brand.  



## Data Source:
[Credible Reviews based on Wine Enthusiasts](http://insightmine.com/bring-your-own-data-analyzing-wine-market)



## Project Requirment Checklist     
- [x] Use Python, Flask  
- [x] JavaScript, one library not taught in course  
- [x] HTML/CSS  
- [x] One database (MySQL / MongoDB/ SQLite)  
- Choice of level:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [x] level 1 - A custom "creative" D3.js project (i.e. non-standard graph or chart)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [x] level 2 - A combination of Web Scraping and Leaflet or Plotly  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [x] level 3 - A dashboard page with multiple charts all updating from the same data  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- [x] level 4 - A "thick" server that performs multiple manipulations on data in a database prior to visualization  
- [x] Data need to have at least 100 record  
- [x] Web page has to be user-driven interaction  
- [x] Need to have at least “3” views (comparison charts)  
- [x] Stick to MVP, then decorate after everything work.
- [x] Tell a Story with Data


## Project Timeline
**12/1/2018 - Weekend**  
	-Collecting Data and Have database ready to use  
	-Steph and Yo Scrape food Pairing and Alcohol Content  
	-Pete and Ed Clean Data  
	
**12/4/2018 - Tuesday**  
	-Getting MongoDB ready to use  
	-Start building individual page  
	
**12/6/2018 - Thursday**  
	-Individual page visualization ready
	
**12/8/2018 - Saturday weekend**  
	-Build our Template/styling  
	-Combine all sheets together  
	-Heroku  
	
**12/11/2018**  
	-Get Drunk and Presentation 
	
