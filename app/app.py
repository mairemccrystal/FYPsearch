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
    #return render_template('testingJune.html')
    return render_template('GarmentType.html')
    #return render_template('2searchbars.html')

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

        #TESTING ADDING KEYWORDS

        showKeywords = []
        #for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
         #   showKeywords.append(x)

        for x in db.TestStyle.find({"ID" : '$i'}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
            showKeywords.append(x)

       # for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
        #        showKeywords.append(x)


        for doc in ids:
            search_results.append(doc)




        # close connection
        client.close()



        return render_template('search_results2.html', search_results=search_results, keywords = showKeywords)

        #return render_template('searchwithKeywords.html', search_results=search_results, showKeywords = showKeywords)


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
    instanceID = []
    y = 0
    for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):

            y = y+1
            z = str(y)
            instanceID.append(z)
            showKeywords.append(x)

    #return render_template('keywordsTRY.html', showKeywords =  instanceID, keywords3 = showKeywords)
    #return render_template('keywords.html')
    return render_template('search_results2.html', instanceID = instanceID, showKeywords = showKeywords, )

   # return json.dumps(showKeywords, indent=4, default=json_util.default)


   # return json.dumps(showKeywords, indent=4, default=json_util.default)

@app.route("/keywords2", methods=['POST', 'GET'])
def showKeywords2():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    theseKWs = []

    #for x in db.TestStyle.find({"ID" : '}):


   # for x in db.TestStyle.find({}), {'ID':1}).sort():
    #   theseKWs.append(x)
    nums = []
    for x in db.TestStyle.find({}, {'Colour' : 0, "_id":0, 'Garment Layer':0}).sort([("_id", pymongo.ASCENDING)]):
        theseKWs.append(x)


    for y in db.TestStyle.find().sort([("_id", pymongo.ASCENDING)]):
        y = str(y)
        nums.append(y)




    #return render_template('keywords.html', showKeywords = theseKWs, ids = nums)
   # return render_template('search_results2.html', showKeywords=theseKWs)
    #return theseKWs
    return str(nums)



    #return json.dumps(theseKWs, indent=4, default=json_util.default)


   # return json.dumps(showKeywords, indent=4, default=json_util.default)


@app.route("/image", methods=['POST', 'GET'])
def Image():

    target = os.path.join(APP_ROOT, 'static/')
    full_filename = 'static/images/1.jpeg'
    print(full_filename)
    print(target)
    return render_template("image.html", user_image=full_filename)

@app.route("/cols2", methods=['POST', 'GET'])
def showGarment():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    colourData = []
    for x in db.TestStyle.find({"Garment Layer" : "0"}):
        colourData.append(x)

    return json.dumps(colourData, indent=4, default=json_util.default)

