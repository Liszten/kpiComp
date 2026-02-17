"""
Stock Rater - FastAPI Application

Provides both:
  - A web interface (single page) for interactive use
  - A REST API endpoint for programmatic access
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import logging
import traceback

from data import analyze_stock, clear_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Stock Rater",
    description="Rate stocks on a 1-10 value scale based on financial KPIs, with sector comparison.",
    version="1.0.0",
)


# --- REST API ---

@app.get("/api/analyze/{ticker}", response_class=JSONResponse)
async def api_analyze(ticker: str):
    """
    REST API endpoint: Analyze a stock ticker.

    Returns JSON with:
      - ticker, company_name, sector, industry
      - stock KPIs, sector averages, differences
      - overall rating (1-10) with breakdown
    """
    try:
        result = analyze_stock(ticker)
        return JSONResponse(content=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing {ticker}: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error analyzing '{ticker}': {str(e)}")


@app.post("/api/clear-cache")
async def api_clear_cache():
    """Clear the sector data cache."""
    clear_cache()
    return {"status": "ok", "message": "Cache cleared."}


# --- Web Interface ---

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the single-page web interface."""
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())
