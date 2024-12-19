from kafka import KafkaConsumer
from pymongo import MongoClient
import json
import os
from time import sleep

sleep(10)

# Configuration Kafka
KAFKA_BROKER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'air_quality_topic')

# Configuration MongoDB
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DB = os.environ.get('MONGO_DB', 'bigdata')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'raw_pollution')

# Initialisation de MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Initialisation du consommateur Kafka
consumer = KafkaConsumer(
    "raw_pollution",
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("En attente de messages Kafka...")

try:
    for message in consumer:
        print(f"Message reçu : {message.value}")
        # Insérer le message dans MongoDB
        collection.insert_one(message.value)
        print("Message inséré dans MongoDB")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    client.close()
    print("Connexion MongoDB fermée")
