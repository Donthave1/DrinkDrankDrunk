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

@app.route("/drunkeness")
def drunkenesspage():
   # """Return the homepage."""
    return render_template("drunkeness.html")

@app.route("/food")
def foodpage():
   # """Return the homepage."""
    return render_template("food.html")


if __name__ == "__main__":
    app.run()
