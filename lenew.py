import streamlit as st
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from llama_index.core import VectorStoreIndex
from llama_index.readers.web import WholeSiteReader

# Initialize OpenAI API Client
client = OpenAI(api_key=st.secrets["open_ai_key"])

import requests
from bs4 import BeautifulSoup

def scrape_data():
    url = "https://www.fire.ca.gov/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Example: Extracting text data from all paragraphs
    documents = [p.get_text() for p in soup.find_all('p')]

    return documents
documents = scrape_data()
print(documents)
