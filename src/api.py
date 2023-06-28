from fastapi import FastAPI
from oakhouse_app import Oakhouse
from pydantic import BaseModel
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        reload=True,
    )
