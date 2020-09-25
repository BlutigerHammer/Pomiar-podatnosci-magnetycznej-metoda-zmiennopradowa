import serial
import time
import pyvisa
import find_com
import math


class Aparature:

    def __init__(self):
        try:
            rm = pyvisa.ResourceManager()
            rm.list_resources()
            self.thermometer = rm.open_resource('USB0::0x164E::0x0DAD::TW00020217::INSTR')
        except pyvisa.VisaIOError:
            print('Multimetr Picotest nie jest podłączony poprawnie')

        try:
            com = find_com.find_device('USB Serial Port')
            self.voltmeter = serial.Serial(com, baudrate=9600, timeout=1)
        except Exception:
            print('Lock-in-Amplifier nie jest podłączony poprawnie')


        try:
            com = find_com.find_device('CH340')
            self.arduino = serial.Serial(com, baudrate=9600, timeout=1)
        except Exception:
            print('Arduino nie jest podłączone poprawnie')

        time.sleep(2)
        self.voltmeter.write(b'P -87 \r')
        self.voltmeter.write(b'G 15 \r')  #set sensivity to 500uV

    def sample_setting(self, position):
        if self.change_position(1, 1):
            position += 1
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        time.sleep(1)
        return [position, voltage]

    def phase_setting(self, phase):
        self.voltmeter.write(bytes(f"P {phase} \r", encoding='utf8'))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [phase, voltage]

    def measurement(self):
        temperature = self.thermometer.query("MEAS:VOLT:DC?")
        temperature = volts_to_kelvins(float(temperature))
        self.voltmeter.write(b' Q \r')
        voltage = self.voltmeter.readline().decode()
        voltage = float(voltage)
        return [temperature, voltage]

    def change_sensivity(self, voltage):
        order_of_magnitude = math.floor(math.log(voltage, 10))
        x = (order_of_magnitude + 8)*3 + 1
        first_digit = voltage/10**order_of_magnitude
        if first_digit < 1:
            x += 0
        elif first_digit < 2:
            x += 1
        elif first_digit < 5:
            x += 2
        else:
            x += 3
        self.voltmeter.write(bytes(f"G {x} \r", encoding='utf8'))



    def change_position(self, direction, distance):
        data_to_arduino = str(direction) + str(distance) + '\n'
        self.arduino.write(bytes(f"{data_to_arduino}", encoding='utf8'))
        while True:
            distance_made = self.arduino.readline().decode()
            if len(distance_made) > 0:
                return int(distance_made)

    def __del__(self):
        try:
            serial.Serial.close(self.voltmeter)
            self.thermometer.close()
        except AttributeError:
            print("AttributeError")

    def cricital_message(self, text):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(text)
        msgBox.setWindowTitle("")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)


def volts_to_kelvins(x):
    x *= 1000  # volts to milivolts
    x += 1  # Cold Junction Compensation
    return 272.99294 + 25.83372 * x - 0.78202 * x ** 2 + 0.23669 * x ** 3 + 0.07095 * x ** 4 + 0.01113 * x ** 5

