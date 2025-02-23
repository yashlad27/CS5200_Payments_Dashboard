import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize Flask App
app = Flask(__name__)
CORS(app)

try:
    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    print("Flask can connect to MySQL ✅")
except pymysql.MySQLError as e:
    print("Flask cannot connect to MySQL ❌", e)

# Database Configuration using .env variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

print("DB_USERNAME:", DB_USERNAME)
print("DB_PASSWORD:", DB_PASSWORD)
print("DB_HOST:", DB_HOST)
print("DB_NAME:", DB_NAME)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?ssl_disabled=True'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Cardholder(db.Model):
    __tablename__ = 'cardholders'
    cardholder_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    cardholder_address = db.Column(db.Text)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cardholders.cardholder_id'), nullable=False)
    merchant_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    transaction_status = db.Column(db.String(20), nullable=False)

# Routes
@app.route('/api/cardholders', methods=['GET'])
def get_cardholders():
    cardholders = Cardholder.query.all()
    return jsonify([{
        'cardholder_id': c.cardholder_id,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'email': c.email,
        'phone': c.phone,
        'cardholder_address': c.cardholder_address
    } for c in cardholders])

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([{
        'transaction_id': t.transaction_id,
        'card_id': t.card_id,
        'merchant_id': t.merchant_id,
        'amount': t.amount,
        'currency': t.currency,
        'transaction_status': t.transaction_status
    } for t in transactions])

@app.route('/api/cardholders', methods=['POST'])
def add_cardholder():
    data = request.json
    new_cardholder = Cardholder(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        cardholder_address=data['cardholder_address']
    )
    db.session.add(new_cardholder)
    db.session.commit()
    return jsonify({'message': 'Cardholder added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)