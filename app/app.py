#
# Libraries
#
import os
from builtins import len, str

import pymongo
from bson import json_util
import json
from flask import Flask, request, render_template, flash, send_file, jsonify, make_response
from flask_cors import CORS
import http.client, urllib.request, urllib.parse, urllib.error, base64
from flask_paginate import Pagination, get_page_args


# create app instance
#from flask_restful.representations import json
from pymongo import MongoClient


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
CORS(app)

#
# Routes
#

@app.route('/tester')
def tester():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)

    # create db client
    db = client.stylesearch
    db.test.createIndex({"Keywords.$**": 1})
    #db.test.createIndex({'Keywords': "$text"})
    #db.test.create_index({"Keywords": 1, "$**", "$text"})
    #db.test.create_index([("Keywords": 1, '$**', 'text')])
    #db.test.create_index(

    #resp = db.test.create_index([("Keywords", -1)])
    #print("index response:", resp)

    search_results = db.test.find({ "Keywords" : "three" })

    return str(search_results)

    #return render_template('search.html')
    #return render_template('testingJune.html')
    #return render_template('GarmentType.html')
    #return render_template('2searchbars.html')

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
        #search_results = db.TestStyle.find({'$text': {'$search': '"\" "' + request.args.get('search') + '\""'}})

        #query = db.TestStyle.find({'$text': {'$search': '"\" "' + request.args.get('search') + '\""'}},
         #                         {'$text': {'$search': request.args.get('search')}})
        #search_results =  db.TestStyle.find({'$text': {'$search': '"\" "' + request.args.get('search') + '\""' + request.args.get('search')}})
        search_results = db.TestStyle.find({'$text': {'$search': request.args.get('search') + '' + '"\" "' + request.args.get('search') + '\""'}})


        #search_results = db.TestStyle.find({'$text': {'$search': request.args.get('search')}})


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
        #db.TestStyle.create_index( { "Keywords": 1, "$**": "text" } )
    #  db.test.create_index(
       #     {
        #        'Garment Layer': 'text',
         #       "Colour" : "text"
          #  }
        #)


        #query = db.TestStyle.find({'$text': {'$search': request.args.get('search')}})
        #query = db.TestStyle.find( { '$text': { '$search': "\" grunge\"" } } )

        #query = db.TestStyle.find({'$text': {'$search': '"\" "' + request.args.get('search') + '\""'}})


        #query = db.TestStyle.find({'$text':{'$search' : "\"pink top\""}})
        #query = db.TestStyle.find({'$text': {'$search': request.args.get('search') + '"\" "' + request.args.get('search') + '\""' + request.args.get('search') }})
        query = db.TestStyle.find({'$text': {'$search': '"\" "' + request.args.get('search') + '\""' + ' '+ request.args.get('search') }})
        ids = query.distinct("ID")

        search_results = []

        #TESTING ADDING KEYWORDS

        showKeywords = []
        #for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
         #   showKeywords.append(x)

        showKeywords = []
        instanceID = []
        y = 0
        for x in db.TestStyle.find({}, {'Colour': 0, "_id": 0, 'Garment Layer': 0}).sort([("_id", pymongo.ASCENDING)]):
            y = y + 1
            z = str(y)
            instanceID.append(z)
            showKeywords.append(x)

        # return render_template('keywordsTRY.html', showKeywords =  instanceID, keywords3 = showKeywords)
        # return render_template('keywords.html')


        for doc in ids:
            search_results.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', instanceID=instanceID, showKeywords=showKeywords, search_results=search_results )
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

    return render_template('topsMultiModal.html', search_results=tops, showKeywords = showKeywords )


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

    return render_template('bottomsMultiModal.html', search_results=trousers, showKeywords = showKeywords)

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

    return render_template('pulloverMultiModal.html', search_results=pullovers, showKeywords = showKeywords)


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

    return render_template('dressMultiModal.html', search_results=dresses, showKeywords = showKeywords)

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

    return render_template('jacketMultiModal.html', search_results=coats, showKeywords = showKeywords)

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

    return render_template('shoesMultiModal.html', search_results=sandals, showKeywords = showKeywords)

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

    return render_template('shirtsMultiModal.html', search_results=shirts, showKeywords = showKeywords)

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

    return render_template('trainersMultiModal.html', search_results=sneakers, showKeywords = showKeywords)


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

    return render_template('bagsMultiModal.html', search_results=bags, showKeywords = showKeywords)


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

    return render_template('bootsMultiModal.html', search_results=boots, showKeywords = showKeywords)

