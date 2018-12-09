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

@app.route("/drunkeness")
def drunkenesspage():
   # """Return the homepage."""
    return render_template("drunkeness.html")

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


    

if __name__ == "__main__":
    app.run()


