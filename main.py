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

        self.voltmeter.write(b'P 0.0 \r')

    def sample_setting(self, position):
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
        self.voltmeter.write(b' Q \r')
        u = self.voltmeter.readline().decode()

        return [t, u]

    def __del__(self):
        serial.Serial.close(self.voltmeter)
        self.thermometer.close()