@app.route('/emoTops')
def topsColour():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "0", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanTops')
def urbanTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch

    queryresults = db.TestStyle.find({"Garment Layer" : "0", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageTops')
def vintageTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    boots = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('vintage')}})
    ids = boots.distinct("ID")
    queryresults = []

    for doc in ids:
        queryresults.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/streetTops')
def streetTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)

    # close connection
    client.close()

    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/retroTops')
def retroTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('retro')}})
    # boots = db.TestStyle.find({"Colour": "pink"})
    # boots = db.TestStyle.find({"Garment Layer": "0"})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()

    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/gothicTops')
def gothicTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/grungeTops')
def grungeTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/alternativeTops')
def alternativeTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/formalTops')
def formalTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch

    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/indieTops')
def indieTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()

    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/athleticTops')
def athleticTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('sporty')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/pastelTops')
def pastelTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch

    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/quirkyTops')
def quirkyTops():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "0", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/indieTrousers')
def indieTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer": "1", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)

@app.route('/emoTrousers')
def emoTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanTrousers')
def urbanTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetTrousers')
def streetTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageTrousers')
def vintageTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroTrousers')
def retroTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicTrousers')
def gothicTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeTrousers')
def grungeTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeTrousers')
def alternativeTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalTrousers')
def formalTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticTrousers')
def athleticTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelTrousers')
def pastelTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    # create db client
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    # close connection
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyTrousers')
def quirkyTrousers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "1", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoJumpers')
def emoJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanJumpers')
def urbanJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageJumpers')
def vintageJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetJumpers')
def streetJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroJumpers')
def retroJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicJumpers')
def gothicJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeJumpers')
def grungeJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeJumpers')
def alternativeJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalJumpers')
def formalJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieJumpers')
def indieJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticJumpers')
def athleticJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelJumpers')
def pastelJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyJumpers')
def quirkyJumpers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "2", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoDresses')
def emoDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanDresses')
def urbanDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageDresses')
def vintageDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetDresses')
def streetDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroDresses')
def retroDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicDresses')
def gothicDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeDresses')
def grungeDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeDresses')
def alternativeDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalDresses')
def formalDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieDresses')
def indieDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticDresses')
def athleticDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelDresses')
def pastelDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyDresses')
def quirkyDresses():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "3", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoJackets')
def emoJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanJackets')
def urbanJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageJackets')
def vintageJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetJackets')
def streetJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroJackets')
def retroJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicJackets')
def gothicJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeJackets')
def grungeJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeJackets')
def alternativeJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalJackets')
def formalJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieJackets')
def indieJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticJackets')
def atleticJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelJackets')
def pastelJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyJackets')
def quirkyJackets():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "4", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoShoes')
def emoShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanShoes')
def urbanShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageShoes')
def vintageShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetShoes')
def streetShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroShoes')
def retroShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicShoes')
def gothicShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeShoes')
def grungeShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeShoes')
def alternativeShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalShoes')
def formalShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieShoes')
def indieShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticShoes')
def athleticShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelShoes')
def pastelShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyShoes')
def quirkyShoes():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "5", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoShirts')
def emoShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanShirts')
def urbanShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageShirts')
def vintageShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetShirts')
def streetShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroShirts')
def retroShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicShirts')
def gothicShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeShirts')
def grungeShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeShirts')
def alternativeShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalShirts')
def formalShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieShirts')
def indieShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticShirts')
def athleticShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelShirts')
def pastelShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyShirts')
def quirkyShirts():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "6", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoSneakers')
def emoSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanSneakers')
def urbanSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageSneakers')
def vintageSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetSneakers')
def streetSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroSneakers')
def retroSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicSneakers')
def gothicSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeSneakers')
def grungeSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeSneakers')
def alternativeSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalSneakers')
def formalSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieSneakers')
def indieSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticSneakers')
def athleticSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelSneakers')
def pastelSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkySneakers')
def quirkYSneakers():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "7", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoBags')
def emoBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanBags')
def urbanBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageBags')
def vintageBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetBags')
def streetBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroBags')
def retroBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicBags')
def gothicBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeBags')
def grungeBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeBags')
def alternativeBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalBags')
def formalBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieBags')
def indieBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticBags')
def athleticBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelBags')
def pastelBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyBags')
def quirkyBags():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "8", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/emoBoots')
def emoBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('emo')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/urbanBoots')
def urbanBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('urban')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/vintageBoots')
def vinatgeBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('vintage')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/streetBoots')
def streetBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('street')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/retroBoots')
def retroBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('retro')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/gothicBoots')
def gothicBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('gothic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/grungeBoots')
def grungeBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('grunge')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/alternativeBoots')
def alternativeBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('alternative')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/formalBoots')
def formalBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('formal')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/indieBoots')
def indieBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('indie')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/athleticBoots')
def athleticBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('athletic')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/pastelBoots')
def pastelBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('pastel')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)

