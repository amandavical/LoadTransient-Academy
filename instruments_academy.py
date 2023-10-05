class Eload:
    """
       Represents an Electronic Load instrument.

       This class simulates an Electronic Load instrument with properties for voltage, current, and power, as well as
       methods for writing commands and querying measurements.

       Attributes:
           voltage (float): The voltage set on the Electronic Load.
           current (float): The current set on the Electronic Load.
           power (float): The calculated power based on the current and voltage settings.
           _buffer: A buffer for temporarily storing query responses.
       """
    def __init__(self):
        # Initialize Eload properties
        self.voltage = 0
        self.current = 0
        self.power = self.voltage * self.current  # Calculate initial power (0)
        self._buffer = None  # Initialize buffer for communication

    def write(self, command):
        assert type(command) is str

        if command.startswith('CURR'):
            if command.endswith('?'):
                # Buffer current value for querying
                self._buffer = self.current
            else:
                command_string = command.split(' ')
                self.current = float(command_string[1])  # Set new current

        elif command == 'MEAS:CURR?':
            # Buffer current value for querying
            self._buffer = self.current

        elif command.startswith('VOLT'):
            if command.endswith('?'):
                # Buffer voltage value for querying
                self._buffer = self.voltage
            else:
                command_string = command.split(' ')
                self.voltage = float(command_string[1])  # Set new voltage

        elif command == 'MEAS:VOLT?':
            # Buffer voltage value for querying
            self._buffer = self.voltage

        elif command == 'MEAS:POW?':
            # Buffer calculated power value for querying
            self._buffer = self.current * self.voltage

        else:
            raise ValueError('Not recognized command')

    def read(self):
        buffer = str(self._buffer)
        self._buffer = None  # Clear buffer after reading

        return buffer

    def query(self, command):
        assert type(command) is str

        if command == 'CURR?':
            return str(self.current)

        elif command == 'MEAS:CURR?':
            return str(self.current)

        elif command == 'VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:VOLT?':
            return str(self.voltage)

        elif command == 'MEAS:POW?':
            return str(self.current * self.voltage)

        else:
            raise ValueError('Not recognized command')


class PSU:
    def __init__(self):
        # Initialize PSU properties
        self.voltage = 0
        self._current = 1  # Default current value

    def get_voltage(self):
        return self.voltage

    def set_voltage(self, voltage):
        assert (type(voltage) is float) or (type(voltage) is int)
        self.voltage = voltage

    def get_current(self):
        return self._current

    def get_power(self):
        return self.voltage * self._current


class Equity:
    def __init__(self):
        # Initialize Equity properties
        self._temperature = 25  # Default temperature value

    def get_temperature(self):
        return self._temperature

    def set_temperature(self, temperature):
        assert (type(temperature) is float) or (type(temperature) is int)
        self._temperature = temperature
