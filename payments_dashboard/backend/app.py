import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import pymysql
import traceback

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow frontend requests

# Database Configuration
DB_USERNAME = os.getenv("DB_USERNAME", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "test123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "visa_payment_network")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?ssl_disabled=True'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Function to establish MySQL connection
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn
    except pymysql.MySQLError as e:
        print("Flask cannot connect to MySQL ❌", e)
        return None

# ------------------ ADVANCED SQL QUERIES ------------------

### ✅ Total Number of Transactions ###
@app.route('/api/total-transactions', methods=['GET'])
def get_total_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = "SELECT COUNT(*) as total_transactions FROM transactions"
        cursor.execute(query)
        result = cursor.fetchone()
        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Average Transaction Amount ###
@app.route('/api/avg-transaction', methods=['GET'])
def get_avg_transaction():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = "SELECT AVG(amount) as avg_transaction FROM transactions"
        cursor.execute(query)
        result = cursor.fetchone()
        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Minimum & Maximum Transaction Amount ###
@app.route('/api/min-max-transaction', methods=['GET'])
def get_min_max_transaction():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT 
            MIN(amount) as min_transaction, 
            MAX(amount) as max_transaction 
        FROM transactions
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Total Revenue Per Merchant ###
@app.route('/api/revenue-per-merchant', methods=['GET'])
def get_revenue_per_merchant():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT m.merchant_name, SUM(t.amount) as total_revenue
        FROM transactions t
        JOIN merchants m ON t.merchant_id = m.merchant_id
        GROUP BY m.merchant_name
        ORDER BY total_revenue DESC
        """
        cursor.execute(query)
        merchants = cursor.fetchall()
        return jsonify(merchants)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Most Active Cardholders (Transaction Count) ###
@app.route('/api/active-cardholders', methods=['GET'])
def get_active_cardholders():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT c.first_name, c.last_name, COUNT(t.transaction_id) as transaction_count
        FROM transactions t
        JOIN cardholders c ON t.card_id = c.cardholder_id
        GROUP BY c.cardholder_id
        ORDER BY transaction_count DESC
        LIMIT 10
        """
        cursor.execute(query)
        cardholders = cursor.fetchall()
        return jsonify(cardholders)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Most Used Currencies in Transactions ###
@app.route('/api/most-used-currencies', methods=['GET'])
def get_most_used_currencies():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT currency, COUNT(*) as transaction_count
        FROM transactions
        GROUP BY currency
        ORDER BY transaction_count DESC
        """
        cursor.execute(query)
        currencies = cursor.fetchall()
        return jsonify(currencies)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Transactions Per Month ###
@app.route('/api/transactions-per-month', methods=['GET'])
def get_transactions_per_month():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT DATE_FORMAT(transaction_timestamp, '%Y-%m') AS month, COUNT(*) as total_transactions
        FROM transactions
        GROUP BY month
        ORDER BY month ASC
        """
        cursor.execute(query)
        transactions = cursor.fetchall()
        return jsonify(transactions)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

### ✅ Merchants with Failed Transactions ###
@app.route('/api/failed-transactions-merchant', methods=['GET'])
def get_failed_transactions_merchant():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = """
        SELECT m.merchant_name, COUNT(*) as failed_transactions
        FROM transactions t
        JOIN merchants m ON t.merchant_id = m.merchant_id
        WHERE t.transaction_status = 'declined'
        GROUP BY m.merchant_name
        ORDER BY failed_transactions DESC
        """
        cursor.execute(query)
        merchants = cursor.fetchall()
        return jsonify(merchants)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# ------------------ APP RUNNER ------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)