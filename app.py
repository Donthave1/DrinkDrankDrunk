from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
import pymongo
import re

app = Flask(__name__)


@app.route("/")
def index():
   # """Return the homepage."""
   
    return render_template("index.html")


# Add any other routes here
@app.route("/budget")
def budgetpage():
   # """Return the homepage."""
    return render_template("budget.html")
   
@app.route("/price/<selected_budget>")
def winebudget(selected_budget):
    #create mongodb connection
    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)

    #extract to DB
    db = client.heroku_3t530jfl
    wine_collections = db.wine_db.find({}, {'_id': 0})
    df = pd.DataFrame(list(wine_collections))

    #sorted by review
    sorted_wine = df.sort_values(by="review", ascending=False)
    sorted_wine.reset_index(inplace=True, drop=True)
    sorted_wine.head()

    #take only top 100 wines
    filtered_data = sorted_wine.loc[sorted_wine["price"]<=int(selected_budget)]
    top_100 = filtered_data[:100]


    #return new data for graphing
    wine_name = list(top_100["brand_name"])
    grape_type = list(top_100["grape_type"])
    price = list(top_100["price"])
    review = list(top_100["review"])

    data = []
    i=0

    while i < len(wine_name):
        wine_info = {
                    "wine_name": wine_name[i],
                    "grape_type": grape_type[i],
                    "price": int(price[i]),
                    "review": int(review[i])
                    }
        data.append(wine_info)
        i +=1
    return jsonify(data)

@app.route("/drunkenness")
def drunkpage():
   # """Return the homepage."""
    return render_template("drunkenness.html")

@app.route("/food")
def foodpage():
    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)

    db = client.heroku_3t530jfl
    food_items = db.wine_db.find({}, {'_id': False, 'food_pairing': True})
    food_list = pd.DataFrame(list(food_items))


    # """Return the homepage."""
    return render_template("food.html", food_list=food_list['food_pairing'].unique())

@app.route("/yummy/<selected_food>")
def foodchart(selected_food):

    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)

    db = client.heroku_3t530jfl
    food_choice = db.wine_db.find({'food_pairing': re.compile('^' + re.escape(selected_food) + '$', re.IGNORECASE)}, {'_id': False})
    food_list = list(food_choice)

    df = pd.DataFrame(food_list)

    grape_type=df.groupby("grape_type").nunique()
    new_df=pd.DataFrame(grape_type)
    
    completed_df = new_df[["brand_name"]]
    new_df=completed_df.reset_index()

    grape_names = list(new_df["grape_type"])
    wine_count = list(new_df["brand_name"])

    data = []
    i=0
    while i < len(grape_names):
        dict = {
            "grape_type":grape_names[i],
            "wine_count":wine_count[i]
        }
        data.append(dict)
        i+=1

   
    return jsonify(data)

    

@app.route("/about")
def aboutpage():
   # """Return the homepage."""
    return render_template("about.html")
  

if __name__ == "__main__":
    app.run()


