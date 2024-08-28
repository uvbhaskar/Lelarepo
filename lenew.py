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

# Configure ChromeDriver
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Initialize ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

def scrape_data():
    # Initialize the scraper with a prefix URL and maximum depth
    scraper = WholeSiteReader(
        prefix="https://www.fire.ca.gov/",  # Example prefix
        max_depth=6,
        driver=driver  # Pass the configured driver to the WholeSiteReader
    )
    
    # Start scraping from a base URL
    documents = scraper.load_data(
        base_url="https://www.fire.ca.gov/"
    )  # Example base URL
    
    return documents
 
# Scrape data
documents = scrape_data()
def response_generator(query):
    try:
        # Scrape data
        #documents = scrape_data()
        
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
    response = response_generator(prompt)
  
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Quit the driver when the script ends
driver.quit()
