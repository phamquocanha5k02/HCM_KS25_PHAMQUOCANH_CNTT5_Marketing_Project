from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import campaign_task, campaign_member, campaign, users as user

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/get_health", tags=["GET_HEALTH"])
def get_health():
    return "Hello World"