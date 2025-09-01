from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from typing import List, Optional
from datetime import datetime, timedelta

app = FastAPI()

# News API configuration
API_KEY = "ff08eb11e86d41619ae0c0a19266adb4"
NEWS_API_URL = "https://newsapi.org/v2/everything"


# Pydantic model for news article
class Article(BaseModel):
    source: dict
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    publishedAt: str
    content: Optional[str]


# Pydantic model for API response
class NewsResponse(BaseModel):
    status: str
    totalResults: int
    articles: List[Article]


@app.get("/news", response_model=NewsResponse)
async def get_tesla_news():
    try:
        # Set date range for the last 30 days
        from_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        to_date = datetime.now().strftime("%Y-%m-%d")

        # Query parameters
        params = {
            "q": "tesla",
            "from": from_date,
            "to": to_date,
            "sortBy": "publishedAt",
            "apiKey": API_KEY,
        }

        # Make request to News API
        response = requests.get(NEWS_API_URL, params=params)
        response.raise_for_status()  # Raise exception for bad status codes

        # Parse JSON response
        data = response.json()

        # Validate response structure
        if data.get("status") != "ok":
            raise HTTPException(status_code=500, detail="News API returned an error")

        return NewsResponse(**data)

    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Failed to fetch news: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error parsing response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
