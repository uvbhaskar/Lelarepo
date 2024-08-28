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
