import streamlit as st
import os
import pandas as pd
from datetime import datetime
import random

from firebase_config import get_firestore

# === CONFIGURATION ===
AUDIO_DIR = "audios"
CSV_FILE = "evaluations.csv"

# === FIREBASE INIT ===
try:
    db = get_firestore()
except Exception as e:
    st.warning(f"⚠️ Firebase non disponible : {e}")
    db = None


# === EN-TÊTE D'INFORMATION ===
st.markdown("""
## 🎯 Objectif de l'évaluation MOS

Bienvenue dans cette interface d’évaluation de la qualité audio par **MOS (Mean Opinion Score)**.

Chaque extrait audio doit être évalué selon **votre perception subjective de sa qualité sonore** globale, indépendamment du contenu linguistique.

**Critères à considérer** :
- Clarté du son
- Absence de bruit de fond
- Fluidité et naturel de la voix
- Intelligibilité

**Échelle de notation (1 à 5)** :
- **1** : Très mauvaise qualité (inintelligible, bruits forts)
- **2** : Mauvaise qualité
- **3** : Moyenne (compréhensible mais peu naturelle)
- **4** : Bonne qualité
- **5** : Excellente qualité (naturelle, fluide, sans artefact)

Merci pour votre contribution à cette évaluation participative !
""")


# === CHOIX DE LA LANGUE ===
langues_disponibles = sorted(os.listdir(AUDIO_DIR))
langue = st.selectbox("🗣️ Choisissez une langue à évaluer :", langues_disponibles)

if langue:
    st.markdown(f"### 📑 Évaluation des extraits en **{langue.capitalize()}**")

    # Initialisation et randomisation une seule fois
    if "extraits_randomises" not in st.session_state or st.session_state.get("langue_active") != langue:
        audio_paths = {
            "in_domain": os.path.join(AUDIO_DIR, langue, "in_domain"),
            "out_of_domain": os.path.join(AUDIO_DIR, langue, "out_of_domain")
        }

        extraits = []
        for domaine, path in audio_paths.items():
            if os.path.exists(path):
                fichiers = [f for f in os.listdir(path) if f.endswith((".mp3", ".wav"))]
                for f in fichiers:
                    extraits.append({
                        "fichier": f,
                        "path": os.path.join(path, f),
                        "domaine": domaine
                    })

        random.shuffle(extraits)
        st.session_state.extraits_randomises = extraits
        st.session_state.langue_active = langue

    # Récupérer les extraits déjà randomisés
    extraits = st.session_state.extraits_randomises

    for idx, extrait in enumerate(extraits):
        st.markdown(f"---\n### 🎧 Extrait {idx + 1}")
        st.audio(extrait["path"])

        note = st.slider(
            "Évaluez cet extrait (1 = Très mauvais, 5 = Excellent)",
            min_value=1,
            max_value=5,
            step=1,
            key=f"slider_{extrait['fichier']}"
        )

        if st.button(f"✅ Enregistrer la note pour l'extrait {idx + 1}", key=f"save_{extrait['fichier']}"):
            data = {
                "timestamp": datetime.now().isoformat(),
                "langue": langue,
                "extrait": extrait["fichier"],
                "domaine": extrait["domaine"],
                "note": note,
            }

            # 🔹 Enregistrement dans le CSV local
            df = pd.DataFrame([data])
            if os.path.exists(CSV_FILE):
                df.to_csv(CSV_FILE, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_FILE, index=False)

            # 🔹 Enregistrement dans Firestore
            if db:
                try:
                    db.collection("evaluations").add(data)
                except Exception as e:
                    st.warning(f"⚠️ Échec de l’enregistrement dans Firebase : {e}")

            st.success(f"✅ Évaluation enregistrée pour l'extrait {idx + 1}")

    # === TÉLÉCHARGEMENT DU CSV ===
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "rb") as f:
            st.download_button("⬇️ Télécharger les résultats", f, file_name="resultats.csv", mime="text/csv")
