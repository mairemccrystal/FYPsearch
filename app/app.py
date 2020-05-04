#
# Libraries
#
from builtins import len, str

import pymongo
from bson import json_util
from flask import Flask, request, render_template, flash
from flask_paginate import Pagination, get_page_args

# create app instance
from flask_restful.representations import json
from pymongo import MongoClient

app = Flask(__name__)


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
        db.Style.create_index([('$**', 'text')])
       # db.test.create_index(
        #    {
         #       "Garment Layer" : "text",
          #      "Colour" : "text"
#
 #           }
  #      )

        search_results = db.Style.find({'$text': {'$search': request.args.get('search')}})


        for entry in search_results:
            flash(entry, 'success')

        # close connection
        client.close()

    return render_template('search.html')


@app.route('/search_results')
def search_results():
    if 'search' in request.args:
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)

        # create db client
        db = client.stylesearch
        db.Style.create_index([('$**', 'text')])
      #  db.test.create_index(
       #     {
        #        'Garment Layer': 'text',
         #       "Colour" : "text"
          #  }
        #)

        query = db.Style.find({'$text': {'$search': request.args.get('search')}})
        search_results = []

        for doc in query:
            search_results.append(doc)

        # close connection
        client.close()



        # automatic pagination handling
       # total = len(search_results)
        #page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
        #pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
#
        return str(search_results)


       # return render_template('search_results.html',
     #                           search_results=search_results, len=len)
   #                            search_results=search_results[offset: offset + per_page])
   #                            page=page,
    #                           per_page=per_page,
     #                          pagination=pagination,
      #                         len=len)


@app.route("/cols", methods=['POST', 'GET'])

def showColor():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    colourData = []
    for x in db.Style.find({"Colour" : "lavender"}):
        colourData.append(x)

    return json.dumps(colourData, indent=4, default=json_util.default)




if __name__ == '__main__':
    app.run(debug=True, threaded=True)