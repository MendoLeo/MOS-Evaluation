import firebase_admin
from firebase_admin import credentials, firestore
import csv

# Initialise l'app Firebase
cred = credentials.Certificate("/home/mendo/Downloads/LM/LM-5/MOS/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Remplace 'ta_collection' par le nom de ta collection
docs = db.collection("evaluations").stream()

# Convertir en CSV
with open("export.csv", "w", newline="") as file:
    writer = None
    for doc in docs:
        data = doc.to_dict()
        if writer is None:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
        writer.writerow(data)
