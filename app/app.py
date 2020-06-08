#
# Libraries
#
import os
from builtins import len, str

import pymongo
from bson import json_util
from flask import Flask, request, render_template, flash, send_file
from flask_cors import CORS
from flask_paginate import Pagination, get_page_args

# create app instance
from flask_restful.representations import json
from pymongo import MongoClient


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

#
# Routes
#


@app.route('/')
def home():
    if 'search' in request.args:
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)

        # create db client
        db = client.stylesearch
        db.TestStyle.create_index([('$**', 'text')])
       # db.test.create_index(
        #    {
         #       "Garment Layer" : "text",
          #      "Colour" : "text"
#
 #           }
  #      )

        search_results = db.TestStyle.find({'$text': {'$search': request.args.get('search')}})


        for entry in search_results:
            flash(entry, 'success')

        # close connection
        client.close()

    #return render_template('search.html')
    return render_template('testingJune.html')

@app.route('/search_results')
def search_results():
    if 'search' in request.args:
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)

        # create db client
        db = client.stylesearch
        db.TestStyle.create_index([('$**', 'text')])
      #  db.test.create_index(
       #     {
        #        'Garment Layer': 'text',
         #       "Colour" : "text"
          #  }
        #)

        query = db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
        ids = query.distinct("ID")
        search_results = []


        for doc in ids:
            search_results.append(doc)


        # close connection
        client.close()



        return render_template('search_results2.html', search_results=search_results)

        #return render_template('imageTemplate.html', value=search_results[0])
               #return send_file('static/images/' + search_results + '.jpeg', mimetype='image/jpeg')



@app.route("/cols", methods=['POST', 'GET'])

def showColor():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    colourData = []
    for x in db.TestStyle.find({"Colour" : "lightpink"}):
        colourData.append(x)


    return json.dumps(colourData, indent=4, default=json_util.default)

@app.route("/keywords", methods=['POST', 'GET'])
def showKeywords():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    showKeywords = []
    for x in db.TestStyle.find({}, {'Colour' : 0, 'ID' : 0, "_id":0, 'Garment Layer':0}):
        showKeywords.append(x)

    return json.dumps(showKeywords, indent=4, default=json_util.default)


@app.route("/image", methods=['POST', 'GET'])
def Image():

    target = os.path.join(APP_ROOT, 'static/')
    full_filename = 'static/images/1.jpeg'
    print(full_filename)
    print(target)
    return render_template("image.html", user_image=full_filename)



if __name__ == '__main__':
    app.run(debug=True, threaded=True)