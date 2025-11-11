import os
import uvicorn

from fastapi import HTTPException
from fastapi import FastAPI

from app.api.v1.routers.auth import auth
app = FastAPI()
app.include_router(auth.router, tags = ["Auth"])

@app.get("/")
def not_found():
    raise HTTPException(status_code=404)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port = port)