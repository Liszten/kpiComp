# Stock Rater

A web application that rates stocks on a **1–10 value scale** based on financial KPIs, benchmarked against S&P 500 sector peers.

- **1** = Most expensive / worst value  
- **10** = Cheapest / best value

## Features

- Enter **any stock ticker** — not limited to S&P 500
- Automatic sector detection via Yahoo Finance
- Comparison against **S&P 500 sector peer medians**
- 10 financial KPIs with weighted scoring
- Combined **absolute** (vs universal thresholds) + **relative** (vs sector) rating
- Session-level caching of sector data (1 hour TTL)
- Clean web interface + REST API for programmatic use

## KPIs Used

| KPI | Weight | Interpretation |
|---|---|---|
| P/E Ratio (TTM) | 15% | Lower = cheaper |
| Forward P/E | 12% | Lower = cheaper |
| P/B Ratio | 10% | Lower = cheaper |
| EV/EBITDA | 12% | Lower = cheaper |
| Debt/Equity | 10% | Lower = less risk |
| ROE | 12% | Higher = more profitable |
| Profit Margin | 10% | Higher = more efficient |
| Revenue Growth | 9% | Higher = faster growing |
| Current Ratio | 5% | Higher = more liquid |
| Dividend Yield | 5% | Higher = more income |

## Rating Algorithm

Each KPI gets two sub-scores:
- **Absolute score**: compared against universal good/bad thresholds
- **Relative score**: compared against the sector median (using a sigmoid function)

Final rating = **40% absolute + 60% relative**, mapped to a 1–10 scale.

## Setup & Run

### Prerequisites
- Python 3.10+
- Internet connection (for Yahoo Finance data)

### Install

```bash
cd kpiComp
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

## REST API

### Analyze a stock

```
GET /api/analyze/{ticker}
```

**Example:**
```bash
curl http://localhost:8000/api/analyze/MSFT
```

**Response:**
```json
{
  "ticker": "MSFT",
  "company_name": "Microsoft Corporation",
  "sector": "Technology",
  "industry": "Software—Infrastructure",
  "stock_kpis": { ... },
  "sector_averages": { ... },
  "sector_peer_count": 72,
  "rating": {
    "overall_rating": 5.4,
    "absolute_score": 4.8,
    "relative_score": 5.8,
    "kpi_scores": { ... }
  },
  "kpi_comparison": [ ... ]
}
```

### Clear cache

```
POST /api/clear-cache
```

## Project Structure

```
kpiComp/
├── main.py              # FastAPI app (routes + web interface)
├── data.py              # Yahoo Finance data fetching + caching + analysis pipeline
├── rating.py            # Rating algorithm (KPI configs, scoring, formatting)
├── sp500.py             # S&P 500 ticker list
├── index.html           # Single-page web frontend
├── requirements.txt
└── README.md
```

## Notes

- First analysis for a given sector will be slow (~1-2 minutes) as it fetches data for all S&P 500 stocks in that sector. Subsequent analyses in the same sector use cached data.
- The S&P 500 list is a static snapshot. Update `sp500.py` periodically for accuracy.
- Rating algorithm weights and thresholds can be tuned in `rating.py`.
- Data is sourced from Yahoo Finance and is for informational purposes only — not financial advice.
