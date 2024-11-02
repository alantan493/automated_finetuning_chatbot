## Singapore Drug and Vape Laws Chatbot


This project is a chatbot fine-tuned to provide information on Singapore's drug and vaping laws. The bot integrates dynamically updated data through web scraping and customized responses via OpenAI's fine-tuning.

Project Overview
The chatbot uses a dataset on Singapore's drug and vape laws, formatted into JSONL and fine-tuned with OpenAI’s API. It is kept current by dynamically scraping credible sources for updates.

File Structure
Key directories and files include:

chatbot_handler/fine-tune: Contains JSONL files and scripts for data scraping, formatting, and fine-tuning.
frontend: HTML, CSS, and JavaScript files for the user interface.
chatbot-backend.py: Flask backend to handle requests and connect the frontend with OpenAI’s model.
Key Processes
Fine-Tuning: Dataset on drug and vape laws is uploaded and fine-tuned using OpenAI’s API to provide custom responses.
Web Scraping: Data from sources like CNA and Straits Times is gathered with ScrapeGraphAI, bypassing anti-scraping measures.
Data Integration: Scraped data is converted to JSONL format, cleaned, and merged, then used to update the fine-tuning model.
Automation
The automated_finetuning.py script orchestrates the entire process—scraping, formatting, merging, and fine-tuning—ensuring the chatbot remains up-to-date with the latest information.

Running the Project
Clone the Repo and Install Dependencies.
Configure the .env file with necessary API keys.
Run Flask Server and access the chatbot at 127.0.0.1:8080.
This setup provides a responsive chatbot that delivers accurate, real-time information on Singapore's laws regarding drugs and vaping.
