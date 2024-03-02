import os


def try_parse(convert, value: str):
    try:
        return convert(value)
    except Exception:
        return None


# MQTT config
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST') or 'test.mosquitto.org'
MQTT_BROKER_PORT = try_parse(int, os.environ.get('MQTT_BROKER_PORT')) or 1883
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'kpi_labwork_1'
MQTT_TOPIC2 = os.environ.get('MQTT_TOPIC2') or 'kpi_labwork_1_parking'

# Delay for sending data to mqtt in seconds
DELAY = try_parse(float, os.environ.get('DELAY')) or 0.1
