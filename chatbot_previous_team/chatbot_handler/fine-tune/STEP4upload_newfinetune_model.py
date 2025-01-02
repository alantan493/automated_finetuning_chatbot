import time
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Open the JSONL file and upload it for fine-tuning
with open("/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/fine-tuning.jsonl", "rb") as file:
    response = client.files.create(file=file, purpose="fine-tune")

# Retrieve and print the file ID
file_id = response.id
print(f"File uploaded successfully with ID: {file_id}")

# Create a fine-tuning job through OpenAI finetuning API
fine_tune_response = client.fine_tuning.jobs.create(
    training_file=file_id,  # Put in the file ID created previously
    model="gpt-4o-mini-2024-07-18"  # Put in the OpenAI LLM model that we are using
)

# Print the fine-tuning job response
print(f"Fine-tuning job created successfully: {fine_tune_response}")

# Retrieve the job ID
fine_tune_job_id = fine_tune_response.id

# Define the full file path for the finetuningmodel.txt file in the VM
file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetuningmodel.txt"

# Polling to check the status of the fine-tuning job until it's completed
while True:
    fine_tune_job = client.fine_tuning.jobs.retrieve(fine_tune_job_id)
    
    # Check if the job is completed
    if fine_tune_job.status == "succeeded":
        print(f"Fine-tuning completed successfully. Fine-tuned model ID: {fine_tune_job.fine_tuned_model}")
        
        # Write the fine-tuned model ID to the specified file path
        with open(file_path, "w") as file:
            file.write(f"Fine-tuned model ID: {fine_tune_job.fine_tuned_model}\n")
        
        print(f"Fine-tuned model ID saved to {file_path}")
        break
    elif fine_tune_job.status == "failed":
        print("Fine-tuning job failed.")
        break
    else:
        print(f"Fine-tuning job status: {fine_tune_job.status}. Waiting...")
    
    # Wait for a while before checking the status again
    time.sleep(30)  # Check every 30 seconds
