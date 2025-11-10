from fastapi import FastAPI

from app.api.v1.routers.auth import auth
from app.api.v1.routers.home import home
from app.api.v1.routers.admin import admin

# email = "viaicamon28@gmail.com"
# password = "utc@123"

app = FastAPI()
app.include_router(auth.router, tags = ["Auth"])
# apptest.include_router(home.router, tags=["Home"])
# apptest.include_router(admin.router, tags=["Admin"])