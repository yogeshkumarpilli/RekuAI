from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
from pipeline.prediction_pipeline import hybrid_recommendation
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Anime Recommender System",
    description="A hybrid recommendation system for anime using collaborative filtering and content-based methods",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """
    Serves the home page with the recommendation form
    """
    logger.info("Serving home page")
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "recommendations": None}
    )

@app.post("/", response_class=HTMLResponse)
async def get_recommendations(request: Request, userID: int = Form(...)):
    """
    Process the user ID and return anime recommendations
    """
    logger.info(f"Processing recommendation request for user ID: {userID}")
    
    try:
        # Call the recommendation pipeline
        recommendations = hybrid_recommendation(userID)
        logger.info(f"Successfully generated {len(recommendations) if recommendations else 0} recommendations")
        
        # Return the template with recommendations
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "recommendations": recommendations}
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {str(e)}")
        # Return error in the template instead of throwing an exception
        # This keeps the user on the page with an error message
        return templates.TemplateResponse(
            "index.html", 
            {
                "request": request, 
                "recommendations": None, 
                "error": "Unable to generate recommendations. Please try a different user ID."
            }
        )

@app.get("/health", status_code=200)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {"status": "healthy"}

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    """
    Custom 404 page
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "recommendations": None, "error": "Page not found"}
    )

if __name__ == "__main__":
    logger.info("Starting Anime Recommender System API")
    uvicorn.run("application:app", host="127.0.0.1", port=5000, reload=True)