@app.route('/quirkyBoots')
def quirkyBoots():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    queryresults = db.TestStyle.find({"Garment Layer" : "9", '$text': {'$search': ('quirky')}})
    ids = queryresults.distinct("ID")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)


@app.route("/classification", methods=['POST', 'GET'])
def classifyImage():


    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
        'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
    }


    #theImageUrl = request.form['classificationSearch']
    theImageUrl = 'https://d2bzx2vuetkzse.cloudfront.net/fit-in/0x450/unshoppable_producs/b6bc60a3-6ff8-4e6d-9a5a-ea4ba784058b.jpeg'

    params = urllib.parse.urlencode({
        # Request parameters
       # 'image' : classification
        #'image' : newImageUrl
        'image' : theImageUrl
        #'image': 'https://d2bzx2vuetkzse.cloudfront.net/fit-in/0x450/unshoppable_producs/b6bc60a3-6ff8-4e6d-9a5a-ea4ba784058b.jpeg',
        #'image': 'https://contestimg.wish.com/api/webimage/5c394bfbe3e6604287a573da-large.jpg?cache_buster=276746c000af54b686498893ade2baea',
        # 'gender': '{string}',
         #'limit': '2',
    })

    conn = http.client.HTTPSConnection('api.mirrorthatlook.com')
    conn.request("GET", "/v2/mirrorthatlook?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    # print(data)

    my_json = data.decode('utf8')
    python_obj = json.loads(my_json)

    loaded_json = json.dumps(my_json)
    loaded_json = json.loads(my_json)

    # this works to classify the group that the item is in from the image
    classification = ((loaded_json["result"][0]["group"]))

    aResponse = (jsonify(classification))
    aResponseString = str(aResponse)

    return render_template('ClassifyLink.html', imageLink = theImageUrl, classif = str(classification))
    #return  make_response(json(classification))
    #return render_template('ClassifyLink.html', imageLink = theImageUrl, theClassification = aResponse)
    #return make_response(jsonify(classification))
    #return aResponse
    #return render_template('ClassifyLinkURLOnly.html')

@app.route("/sim", methods=['POST', 'GET'])
def mirrorLook():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
        'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'image': 'https://contestimg.wish.com/api/webimage/5c394bfbe3e6604287a573da-large.jpg?cache_buster=276746c000af54b686498893ade2baea',
        # 'gender': '{string}',
         #'limit': '2',
    })

    conn = http.client.HTTPSConnection('api.mirrorthatlook.com')
    conn.request("GET", "/v2/mirrorthatlook?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    # print(data)

    my_json = data.decode('utf8')
    python_obj = json.loads(my_json)

    loaded_json = json.dumps(my_json)
    loaded_json = json.loads(my_json)

    #print(loaded_json)
    linksData = []
    links = ((loaded_json["result"][0]["products"][0]["affiliates"][0]["link"]))
    for x in range(10):
        y = ((loaded_json["result"][0]["products"][x]["affiliates"][0]["link"]))
        linksData.append(y)

    # new_json = str(new_json).strip('[]')

    #return links

    return make_response(jsonify(linksData))
    # ^ thiz returns the array i.e multiple links

@app.route('/toClassify')
def toClassify():
    return render_template('ClassifyLinkURLOnly.html')

@app.route('/classifiedResults', methods = ['GET', 'POST'])
def classifiedResults():
    if request.method == 'POST':
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
            'Ocp-Apim-Subscription-Key': 'ba10a036532d4c438ded719c0f797a4e',
        }

        # theImageUrl = request.form['classificationSearch']
        theImageUrl = request.form['URLtoClassify']

        params = urllib.parse.urlencode({
            # Request parameters
            # 'image' : classification
            # 'image' : newImageUrl
            'image': theImageUrl
            # 'image': 'https://d2bzx2vuetkzse.cloudfront.net/fit-in/0x450/unshoppable_producs/b6bc60a3-6ff8-4e6d-9a5a-ea4ba784058b.jpeg',
            # 'image': 'https://contestimg.wish.com/api/webimage/5c394bfbe3e6604287a573da-large.jpg?cache_buster=276746c000af54b686498893ade2baea',
            # 'gender': '{string}',
            # 'limit': '2',
        })

        conn = http.client.HTTPSConnection('api.mirrorthatlook.com')
        conn.request("GET", "/v2/mirrorthatlook?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        # print(data)

        my_json = data.decode('utf8')
        python_obj = json.loads(my_json)

        loaded_json = json.dumps(my_json)
        loaded_json = json.loads(my_json)

        # this works to classify the group that the item is in from the image
        classification = ((loaded_json["result"][0]["group"]))

        aResponse = (jsonify(classification))
        aResponseString = str(aResponse)

        return render_template('ClassifyLink.html', imageLink=theImageUrl, classif=str(classification))


        #return render_template('display.html', URLtoClassify=URLtoClassify)

@app.route('/getColour')
def getColour():
    return render_template('displayColours.html')

@app.route('/trousersColour', methods = ['GET', 'POST'])
def colourReturned():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "1", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/topColour', methods = ['GET', 'POST'])
def topColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "0", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/pulloverColour', methods = ['GET', 'POST'])
def pulloverColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "2", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/dressColour', methods = ['GET', 'POST'])
def dressColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "3", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/coatsColour', methods = ['GET', 'POST'])
def coatColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "4", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/shoesColour', methods = ['GET', 'POST'])
def shoesColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "5", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/shirtColour', methods = ['GET', 'POST'])
def shirtColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "6", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/sneakerColour', methods = ['GET', 'POST'])
def sneakerColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "7", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/bagColour', methods = ['GET', 'POST'])
def bagColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "8", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/bootsColour', methods = ['GET', 'POST'])
def bootsColour():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "9", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/locationSearch')
def locationSearch():
    #return render_template('search.html')
    #return render_template('testingJune.html')
    return render_template('locationSearch.html')
    #return render_template('2searchbars.html')


@app.route('/DressStyle')
def styleSelecDresst():
    return render_template('dressMultiModal.html')


@app.route('/styleResults', methods = ['GET', 'POST'])
def styleResults():
    if request.method == 'POST':
        #theColour = request.form['colourInput']
        theColour = request.form['colourInput']
        connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
        client = pymongo.MongoClient(connect_uri)
        # create db client
        db = client.stylesearch
        queryresults = db.TestStyle.find({"Garment Layer": "1", "Colour": theColour})
        ids = queryresults.distinct("ID")
        queryresults = []
        for doc in ids:
            queryresults.append(doc)
        # close connection
        client.close()

        return render_template('search_results2.html', search_results=queryresults, showKeywords=showKeywords)
        #return render_template('testDisplayColour.html', theColour = theColour, queryresults = queryresults)
        #return str(queryresults)

@app.route('/searchIn', methods = ['GET', 'POST'])
def searchIn():
    connect_uri = 'mongodb+srv://admin:admin@cluster0-zgcvy.mongodb.net/test?retryWrites=true&w=majority'
    client = pymongo.MongoClient(connect_uri)
    db = client.stylesearch
    #queryresults = db.TestStyle.find({}, {'Keywords': 1})
    #queryresults = db.TestStyle.find({}, {'Keywords': {'$search': ('gothic')}})

    queryresults = db.TestStyle.find({'$text': {'$search': ('tie dye')}})
    #queryresults = db.TestStyle.aggregate([{"$match:"{$and : [{'Keywords' : {$exists: true, $in}}]}}])

    #queryresults = db.TestStyle.find(({'Keywords': {'$text': ('quirky')}}))
    #queryresults = db.TestStyle.find({'$text': {'$search': ('quirky')}})
    #queryresults = db.TestStyle.find({"Keywords": {'$all': ('tie dye')}})


    ids = queryresults.distinct("ID")
   # keywords = queryresults.distinct("Keywords")
    queryresults = []
    for doc in ids:
        queryresults.append(doc)
    client.close()
    #return render_template('search_results2.html', search_results=queryresults, showKeywords = showKeywords)
    return str(queryresults)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)#
