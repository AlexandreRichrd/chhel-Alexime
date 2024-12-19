# import requests
# from kafka import KafkaProducer
# import json
# import time
# import os
# from time import sleep


# sleep(15)

# # Kafka configuration
# KAFKA_BROKER = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
# KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC', 'air_quality_topic')

# # API endpoint
# url = "https://data.angers.fr/api/explore/v2.1/catalog/datasets/indice-de-qualite-de-lair-angers-loire-metropole/records"
# params = {
#     "fields": "valeur,date_ech",  # Fields to fetch
#     "limit": 10,
#     "offset": 0,
#     "timezone": "UTC"
# }

# # Initialize Kafka producer
# producer = KafkaProducer(
#     bootstrap_servers=[KAFKA_BROKER],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )
# print("Kafka producer initialized successfully.")

# try:
#     while True:  # Infinite loop to fetch and send data periodically
#         # Fetch data from API
#         response = requests.get(url, params=params)
#         response.raise_for_status()
#         data = response.json()

#         # Loop through results and send to Kafka
#         for record in data.get('records', []):  # Correction du chemin
#             fields = record.get('fields', {})
#             message = {
#                 "date_ech": fields.get('date_ech', 'No date'),
#                 "valeur": fields.get('valeur', 'No value')
#             }
#             producer.send(KAFKA_TOPIC, value=message)
#             print(f"Sent to Kafka: {message}")

#         # Sleep before fetching new data (e.g., refresh every 60 seconds)
#         time.sleep(60)  # Sleep for 60 seconds

# except requests.exceptions.RequestException as e:
#     print("Error fetching data from API:", e)
# except Exception as e:
#     print("Error sending data to Kafka:", e)
# finally:
#     producer.flush()
#     producer.close()
#     print("Kafka producer closed successfully.")


import json
import os
import time
import datetime
import requests
from kafka import KafkaProducer

# Configurer les paramètres
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
kafka_topic = os.getenv("KAFKA_TOPIC", "raw_pollution")
api_url = os.getenv("API_URL",
                    "https://data.angers.fr/api/explore/v2.1/catalog/datasets/dataairplqualiteairangers/records?select=date%2Cvaleur&where=commune_nom%3D%22Angers%22&limit=100")
#https://data.angers.fr/api/explore/v2.1/catalog/datasets/dataairplqualiteairangers/records?select=date%2Cvaleur&where=commune_nom%3D%22Angers%22&limit=1
#https://data.angers.fr/explore/dataset/dataairplqualiteairangers/api/?sort=date

def fetch_and_send_data(producer):
    print(f"Producteur Kafka connecté au topic '{kafka_topic}'...")
    try:
        # Récupérer les données de l'API
        response = requests.get(api_url)
        response.raise_for_status()
        # Adapter selon le format de réponse de l'API
        data = response.json()
        #timestamp
        data = response.json()  # Adapter selon le format de réponse de l'API
        #  data['timestamp']=datetime.datetime.now().ctime()
        del data['total_count']
        for entry in data['results']:
            producer.send(kafka_topic, entry)
            print(f"Data sent to Kafka: {entry}")

    except Exception as e:
        print(f"Error fetching or sending data: {e}")


if __name__ == "__main__":
    # Temporise pour Kafka
    print(f"Waiting...")
    time.sleep(15)
    # Initialiser le producteur Kafka
    producer = KafkaProducer(
        bootstrap_servers=kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print(f"Running data ingestion from Kafka")
    try:
        #while True:
        fetch_and_send_data(producer)
        #time.sleep(30)  # Intervalle entre les appels à l'API (60 secondes)
    except KeyboardInterrupt:
        print("Arrêt par l'utilisateur.")
    except Exception as e:
        print(f"Erreur fatale : {e}")
    finally:
        # Fermeture propre des connexions
        if producer in locals():
            producer.close()
        print("Fermeture des connexions.")