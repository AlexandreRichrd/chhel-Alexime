import requests

url = "https://data.angers.fr/api/explore/v2.1/catalog/datasets/indice-de-qualite-de-lair-angers-loire-metropole/records"

# Paramètres pour inclure uniquement 'valeur' et 'date_ech'
params = {
    "fields": "valeur,date_ech",  # Champs désirés
    "limit": 10,                 # Nombre maximum de résultats
    "offset": 0,                 # Point de départ des résultats
    "timezone": "UTC"            # Fuseau horaire
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for record in data.get('results', []):
        date_ech = record.get('date_ech', 'No date provided')
        valeur = record.get('valeur', 'No value provided')
        print(f"----------{date_ech}-----------")
        print(f"Valeur: {valeur}\n\n")
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
