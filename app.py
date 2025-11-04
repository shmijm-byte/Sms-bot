from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Load your OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/sms", methods=["POST"])
def sms_reply():
    """Respond to incoming messages with AI-generated answers."""
    incoming_msg = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Hi! Please send me a message.")
        return str(resp)

    try:
        # Generate AI response
        ai_response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        reply = ai_response.choices[0].message.content.strip()
        msg.body(reply)
    except Exception as e:
        msg.body(f"Sorry, something went wrong: {e}")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
