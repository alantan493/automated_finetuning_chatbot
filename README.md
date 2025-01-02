# Chatbot for Drug and Vape Law Information in Singapore

## Overview
This project develops a chatbot utilizing a fine-tuned large language model (LLM) to provide accurate and relevant information about drug and vape laws in Singapore. The chatbot is designed to engage users through a dynamic web interface, ensuring updated responses based on the latest news and statutory regulations.

## Features
- **Fine-Tuned Chatbot:** Utilizes OpenAI's GPT-4o-mini, fine-tuned on local legislative content.
- **Dynamic Web Scraping:** Incorporates up-to-date information from local news sources using ScrapeGraphAI.
- **Interactive Frontend:** A user-friendly interface designed with HTML, CSS, and JavaScript.
- **Backend Integration:** Flask application facilitating backend to frontend communication.
- **Cloud Hosting:** Deployed on Google Cloud Platform to ensure accessibility and scalability.
- **Automation:** Automated scripts for continuous updating of the chatbot's knowledge base.

## Prerequisites
- Python 3.8+
- Flask
- Docker
- Google Cloud SDK
- Access to OpenAI's APIs

## Installation
1. Clone the repository to your local machine.
2. Set up a virtual environment and install the required Python libraries.
3. Enter your OpenAI's API key into the env. file
4. Deploy the application to Google Cloud Platform using the provided configuration files.
5. Running the Application:

Start the Flask server to run the chatbot locally or access it through the cloud deployment.
Interact with the chatbot through the web interface to get information on drug and vape laws.
