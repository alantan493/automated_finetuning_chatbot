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
        "model": "openai/gpt-4o-mini",
    },
    "verbose": True,
    "headless": True,  # Set to False to observe browser activity
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

multiple_search_graph = SmartScraperMultiGraph(
    prompt="Collect and provide comprehensive details of each penalty for vape-related cases in Singapore. Focus on the following details: 1) Vape law or penalty 2) Last Updated Dates in DD/MM/YYYY 3) Summaries of each vape-related law or movement in a paragraph.",
    source=[
        "https://www.hsa.gov.sg/consumer-safety/articles/vaping-enforcement-in-singapore"
    ],
    schema=None,
    config=graph_config
)

# Run the scraper graph and get the result
result = multiple_search_graph.run()

# Debugging step: Print the result object type and keys
print("Type of result:", type(result))
print("Result keys:", result.keys())

# Path to save the output (Updated to the VM environment)
file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_vapelaws.jsonl"

# Check if the correct key 'penalties' exists in the result and contains data
if 'penalties' in result and isinstance(result['penalties'], list):
    print(f"Found {len(result['penalties'])} vape law entries.")

    # Write to the .jsonl file
    with open(file_path, 'w', encoding='utf-8') as jsonl_file:
        for entry in result['penalties']:
            # Create a dictionary structure for each penalty
            article = {
                "vape_law_or_penalty": entry.get('vape_law_or_penalty', 'NA'),
                "last_updated_date": entry.get('last_updated', 'NA'),
                "summary": entry.get('summary', 'NA')
            }
            
            # Print the entry to display it
            print("Vape Law or Penalty:", article['vape_law_or_penalty'])
            print("Last Updated Date:", article['last_updated_date'])
            print("Summary:", article['summary'])
            print("="*50)  # Separator for readability
            
            # Ensure each entry is written as a separate line in the .jsonl file
            jsonl_file.write(json.dumps(article) + '\n')
    
    print(f"Data has been saved to {file_path}")
else:
    print("No 'penalties' key found in result. Printing the full result to understand the structure:")
    print(json.dumps(result, indent=4))  # Print the full result for inspection
