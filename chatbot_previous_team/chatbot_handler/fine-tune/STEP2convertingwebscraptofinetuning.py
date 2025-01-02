import os
import json
from dotenv import load_dotenv

# Define a consistent system message
system_message = {
    "role": "system",
    "content": ("You are a helpful assistant. You are tasked with answering questions provided by the user. The user is a University Student keen on learning more about the dangers of drugs and vaping. Your objective is to be informative about these topics and discourage the user on trying drugs or vaping.")
}

# A function to generate user and assistant conversation from articles, with different prompts for each file
def generate_conversation(article, file_type, prompt_version=1):
    user_content = None  # Initialize user_content with a default value

    # Handle articles with "headline" (main file)
    if "headline" in article:
        if file_type == "main":
            if prompt_version == 1:
                user_content = f"What are the recent updates about '{article['headline']}'? Can you give me more details?"
            elif prompt_version == 2:
                user_content = f"What are some of the recent drug or vape cases in Singapore?"
    
    # Handle penalties with "drug_name" or "vape law" (drug_laws and vape_laws files)
    elif "drug_name" in article or "vape_law_or_penalty" in article:
        if file_type == "drug_laws":
            user_content = f"Can you tell me more about the drug laws related to '{article.get('drug_name', 'this drug')}'?"
        elif file_type == "vape_laws":
            user_content = f"What is the current law regarding vaping and '{article.get('vape_law_or_penalty', 'vaping')}'?"
    
    # Fallback if neither "headline" nor "drug_name" exists
    if not user_content:
        user_content = "Can you share more details about recent laws and penalties?"

    # Generate assistant content, including the article link if available
    assistant_content = article.get(
        "summary", 
        article.get("penalty_details", "Unfortunately, I don't have more detailed information on this topic at the moment.")
    )
    
    # Append the article link if it exists
    if "link" in article:
        assistant_content += f"\nFor more details, you can read the full article here: {article['link']}"

    conversation = {
        "messages": [
            system_message,
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    return conversation

# Function to process a single file and output the generated conversations
def process_file(input_file_path, output_file_path, file_type):
    conversations = []
    
    # Read the articles from the input file
    with open(input_file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            article = json.loads(line.strip())
            # Generate two prompts for the main file
            if file_type == "main":
                # First prompt version
                conversations.append(generate_conversation(article, file_type, prompt_version=1))
                # Second prompt version
                conversations.append(generate_conversation(article, file_type, prompt_version=2))
            else:
                # Generate a conversation based on the article and the file type (for custom prompt)
                conversations.append(generate_conversation(article, file_type))
    
    # Write the formatted conversations to the output file
    with open(output_file_path, 'w', encoding='utf-8') as jsonl_output_file:
        for conversation in conversations:
            jsonl_output_file.write(json.dumps(conversation) + '\n')

    print(f"Conversations have been saved to {output_file_path}")

# File paths for input and output files with corresponding types
input_file_paths = {
    "main": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_main.jsonl",
    "drug_laws": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_druglaws.jsonl",
    "vape_laws": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_vapelaws.jsonl"
}

output_file_paths = {
    "main": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_main.jsonl",
    "drug_laws": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_druglaws.jsonl",
    "vape_laws": "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_vapelaws.jsonl"
}

# Process each file with its corresponding prompt
for key in input_file_paths:
    process_file(input_file_paths[key], output_file_paths[key], key)