@app.route('/tops')
def tops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    tops = db.TestStyle.find({"Garment Layer" : "0"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = tops.distinct("ID")
    tops = []

    for doc in ids:
        tops.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=tops)


@app.route('/trousers')
def trousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    trousers = db.TestStyle.find({"Garment Layer" : "1"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = trousers.distinct("ID")
    trousers = []

    for doc in ids:
        trousers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=trousers)

@app.route('/pullovers')
def pullovers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    pullovers = db.TestStyle.find({"Garment Layer" : "2"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = pullovers.distinct("ID")
    pullovers = []

    for doc in ids:
        pullovers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=pullovers)


@app.route('/dresses')
def dresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    dresses = db.TestStyle.find({"Garment Layer" : "3"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = dresses.distinct("ID")
    dresses = []

    for doc in ids:
        dresses.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=dresses)

@app.route('/coats')
def coats():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    coats = db.TestStyle.find({"Garment Layer" : "4"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = coats.distinct("ID")
    coats = []

    for doc in ids:
        coats.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=coats)

@app.route('/sandals')
def sandals():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    sandals = db.TestStyle.find({"Garment Layer" : "5"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = sandals.distinct("ID")
    sandals = []

    for doc in ids:
        sandals.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=sandals)

@app.route('/shirts')
def shirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    shirts = db.TestStyle.find({"Garment Layer" : "6"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = shirts.distinct("ID")
    shirts = []

    for doc in ids:
        shirts.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=shirts)

@app.route('/sneakers')
def sneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    sneakers = db.TestStyle.find({"Garment Layer" : "7"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = sneakers.distinct("ID")
    sneakers = []

    for doc in ids:
        sneakers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=sneakers)


@app.route('/bags')
def bags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    bags = db.TestStyle.find({"Garment Layer" : "8"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = bags.distinct("ID")
    bags = []

    for doc in ids:
        bags.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=bags)


@app.route('/boots')
def boots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    boots = db.TestStyle.find({"Garment Layer" : "9"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = boots.distinct("ID")
    boots = []

    for doc in ids:
        boots.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=boots)

@app.route('/topsColour')
def topsColour():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch

    boots = db.TestStyle.find({"Colour": "olive"})
    boots = db.TestStyle.find({"Garment Layer": "0"})

    ids = boots.distinct("ID")
    boots = []


    for doc in ids:
        boots.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=boots)











if __name__ == '__main__':
    app.run(debug=True, threaded=True)#
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
    #return render_template('testingJune.html')
    return render_template('GarmentType.html')
    #return render_template('2searchbars.html')

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

        #TESTING ADDING KEYWORDS

        showKeywords = []
        #for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
         #   showKeywords.append(x)

        for x in db.TestStyle.find({"ID" : '$i'}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
            showKeywords.append(x)

       # for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
        #        showKeywords.append(x)


        for doc in ids:
            search_results.append(doc)




        # close connection
        client.close()



        return render_template('search_results2.html', search_results=search_results, keywords = showKeywords)

        #return render_template('searchwithKeywords.html', search_results=search_results, showKeywords = showKeywords)


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
    instanceID = []
    y = 0
    for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):

            y = y+1
            z = str(y)
            instanceID.append(z)
            if y < 3028:
                showKeywords.append(x)


    #return render_template('keywordsTRY.html', showKeywords =  instanceID, keywords3 = showKeywords)
    #return render_template('keywords.html')
    return render_template('search_results2.html', instanceID = instanceID, showKeywords = showKeywords[y])

   # return json.dumps(showKeywords, indent=4, default=json_util.default)


   # return json.dumps(showKeywords, indent=4, default=json_util.default)

@app.route("/keywords2", methods=['POST', 'GET'])
def showKeywords2():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    theseKWs = []

    #for x in db.TestStyle.find({"ID" : '}):


   # for x in db.TestStyle.find({}), {'ID':1}).sort():
    #   theseKWs.append(x)
    nums = []
    for x in db.TestStyle.find({}, {'Colour' : 0, "_id":0, 'Garment Layer':0}).sort([("_id", pymongo.ASCENDING)]):
        theseKWs.append(x)


    for y in db.TestStyle.find().sort([("_id", pymongo.ASCENDING)]):
        y = str(y)
        nums.append(y)




    #return render_template('keywords.html', showKeywords = theseKWs, ids = nums)
   # return render_template('search_results2.html', showKeywords=theseKWs)
    #return theseKWs
    return str(nums)



    #return json.dumps(theseKWs, indent=4, default=json_util.default)


   # return json.dumps(showKeywords, indent=4, default=json_util.default)


@app.route("/image", methods=['POST', 'GET'])
def Image():

    target = os.path.join(APP_ROOT, 'static/')
    full_filename = 'static/images/1.jpeg'
    print(full_filename)
    print(target)
    return render_template("image.html", user_image=full_filename)

@app.route("/cols2", methods=['POST', 'GET'])
def showGarment():
    client = MongoClient(
        "mongodb://admin:admin@cluster0-shard-00-00-zgcvy.mongodb.net:27017,cluster0-shard-00-01-zgcvy.mongodb.net:27017,cluster0-shard-00-02-zgcvy.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.stylesearch
    # dbCollection = db.Style
    colourData = []
    for x in db.TestStyle.find({"Garment Layer" : "0"}):
        colourData.append(x)

    return json.dumps(colourData, indent=4, default=json_util.default)

@app.route('/tops')
def tops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    tops = db.TestStyle.find({"Garment Layer" : "0"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = tops.distinct("ID")
    tops = []

    for doc in ids:
        tops.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=tops)


@app.route('/trousers')
def trousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    trousers = db.TestStyle.find({"Garment Layer" : "1"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = trousers.distinct("ID")
    trousers = []

    for doc in ids:
        trousers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=trousers)

@app.route('/pullovers')
def pullovers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    pullovers = db.TestStyle.find({"Garment Layer" : "2"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = pullovers.distinct("ID")
    pullovers = []

    for doc in ids:
        pullovers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=pullovers)


@app.route('/dresses')
def dresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    dresses = db.TestStyle.find({"Garment Layer" : "3"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = dresses.distinct("ID")
    dresses = []

    for doc in ids:
        dresses.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=dresses)

@app.route('/coats')
def coats():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    coats = db.TestStyle.find({"Garment Layer" : "4"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = coats.distinct("ID")
    coats = []

    for doc in ids:
        coats.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=coats)

@app.route('/sandals')
def sandals():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    sandals = db.TestStyle.find({"Garment Layer" : "5"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = sandals.distinct("ID")
    sandals = []

    for doc in ids:
        sandals.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=sandals)

@app.route('/shirts')
def shirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    shirts = db.TestStyle.find({"Garment Layer" : "6"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = shirts.distinct("ID")
    shirts = []

    for doc in ids:
        shirts.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=shirts)

@app.route('/sneakers')
def sneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    sneakers = db.TestStyle.find({"Garment Layer" : "7"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = sneakers.distinct("ID")
    sneakers = []

    for doc in ids:
        sneakers.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=sneakers)


@app.route('/bags')
def bags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    bags = db.TestStyle.find({"Garment Layer" : "8"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = bags.distinct("ID")
    bags = []

    for doc in ids:
        bags.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=bags)


@app.route('/boots')
def boots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    boots = db.TestStyle.find({"Garment Layer" : "9"})
        #db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
    ids = boots.distinct("ID")
    boots = []

    for doc in ids:
        boots.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=boots)

@app.route('/topsColour')
def topsColour():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch

    boots = db.TestStyle.find({"Colour": "olive"})
    boots = db.TestStyle.find({"Garment Layer": "0"})

    ids = boots.distinct("ID")
    boots = []


    for doc in ids:
        boots.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=boots)











if __name__ == '__main__':
    app.run(debug=True, threaded=True)