import json
from logging import info
from typing import List

import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_api_gateway import StoreGateway


def convert_time(time):
    return time.isoformat()


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        # Make a POST request to the Store API endpoint with the processed data
        data = [item.dict() for item in processed_agent_data_batch]
        data_json = json.dumps(data, default=convert_time)

        response = requests.post(
            f"{self.api_base_url}/processed_agent_data",
            data=data_json
        )

        info(f"Request to Store API returned status code: {response.status_code}")

        return response.status_code == 201
