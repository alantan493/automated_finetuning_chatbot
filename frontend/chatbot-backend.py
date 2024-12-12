import os
import json
import sys
import time
import logging
import openai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from werkzeug.serving import make_server
from threading import Thread

# Import the chatbot functions from chat.py
from chat import ask_finetuned_model

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://httpsee3180-smapps2webappchatbot.com"])

# Setup logging
logging.basicConfig(level=logging.INFO)

# Path to the finetuningmodel.txt file (ensure this path is correct)
# C:/Users/alant/OneDrive/Documents/VisualStudios/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt"
# /home/alant/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt
finetune_file_path = "/home/alant/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt"

# Initialize last_modified with the current modification time of the finetuningmodel.txt file
try:
    last_modified = os.path.getmtime(finetune_file_path)
except FileNotFoundError as e:
    logging.error(f"File not found: {finetune_file_path}. Error: {e}")
    last_modified = None  # Initialize as None in case the file doesn't exist

# Debounce parameters to avoid multiple restarts in a short time
debounce_time = 30  # Time in seconds to wait before allowing another restart
last_restart_time = time.time()

# Error handling for routes that don't exist
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    logging.error(f"HTTPException: {e}")
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

# Route to render the frontend (base.html)
@app.route("/")
def index():
    return render_template("base.html")

# A POST route to /chatbot/send. It will take in a JSON request body and send it to the chatbot model.
@app.route("/chatbot/send", methods=["POST"])
def send_chatbot():
    try:
        # Get value from request body. Only accept 'message'
        request_data = request.get_json()
        logging.info(f"Request Data: {request_data}")

        if 'message' not in request_data:
            logging.warning("Bad Request: 'message' key not found in request data")
            return {"message": "Bad Request"}, 400
        
        # System prompt for the chatbot
        system_prompt = "Hello! I'm here to help you learn more about the dangers of drugs and vaping..."
        
        logging.info(f"Sending prompt to model: {system_prompt}, user input: {request_data['message']}")
        
        # Call the chatbot function from chat.py
        response = ask_finetuned_model(request_data["message"], system_prompt)
        
        logging.info(f"Chatbot Response: {response}")

        if not response:
            response_message = "No response from the chatbot"
        else:
            response_message = response

        return {"message": response_message}, 200

    except openai.AuthenticationError:
        logging.error("OpenAI Authentication Error")
        return {"error": {"message": "Incorrect API key provided"}}, 401
    except Exception as e:
        # Log any other exceptions
        logging.error(f"Exception occurred: {e}")
        return {"error": {"message": "Internal Server Error"}}, 500

# Server control for Flask
class ServerControl(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.srv = make_server('0.0.0.0', 80, app)  # Set to port 80
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logging.info("Starting Flask server on port 80...")
        self.srv.serve_forever()

    def shutdown(self):
        logging.info("Shutting down the server...")
        self.srv.shutdown()

server_control = None

# Function to monitor the finetuningmodel.txt file for changes and restart the app
def monitor_file_change():
    global last_modified, last_restart_time
    while True:
        try:
            # Check if the file has been modified
            current_modified = os.path.getmtime(finetune_file_path)
            if current_modified != last_modified:
                # Check if debounce time has passed since the last restart
                if time.time() - last_restart_time > debounce_time:
                    logging.info(f"{finetune_file_path} has been updated. Shutting down for restart.")
                    last_modified = current_modified  # Update the last modified time
                    last_restart_time = time.time()  # Update the restart time
                    
                    # Shutdown the server and exit
                    sys.exit(0)

            time.sleep(10)  # Check every 10 seconds
        except Exception as e:
            logging.error(f"Error monitoring file: {e}")
            time.sleep(10)

# Ensure the app listens on port 80
if __name__ == "__main__":
    # Start monitoring the file in a separate thread
    monitor_thread = Thread(target=monitor_file_change, daemon=True)
    monitor_thread.start()

    # Start the Flask server in a separate thread
    server_control = ServerControl(app)
    server_control.start()


