# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = 'broadcasts.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS broadcasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/panel')
def panel():
    return render_template('panel.html')

@app.route('/add_broadcast', methods=['POST'])
def add_broadcast():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'message': 'URL boş bırakılamaz.'}), 400

    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO broadcasts (url) VALUES (?)", (url,))
        conn.commit()
        return jsonify({'message': 'Yayın başarıyla eklendi!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Bu yayın zaten eklenmiş.'}), 409
    finally:
        conn.close()

@app.route('/broadcasts', methods=['GET'])
def get_broadcasts():
    conn = get_db_connection()
    broadcasts = conn.execute("SELECT url FROM broadcasts ORDER BY id DESC").fetchall()
    conn.close()
    urls = [row['url'] for row in broadcasts]
    return jsonify(urls)

if __name__ == '__main__':
    # Flask ve SQLite kütüphaneleri kurulu değilse:
    # pip install Flask
    # pip install Flask-Cors
    app.run(debug=True)
