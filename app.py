
from flask import Flask, redirect, render_template, request, jsonify, session, url_for
from datetime import timedelta
import json
import os
import random

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"stars": 0, "badge_unlocked": False}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

PROGRESS_FILE = "progress.json"

def save_user_progress(user_id, data):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            all_progress = json.load(f)
    else:
        all_progress = {}

    all_progress[user_id] = data

    with open(PROGRESS_FILE, 'w') as f:
        json.dump(all_progress, f, indent=4)

def load_user_progress(user_id):
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            all_progress = json.load(f)
        return all_progress.get(user_id, {})
    return {}



app = Flask(__name__)
app.secret_key = 'supersecretkey'  
app.permanent_session_lifetime = timedelta(days=1)


@app.route("/quiz")
def quiz_redirect():
    return redirect(url_for("emotion_quiz"))
@app.route("/games/emotion-quiz")
def quiz_alias():
    return redirect(url_for("emotion_quiz"))


@app.route("/quiz/emotion")
def emotion_quiz():
    if "score" not in session:
        session["score"] = 0

    questions = [
        {
            "text": "Your friend gives you a surprise gift. How do you feel?",
            "image": "questions/happy_gift.png",
            "options": ["Sad", "Angry", "Happy", "Scared"],
            "answer": "Happy"
        },
        {
            "text": "You lost your toy at the park. How do you feel?",
            "image": "questions/lost_toy.png",
            "options": ["Excited", "Surprised", "Sad", "Happy"],
            "answer": "Sad"
        },
        {
            "text": "You are about to go on stage to perform. What might you feel?",
            "image": "questions/stage.png",
            "options": ["Scared", "Excited", "Sleepy", "Bored"],
            "answer": "Scared"
        }
    ]
    question = random.choice(questions)
    session["answer"] = question["answer"]
    return render_template("emotion_quiz.html", question=question, score=session["score"])

@app.route("/quiz/emotion/submit", methods=["POST"])
def emotion_submit():
    answer = request.form["answer"]
    if answer == session["answer"]:
        session["score"] += 1
        return redirect(url_for("emotion_quiz"))
    else:
        return redirect(url_for("emotion_quiz"))
    
@app.route("/quiz/emotion/results")
def emotion_results():
    return render_template("emotion_results.html", score=session["score"])
    
@app.route("/quiz/update-score")
def update_score():
    if "score" in session:
        session["score"] += 1
    else:
        session["score"] = 1

    # also update stars and progress
    session["stars"] = session.get("stars", 0) + 1
    session["last_activity"] = "Emotion Quiz"

    progress_data = {
        "last_activity": session["last_activity"],
        "quiz_score": session["score"],
        "stars": session["stars"],
        "badge_unlocked": session["stars"] >= 5
    }
    save_user_progress("child_1", progress_data)

    return ("", 204)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        # Save or send this info
        print(f"Feedback from {name}: {message}")
        return render_template("thank_you.html")

    return render_template("feedback.html")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/games/face-match")
def face_match():
    items = [
        {"image": "images/emotions/happy.png", "name": "Happy"},
        {"image": "images/emotions/sad.png", "name": "Sad"},
        {"image": "images/emotions/angry.png", "name": "Angry"},
        {"image": "images/emotions/surprised.png", "name": "Surprised"}
    ]
    images = random.sample(items, len(items))
    words = [item["name"] for item in images]
    random.shuffle(words)

    progress = load_progress()
    return render_template("face_match.html", images=images, words=words, badge=progress["badge_unlocked"])

@app.route("/update-face-match-score", methods=["POST"])
def update_face_score():
    progress = load_progress("child_1")
    progress["stars"] = progress.get("stars", 0) + 1

    if progress["stars"] >= 5:  
        progress["badge_unlocked"] = True

    save_progress("child_1", progress)

    return jsonify(progress)


@app.route("/activities")
def activities():
    return render_template("activities.html")

@app.route("/gesture")
def gesture():
    return render_template("gesture.html")

@app.route("/progress")
def progress():
    user_id = "child_1"
    user_data = load_user_progress(user_id)
    return render_template("progress.html", user=user_data)

@app.route("/detect_gesture", methods=["POST"])
def detect_gesture():
    
    return jsonify({"gesture": "Waving"})

@app.route("/games")
def games():
    return render_template("games.html")

@app.route("/games/color-match")
def color_match():
    colors = [
        {"name": "Red", "code": "#FF0000"},
        {"name": "Green", "code": "#00FF00"},
        {"name": "Blue", "code": "#0000FF"},
        {"name": "Yellow", "code": "#FFFF00"},
        {"name": "Purple", "code": "#800080"},
    ]

    target_color = random.choice(colors)
    options = random.sample(colors, 3)

    
    if target_color not in options:
        options[random.randint(0, 2)] = target_color

    return render_template("color_match.html", target=target_color, options=options)


@app.route("/games/matching")
def matching_game():
    return render_template("matching.html")

@app.route("/games/quiz")
def quiz_game():
    return render_template("quiz.html")

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    answers = request.json
    score = 0

    if answers.get("q1") == "Happy":
        score += 1
    if answers.get("q2") == "Hand":
        score += 1

    session['quiz_score'] = score
    session['stars'] = session.get('stars', 0)
    session['last_activity'] = "Quiz"

    if score == 2:
        session['stars'] += 1

    
    user_id = "child_1"
    progress_data = {
        "last_activity": session['last_activity'],
        "quiz_score": session['quiz_score'],
        "stars": session['stars']
    }

    save_user_progress(user_id, progress_data)

    return jsonify({"score": score})


@app.route("/matching_star", methods=["POST"])
def matching_star():
    session["last_activity"] = "Matching Game"
    session["stars"] = session.get("stars", 0) + 1

    progress_data = {
        "last_activity": session["last_activity"],
        "stars": session["stars"],
        "badge_unlocked": session["stars"] >= 5
    }
    save_user_progress("child_1", progress_data)

    return jsonify({"stars": session["stars"]})


if __name__ == "__main__":
    app.run(debug=True)
