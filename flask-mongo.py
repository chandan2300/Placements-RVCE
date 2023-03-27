from flask import Flask, url_for, request, session, g
import os

from flask_pymongo import PyMongo
from flask.templating import render_template
from werkzeug.utils import redirect
from pymongo import MongoClient
from transformers import pipeline


app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017",tls=True,tlsAllowInvalidCertificates=True)
mongo_db = client.get_database()
test = mongo_db.Reviews
nlp = pipeline("sentiment-analysis")


@app.route('/')
def index():
    return render_template('testmongo.html')

@app.route('/review',methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        data = request.form.get("review")
        print(data)
        result = nlp(data)
        print(result)
        
        print(test.insert_one({'text':data.strip(),'sentiment':result[0]['label']}))
        # reviews = mongodb_client.db.reviews
        # reviews.insert_one({'text':data})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)