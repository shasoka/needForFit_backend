from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database.router import router as db_router
from exercises.router import router as exercise_router
from workouts.router import router as workout_router
from approaches.routers import router as approach_router



app = FastAPI(title="Need for fit")


@app.get("/")
async def root():
    return {"message": "Hello World!"}


app.include_router(db_router)
app.include_router(exercise_router)
app.include_router(workout_router)
app.include_router(approach_router)
