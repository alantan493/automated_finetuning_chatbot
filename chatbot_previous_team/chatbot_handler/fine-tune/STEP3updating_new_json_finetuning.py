import re
import json
import os

# File paths for input and output in the VM environment
input_file_paths = [
    "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_main.jsonl",
    "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_druglaws.jsonl",
    "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/finetunenew_vapelaws.jsonl",
    "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/fine-tuning.jsonl"
]
output_file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/fine-tuning-temp.jsonl"

# Function to clean non-ASCII characters
def clean_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# Create a list to store all cleaned JSON objects
cleaned_data_list = []

# Iterate through the list of input file paths
for file_path in input_file_paths:
    # Check if the file exists before attempting to open it
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Skipping...")
        continue  # Skip to the next file if it doesn't exist

    # Open each input file in read mode
    with open(file_path, 'r', encoding='utf-8') as infile:
        # Process each line (which represents a JSON object) in the input file
        for line_num, line in enumerate(infile, 1):
            try:
                # Load the JSON object from the line
                data = json.loads(line.strip())
                # Clean any non-ASCII characters in the JSON object
                cleaned_data = {key: clean_non_ascii(str(value)) if isinstance(value, str) else value for key, value in data.items()}
                
                # Log the size of the cleaned data object (for debugging)
                data_size = len(json.dumps(cleaned_data))
                print(f"File: {file_path}, Line: {line_num}, Size of cleaned data: {data_size} bytes")
                
                # Append the cleaned data to the list
                cleaned_data_list.append(cleaned_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in file {file_path} on line {line_num}: {e}")

# Now write all cleaned data to the temporary output file only once
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for cleaned_data in cleaned_data_list:
        # Write each cleaned JSON object to the output file
        outfile.write(json.dumps(cleaned_data, ensure_ascii=False) + '\n')

# Log the final output file size
output_file_size = os.path.getsize(output_file_path)
print(f"Final output file size: {output_file_size / (1024 * 1024)} MB")

# Replace the original input file with the cleaned version if needed
# Ensure no errors occurred before this step
os.replace(output_file_path, "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/fine-tuning.jsonl")
print("The cleaned file has replaced the original file.")
