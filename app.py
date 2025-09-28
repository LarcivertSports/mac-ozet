# app.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# Gerçek bir uygulamada burası bir veritabanı olmalıdır.
# Şimdilik, yayınları saklamak için basit bir liste kullanıyoruz.
broadcasts_db = []

@app.route('/add_broadcast', methods=['POST'])
def add_broadcast():
    data = request.json
    broadcast_url = data.get('broadcastUrl')

    if not broadcast_url:
        return jsonify({'error': 'URL sağlanmadı'}), 400

    # Gerçek bir senaryoda burada daha gelişmiş URL doğrulama ve işleme yapılır.
    broadcasts_db.append(broadcast_url)
    
    return jsonify({'message': 'Yayın başarıyla eklendi', 'url': broadcast_url}), 201

if __name__ == '__main__':
    app.run(debug=True)
 
