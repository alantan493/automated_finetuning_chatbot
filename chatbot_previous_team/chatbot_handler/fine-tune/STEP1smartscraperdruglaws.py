import os
import json
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperMultiGraph

load_dotenv()

# ************************************************
# Define the configuration for the graph
# ************************************************

graph_config = {
    "llm": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "openai/gpt-4o-mini",  # Ensure this model is available
    },
    "verbose": True,
    "headless": True,  # Set to False to observe browser activity
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

multiple_search_graph = SmartScraperMultiGraph(
    prompt="Collect comprehensive details of drug laws and penalties from the source page. Focus on the following details: 1) Drug name or law title 2) Last updated dates 3) Penalty details or legal implications in a summary.",
    source=[
        "https://www.cnb.gov.sg/drug-information/drugs-and-inhalants"
    ],
    schema=None,
    config=graph_config
)

# Run the scraper graph and get the result
result = multiple_search_graph.run()

# Debugging step: Print the result object type and keys (already verified from your output)
print("Type of result:", type(result))
print("Result keys:", result.keys())

# Path to save the output (Updated to the VM environment)
file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_druglaws.jsonl"

# Check if 'drug_laws_and_penalties' key exists in the result and contains data
if 'drug_laws_and_penalties' in result and isinstance(result['drug_laws_and_penalties'], list):
    print(f"Found {len(result['drug_laws_and_penalties'])} drug law entries.")

    # Write to the .jsonl file
    with open(file_path, 'w', encoding='utf-8') as jsonl_file:
        for entry in result['drug_laws_and_penalties']:
            # Ensure each entry is written as a separate line in the .jsonl file
            jsonl_file.write(json.dumps(entry) + '\n')
    
    print(f"Data has been saved to {file_path}")
else:
    print("No 'drug_laws_and_penalties' key found in result. Printing the full result to understand the structure:")
    print(json.dumps(result, indent=4))  # Print the full result for inspection


