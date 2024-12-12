from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from the .env file or environment
api_key = os.getenv('OPENAI_API_KEY')

bot_name = "Chatbot"

# Ensure that the API key is correctly loaded
if not api_key:
    raise ValueError("API key is not set. Please set OPENAI_API_KEY in your .env file or environment.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Track the last modification time of the finetuningmodel.txt file
# /home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt
# C:/Users/alant/OneDrive/Documents/VisualStudios/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt
finetune_file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt"
last_modified = os.path.getmtime(finetune_file_path)

def get_finetuned_model_id():
    global last_modified
    try:
        # Monitor if the file has been updated
        current_modified = os.path.getmtime(finetune_file_path)
        if current_modified != last_modified:
            print(f"File {finetune_file_path} has been modified, reloading model ID.")
            last_modified = current_modified

        # Extract the model ID from the text file
        with open(finetune_file_path, "r") as file:
            first_line = file.readline().strip()
            model_id = first_line.split(": ")[1]  # Extract the model ID by splitting the line
            return model_id
    except Exception as e:
        print(f"An error occurred while retrieving the model ID: {e}")
        return None

def ask_finetuned_model(prompt, system_prompt):
    model_id = get_finetuned_model_id()

    if not model_id:
        print("No valid model ID found. Please ensure the finetuningmodel.txt file exists.")
        return None

    try:
        # Make an API call to the fine-tuned model with a system message introduction
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return the chatbot's response
        chat_response = response.choices[0].message.content
        return chat_response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    system_prompt = "Hello! I'm here to help you learn more about the dangers of drugs and vaping..."
    print(f"Chatbot: {system_prompt}")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chatbot.")
            break

        response = ask_finetuned_model(user_input, system_prompt)
        if response:
            print(f"Chatbot: {response}")
