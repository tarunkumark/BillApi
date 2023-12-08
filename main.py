from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import json
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fyproject_user:7QMbmgPI18cRIsmXrHgXdzSQt0PcIxb5@dpg-ch8cf0g2qv2864s908eg-a.oregon-postgres.render.com/fyproject'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)


app.secret_key='asdsdfsdfs13sdf_df%&'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_no = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    water_consumer_no = db.Column(db.String(120), nullable=True)
    electricity_consumer_no = db.Column(db.String(120), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
def home():
    if 'phone_no' not in session:
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'}

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        phone_no = request.json['phone_no']
        password = request.json['password']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        water_consumer_no = request.json['water_consumer_no']
        electricity_consumer_no = request.json['electricity_consumer_no']

        fullname = firstname + " " + lastname
        user =User.query.filter_by(phone_no=phone_no).first()
        if user:
            return json.dumps({'success':False}), 401, {'ContentType':'application/json'}
        user = User(phone_no=phone_no, password=password, fullname=fullname, water_consumer_no=water_consumer_no, electricity_consumer_no=electricity_consumer_no)
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    return json.dumps({'success':False}), 401, {'ContentType':'application/json'}

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        phone_no = request.json['phone_no']
        password = request.json['password']
        user = User.query.filter_by(phone_no=phone_no, password=password).first()
        if user is not None:
            session['phone_no'] = phone_no
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        else:
            return json.dumps({'success':"user is NOne"}), 401, {'ContentType':'application/json'}

    return json.dumps({'success':"idk"}), 401, {'ContentType':'application/json'}

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('phone_no', None)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route("/me", methods=['GET'])
def me():
    if 'phone_no' in session:
        user = User.query.filter_by(phone_no=session['phone_no']).first()
        return json.dumps({'success':True, "phone_no":user.phone_no,"fullname":user.fullname,"electric_consumer_no":user.electricity_consumer_no,"water_consumer_no":user.water_consumer_no}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 401, {'ContentType':'application/json'}

if __name__ == '__main__':
    app.run(debug=True)