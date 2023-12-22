from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from src.database.router import router as db_router
from src.exercises.router import router as exercise_router
from src.workouts.router import router as workout_router
from src.approaches.router import router as approach_router
from src.users.router import router as user_router

app = FastAPI(title="Need for fit")

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )


@app.get("/")
async def root():
    return RedirectResponse("/docs")


app.include_router(db_router)
app.include_router(exercise_router)
app.include_router(workout_router)
app.include_router(approach_router)
app.include_router(user_router)
