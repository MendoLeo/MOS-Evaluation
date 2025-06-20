# 🔊 MOS Evaluation Web App

## 🧽 Introduction & Motivation

This project is a web-based application designed to simplify **MOS (Mean Opinion Score)** evaluations for speech and audio samples.
Most existing evaluation platforms rely heavily on text forms. Very few embed audio players directly into the evaluation interface. At best, evaluators are redirected to **external video or audio links**, which significantly degrades the user experience.

**This app solves that problem** by providing a clean, audio-first interface that allows evaluators to play samples and rate them on a 1–5 scale, all within a single page — no external links or distractions..

---

## 🖼️ Interface

* Audio samples are displayed in a list with individual audio players.
* Evaluators rate each sample using a 1–5 MOS scoring system.
* A submit button saves the ratings to a connected database.
* Mobile-friendly and responsive design.

---

## ✨ Features

* 🎷 **Inline audio playback** for seamless evaluation
* ✅ **1–5 MOS rating** for each sample
* ☁️ **Firebase integration** for real-time data storage
* 🧪 **Minimal setup**, fully built with [Streamlit](https://streamlit.io/)
* 📄 Easily deployable on **Streamlit Cloud**
* 🔐 Secure data handling via `.streamlit/secrets.toml`

---

## 🔧 Use Cases

### 🔍 Local Usage (Offline Testing)

1. Clone the repository:

   ```bash
   git clone https://github.com/MendoLeo/MOS-Evaluation.git
   cd MOS-Evaluation
   ```

2. **Disable Firebase (Optional):**
   If you're testing locally, you can skip Firebase configuration.
   After each evaluation, a local CSV file will be created to store results.

3. Run the app:

   ```bash
   streamlit run app.py
   ```

---

### ☁️ Online Usage (Streamlit Cloud Deployment)

To use the app online and collect evaluations in real-time:

1. **Create a Firebase Project**

   * Go to [Firebase Console](https://console.firebase.google.com)
   * Create a new project and enable Firestore or Realtime Database
   * Under Project Settings > General, register a Web App
   * Copy the generated Firebase config object

2. **Configure Streamlit Secrets**
   Create a file at `.streamlit/secrets.toml` with the following content:

   ```toml
   [firebase]
   apiKey = "YOUR_API_KEY"
   authDomain = "YOUR_PROJECT.firebaseapp.com"
   databaseURL = "https://YOUR_PROJECT.firebaseio.com"
   projectId = "YOUR_PROJECT_ID"
   storageBucket = "YOUR_PROJECT.appspot.com"
   messagingSenderId = "YOUR_SENDER_ID"
   appId = "YOUR_APP_ID"
   ```

3. **Push to GitHub**

4. **Deploy on Streamlit Cloud**
   Follow the [Streamlit Cloud Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app) to launch your app online.
   You’ll get a public link like:

   ```
   https://your-username-your-repo.streamlit.app
   ```

5. **Fetching Evaluation Results**
   To retrieve the evaluation data stored in Firebase, run the `getdata.py` script locally:

   ```bash
   python getdata.py
   ```
   ### **csv informations**
  
| evaluate record           | timestamp                  | note | language | domaine|
|-------------------|----------------------------|------|--------|-----------------|
| 1JN_001_002.wav   | 2025-04-30T16:36:13.950968 | 2    | bafia  | in_domain       |
| 1JN_001_003.wav   | 2025-04-30T16:34:18.114201 | 2    | bafia  | in_domain       |
| LUK_001_002.wav   | 2025-04-30T11:44:59.781822 | 3    | bulu   | out_of_domain   |


---

## ✅ Conclusion

This app simplifies perceptual audio evaluation for tasks like voice synthesis, speech enhancement, and TTS benchmarking. It focuses on enhancing the evaluator's experience by providing a smooth and integrated audio interface.

Feel free to fork, adapt, or contribute to improve the tool further!

---

## 📄 License

MIT License
