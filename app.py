from flask import Flask, render_template
import pandas as pd
import pymongo

app = Flask(__name__)


@app.route("/")
def index():
   # """Return the homepage."""
   
    return render_template("index.html")


# Add any other routes here
@app.route("/budget/<price>")
def budgetpage(price):
   # """Return the homepage."""
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
    filtered_data = sorted_wine.loc[sorted_wine["price"]<=price]
    top_100 = filtered_data[:100]

    top_100.to_csv("asset/data/data.csv")

    #return new data for graphing
    wine_name = top_100["brand_name"]
    grape_type = top_100["grape_type"]
    price = top_100["price"]
    review = top_100["review"]

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
    
   # """Return the homepage."""

    return render_template("budget.html", wine=data)

@app.route("/drunkeness/")
def drunkenesspage():
   
    return render_template("drunkeness.html")

@app.route("/food")
def foodpage():
   # """Return the homepage."""
    return render_template("food.html")


if __name__ == "__main__":
    app.run()
