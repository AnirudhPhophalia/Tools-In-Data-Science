from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Allow browser requests from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "24f2003068@ds.study.iitm.ac.in"

API_KEY = "ak_ha34ag6v07l0aqcbar1mdnmt"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(None)
):
    # Authentication
    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"}
        )

    events = request.events

    total_events = len(events)

    unique_users = len(set(event.user for event in events))

    revenue = 0.0

    user_totals = {}

    for event in events:
        if event.amount > 0:
            revenue += event.amount

            user_totals[event.user] = (
                user_totals.get(event.user, 0)
                + event.amount
            )

    top_user = ""

    if user_totals:
        top_user = max(
            user_totals,
            key=user_totals.get
        )

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }