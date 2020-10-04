import serial.tools.list_ports


def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def find_device(name):
    comcomm_port = 'None'
    ports_found = get_ports()
    for port in ports_found:
        str_port = str(port)
        
        if name in str_port:
            split_port = str_port.split(' ')
            comcomm_port = (split_port[0])
    if comcomm_port == 'None':
        print('port not found')

    return comcomm_port
            

if __name__ == '__main__':
    # connect_port = find_device('CH340')  # 'CH340'-Arduino clone name
    all_ports = get_ports()
    for port in all_ports:
        x = str(port)
        print(x)
        x = x.split(' ')
        print('split\n', x)

    '''
    if connect_port != 'None':
        ser = serial.Serial(connect_port, baudrate=9600, timeout=1)
        print('Connected to ' + connect_port)

    else:
        print('Connection Issue!')
    '''
