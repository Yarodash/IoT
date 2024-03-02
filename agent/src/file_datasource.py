from csv import DictReader
from datetime import datetime

from domain.accelerometer import Accelerometer
from domain.aggregated_data import AggregatedData
from domain.gps import Gps
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename

        self.accelerometer_data = None
        self.gps_data = None
        self.parking_data = None

    def read(self) -> AggregatedData:
        if self.accelerometer_data is None or self.gps_data is None:
            raise Exception("Datasources are not started")

        return AggregatedData(
            accelerometer=Accelerometer(**self.accelerometer_data.read()),
            gps=Gps(**self.gps_data.read()),
            timestamp=datetime.now()
        )

    def read2(self) -> Parking:
        if self.parking_data is None:
            raise Exception("Datasources are not started")

        return Parking(
            **self.parking_data.read(),
            gps=Gps(**self.gps_data.read())
        )

    def start(self):
        self.accelerometer_data = CSV(self.accelerometer_filename)
        self.gps_data = CSV(self.gps_filename)
        self.parking_data = CSV(self.parking_filename)

    def stop(self):
        self.accelerometer_data.close()
        self.gps_data.close()
        self.parking_data.close()


class CSV:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.file = None
        self.reader = None

        self.start()

    def start(self):
        self.file = open(self.filename, 'r')
        self.reader = DictReader(self.file)

        print("Start reading", self.filename, self.file)

    def read(self):
        try:
            return next(self.reader)
        except StopIteration:
            self.start()
            return self.read()

    def close(self):
        self.file.close()
        self.file = None
