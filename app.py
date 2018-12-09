from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd
import pymongo

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
    wine_collections = db.wine_db.find()
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
                    "price": price[i],
                    "review": review[i]
                    }
        data.append(wine_info)
        i +=1
    return jsonify(data)

@app.route("/drunkeness")
def drunkenesspage():
   
    return render_template("drunkeness.html")

@app.route("/alcohol/<selected_percent>")
def drinkbudget(selected_percent):
    #create mongodb connection
    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)

    #extract to DB
    db = client.heroku_3t530jfl
    wine_collections = db.wine_db.find()
    df = pd.DataFrame(list(wine_collections))


    filtered_data = df.loc[df["lower_alcohol"]<=int(selected_percent)]
    top_10 = filtered_data[:10]

    wine_name = list(top_10["brand_name"])
    grape_type = list(top_10["grape_type"])
    alcohol = list(top_10["lower_alcohol"])

    data = []
    i=0

    while i < len(wine_name):
        wine_info = {
                    "wine_name": wine_name[i],
                    "grape_type": grape_type[i],
                    "alcohol": alcohol[i]
                    }
        data.append(wine_info)
        i +=1
    return jsonify(data)

@app.route("/food")
def foodpage():
   # """Return the homepage."""
    return render_template("food.html")


if __name__ == "__main__":
    app.run()
