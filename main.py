from fastapi import FastAPI

from app.api.v1.routers.auth import auth
app = FastAPI()
app.include_router(auth.router, tags = ["Auth"])