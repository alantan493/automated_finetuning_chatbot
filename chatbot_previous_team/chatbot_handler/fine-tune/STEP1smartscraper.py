import os
import openai
import json
from dotenv import load_dotenv
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.graphs import SmartScraperMultiGraph
from scrapegraphai.utils import prettify_exec_info
from playwright._impl._errors import TargetClosedError  # Import Playwright error for exception handling

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
    "headless": True,  # Set to False to keep browser visible for debugging, can be set to True later
    "timeout": 60000,  # Set a timeout to wait for each operation
}

# ************************************************
# Create the SmartScraperGraph instance and run it with retries
# ************************************************

def run_scraper_with_retries(scraper, max_retries=3):
    """Runs the scraper with retries in case of TargetClosedError."""
    for attempt in range(max_retries):
        try:
            print(f"Running scraper (Attempt {attempt + 1})...")
            result = scraper.run()
            return result
        except TargetClosedError:
            print(f"Attempt {attempt + 1} failed: Browser or page closed unexpectedly.")
            if attempt == max_retries - 1:
                raise  # Raise the error after max retries

# Instantiate the scraper
multiple_search_graph = SmartScraperMultiGraph(
    prompt=(
        "Collect and provide the following details from the provided link that is dated within 18 months from now, "
        "focusing on articles related to drug trafficking, drug consumption cases, drug-related statistics, drug laws, "
        "vaping offense cases, vape-related statistics, and vape laws in Singapore: 1) Headlines 2) Publication Dates "
        "in DD/MM/YYYY 3) Summaries of each article covering the full details 4) Link of news"
    ),
    source=[
        "https://www.channelnewsasia.com/search?q=singapore%20drugs%20cases&type%5B0%5D=article&categories%5B0%5D=Singapore",
        "https://www.channelnewsasia.com/search?q=singapore%20drugs%20cases&type%5B0%5D=article&categories%5B0%5D=Singapore&page=2",
        "https://www.straitstimes.com/search?searchkey=drug%20cases%20in%20singapore",
        "https://www.channelnewsasia.com/search?q=singapore%20vape&type%5B0%5D=article&categories%5B0%5D=Singapore",
        "https://www.channelnewsasia.com/search?q=singapore%20vape&type%5B0%5D=article&categories%5B0%5D=Singapore&page=2",
        "https://www.straitstimes.com/search?searchkey=singapore%20anti%20vape",
        "https://www.straitstimes.com/search?searchkey=singapore%20anti%20drugs"
    ],
    schema=None,
    config=graph_config
)

# Run the scraper with retries
result = run_scraper_with_retries(multiple_search_graph, max_retries=3)

# Pretty print the result
print(json.dumps(result, indent=4))

# Path updated to reflect a VM environment
file_path = "/home/alantan493/vm/chatbot_previous_team/chatbot_handler/fine-tune/scraped_data_main.jsonl"

# Check if 'articles' key exists in the result and contains data
if 'articles' in result and isinstance(result['articles'], list) and result['articles']:
    # Write to the .jsonl file
    with open(file_path, 'w', encoding='utf-8') as jsonl_file:
        for article in result['articles']:
            # Ensure each article is written as a separate line in the .jsonl file
            jsonl_file.write(json.dumps(article) + '\n')

    print(f"Data has been saved to {file_path}")
else:
    print("No articles found in the result.")
