# 🧠 Fake Ad Detector - Browser Extension

This project is a **real-time fake ad detection system** that scans webpage content and flags suspicious ads based on language patterns, exaggeration, and credibility.

It uses **Cohere’s Command-R Large Language Model** for classification and integrates **Google’s Fact Check API** to verify questionable claims. Users instantly see whether ad content is Safe, Exaggerated, or Misleading — right in the browser.

---

## 🔍 Why This Project?

Online ads often make unrealistic claims: “Lose 10 kg in 3 days!” or “Doctors hate this simple trick.”  
This extension helps users avoid misinformation by analyzing ad text and displaying trust scores and factual sources, if available.

---

## 🚀 Features

- ✅ Detects ads with suspicious or exaggerated claims
- 🧠 Uses LLM (Cohere Command-R) to classify ads as:
  - Safe
  - Exaggerated
  - Misleading
- 🟢 Color-coded ad borders and tooltips for instant feedback
- 🔐 Displays trust score (0–100)
- 🔗 Checks Google Fact Check API for credible sources
- 🌐 Built as a browser extension (content script)
- 🗃️ Logs each analysis result to the backend database

---

## 🧩 Tech Stack

| Component      | Technology                     |
|----------------|------------------------------  |
| Frontend       | JavaScript (Browser Extension) |
| Backend        | Python (Flask)                 |
| AI/LLM         | Cohere Command-R               |
| Verification   | Google Fact Check API          |
| DB Logging     | Python `log_result()` function |
| CORS/Requests  | Flask-CORS, dotenv, requests   |

---

## 🛠️ Installation & Setup

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/Fake-Ad-Detector.git
cd Fake-Ad-Detector
```

### 2. Backend Setup (Flask):
- Create a `.env` file with:
  ```
  COHERE_API_KEY=your-cohere-key
  GOOGLE_FACT_CHECK_API_KEY=your-google-fact-check-api-key
  ```
- Install dependencies:
  ```bash
  pip install flask flask-cors python-dotenv cohere beautifulsoup4 requests
  ```
- Run the server:
  ```bash
  python app.py
  ```

### 3. Load the Extension:
- Go to `chrome://extensions/` (Developer Mode ON)
- Click **Load Unpacked** and select the extension folder

---

## 📊 Performance

- Handles 20–30 ad segments per page
- Average analysis time: a few seconds
- Backend hosted locally (can be deployed on Heroku/Render)

---

## 📌 Future Enhancements

- Host as a public Chrome extension
- Admin dashboard for ad stats
- User feedback for model fine-tuning
- Multilingual ad detection
- Support for video ad description analysis

---

## 📎 Links

- **Demo Video:** [Demo Link](#)
- **Prototype PPT:** [Submission Slides](#)
- **Hosted Backend:** `http://localhost:5000/analyze`

---

## 🧑‍💻 License

License © 2025 CacheMeOutside
