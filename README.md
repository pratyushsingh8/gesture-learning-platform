# GesturePlay 🎓✋

A gesture-based interactive learning platform designed for children with autism. Built with AI-powered gesture recognition and engaging learning modules to support visual and behavioral learning.

---

## 📌 Project Overview

**GesturePlay** uses real-time hand gesture recognition to help children with autism engage in learning activities like:
- **Gesture Imitation**
- **Emotion Quiz**
- **Face Matching**
- **Progress Tracking**

The platform leverages **MediaPipe**, **OpenCV**, and **Flask** for a responsive backend and gesture-based interactions.

---

## 🧠 Key Features

- ✋ **Hand Gesture Detection** with Mediapipe
- 📷 **Camera Input** via OpenCV
- 🧠 **AI-powered learning modules**
- 📈 **Progress tracker** to monitor improvements
- 🎮 Simple and child-friendly UI
- 🖥️ Web-based platform using Flask + HTML/CSS/JS

---

## 🧱 Tech Stack

| Component         | Technology       |
|------------------|------------------|
| Backend           | Python, Flask     |
| Frontend          | HTML, CSS, JavaScript |
| AI / ML Libraries | MediaPipe, OpenCV |
| Others            | NumPy, Matplotlib, Git |

---

## 🛠️ How to Run Locally

 **Clone this repo**  
```bash
git clone https://github.com/your-username/GesturePlay.git
cd GesturePlay
python -m venv venv                     # Create a virtual environment
source venv/bin/activate                # for Linux/Mac
venv\Scripts\activate                   # for Windows
pip install -r requirements.txt         # Install dependencies
python app.py                           # Run the app

GesturePlay/
├── app.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── modules/
│   ├── gesture_recognition.py
│   ├── emotion_quiz.py
│   └── face_matcher.py
├── requirements.txt
└── README.md

🧑‍💻 Contributors
Pratyush Kumar Singh
Prattoy Dey