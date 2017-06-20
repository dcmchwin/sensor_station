import logging
import serial
import serial.tools.list_ports as lp
from threading import Thread, Event
from data_store import get_db_connection, get_table_cursor, write_table_entry
from utils import time_format
import time

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

class DataRead(Thread):
    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event
        # We don't want to block the db by keeping it open
        self.db = None
        self.cursor = None

    def run(self):
        ser = get_arduino_serial_connection()
        ser.open()
        while not self.stop_event.isSet():
            # input is bytes, which must be decoded and then split
            # by whitespace
            line = ser.readline().decode('UTF-8').split()
            temperature = float(line[0])
            
            # Get a formatted time string to save
            time_str = time.strftime(time_format)

            # Get a database connection and write to the table
            self.db = get_db_connection()
            self.cursor = get_table_cursor(self.db)

            write_table_entry(self.db, self.cursor, time_str, temperature)

            # Close connection for use by other functions
            self.db.close()

            logger.info('Time: {} \t Temperature: {:.2f} {}C'.
                         format(time_str, temperature, u'\N{DEGREE SIGN}'))
        ser.close()


def get_port():
    """Look through open com ports for Arduino Uno."""
    arduino_ports = [p for p, n, _ in lp.comports() if
                    'Arduino Uno' in n]
    if len(arduino_ports) == 0:
        raise ValueError('No Arduino Uno connected')
    elif len(arduino_ports) > 1:
        raise ValueError('Multiple Arduino Unos connected,' + 
                         ' a port must be specified')
    else:
        port = arduino_ports[0]
        return port


def get_arduino_serial_connection(port=None,
                                  baudrate=9600):
    """Return a serial object for the arduino connection."""
    # Get com port to use if unspecified
    if port is None:
        port = get_port()

    ser = serial.Serial()
    ser.port = port
    ser.baudrate = baudrate

    return ser
    


if __name__ == '__main__':
    logger.info("Beginning data reader")
    stop_event = Event()
    read_thread = DataRead(stop_event)
    read_thread.start()
    cmd = None
    while cmd not in ['q', 'Q']:
        cmd = input('Press q to quit at any time \n')
    stop_event.set()