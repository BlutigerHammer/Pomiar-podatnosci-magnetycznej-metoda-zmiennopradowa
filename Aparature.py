import serial
import time
import pyvisa
import find_com
import math


class Aparature:

    def __init__(self):
        self.sensivities = {1: '10nV', 2: '20nV', 3: '50nV', 4: '100nV', 5: '200nV', 6: '500nV', 7: '1uV', 8: '2uV',
                            9: '5uV', 10: '10uV', 11: '20uV', 12: '50uV', 13: '100uV', 14: '200uV', 15: '500uV',
                            16: '1mV', 17: '2mV', 18: '5mV', 19: '10V', 20: '20mV', 21: '50mV', 22: '100mV',
                            23: '200mV', 24: '500mV'}
        self.cold_junction_compesation = 0.87  # cold junction compesation for 20 deg Celsjus
        errors = []
        try:
            rm = pyvisa.ResourceManager()
            self.thermometer = rm.open_resource('USB0::0x164E::0x0DAD::TW00020217::INSTR')
        except pyvisa.VisaIOError:
            errors.append('Multimetr M3500A')

        try:
            com = find_com.find_device('USB Serial Port')
            self.voltmeter = serial.Serial(com, baudrate=9600, timeout=1)
        except OSError:
            errors.append('Lock-in Amplifier SR510')


        try:
            com = find_com.find_device('CH340')
            self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
        except OSError:
            errors.append('Płytka Arduino')

        if errors:
            raise Exception(f"{', '.join(errors)}")

        else:
            time.sleep(2)
            self.voltmeter.write(b'P -87 \r')  # set phase to -87
            self.voltmeter.write(b'G 15 \r')  # set sensivity to 500uV
            self.voltmeter.write(b'T 1,6 \r')  # set pre time constant to 300ms
            self.voltmeter.write(b'T 2,1 \r')  # set post time constant to 0.1ms

    def sample_setting(self, position):
        if self.change_position(1, 1):
            position += 1
        time.sleep(1.5)
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [position, voltage]

    def phase_setting(self, phase):
        self.voltmeter.write(bytes(f"P {phase} \r", encoding='utf8'))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [phase, voltage]

    def measurement(self):
        temperature = self.thermometer.query("MEAS:VOLT:DC?")
        temperature = self.volts_to_kelvins(float(temperature))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [temperature, voltage]

    def change_sensivity(self, voltage):
        order_of_magnitude = math.floor(math.log(voltage, 10))
        sensivity = (order_of_magnitude + 8) * 3 + 1
        first_digit = voltage / 10 ** order_of_magnitude
        if first_digit < 1:
            sensivity += 0
        elif first_digit < 2:
            sensivity += 1
        elif first_digit < 5:
            sensivity += 2
        else:
            sensivity += 3
        sensivity = min(sensivity, 24)
        self.voltmeter.write(bytes(f"G {sensivity} \r", encoding='utf8'))
        return self.sensivities[sensivity]

    def change_position(self, direction, distance):
        data_to_arduino = str(direction) + str(distance) + '\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))
        while True:
            distance_made = self.arduino.readline().decode()
            if len(distance_made) > 0:
                return int(distance_made)


    def volts_to_kelvins(self, x):
        x *= 1000  # volts to milivolts
        x += self.cold_junction_compesation
        return 272.99294 + 25.83372 * x - 0.78202 * x ** 2 + 0.23669 * x ** 3 + 0.07095 * x ** 4 + 0.01113 * x ** 5

    def __del__(self):
        try:
            serial.Serial.close(self.voltmeter)
            self.thermometer.close()
        except AttributeError:
            print("AttributeError")
