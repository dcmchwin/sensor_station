import serial
import serial.tools.list_ports as lp


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


def read_data():
    ser = get_arduino_serial_connection()
    ser.open()
    for i in range(0, 10):
        # input is bytes, which must be decoded and then split
        # by whitespace
        line = ser.readline().decode('UTF-8').split()
        temperature = float(line[0])
        print('Temperature: {:.2f} {}C'.format(temperature, u'\N{DEGREE SIGN}'))
    ser.close()


if __name__ == '__main__':
    read_data()