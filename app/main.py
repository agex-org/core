# app/main.py

from fastapi import FastAPI

from app.routers import api

app = FastAPI()

# Include the API router with a prefix, e.g., /api.
app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
