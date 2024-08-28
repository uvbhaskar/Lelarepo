import streamlit as st
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from llama_index.core import VectorStoreIndex
from llama_index.readers.web import WholeSiteReader
from llama_index.core import Document
import openai

# Initialize OpenAI API Client
openai.api_key = st.secrets["open_ai_key"]
# client = OpenAI()

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_data(url, prefix, max_depth=6, current_depth=0, visited=None):
    # st.write(Document.__init__.__annotations__)
    if visited is None:
        visited = set()  # Initialize the set of visited URLs

    if current_depth > max_depth:
        return []

    if url in visited:
        return []  # Avoid revisiting the same URL

    visited.add(url)
    documents = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text data from all paragraphs
        page_content = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]

        # Convert each piece of text data to a Document object
        for text in page_content:
            doc = Document(text=text, metadata={"url": url, "depth": current_depth})
            documents.append(doc)

        # Find all links on the page to follow
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
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

# st.write("Scraped Data:")
# st.write(documents)

def response_generator(query):
    try:
        # Create an index from the documents
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        response = query_engine.query(query)

    except Exception as e:
        # Log or handle the exception
        response = f"An error occurred: {e}"

    return response

st.title("FireBot chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    st.write('Before Response generator')
    response = response_generator(prompt)
  
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
