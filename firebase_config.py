# firebase_config.py
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

def init_firebase():
    if not firebase_admin._apps:
        try:
            # 🔐 1. Utilisation de Streamlit secrets s'ils existent
            if "FIREBASE" in st.secrets:
                cred = credentials.Certificate(st.secrets["FIREBASE"])

            # 🌍 2. Sinon, via variable d'environnement
            elif "FIREBASE_KEY_JSON" in os.environ:
                key_dict = json.loads(os.environ["FIREBASE_KEY_JSON"])
                cred = credentials.Certificate(key_dict)

            # 📄 3. Sinon, fichier local
            else:
                cred_path = os.getenv("FIREBASE_KEY_PATH", "serviceAccountKey.json")
                cred = credentials.Certificate(cred_path)

            firebase_admin.initialize_app(cred)

        except Exception as e:
            st.warning(f"❌ Échec de l'initialisation Firebase : {e}")

def get_firestore():
    init_firebase()
    return firestore.client()
