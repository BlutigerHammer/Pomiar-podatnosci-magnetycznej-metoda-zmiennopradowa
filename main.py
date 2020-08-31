import serial
import time
import pyvisa


class Aparature:

    def __init__(self):
        rm = pyvisa.ResourceManager()
        rm.list_resources()
        # ('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
        self.thermometer = rm.open_resource('USB0::0x164E::0x0DAD::TW00020217::INSTR')
        # print(thermometer.query("*IDN?"))

        com = 'COM10'
        self.voltmeter = serial.Serial(com, baudrate=9600, timeout=1)
        time.sleep(2)

        self.voltmeter.write(b'P -90 \r')

    def sample_setting(self):
        position = 0
        # there will be connection with function which controls servo
        self.voltmeter.write(b' Q \r')
        u = self.voltmeter.readline().decode()
        return [position, u]

    def phase_setting(self, phase):
        self.voltmeter.write(bytes(f"P {phase} \r", encoding='utf8'))
        self.voltmeter.write(b' Q \r')
        u = self.voltmeter.readline().decode()
        return [phase, u]

    def measurement(self):
        t = self.thermometer.query("MEAS:VOLT:DC?")
        t = voltage_to_kelvins(float(t))
        self.voltmeter.write(b' Q \r')
        u = self.voltmeter.readline().decode()
        u = float(u)

        return [t, u]

    def sensivity_ranging(self, voltage):
        if voltage > 10:
            self.voltmeter.write(b' K 22 \r')  # Sensitivity Up
        if voltage < 10:
            self.voltmeter.write(b' K 23 \r')  # Sensitivity Down

    def __del__(self):
        serial.Serial.close(self.voltmeter)
        self.thermometer.close()


def voltage_to_kelvins(x):
    x *= 1000  # volts to milivolts
    x += 1  # Cold Junction Compensation
    return 272.99294 + 25.83372 * x - 0.78202 * x ** 2 + 0.23669 * x ** 3 + 0.07095 * x ** 4 + 0.01113 * x ** 5
