from fastapi import FastAPI
from app.core.database import engine,Base
from app.models.user import User
from app.models.notification import Notification
from app.routers.auth import router as auth_router
from app.routers.notifications import router as notification_router


app = FastAPI()


Base.metadata.create_all(engine)

app.include_router(auth_router)
app.include_router(notification_router)

@app.on_event("startup")
def startup():
    with engine.connect() as conn:
        print("Connected to DB")

@app.get("/")
def root():
    return {"message": "Hello"}

