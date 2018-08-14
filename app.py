from flask import Flask
from datetime import datetime
from flask import request
from flask import render_template_string, render_template
from flask import jsonify
import uuid
import firebase_client
import process
import json
from collections import OrderedDict
import HTMLParser
import os
from flask_caching import Cache
import requests
from jinja2 import Template
import data_struct_utils as du


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def index():
    return "track release status "

@app.route('/createplan',methods=['POST'])
def createReleasePlan():
    plan_data= request.data
    FBC=firebase_client.Firebase_Client()
    uniq= str(uuid.uuid4())
    try:
        FBC.putvalue(uniq,plan_data)
        return uniq
    except:
        return 'error'

@app.route('/track',methods=['GET'])
@cache.cached(timeout=25)
def get_tracking_status():
    key=request.args.get('id')
    FBC=firebase_client.Firebase_Client()
    plan=FBC.getdb().child(key).get().val()
    p1=process.processor(json.loads(plan, object_pairs_hook=OrderedDict))
    return render_template_string(p1)


@app.route('/release_history_backend/<product>', methods=['GET'])
@cache.cached(timeout=50)
def releasehistorypage(product):
    return jsonify( process.process_historical_releases(product_name=product))



@app.route('/release_history/<product>', methods=['GET'])
def releasehistory(product,methods=['GET']):
    rs=requests.get('http://0.0.0.0:5000/release_history_backend/'+product)
    data=rs.json()
    return render_template('releasehistory.html', data= data , product = product, monthSorter= du.monthSorter)


@app.route('/release_history/<product>/<year>/<month>',methods=['GET'])
def release_history_year(product,year,month):
    rs=requests.get('http://0.0.0.0:5000/release_history_backend/'+product)
    data=rs.json()
    return render_template('releasehistoryDetail.html', data=data[year][month], dateformat=du.date_formater )
    


if __name__ == '__main__':
    from os import environ    
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000), threaded=True)
    