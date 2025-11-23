import os
import uvicorn

from fastapi import HTTPException
from fastapi import FastAPI

from app.api.v1.routers import auth, genre, home, singer, user, admin
from app.core.config import Settings

app = FastAPI()
app.include_router(auth.router, tags = ["Auth"])
app.include_router(user.router, tags = ["User"])
app.include_router(singer.router, tags = ["Singer"])
app.include_router(genre.router, tags = ["Genre"])
app.include_router(home.router, tags = ["Home"])
app.include_router(admin.router, tags = ["Admin"])

@app.get("/")
def not_found():
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    settings = Settings()

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port = port)