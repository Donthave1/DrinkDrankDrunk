from flask import Flask, render_template, jsonify, request, redirect, send_from_directory
import pandas as pd
import pymongo
import numpy as np
import re
import os

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
    top_50 = filtered_data[:50]


    #return new data for graphing
    wine_name = list(top_50["brand_name"])
    grape_type = list(top_50["grape_type"])
    price = list(top_50["price"])
    review = list(top_50["review"])
    wine_type = list(top_50["wine_type"])

    data = []
    i=0

    while i < len(wine_name):
        wine_info = {
                    "wine_name": wine_name[i],
                    "grape_type": grape_type[i],
                    "price": int(price[i]),
                    "review": int(review[i]),
                    "wine_type": wine_type[i]
                    }
        data.append(wine_info)
        i +=1
    return jsonify(data)

@app.route("/taste")
def tastepage():
    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)

    #extract database to DB
    db = client.heroku_3t530jfl

    df_taste = pd.DataFrame(list(db.taste.find({})))
    df_taste = df_taste.drop(columns='_id')

    #pull out the tasting notes for the dropdown
    notes_df = pd.DataFrame(df_taste.tasting_notes.values.tolist())
    #get rid of the duplicates in the dataframe
    check_df = notes_df.drop_duplicates(keep='first',inplace=False)
    check_df = check_df.reset_index()

    s1 = pd.Series(data=check_df[0].dropna())
    s2 = pd.Series(data=check_df[1].dropna())
    s3 = pd.Series(data=check_df[2].dropna())
    s4 = pd.Series(data=check_df[3].dropna())
    s5 = pd.Series(data=check_df[4].dropna())
    s6 = pd.Series(data=check_df[5].dropna())
    s7 = pd.Series(data=check_df[6].dropna())
    s8 = pd.Series(data=check_df[7].dropna())

    tastes_df = pd.DataFrame(np.hstack((s1.values, s2.values, s3.values, s4.values, s5.values, s6.values, s7.values, s8.values)))
    tastes_df = tastes_df.rename(columns={0:'tastes'})
    tastes_df = tastes_df.sort_values(by='tastes')
    tastes_df = tastes_df.drop_duplicates(keep='first', inplace=False)
    tastes_df = tastes_df.reset_index().drop(columns='index')

    # """Return the homepage."""
    return render_template("taste.html", taste_list=tastes_df['tastes'])


@app.route("/taste/<selected_taste>")
def taste_func(selected_taste):

    conn = 'mongodb://test:password1@ds123444.mlab.com:23444/heroku_3t530jfl'
    client = pymongo.MongoClient(conn)
    
    #extract to DB
    db = client.heroku_3t530jfl
    df = pd.DataFrame(list(db.styles.find({})))

    new_df = df[['alcohol', 'brand_name', 'grape_type', 'review', 'wine_style', 'wine_type']]
      
    #strip the wine type from the front of the wine style
    new_df['wine_style'] = new_df['wine_style'].apply(lambda x: x.split(" - ")[-1] if(x) else x)
        
    #bring in the intensity collection from Mongo and put in dataframe
    df_int = pd.DataFrame(list(db.intensity.find({})))
    df_int = df_int.drop(columns='_id')
    
    #the wine_style column header is coming in with garbage characters
    #use this code to rename it
    df_int.columns = ['intensity_score', 'wine_style']
    
    #strip the wine type from the front of the wine style
    df_int['wine_style'] = df_int['wine_style'].apply(lambda x: x.split(" - ")[-1] if(x) else x)
    
    #merge the wine intensities with the styles data
    df_with_int = new_df.merge(df_int, on='wine_style')
    
    #bring in the tasting notes collection from Mongo and put in dataframe
    df_taste = pd.DataFrame(list(db.taste.find({})))
    df_taste = df_taste.drop(columns='_id')
    
    #merge again to include the tasting notes in the big dataframe
    df_merge = df_with_int.merge(df_taste, on='wine_style')
    
    #rename the wine_type column
    df_merge = df_merge.rename(columns={"wine_type_x":"wine_type"})
    df_merge = df_merge.drop(columns='wine_type_y')
    
    #turn the tasting notes column from a list into a string so we can search it
    df_merge['notes'] = df_merge['tasting_notes'].apply(', '.join)
    df_merge = df_merge.drop(columns='tasting_notes')
    
    #now search the dataframe for the selected tasting note
    search_df = df_merge[df_merge['notes'].str.contains(selected_taste)]
    search_df = search_df.sort_values(by=['brand_name'])

    search_df = search_df.reset_index()

    #convert dataframe columns to lists, put into a dictionary and then jsonify
    alcohol_pct = list(search_df['alcohol'])
    brand = list(search_df['brand_name'])
    grape = list(search_df['grape_type'])
    review = list(search_df['review'])
    style = list(search_df['wine_style'])
    wine_type = list(search_df['wine_type'])
    intensity_score = list(search_df['intensity_score'])
   
    table_data = []
    i=0
    while i < len(brand):

        dict = {
        "Brand":brand[i], 
        "Grape":grape[i],
        "Wine Type":wine_type[i],
        "Alcohol %":alcohol_pct[i],
        "Score":review[i],
        "Style":style[i],
        "Intensity":intensity_score[i]    
        }
        table_data.append(dict)
        i+=1

    return jsonify(table_data)


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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/png')
  

if __name__ == "__main__":
    app.run()


