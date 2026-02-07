# Expense Tracker

## Overview
A simple web-based expense tracker built with Python Flask. Users can add expenses with item names and amounts, view all expenses, and see the running total.

## Project Architecture
- **Framework**: Python Flask
- **Entry Point**: `main.py`
- **Port**: 5000 (bound to 0.0.0.0)
- **Production Server**: gunicorn

## How to Run
The application runs via the "Start application" workflow which executes `python main.py`. The Flask development server starts on port 5000.

## Deployment
Configured for autoscale deployment using gunicorn:
```
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```

## Dependencies
- flask
- gunicorn
