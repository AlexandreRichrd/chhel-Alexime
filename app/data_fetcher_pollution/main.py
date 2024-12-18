import requests
from kafka import KafkaProducer
import json

# Kafka configuration
KAFKA_BROKER = 'kafka:9092'  # Utilise 'kafka' car Docker Compose utilise ce hostname
KAFKA_TOPIC = 'air_quality_topic'  # Assure-toi que le topic est cohérent avec Docker Compose

# API endpoint
url = "https://data.angers.fr/api/explore/v2.1/catalog/datasets/indice-de-qualite-de-lair-angers-loire-metropole/records"
params = {
    "fields": "valeur,date_ech",  # Fields to fetch
    "limit": 10,
    "offset": 0,
    "timezone": "UTC"
}

try:
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("Kafka producer initialized successfully.")

    # Fetch data from API
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Loop through results and send to Kafka
    for record in data.get('records', []):  # Correction du chemin
        fields = record.get('fields', {})
        message = {
            "date_ech": fields.get('date_ech', 'No date'),
            "valeur": fields.get('valeur', 'No value')
        }
        producer.send(KAFKA_TOPIC, value=message)
        print(f"Sent to Kafka: {message}")

    # Close the producer
    producer.flush()
    producer.close()
    print("Kafka producer closed successfully.")

except requests.exceptions.RequestException as e:
    print("Error fetching data from API:", e)
except Exception as e:
    print("Error sending data to Kafka:", e)
