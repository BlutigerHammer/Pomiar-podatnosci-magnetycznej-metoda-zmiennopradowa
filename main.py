import serial
import time
import pyvisa

rm = pyvisa.ResourceManager()
rm.list_resources()
('ASRL1::INSTR', 'ASRL2::INSTR', 'GPIB0::12::INSTR')
thermometer = rm.open_resource('USB0::0x164E::0x0DAD::TW00020217::INSTR')
# print(thermometer.query("*IDN?"))

com = 'COM10'
voltmeter = serial.Serial(com, baudrate=9600, timeout=1)
time.sleep(2)

voltmeter.write(b'P 0.0 \r')

def sample_setting():
    with open ('data\\sample_setting.txt', 'w') as f:
        f.write('Position\tU:\n')
        for i in range(0, 100):
            position = 0
            #there will be connection with function which controls servo
            position += '\t'
            print('position:', position)
            f.write(position)
            
            voltmeter.write(b' Q \r')
            u = voltmeter.readline().decode()
            u += '\n'
            print('U', u)
            f.write(u)    

def phase_setting():
    with open ('data\\phase.txt', 'w') as f:
        f.write('Phase[deg]\tU:\n')
        for i in range(0, 181):
            voltmeter.write(bytes(f"P {i} \r", encoding='utf8'))
            phase = i + '\t'
            print('phase:', phase)
            f.write(phase)
            
            voltmeter.write(b' Q \r')
            u = voltmeter.readline().decode()
            u += '\n'
            print('U', u)
            f.write(u)         


def measurement():
    with open ('data\\measurement.txt', 'w') as f:
        f.write('Temp:\tU:\n')
        for i in range(5*60):
            print(i)
            t = thermometer.query("MEAS:VOLT:DC?")
            t = str(t)
            t += '\t'
            print('temp:', t)
            f.write(t)

            voltmeter.write(b' Q \r')
            u = voltmeter.readline()
            u = str(u)
            u = u[2:-3]
            u += '\n'
            print('U', u)
            f.write(u)



f.close()
serial.Serial.close(voltmeter)
thermometer.close()
