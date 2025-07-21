from flask import Flask, render_template, request, jsonify
import random
import spacy
import re
import datetime
import os
import math
app = Flask(__name__)

nlp = spacy.load("en_core_web_sm")

responses = {
    "greeting": ["Hello!", "Hi there!", "Hey!", "How can I help you today?"],
    "goodbye": ["Goodbye!", "See you later!", "Bye!", "Catch you next time!"],
    "thanks": ["You're welcome!", "Glad to help!", "No worries!"],
    "name": ["I'm ChatBuddy, your assistant.", "They call me ChatBuddy."],
    "creator": ["I was created by a developer who loves Python!", "I'm the result of someone's caffeine-fueled coding!"],
    "real": ["I'm virtual, but my answers are real!", "I'm as real as your imagination 😉"],
    "age": ["I was born the moment you ran this code!", "I'm timeless, unlike humans!"],
    "ai": ["AI stands for Artificial Intelligence — machines that can mimic human thinking.", "Artificial Intelligence helps machines learn and make decisions."],
    "laughter": ["😂 Glad you liked it!", "Haha!", "I'm happy to make you laugh!"],
    "time": [datetime.datetime.now().strftime("The time is %H:%M.")],
    "date": [datetime.datetime.now().strftime("Today's date is %d %B %Y.")],
    "joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the computer go to therapy? It had too many bytes of sadness.",
        "I told my computer I needed a break, and it said: 'Why? I just rebooted!'"
    ],
    "help": [
        "I can tell you jokes, solve math problems, tell the date and time, and chat with you!",
        "Try asking me to calculate something or tell you a joke.",
    ],
    "how_are_you": [
        "I'm just code, but thanks for asking! I'm running smoothly.",
        "Doing great! Ready to help you with anything you need."
    ],
    "fun_fact": [
        "Did you know? The Eiffel Tower can grow over 6 inches in summer due to heat!",
        "Octopuses have three hearts. And all of them might love you!",
        "Bananas are berries, but strawberries aren't. Wild, right?"
    ]
}

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)

def detect_intent(user_input):
    cleaned = preprocess_text(user_input)

    if any(word in cleaned for word in ["hi", "hello", "hey"]):
        return "greeting"
    elif "thank" in cleaned:
        return "thanks"
    elif any(word in cleaned for word in ["bye", "goodbye", "exit"]):
        return "goodbye"
    elif "your name" in user_input or "who are you" in user_input:
        return "name"
    elif "who made you" in cleaned or "who create" in cleaned:
        return "creator"
    elif "real" in cleaned:
        return "real"
    elif "old are you" in cleaned or "your age" in cleaned:
        return "age"
    elif "what is ai" in cleaned or "define ai" in cleaned:
        return "ai"
    elif re.search(r'[\d\+\-\*/\(\)]', user_input):
        return "math"
    elif "time" in cleaned:
        return "time"
    elif "date" in cleaned or "today" in cleaned:
        return "date"
    elif "joke" in cleaned or "funny" in cleaned:
        return "joke"
    elif "haha" in cleaned or "lol" in cleaned or "lmao" in cleaned:
        return "laughter"
    elif "help" in cleaned or "what can you do" in cleaned:
        return "help"
    elif "how be" in cleaned or "how go" in cleaned:
        return "how_are_you"
    elif "fun fact" in user_input or "interesting" in cleaned:
        return "fun_fact"
    else:
        return "unknown"


def solve_math(expression):
    try:
        if not re.match(r'^[\d\s\+\-\*/\(\)\.\,a-zA-Z_]+$', expression):
            return "Invalid characters in expression."
        allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        allowed_names.update({"abs": abs, "round": round})
        result = eval(expression, {"__builtins__": None}, allowed_names)
        return f"The answer is {result}."
    except Exception as e:
        return f"Sorry, I couldn't calculate that. Error: {str(e)}"

@app.route("/")
def home():
    return render_template(r"chat.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_input = request.form["msg"]
    intent = detect_intent(user_input)

    if intent == "math":
        bot_response = solve_math(user_input)
    elif intent in responses:
        bot_response = random.choice(responses[intent])
    else:
        bot_response = "I'm not sure how to respond to that. Try asking me a math question or say hi!"

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
