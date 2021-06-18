# app.py file for Mission to Mars web-scraping-challenge
# Jonathan Surgeon

# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# create Flask object
app = Flask(__name__)

# create flask_pymong -> mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    db_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = db_info)


@app.route('/scrape')
def scraper():
    # import scrape from scrape_mars.py
    from scrape_mars import scrape

    # store scrape() return value (is a dictionary)
    info = scrape()

    mars_collection = mongo.db.mars_info
    mars_collection.drop()
    mars_collection.update({},info,upsert=True)

    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)

