from flask import Flask
from datetime import datetime
from flask import request
from flask import render_template
import uuid
import firebase_client
import process
import json
from collections import OrderedDict
import HTMLParser
import os

HTMLTEMPLATE="""
<!DOCTYPE html>
<html lang="en">
<head>
<title>Live Release Tracker</title>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
   {0}
</body>
</html>

"""

app = Flask(__name__)

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
def get_tracking_status():
    key=request.args.get('id')
    FBC=firebase_client.Firebase_Client()
    plan=FBC.getdb().child(key).get().val()
    p1=process.processor(json.loads(plan, object_pairs_hook=OrderedDict))
    p2=process.plan2html(p1)
    html_parser = HTMLParser.HTMLParser()
    return HTMLTEMPLATE.format(html_parser.unescape(p2))

if __name__ == '__main__':
    from os import environ
    app.run(debug=False , host='0.0.0.0', port=environ.get("PORT", 5000), threaded=True)
    