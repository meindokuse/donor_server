from src.api.users import router as user_router
from src.api.donations import router as blood_router

all_routers = [
    user_router,
    blood_router
]
