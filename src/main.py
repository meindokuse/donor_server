from fastapi import FastAPI
from src.auth.router import router as user_router
from src.blood.router import router as blood_router
app = FastAPI(
    title="Donor Service",
)

app.include_router(user_router)
app.include_router(blood_router)
