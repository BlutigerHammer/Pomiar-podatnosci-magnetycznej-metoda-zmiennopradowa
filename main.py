import serial
import time
import pyvisa
import find_com


class Aparature:

    def __init__(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        # ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
        self.thermometer = rm.open_resource('USB0::0x164E::0x0DAD::TW00020217::INSTR')

        com = 'COM10'
        self.voltmeter = serial.Serial(com, baudrate=9600, timeout=1)

        com = find_com.find_device('CH340')
        self.arduino = serial.Serial(com, baudrate=9600, timeout=1)

        time.sleep(2)
        self.voltmeter.write(b'P -90 \r')


    def sample_setting(self, position):
        if self.change_position(1, 1):
            position += 1
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        return [position, voltage]

    def phase_setting(self, phase):
        self.voltmeter.write(bytes(f"P {phase} \r", encoding='utf8'))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        return [phase, voltage]

    def measurement(self):
        temperature = self.thermometer.query("MEAS:VOLT:DC?")
        temperature = volts_to_kelvins(float(temperature))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [temperature, voltage]

    def sensivity_ranging(self, voltage):
        if voltage > 10:
            self.voltmeter.write(b' K 22 \r')  # Sensitivity Up
        if voltage < 10:
            self.voltmeter.write(b' K 23 \r')  # Sensitivity Down

    def change_position(self, direction, distance):
        data_to_arduino = str(direction) + str(distance)
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))
        while True:
            distance_made = arduino.readline().decode()
            if len(distance_made) > 0:
                return int(distance_made)

    def __del__(self):
        serial.Serial.close(self.voltmeter)
        self.thermometer.close()


def volts_to_kelvins(x):
    x *= 1000  # volts to milivolts
    x += 1  # Cold Junction Compensation
    return 272.99294 + 25.83372 * x - 0.78202 * x ** 2 + 0.23669 * x ** 3 + 0.07095 * x ** 4 + 0.01113 * x ** 5

