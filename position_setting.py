import serial
import time
import find_com


def connect_with_motor():
    com = find_com.find_device('CH340')
    arduino = serial.Serial(com, baudrate=9600, timeout=1)
    time.sleep(2)  # waits for connection to establish
    return arduino

def setting_to_position(actual_position, target_position):
    x = target_position - actual_position
    if x > 0:
        direction = 1
    elif x < 0:
        direction = 0
    else:
        print("ERROR")
    i=0
    while i<x:
        if arduino.in_waiting:
            arduino.write(bytes(f"{direction}", encoding='utf8'))
            print(i)
            i += 1
            time.sleep(0.4)
        else:
            time.sleep(1)

        
        

    
if __name__ == "__main__":
    arduino = connect_with_motor()
    setting_to_position(0,10)
    '''
    while True:
        while arduino.in_waiting:
            a = arduino.readline().decode()
            print(a)
            if a == 1:
                arduino.write(b'1')
            elif a == 0:
                arduino.write(b'0')
            else:
                print('Error')
        time.sleep(1)
    '''
            
    '''
    print("Enter:\n\
          '1' to turn clockwise\n\
          '0' to counterclockwise\n\
          'e' or 'exit' to exit")
    t = 1
    while t:
        var = input()
        if var == '1':
            arduino.write(b'1')
            time.sleep(1)
        elif var == '0':
            arduino.write(b'0')
            time.sleep(1)
        elif var == 'exit' or var == 'e':
            t = 0
        else:
            print('invalid input')
        aaa = arduino.readline().decode()
        print(aaa)
    '''
