from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------------------
# Context Memory (per session)
# ------------------------------
context = {
    "last_question": None,
    "mood": None,
    "topic": None
}

def chatbot_reply(user_text):
    text = user_text.lower().strip()

    greetings = {"hi", "hello", "hey"}
    positive_states = {"good", "fine", "okay", "ok", "great", "happy"}
    negative_states = {
        "sad", "bad", "tired", "upset", "stressed",
        "anxious", "lonely", "confused", "lost"
    }

    # ------------------------------
    # Greetings
    # ------------------------------
    if text in greetings:
        context["last_question"] = "mood"
        return "Hey! 👋 How are you feeling today?"

    # ------------------------------
    # Mood Handling
    # ------------------------------
    if context["last_question"] == "mood":
        if any(word in text for word in positive_states):
            context["mood"] = "positive"
            context["last_question"] = "topic"
            return (
                "Nice 😄 What would you like to talk about today?\n"
                "Tech, studies, career, or just life?"
            )
        if any(word in text for word in negative_states):
            context["mood"] = "negative"
            context["topic"] = "life"
            context["last_question"] = None
            return (
                "That sounds heavy 😔\n"
                "Do you want to talk about what’s been bothering you?"
            )

    # ------------------------------
    # Life / Emotional Talk
    # ------------------------------
    if any(word in text for word in ["stress", "stressed", "pressure"]):
        context["topic"] = "life"
        return (
            "Pressure can really drain you 😕\n"
            "Is it college, family expectations, or something personal?"
        )

    if any(word in text for word in ["sad", "lonely", "lost", "confused"]):
        context["topic"] = "life"
        return (
            "I’m really glad you shared that 💙\n"
            "What’s been weighing on your mind lately?"
        )

    if context["topic"] == "life" and "college" in text:
        return (
            "College life can be overwhelming 😓\n"
            "Is it studies, comparison with others, or future tension?"
        )

    if context["topic"] == "life" and "future" in text:
        return (
            "Thinking about the future can feel scary sometimes 🌱\n"
            "Are you worried about career, direction, or confidence?"
        )

    if context["topic"] == "life" and "relationship" in text:
        return (
            "Relationships can be complicated 💔\n"
            "Do you want advice, or just someone to listen?"
        )

    # ------------------------------
    # Topic Detection
    # ------------------------------
    if any(word in text for word in ["python", "coding", "ai", "ml"]):
        context["topic"] = "tech"
        return (
            "Nice 💻 Are you learning this for college, projects, "
            "or interview preparation?"
        )
    if context["topic"] == "tech" and "college" in text:
        return (
            "Great continue learning, take classes on time.\n"
            "Do you want advice, or just a motivation?"
        )
    if context["topic"] == "tech" and "projects" in text:
        return (
            "Great continue learning, take classes on time.\n"
            "Do you want advice, or any roadmap for the project?"
        )
    if context["topic"] == "tech" and "interview" in text:
        return (
            "Great continue learning, take classes on time.\n"
            "Do you want advice for your interview?"
        )

    if any(word in text for word in ["exam", "study", "syllabus"]):
        context["topic"] = "study"
        return "Got it 📚 Which subject are you preparing for right now?"

    if any(word in text for word in ["job", "resume", "career"]):
        context["topic"] = "career"
        return (
            "Career stress is real 😬\n"
            "Are you aiming for placements, internships, or skill building?"
        )
    if context["topic"] == "career" and "placements" in text:
        return (
            "Great trust youself , you can crack the college placements.\n"
            "Do you want advice? "
        )
    if context["topic"] == "career" and "internships" in text:
        return (
            "Great trust youself , you can crack the internships.\n"
            "Do you want advice? "
        )
    if context["topic"] == "career" and "skill" in text:
        return (
            "Great continue learning new skills and sharpening your skills .\n"
            "Do you want advice? "
        )

    # ------------------------------
    # Common Questions
    # ------------------------------
    if "how are you" in text:
        return "I’m doing good 😊 Thanks for asking. How are you holding up?"

    if "your name" in text:
        return "I’m your friendly Flask chatbot 🤖 Always here to listen."

    if "what can you do" in text:
        return (
            "I can chat with you, listen when you’re low, help with studies, "
            "tech doubts, career talks, or just be here with you 🙂"
        )

    # ------------------------------
    # Exit
    # ------------------------------
    if text in {"bye", "exit", "quit"}:
        return "Goodbye 👋 Take care of yourself, okay?"

    # ------------------------------
    # Smart Fallback
    # ------------------------------
    return (
        "I’m listening 🤍\n"
        "Tell me a bit more about what you’re thinking."
    )

# ------------------------------
# Flask Routes
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.form["message"]
    reply = chatbot_reply(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
