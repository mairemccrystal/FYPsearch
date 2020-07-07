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

    return render_template('search_results2.html', search_results=pullovers, showKeywords = showKeywords)


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

    return render_template('search_results2.html', search_results=dresses, showKeywords = showKeywords)

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

    return render_template('search_results2.html', search_results=coats, showKeywords = showKeywords)

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

    return render_template('search_results2.html', search_results=sandals, showKeywords = showKeywords)

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

    return render_template('search_results2.html', search_results=shirts, showKeywords = showKeywords)

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

    return render_template('search_results2.html', search_results=sneakers, showKeywords = showKeywords)


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

    return render_template('search_results2.html', search_results=bags, showKeywords = showKeywords)


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

    return render_template('search_results2.html', search_results=boots, showKeywords = showKeywords)

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
        boots.append(doc)

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
        boots.append(doc)
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


if __name__ == '__main__':
    app.run(debug=True, threaded=True)#
