from typing import Set

import uvicorn
from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from models.agent_model import ProcessedAgentDataInDB, ProcessedAgentData
from tables.processed_data import ProcessedAgentDataSQL, Session

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket subscriptions
subscriptions: Set[WebSocket] = set()


# FastAPI WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)


# Function to send data to subscribed users
async def send_data_to_subscribers(data: str):
    for websocket in subscriptions:
        await websocket.send_text(data)


# FastAPI CRUDL endpoints

@app.post("/processed_agent_data", status_code=201)
async def create_processed_agent_data(data: list[ProcessedAgentData]):
    with Session() as session:
        for item in data:
            new_item = ProcessedAgentDataSQL(
                road_state=item.road_state,
                x=item.agent_data.accelerometer.x,
                y=item.agent_data.accelerometer.y,
                z=item.agent_data.accelerometer.z,
                latitude=item.agent_data.gps.latitude,
                longitude=item.agent_data.gps.longitude,
                timestamp=item.agent_data.timestamp
            )
            session.add(new_item)
            session.commit()
            session.refresh(new_item)

            await send_data_to_subscribers(item.json())


@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    with Session() as session:
        item = session\
            .query(ProcessedAgentDataSQL)\
            .filter(ProcessedAgentDataSQL.id == processed_agent_data_id)\
            .first()

        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")

        return item


@app.get("/processed_agent_data", response_model=list[ProcessedAgentDataInDB])
def list_processed_agent_data():
    with Session() as session:
        return session.query(ProcessedAgentDataSQL).all()


@app.put("/processed_agent_data/{processed_agent_data_id}")
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    print(data)
    with Session() as session:
        item = session\
            .query(ProcessedAgentDataSQL)\
            .filter(ProcessedAgentDataSQL.id == processed_agent_data_id)\
            .first()

        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")

        item.road_state = data.road_state
        item.x = data.agent_data.accelerometer.x
        item.y = data.agent_data.accelerometer.y
        item.z = data.agent_data.accelerometer.z
        item.latitude = data.agent_data.gps.latitude
        item.longitude = data.agent_data.gps.longitude
        item.timestamp = data.agent_data.timestamp

        session.commit()
        session.refresh(item)

        return item


@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    with Session() as session:
        item = session\
            .query(ProcessedAgentDataSQL)\
            .filter(ProcessedAgentDataSQL.id == processed_agent_data_id)\
            .first()

        if item is None:
            raise HTTPException(status_code=404, detail="Data not found")

        session.delete(item)
        session.commit()

        return item


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
