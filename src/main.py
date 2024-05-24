from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from src.approaches.router import router as approach_router
from src.database.router import router as db_router
from src.exercises.router import router as exercise_router
from src.users.router import router as user_router
from src.users.phrases.router import router as phrases_router
from src.workouts.router import router as workout_router
from src.workouts.workout_types.router import router as workout_types_router
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="Need for fit")

app.mount("/static", StaticFiles(directory="static"), name="static")

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
app.include_router(workout_types_router)
app.include_router(approach_router)
app.include_router(user_router)
app.include_router(phrases_router)
