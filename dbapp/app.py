from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sl= db.Column(db.Float)
    sw= db.Column(db.Float)
    pl= db.Column(db.Float)
    pw= db.Column(db.Float)
    prediction=db.Column(db.String(50))

@app.route("/add_record", methods=['POST'])
def add_record():
    record= request.get_json()
    record=Prediction(**record)
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "Record added successfully"}), 201

@app.route("/records", methods=['GET'])
def get_records():
    records=Prediction.query.all()
    output=[]
    for record in records:
        rec_dict={
            "id": record.id,
            "sl": record.sl,
            "sw": record.sw,
            "pl": record.pl,
            "pw": record.pw,
            "prediction": record.prediction
        }
        output.append(rec_dict)
    return jsonify(output)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    serve(app, host="0.0.0.0", port=8001)