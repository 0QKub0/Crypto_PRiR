from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

main = Blueprint('main', __name__)
databaseURL = 'mongodb+srv://desirecutieqb:Bloodqkub36@baza1.kxccyjn.mongodb.net/?retryWrites=true&w=majority&appName=Baza1'

client = MongoClient(databaseURL, server_api=ServerApi('1'))
db = client.crypto_db
collection = db.crypto_collection
alerts_collection = db.alerts

@main.route('/')
def index():
    docs = list(collection.find({}))
    prices = {doc['crypto']: doc for doc in docs}
    return render_template('index.html', prices=prices)

@main.route('/<crypto>')
def crypto_detail(crypto):
    doc = collection.find_one({'crypto': crypto.upper()})
    if not doc:
        price_data = {'price': 'N/A', 'volume': 'N/A', 'percent_change': 'N/A', 'market_cap': 'N/A'}
    else:
        price_data = {
            'price': doc['price'],
            'volume': doc['volume'],
            'percent_change': doc['percent_change'],
            'market_cap': doc['market_cap']
        }
    return render_template('crypto.html', crypto=crypto.upper(), price_data=price_data)

@main.route('/set_alert', methods=['POST'])
def set_alert():
    data = request.json
    crypto = data['crypto'].upper()
    price_threshold = data['price_threshold']
    
    alert = {
        'crypto': crypto,
        'price_threshold': price_threshold
    }
    alerts_collection.insert_one(alert)
    return jsonify({'message': 'Próg został dodany pomyślnie'}), 201
