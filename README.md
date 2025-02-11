# **MindPen** 📝💡  
#### AI-powered journaling with speech recognition & sentiment analysis  

![Sign-in Page](https://www.dropbox.com/scl/fi/cco6dfmo1c1cfgsor6t6s/Sign-in.png?rlkey=bw7nzhng97g76tpc5c4jh94we&st=8gdl4jyu&raw=1)

![MindPen Screenshot](https://www.dropbox.com/scl/fi/d8whembiyo4kxkrf3icbx/Dashboard.png?rlkey=a5913z1z1lw64bghhyhrnepxt&st=yiidxtb9&raw=1)  

![MindPen Screenshot](https://www.dropbox.com/scl/fi/yfurgiczidd3792d29vxg/All_Journals.png?rlkey=xbjvm812d661ooit15cchpssh&st=k3x97r8i&raw=1) 
![MindPen Screenshot](https://www.dropbox.com/scl/fi/vi82jhnijahlyi4guvu2z/Mood.png?rlkey=xmci86judicabxvdw09u99ls2&st=281snnz8&raw=1)  
![MindPen Screenshot](https://www.dropbox.com/scl/fi/wpgkei25i7ov0ecwwtp5v/Mood-History.png?rlkey=hdhfldg1morcwpaqlywtw4knm&st=7pm19ylq&raw=1)  
 

## **📌 Overview**  
**MindPen** is an AI-driven journaling web application designed to enhance the journaling habit by integrating:  

✅ **Speech-to-text transcription** using Deepgram.

✅ **Sentiment analysis** for mood detection.  

✅ **Journaling Habit tracking** to encourage consistency.  

✅ **Graphical mood trend visualizations** to monitor emotional patterns.  

✅ **WebSockets support** for real-time interaction.  

This project builds upon the ideas of **PenMind**, with an emphasis on automating journaling and mood tracking through AI & NLP integration.  

---

## **🚀 Features**  
✔ **Voice Journaling**  with live transcription

✔ **Mood Analysis** positive, neutral, and negative

✔ **Text Journaling & SVM** for fallback mechanism
 
✔ **Journaling Habit Tracking** Visualize journaling frequency to stay motivated  

✔ **Real-Time WebSockets** supports asynchronous communication
 
 

---

## **⚡ Tech Stack**  
- **Backend:** Django, Django Channels  
- **Frontend:** Bootstrap  
- **AI Models:** Deepgram API, Scikit-learn (SVM fallback)  
- **Database:** SQLite (for testing) 
- **WebSockets:** ASGI, Daphne  


---

## **🛠 Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/Slim-Mejdoub/MindPen.git
cd MindPen
```

### **2️⃣ Create a Virtual Environment** 
```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate  # For Windows
```
### **3️⃣ Install Dependencies** 
```bash
pip install -r requirements.txt
```

### **4️⃣ Get Your Deepgram API Key 🔑 (optionally)** 
- Go to Deepgram Console → https://console.deepgram.com/signup
- Sign up (if you don’t have an account)
- Generate an API Key (**$200 free** credit for new users!)
- Keep this API Key secure 
- Alternatively, setup GCP service account and set path as env var `GOOGLE_CLOUD_CREDENTIALS_FILE`

### **5️⃣ Create a `.env` file in the **MindPen root directory** and add:** 
```bash
DEEPGRAM_API_KEY=your_deepgram_api_key
```

or 

```bash
GOOGLE_CLOUD_CREDENTIALS_FILE=/path/to/file/credentials.json
```

### **6️⃣ Apply Migrations & Run the Server** 
```bash
python manage.py makemigrations
python manage.py migrate
```

### **7️⃣  Run the Server** 
Since **MindPen** uses WebSockets, Daphne must be used instead of runserver!
```bash
daphne -b 127.0.0.1 -p 8000 Journaling_web_app.asgi:application
```

### **🧪 Running Tests** 
To run all test cases:
```bash
python manage.py test
```

