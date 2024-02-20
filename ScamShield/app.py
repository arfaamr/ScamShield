import sqlite3
from flask import Flask, render_template, request

import urllib.parse

import requests
import config
import json


app = Flask(__name__)

# run: cd Testing, export flask_app=testapp.py, flask run


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# open index template
@app.route("/")
def index():
    conn = get_db_connection()
    scams = conn.execute("SELECT * FROM scams").fetchall()
    conn.close()
    return render_template("index.html", scams=scams)


# open page2
@app.route("/page2")
def page2():
    return render_template("page2.html")


# open page3
@app.route("/page3")
def page3():
    return render_template("page3.html")


# ----- APIS

# gets textbox/imagebox
@app.route("/", methods=["POST"])
def getForm():
    d = request.form.to_dict()
    if "textbox" in d.keys():
        text = d["textbox"]
        is_spam = checkSpam(text)
        return render_template("page2.html", spam=is_spam)

    elif "imagebox" in d.keys():
        fpath = "images/" + d["imagebox"]
        text = ocr(fpath)
        is_spam = checkSpam(text)
        return render_template("page2.html", spam=is_spam)
    else:
        print("Err")


#! api kinda brokey
# https://apilayer.com/marketplace/spamchecker-api 3000/mo
def checkSpam(text):
    if isinstance(text, str):
        text = text.split()

    for l in text:
        print(l)
        if "www" in l:
            return checkURL(l)

    #return False  # TEMP so that api calls don't get wasted in testing
    # return render_template("index.html", spam=False)   # force return False for frontend testing
    
    text = " ".join(text)
    print(text)
    key = config.SPAM_KEY
    headers = {"apikey": key}
    payload = text.encode("utf-8")  # encoded input data to scan
    threshold = 2
    api_url = "https://api.apilayer.com/spamchecker?threshold=%d" % threshold

    r = requests.request("POST", api_url, headers=headers, data=payload, verify=True)

    # status_code = r.status_code
    result = r.text
    dct = json.loads(result)
    return dct["is_spam"]


# FIXME: calling, but url invalid?
# https://www.apivoid.com/api/url-reputation/
def checkURL(url):
    print(url)
    key = config.DOM_KEY
    api_url = "https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key=%s&url=%s" % (
        key,
        urllib.parse.quote(url),
    )

    print("calling")
    r = requests.post(api_url)

    j = r.json()
    print(j)

    print(j["data"]["report"]["risk_score"]["result"])

    return False


# https://api-ninjas.com/api/imagetotext 10000/mo
def ocr(fpath):

    key = config.OCR_KEY
    headers = {"X-Api-Key": key}
    fd = open(fpath, "rb")
    files = {"image": fd}
    api_url = "https://api.api-ninjas.com/v1/imagetotext"

    r = requests.post(api_url, files=files, headers=headers)

    text = []
    for l in r.json():
        text.append(l["text"])

    return text
