from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo 
from bson import json_util
import datetime
import json 

app = Flask(__name__)

def Connect():
    return PyMongo(app, uri="mongodb://localhost:27017/Blog")

@app.route("/")
def home():    
    return render_template("index.html")

@app.route("/loadmessages")
def load():
    #Read data from mongo and pass it to our template
    mongo = Connect()
    messages = list(mongo.db.Messages.find())
    return jsonify(json.loads(json_util.dumps(messages)))

#Note the methods, we have post to match what is in index.html under the form tag
@app.route("/postmessage", methods=["GET","POST"])
def post():
    #we sent data to this page via the form (in index.html). Notice that 
    #UserName matches the name attribute in the input tag
    #Message matches the name attribute in the textarea tag

    j = request.get_json()

    user = j["UserName"]
    message = j["Message"]
    postTime = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
    
    mongo = Connect()
    mongo.db["Messages"].insert_one({
            "User" : user,
            "Message" : message.strip(),
            "PostTime" : postTime})


    return jsonify(['success'])

if __name__ == '__main__':
    app.run(debug=True)