from fastapi import FastAPI, Request, HTTPException

from routes.notes.route import router as notes_routes
from routes.github.route import router as github_routes
from routes.health.route import router as health_routes

app = FastAPI()

app.include_router(notes_routes)

app.include_router(github_routes)

app.include_router(health_routes)



