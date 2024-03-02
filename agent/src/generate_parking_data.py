import csv
import math

from schema.parking_schema import ParkingSchema

parking_schema = ParkingSchema()

csv_file_path = "data/parking.csv"

with open(csv_file_path, mode="w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["empty_count"])

    writer.writeheader()

    for i in range(100):
        writer.writerow({"empty_count": int(10 + 10 * math.sin(i * 0.2))})
