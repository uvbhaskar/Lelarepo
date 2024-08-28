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

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_data(url, prefix, max_depth=6, current_depth=0, visited=None):
    if visited is None:
        visited = set()  # Initialize the set of visited URLs

    if current_depth > max_depth:
        return []

    if url in visited:
        return []  # Avoid revisiting the same URL

    visited.add(url)
    documents = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text data from all paragraphs
        page_content = [p.get_text() for p in soup.find_all('p')]
        documents.extend(page_content)

        # Find all links on the page to follow
        for link in soup.find_all('a', href=True):
            # Construct full URL
            full_url = urljoin(url, link['href'])

            # Only follow links that start with the prefix to stay within the domain
            if full_url.startswith(prefix):
                documents.extend(scrape_data(full_url, prefix, max_depth, current_depth + 1, visited))

    except requests.RequestException as e:
        st.write(f"An error occurred while scraping {url}: {e}")

    return documents

# Set the base URL and prefix for the scraper
base_url = "https://www.fire.ca.gov/"
prefix = "https://www.fire.ca.gov/"

# Scrape data up to a depth of 6
documents = scrape_data(base_url, prefix, max_depth=6)

st.write("Scraped Data:")
st.write(documents)
