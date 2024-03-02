import time

from paho.mqtt import client as mqtt

import config
from file_datasource import FileDatasource
from schema.aggregated_data_schema import AggregatedDataSchema
from schema.parking_schema import ParkingSchema


def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution

    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client


def send(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def publish(client, topic, topic_parking, datasource, delay):
    datasource.start()

    while True:
        time.sleep(delay)

        data = datasource.read()
        msg = AggregatedDataSchema().dumps(data)
        send(client, topic, msg)

        parking = datasource.read2()
        msg_parking = ParkingSchema().dumps(parking)
        send(client, topic_parking, msg_parking)

    datasource.stop()


def run():
    # Prepare mqtt client
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)
    # Prepare datasource
    datasource = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    # Infinity publish data
    publish(client, config.MQTT_TOPIC, config.MQTT_TOPIC2, datasource, config.DELAY)


if __name__ == '__main__':
    run()
