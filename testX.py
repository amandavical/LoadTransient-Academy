from instruments_academy import PSU, Equity, Eload
from time import sleep


class LoadTransientTest:
    """
    This class represents a Load Transient test.
    """

    def __init__(self) -> None:
        # Test parameters and initial state
        self._id = 1000
        self._name = 'Load Transient'
        self._description = 'None'
        self._current_state = 'START'
        self._state_sleep_time = 0.1
        self._temperature_step = 0

        # Initialize instruments and configure instruments
        self.psu = PSU()
        self.equity = Equity()
        self.eload = Eload()
        self._configure_eload()
        self._configure_equity()
        self._configure_psu()

        # List of temperatures in degrees Celsius to be tested
        self._temperature = [-10.0, 25.0, 85.0]  # [10.0, 25.0, 45.0]

    def _finite_state_machine(self):
        # Finite State Machine (FSM) to control the test process

        if self._current_state == 'START':
            self._initialize_test()

        elif self._current_state == 'CONFIG_EQUITY':
            self._configure_equity_chamber()

        elif self._current_state == 'CONFIG_PSU':
            self._configure_power_supply()

        elif self._current_state == 'CONFIG_ELOAD':
            self._configure_electronic_load()

        elif self._current_state == 'SHOW_OUTPUT':
            self._display_output_measurements()

        elif self._current_state == 'VERIFY_TEMPERATURE_STEP':
            self._check_temperature_steps()

        elif self._current_state == 'END':
            self._finish_test()

        else:
            raise Exception('Invalid state in FSM')

    def _initialize_test(self):
        # Initialize test parameters at the beginning of the test

        # Set the current temperature to the first value in the temperature list
        self._current_temperature = self._temperature[self._temperature_step]

        # Check if the current temperature is within a valid range
        if not 0 <= self._current_temperature <= 60:
            raise ValueError('Temperature out of range')

        # Set stabilization temperature time
        self._stabilization_temperature_time = 40 * 60

        # Check if the stabilization temperature time is within a valid range
        if not 0 <= self._stabilization_temperature_time <= 3600:
            raise ValueError('Stabilization temperature time out of range')

        # Set voltage C
        self._voltage_C = 120.0

        # Set electronic charge

        # Initial electric current
        self._initial_electric_current = 3.0

        # Check if the initial electric current is within a valid range
        if not 0 <= self._initial_electric_current <= 5:
            raise ValueError('Initial electric current out of range')

        assert type(self._initial_electric_current) is float

        # Final electric current
        self._final_electric_current = 6.0

        # Check if the final electric current is within a valid range
        if not 1 <= self._final_electric_current <= 10:
            raise ValueError('Final electric current out of range')

        assert type(self._final_electric_current) is float

        # Set voltage X
        self._voltage_X = 20.0

        # Set the voltage for the Electronic Load (Eload)
        self.eload.write(f'VOLT {self._voltage_X}')

        # Transition to the next state
        self._current_state = 'CONFIG_EQUITY'

    def _configure_equity_chamber(self):
        # Configure the Temperature Chamber (Equity)

        # Set the actual electric current to the initial electric current
        self._actual_electric_current = self._initial_electric_current

        # Set the temperature of the chamber to the current temperature
        self.equity.set_temperature(self._current_temperature)

        # Wait until the chamber temperature stabilizes
        while self._current_temperature != self.equity.get_temperature():
            sleep(1)

        # Transition to the next state
        self._current_state = 'CONFIG_PSU'

    def _configure_power_supply(self):
        # Configure the Power Supply (PSU)

        # Set the voltage for the Power Supply (PSU)
        self.psu.set_voltage(self._voltage_X)

        # Wait for a moment
        sleep(1)

        # Transition to the next state
        self._current_state = 'CONFIG_ELOAD'

    def _configure_electronic_load(self):
        # Configure the Electronic Load (Eload)

        # Set the current for the Electronic Load (Eload)
        self.eload.write(f'CURR {self._actual_electric_current}')

        # Wait for a moment
        sleep(1)

        # Transition to the next state
        self._current_state = 'SHOW_OUTPUT'

    def _display_output_measurements(self):
        # Collect and display output measurements

        # Measure and print Electronic Load (Eload) values
        print(f'ELOAD Actual electric current: {self.eload.query("MEAS:CURR?")}')
        print(f'ELOAD Actual electric voltage: {self.eload.query("MEAS:VOLT?")}')

        # Measure and print Power Supply (PSU) values
        print(f'PSU Actual electric current: {self.psu.get_current()}')
        print(f'PSU Actual electric voltage: {self.psu.get_voltage()}')

        # Measure and print Electronic Load (Eload) output power
        self._output_power = float(self.eload.query("MEAS:POW?"))
        print(f'ELOAD Actual output power: {self._output_power}')

        # Check if the output power is greater than or equal to the set voltage (X)
        if self._output_power >= self._voltage_X:
            self._current_state = 'END'
        else:
            self._current_state = 'CONFIG_ELOAD'

        # Transition to the next state
        self._current_state = 'VERIFY_TEMPERATURE_STEP'

    def _check_temperature_steps(self):
        # Check if there are more temperature steps to test

        # Increment the temperature step counter
        self._temperature_step += 1

        # If there are more steps, set the current temperature to the next value
        if self._temperature_step < len(self._temperature):
            self._current_temperature = self._temperature[self._temperature_step]
            self._current_state = 'START'
        else:
            # If all steps are completed, transition to the end state
            self._current_state = 'END'

    def _finish_test(self):
        # End the test and reset instruments

        # Set the voltage of the Power Supply (PSU) to 0
        self.psu.set_voltage(0)

        # Set the current of the Electronic Load (Eload) and its voltage to 0
        self.eload.write('CURR 0')
        self.eload.write('VOLT 0')

        # Set the stop flag to indicate the test has ended
        self._stop_flag = True

    def _configure_eload(self):
        # Configure the Electronic Load (Eload)

        # Set the current of the Electronic Load (Eload) to 0
        self.eload.write('CURR 0')

    def _configure_equity(self):
        # Configure the Temperature Chamber (Equity)

        # Set the initial temperature of the chamber to 25°C
        self.equity.set_temperature(25.0)

    def _configure_psu(self):
        # Configure the Power Supply (PSU)

        # Set the voltage of the Power Supply (PSU) to 0
        self.psu.set_voltage(0.0)

    def _generate_report(self):
        # Placeholder for generating a test report
        pass

    def _main(self):
        # Main test execution function
        self._stop_flag = False
        while self._stop_flag is False:
            self._finite_state_machine()  # Execute the Finite State Machine
            sleep(self._state_sleep_time)
        print('Test completed. Thank you!')


if __name__ == '__main__':
    load_transient_test = LoadTransientTest()
    load_transient_test._main()
