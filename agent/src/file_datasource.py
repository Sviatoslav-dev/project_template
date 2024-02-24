from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
            self,
            accelerometer_filename: str,
            gps_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.accelerometer_reader = None
        self.gps_file_reader = None

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        try:
            gps_line = next(self.gps_file_reader)
            accelerometer_line = next(self.accelerometer_reader)
            return AggregatedData(
                accelerometer=Accelerometer(*accelerometer_line),
                gps=Gps(*gps_line),
                timestamp=datetime.now(),
                user_id=1,
            )
        except StopIteration:
            self.stopReading()

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, "r")
        self.accelerometer_reader = reader(self.accelerometer_file, delimiter=",")
        next(self.accelerometer_reader)

        self.gps_file = open(self.gps_filename, "r")
        self.gps_file_reader = reader(self.gps_file, delimiter=",")
        next(self.gps_file_reader)

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.accelerometer_file.close()
        self.gps_file.close()
        raise StopIteration

# fd = FileDatasource("data/accelerometer.csv", "data/gps.csv")
# fd.startReading()
# print(fd.read())
# fd.stopReading()
