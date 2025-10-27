from flask import Flask, render_template, redirect, url_for, request
import pickle
import requests
import numpy as np
import os
from waitress import serve

app = Flask(__name__)
DB_URL = os.environ.get('DB_URL', 'http://dbapp:8001')
DB_SERVICE_URL = f"{DB_URL}/add_record"
model_path=os.path.join(os.path.abspath(os.path.dirname(__file__)),'model.pkl')
with open(file=model_path,mode="rb") as f:
    model=pickle.load(f)

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def make_pred():
        sl=float(request.form['sl'])
        sw=float(request.form['sw'])
        pl=float(request.form['pl'])
        pw=float(request.form['pw'])
        inp=np.array([sl,sw,pl,pw])
        inp=inp.reshape([1,-1])
        pred=model.predict(inp)
        requests.post(url=DB_SERVICE_URL,json={"sl":sl,"sw":sw,"pl":pl,"pw":pw,"prediction":str(pred[0])})
        return str(pred[0])

@app.route("/showrecord", methods=['GET'])
def show_record():
    records=requests.get(url=f"{DB_URL}/records")
    return render_template("records.html",records=records.json())

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)