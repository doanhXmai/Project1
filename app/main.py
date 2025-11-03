from fastapi import FastAPI

# import app.api.v1.routes.auth.auth
from app.api.v1.routes.home import home
from app.api.v1.routes.admin import admin

# email = "viaicamon28@gmail.com"
# password = "utc@123"

apptest = FastAPI()
# apptest.include_router(app.api.v1.routes.auth.auth.router, tags = ["Auth"])
# apptest.include_router(home.router, tags=["Home"])
apptest.include_router(admin.router, tags=["Admin"])