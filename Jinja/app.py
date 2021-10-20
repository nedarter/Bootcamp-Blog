from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo 
import datetime

app = Flask(__name__)

def Connect():
    return PyMongo(app, uri="mongodb://localhost:27017/Blog")

@app.route("/")
def home():

    #Read data from mongo and pass it to our template
    mongo = Connect()
    messages = list(mongo.db.Messages.find())
    
    return render_template("index.html", messages = messages)

#Note the methods, we have post to match what is in index.html under the form tag
@app.route("/postmessage", methods=["POST"])
def post():

    #we sent data to this page via the form (in index.html). Notice that 
    #UserName matches the name attribute in the input tag
    #Message matches the name attribute in the textarea tag

    user = request.form["UserName"]
    message = request.form["Message"]
    postTime = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
    
    mongo = Connect()
    mongo.db["Messages"].insert_one({
            "User" : user,
             "Message" : message.strip(),
             "PostTime" : postTime})

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)