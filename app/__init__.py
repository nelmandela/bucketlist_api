from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import datetime
import jwt
import json
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///test_db', echo=True)

# local import
from instance.config import app_config

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/api/v1/')

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


def user_exists(email):
    user = session.query(User).filter(User.email == email).first()
    if user:
        return user
    return False

@app.route('/auth/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        if not user_exists(email):
            user = User(name, email, password)
            session.add(user)
            session.commit()
            response = jsonify({
                'message': 'signup successful'
            })
            response.status_code = 201
            return response
        else:
            response = jsonify({
                'error': 'signup unsuccessful,user already exists'
            })
            response.status_code = 400
            return response

    

@app.route('/auth/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = user_exists(email)
        if user:
            if user.compare_password(password):
                encoded = jwt.encode({'id': user.id}, 'secret', algorithm='HS256')
                response = jsonify({
                    'message': 'login successful',
                    'access_token':encoded
                })
                response.status_code = 200
                return response
        
        response = jsonify({
            'error': 'invalid username/password'
        })
        response.status_code = 400
        return response

@app.route('/bucketlists', methods=['GET', 'POST'])
def bucketlists():
    if request.method == 'POST':
        if 'Access-Token' in request.headers:
            token = request.headers['Access-Token']
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            created_by = session.query(User).filter(User.id == decoded['id']).first()
            print request.json
            bucketlist_id = request.json['bucketlist_id']
            bucketlist = Bucketlist(bucketlist_id, decoded['id'])
            session.add(bucketlist)
            session.commit()
            response = jsonify({
                'message': 'bucketlist created'
            })
            response.status_code = 201
            return response

    if request.method == 'GET':
        if 'Access-Token' in request.headers:
            token = request.headers['Access-Token']
            decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = session.query(User).filter(User.id == decoded['id']).first()
            bucketlists =[]
            for bucketlist in user.bucketlists:
                bucketlists.append({
                    "bucketlist_id": bucketlist.bucketlist_id,
                    "date_created": bucketlist.date_created,
                    "date_modified": bucketlist.date_modified,
                })
            return jsonify(bucketlists)
        else:
            response = jsonify({
                'message': 'You are not logged in'
            })
            response.status_code = 401
            return response

@app.route('/bucketlists/<id>', methods=['PUT', 'DELETE'])
def update_bucketlists(id=None):
    if request.method == 'PUT':
        if id is not None:
            if 'Access-Token' in request.headers:
                token = request.headers['Access-Token']
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                bucketlist = session.query(Bucketlist).filter(Bucketlist.id == id).first()
                if bucketlist:
                    query = update(Bucketlist).where(Bucketlist.id== bucketlist.id).values(bucketlist_id=request.json['bucketlist_id'])
                    session.execute(query);
                    session.commit()
                    response = jsonify({
                        'message': 'bucketlist updated'
                    })
                    response.status_code = 200
                    return response
                else:
                    response = jsonify({"error": "bucket list not found"})
                    response.status_code = 404
                    return response
            else:
                response = jsonify({})
                response.status_code = 401
                return response

    if request.method == 'DELETE':
        if id is not None:
            if 'Access-Token' in request.headers:
                token = request.headers['Access-Token']
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = session.query(User).filter(User.id == decoded['id']).first()
                bucketlists =[]
                for bucketlist in user.bucketlists:
                    user.bucketlists[int(id)].finished = True
                session.delete(bucketlist)
                session.commit()
                response = jsonify({
                    'message': 'bucketlist deleted'
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({})
                response.status_code = 401
                return response

@app.route('/bucketlists/<id>/items', methods=['POST'])
def bucketlists_items(id):
    if request.method == 'POST':
        item_name = request.json["bucketlist_item"]
        bucketlist_item = Bucketlist_item(id, item_name)
        session.add(bucketlist_item)
        session.commit()
        response = jsonify({
            'message': 'bucketlist_item created'
        })
        response.status_code = 201
        return response
    else:
        return "unsuccessful,post only"

@app.route('/bucketlists/<id>/items', methods=['PUT','DELETE'])
def update_bucketlist_items(id=None):
    if request.method == 'PUT':
        if id is not None:
            if 'Access-Token' in request.headers:
                token = request.headers['Access-Token']
                decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
                bucketlist_item = session.query(Bucketlist_item).filter(Bucketlist_item.id == id).first()
                if bucketlist_item:
                    query = update(Bucketlist_item).where(Bucketlist_item.id== bucketlist_item.id).values(bucketlist_item_id=request.json['bucketlist_item_id'])
                    session.execute(query);
                    session.commit()
                    response = jsonify({
                        'message': 'bucketlist item updated'
                    })
                    response.status_code = 200
                    return response
                else:
                    response = jsonify({"error": "bucketlist item not found"})
                    response.status_code = 404
                    return response
            else:
                response = jsonify({})
                response.status_code = 401
                return response

    if request.method == 'DELETE':
        if id is not None:
          if 'Access-Token' in request.headers:
              token = request.headers['Access-Token']
              decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
              bucketlist_item = session.query(Bucketlist_item).filter(Bucketlist_item.id == id).delete()
              #bucketlist_items =[]
              #if bucketlist_item:
                  #query = delete(Bucketlist_item).where(Bucketlist_item.id== bucketlist_item.id).values(bucketlist_item_id=request.json['bucketlist_item_id'])
                  #session.delete(query);
              session.commit()
              response = jsonify({
                  'message': 'bucketlist item deleted'
              })
              response.status_code = 200
              return response
          #else:
              #response = jsonify({"error": "bucketlist item not found"})
              #response.status_code = 404
          else:
              response = jsonify({})
              response.status_code = 401
              return response  


    return app