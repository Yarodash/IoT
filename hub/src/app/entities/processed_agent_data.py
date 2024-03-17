import random

from pydantic import BaseModel
from app.entities.agent_data import AgentData


class ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData


def process_agent_data(agent_data: AgentData) -> ProcessedAgentData:
    road_state = random.choice(["good", "bad", "average"])
    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
