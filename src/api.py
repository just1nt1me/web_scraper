from fastapi import FastAPI
from oakhouse_app import Oakhouse
from pydantic import BaseModel
import requests
import streamlit as st

app = FastAPI(
    title="ShareHouses web scraper",
    version="1.0",
    description="Scrape off web pages to check rooms availability",
)

class UrlInput(BaseModel):
    url: str

sharehouse = Oakhouse()

@app.post('/sharehouse')
async def predict(input: UrlInput):
    urls = {input.url: input.url}
    vacancies = sharehouse.get_vacancies(urls)
    return {'The rooms available are:': vacancies}

st.title("ShareHouses web scraper")

# Input for URL
url_input = st.text_input("Enter the URL of the OakHouse:")

if st.button("Check Vacancies"):
    # Make a POST request to the FastAPI server
    response = requests.post("http://localhost:8000/sharehouse", json={"url": url_input})

    if response.status_code == 200:
        # Display the response from FastAPI server
        vacancies = response.json()['The rooms available are:']
        st.write(vacancies)
    else:
        st.write("Error: Could not retrieve vacancies.")
