import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

# ---------------------------------
# Logging setup
# ---------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ---------------------------------
# Event model
# ---------------------------------
@dataclass
class Event:
    event_type: str
    user: Optional[str] = None
    text: Optional[str] = None


# ---------------------------------
# Interactive client (terminal chat)
# ---------------------------------
class InteractiveClient:
    async def connect(self):
        logging.info("Chatbot started. Type 'exit' to quit.")

    async def disconnect(self):
        logging.info("Chatbot stopped.")

    async def send_message(self, message: str):
        print(f"Bot: {message}")

    async def receive(self) -> Event:
        user_input = await asyncio.to_thread(input, "You: ")
        return Event(
            event_type="message",
            user="You",
            text=user_input
        )


# ---------------------------------
# ChatBot logic
# ---------------------------------
class ChatBot:
    def __init__(self, client):
        self.client = client
        self.last_bot_question = None

    async def on_message(self, event: Event):
        text = event.text.lower().strip()

        greetings = {"hi", "hello", "hey"}
        positive_states = {
            "i'm good", "im good", "good",
            "fine", "okay", "ok", "great"
        }
        negative_states = {
            "not good", "bad", "sad",
            "tired", "upset"
        }

        # ---- Greetings ----
        if text in greetings:
            reply = "Hey! How are you doing today? 🙂"
            self.last_bot_question = "how_are_you"

        # ---- Reply to 'how are you' ----
        elif self.last_bot_question == "how_are_you" and text in positive_states:
            reply = "Nice! 😊 Anything interesting going on today?"
            self.last_bot_question = "follow_up"

        elif self.last_bot_question == "how_are_you" and text in negative_states:
            reply = "Oh, I’m sorry to hear that 😕 Want to talk about it?"
            self.last_bot_question = "support"

        # ---- Direct questions ----
        elif "how are you" in text:
            reply = "I’m doing great! Thanks for asking 😊 What about you?"
            self.last_bot_question = "how_are_you"

        elif "your name" in text:
            reply = "I’m your friendly Python chatbot 🤖"

        elif "what can you do" in text:
            reply = "I can chat with you and learn step by step 😄"

        # ---- Exit ----
        elif text in {"bye", "exit", "quit"}:
            reply = "Goodbye! It was nice talking to you 👋"
            await self.client.send_message(reply)
            raise KeyboardInterrupt

        # ---- Fallback ----
        else:
            reply = "Hmm 🤔 tell me more about that."

        await self.client.send_message(reply)

    async def run(self):
        await self.client.connect()
        try:
            while True:
                event = await self.client.receive()
                await self.on_message(event)
        except KeyboardInterrupt:
            pass
        finally:
            await self.client.disconnect()


# ---------------------------------
# Entry point (VERY IMPORTANT)
# ---------------------------------
async def main():
    client = InteractiveClient()
    bot = ChatBot(client)
    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())
