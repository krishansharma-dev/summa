from fastapi import FastAPI
from api.news import app as news_app  # Rename to avoid namespace collision

# Create a new FastAPI instance
main_app = FastAPI(title="News API Service", description="A service for fetching news data")

# Mount the news app under the /api prefix
main_app.mount("/api", news_app)

# Root endpoint for the main app
@main_app.get("/")
async def root():
    return {"message": "Welcome to the News API Service"}