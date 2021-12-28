from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timedelta
import os
import random
import pandas as pd
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotions.db'
app.config['SECRET_KEY'] = b'sjfhwfu4w87iowjddo3uwiokMlaEGU9O\IAO'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Game(db.Model):
    __tablename__ = 'games'
    gameid = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    initial_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)
    monsters = db.Column(db.Integer)
    coins = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

db.create_all()
db.session.commit()

class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Game

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/game', methods = ['POST'])
@cross_origin(supports_credentials=True)
def game_post():
    info = request.json

    completed = True if info["completed"]=="true" else False

    new_game = Game(type=info["type"],initial_time=info["initial_time"],end_time=info["end_time"],monsters=info["monsters"],coins=info["coins"],completed=completed)

    db.session.add(new_game)
    db.session.commit()
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/getgames')
def getgames():
    games = Game.query.all()
    game_schema = GameSchema(many=True)
    output = game_schema.dump(games)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)