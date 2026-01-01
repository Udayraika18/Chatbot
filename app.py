from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

last_bot_question = None

def chatbot_reply(user_text):
    global last_bot_question
    text = user_text.lower().strip()

    greetings = {"hi", "hello", "hey"}
    positive_states = {"i'm good", "im good", "good", "fine", "ok", "okay", "great"}
    negative_states = {"not good", "bad", "sad", "tired", "upset"}

    if text in greetings:
        last_bot_question = "how_are_you"
        return "Hey! How are you doing today? 🙂"

    elif last_bot_question == "how_are_you" and text in positive_states:
        last_bot_question = "follow_up"
        return "Nice! 😊 Anything interesting going on today?"

    elif last_bot_question == "how_are_you" and text in negative_states:
        last_bot_question = "support"
        return "Oh, I’m sorry to hear that 😕 Want to talk about it?"

    elif "how are you" in text:
        last_bot_question = "how_are_you"
        return "I’m doing great! Thanks for asking 😊 What about you?"

    elif "your name" in text:
        return "I’m your friendly Python chatbot 🤖"

    elif "what can you do" in text:
        return "I can chat with you and learn step by step 😄"

    elif text in {"bye", "exit", "quit"}:
        return "Goodbye! It was nice talking to you 👋"

    else:
        return "Hmm 🤔 tell me more about that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.form["message"]
    bot_msg = chatbot_reply(user_msg)
    return jsonify({"reply": bot_msg})

if __name__ == "__main__":
    app.run(debug=True)
