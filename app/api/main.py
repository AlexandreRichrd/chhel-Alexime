from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client.bigdata
collection = db.raw_pollution

@app.route('/data', methods=['GET'])
def get_data():
    data = []
    for doc in collection.find():
        data_iso=str(doc["date"])+""
        data.append({
            "time": doc["date"],  # Assurez-vous que c'est une date ISO 8601
            "value": doc["valeur"]
        })
    print(f"Get data")
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)