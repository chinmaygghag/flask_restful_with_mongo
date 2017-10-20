from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson import json_util
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

MONGO_URI = 'mongodb://127.0.0.1/test'
PORT = 27017
mongo = PyMongo(app)

# def db_conn():
#     client = MongoClient(MONGO_URI, PORT)
#     return client

@app.route('/wbtestGet', methods=['GET'])
def get_all_wbTestData():
  client = MongoClient(MONGO_URI, PORT)
  db = client['test']
  data_set = mongo.db.wbtest.find()
  data = [json.dumps(item, default=json_util.default) for item in data_set]
  return '<pre>{}</pre>'.format(data)
  #return jsonify(data = data)

@app.route('/wbtestSpecificData', methods=['POST'])
def get_specific_wbTestData():
  client = MongoClient(MONGO_URI, PORT)
  db = client['test']
  req_data_set = request.get_json()
  if not req_data_set:
      data = {"response": "ERROR"}
      return jsonify(data)
  else:
      registration = req_data_set.get('email')
      if registration:
          data_set = mongo.db.wbtest.find_one({"email":registration})
          if data_set:
              data_set = mongo.db.wbtest.find({"email":registration})
              data_req = [json.dumps(item, default=json_util.default) for item in data_set]
              return '<pre>{}</pre>'.format(data_req)
            #return jsonify(data)
          else:
              return ("User doesn't exist")

@app.route('/wbtestPost', methods=['POST'])
def add_wbData():
  client = MongoClient(MONGO_URI, PORT)
  db = client['test']
  data = request.get_json()
  if not data:
    data = {"response": "ERROR"}
    return jsonify(data)
  else:
    registration = data.get('email')
    if registration:
        if mongo.db.wbtest.find_one({"email": registration}):
            return ("User already exist ")

        else:
            mongo.db.wbtest.insert_one(data)
    else:
        return jsonify({"response": "e-mail missing"})
  return ("Added Succesfully")


@app.route('/wbtestUpdate', methods=['POST'])
def update_wbData():
  client = MongoClient(MONGO_URI, PORT)
  db = client['test']
  wbtest = mongo.db.wbtest
  data = request.get_json()
  if not data:
    data = {"response": "ERROR"}
    return jsonify(data)
  else:
    registration = data.get('email')
    data_set = mongo.db.wbtest.find_one({"email": registration})
    if registration:
        if mongo.db.wbtest.find_one({"email": registration}):
            db.wbtest.update(data_set,data)
            return ("Updated Succesfully")
        else:
            return ("User does not exist")
    else:
        return jsonify({"response": "e-mail missing"})


if __name__ == '__main__':
    app.run(debug=True)
