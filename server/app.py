#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id":bakery.id,
            "name":bakery.name,
            "created_at":bakery.created_at,
        }
        bakeries.append(bakery_dict)
    response = make_response(bakeries, 200)
    return response    
     

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    bakery_dict = {"id":bakery.id, "name":bakery.name, "created_at":bakery.created_at,}
    
    response = make_response(jsonify(bakery_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
    

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    goods_dict = [{"id":good.id, "name":good.name, "price":good.price, "bakery_id":good.bakery_id, "created_at":good.created_at, "updated_at":good.updated_at} for good in goods]
    response = make_response(jsonify(goods_dict), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
     
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    expensive_dict = {"id":expensive.id, "name":expensive.name, "price":expensive.price, "bakery_id":expensive.bakery_id, "created_at":expensive.created_at, "updated_at":expensive.updated_at}

    response = make_response(jsonify(expensive_dict), 200)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
