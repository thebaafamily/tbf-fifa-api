from fastapi import FastAPI
from requests import request
import meta
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://192.168.1.101:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"FIFA": "Root"}

@app.get("/groups")
async def get_groups() -> dict:
    groups = meta.GetGroups()
    return {"data" : groups}

@app.get("/itinerary/{groupId}")
async def get_itinerary(groupId: int = -1) -> dict:
    itinerary = meta.GetItinerary(groupId)
    return {"data" : itinerary}

@app.get("/points/{groupId}")
async def get_points(groupId: int = -1) -> dict:
    points = meta.GetPoints(groupId)
    print(points)
    return {"data" : points}

@app.put("/score/")
async def update_score(request: dict) -> dict:
    itinerary = meta.UpdateScore(request)
    return {"data": itinerary}


if __name__ == '__main__' :
    uvicorn.run("main:app", port=3003, host="0.0.0.0", reload=True)