import serial
import time
import find_com


def connect_with_motor():
    com = find_com.find_device('CH340')
    arduino = serial.Serial(com, baudrate=9600, timeout=1)
    time.sleep(2)  # waits for connection to establish
    return arduino


if __name__ == "__main__":
    arduino = connect_with_motor()
    print("Enter:\n\
          '1' to turn clockwise\n\
          '2' to counterclockwise\n\
          'e' or 'exit' to exit")
    t = 1
    while t:
        var = input()
        if var == '1':
            arduino.write(b'1')
            time.sleep(1)
        elif var == '2':
            arduino.write(b'2')
            time.sleep(1)
        elif var == 'exit' or var == 'e':
            t = 0
        else:
            print('invalid input')
