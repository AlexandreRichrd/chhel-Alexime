# Utilise une image de base Python
FROM python:3.8-slim

# Crée un répertoire de travail
WORKDIR /app

# Copie le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt /app/requirements.txt

# Installe les dépendances à partir de requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie ton script Python dans le conteneur
COPY consumer.py /app/consumer.py

# Exécute le script quand le container démarre
CMD ["python", "consumer.py"]
