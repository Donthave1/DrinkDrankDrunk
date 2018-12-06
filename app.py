from flask import Flask, render_template

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

@app.route("/drunkeness/<price>")
def drunkenesspage(price):
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

    #return new data for graphing
    wine_name = sorted_wine["brand_name"]
    grape_type = sorted_wine["grape_type"]
    price = sorted_wine["price"]
    review = sorted_wine["review"]

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

    return render_template("drunkeness.html")

@app.route("/food")
def foodpage():
   # """Return the homepage."""
    return render_template("food.html")


if __name__ == "__main__":
    app.run()
