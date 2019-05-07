from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)


@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    # Run the scrape function
    mars_dict = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.mars_dict.update({}, mars_dict, upsert=True)
    
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
