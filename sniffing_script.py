import serial
import time
from datetime import datetime
import os
dir_name = 0

# Create a database directory
def create_dir():
    global dir_name
    dir_name = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
    os.mkdir(f'C:\\Users\\ДЭС\\Desktop\\Scada\\database\\{dir_name}')
    with open(f'C:\\Users\\ДЭС\\Desktop\\Scada\\database\\{dir_name}\\{dir_name}.txt', 'w') as f:
            f.write('\t')
            for values in generator_1_parameters.keys():
                f.write(f'{values}\t')
            f.write('\n')


# Add time and parameters in a log
def write_log(generator_dictionary):
    global dir_name
    with open(f'C:\\Users\\ДЭС\\Desktop\\Scada\\database\\{dir_name}\\{dir_name}.txt', 'a') as f:
        current_datetime = datetime.now()
        f.write(f'{current_datetime}\t')
        for values in generator_dictionary.values():
            f.write(f'{values}\t')
        f.write('\n')


listener = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                             bytesize=serial.EIGHTBITS, timeout=None)
request_start_list = ['01', '02', '03', '04']
request_start_list_two = ['0103', '0203', '0303', '0403']
request_start_list_four = ['0103008c', '0203008c', '0303008c', '0403008c']
response = ''
request = ''

## Dictionary for generator with its parameters
generator_1_parameters = {'Generator number': None, 'Engine rpm': None, 'Engine Coolant Temperature': None, 'Generator Total Percent Current': None,
                          'Engine Oil Temperature': None, 'Engine Oil Pressure': None, 'Exhaust Left Temperature': None,
                          'Exhaust Right Temperature': None, 'Fuel Pressure': None, 'Oil Filter Diff': None,
                          'Fuel Filter Diff': None, 'Fuel Consumption': None}
generator_2_parameters = {'Generator number': None, 'Engine rpm': None, 'Engine Coolant Temperature': None, 'Generator Total Percent Current': None,
                          'Engine Oil Temperature': None, 'Engine Oil Pressure': None, 'Exhaust Left Temperature': None,
                          'Exhaust Right Temperature': None, 'Fuel Pressure': None, 'Oil Filter Diff': None,
                          'Fuel Filter Diff': None, 'Fuel Consumption': None}
generator_3_parameters = {'Generator number': None, 'Engine rpm': None, 'Engine Coolant Temperature': None, 'Generator Total Percent Current': None,
                          'Engine Oil Temperature': None, 'Engine Oil Pressure': None, 'Exhaust Left Temperature': None,
                          'Exhaust Right Temperature': None, 'Fuel Pressure': None, 'Oil Filter Diff': None,
                          'Fuel Filter Diff': None, 'Fuel Consumption': None}
generator_4_parameters = {'Generator number': None, 'Engine rpm': None, 'Engine Coolant Temperature': None, 'Generator Total Percent Current': None,
                          'Engine Oil Temperature': None, 'Engine Oil Pressure': None, 'Exhaust Left Temperature': None,
                          'Exhaust Right Temperature': None, 'Fuel Pressure': None, 'Oil Filter Diff': None,
                          'Fuel Filter Diff': None, 'Fuel Consumption': None}

## Dictionary for each generator
generator_parameters_dict = [generator_1_parameters, generator_2_parameters,
                             generator_3_parameters, generator_4_parameters]


def parsing_response_for_generator(generator_dictionary):
    generator_dictionary['Generator number'] = response[1:2]
    generator_dictionary['Generator Total Percent Current'] = int(((int(response[138:142], 16) * 0.0078125 - 251) / 0.8) * 18)
    generator_dictionary['Engine Oil Temperature'] = int(int(response[238:242], 16) * 0.03125 - 273) # 1 register
    generator_dictionary['Engine Oil Pressure'] = int(int(response[242:246], 16) * 0.125) # 1 register
    generator_dictionary['Engine Coolant Temperature'] = int(int(response[246:250], 16) * 0.03125 - 273) # 1 register
    generator_dictionary['Engine rpm'] =  int(int(response[254:258], 16) * 0.125) # 1 register
    generator_dictionary['Exhaust Left Temperature'] = int(int(response[406:410], 16) * 0.03125 - 273)
    generator_dictionary['Exhaust Right Temperature'] = int(int(response[410:414], 16) * 0.03125 - 273)
    generator_dictionary['Fuel Pressure'] = int(int(response[430:434], 16) * 0.125) # 1 register   
    generator_dictionary['Oil Filter Diff'] = int(int(response[446:450], 16) * 0.125)
    generator_dictionary['Fuel Filter Diff'] = int(int(response[450:454], 16) * 0.125)
    generator_dictionary['Fuel Consumption'] = int(int(response[466:470], 16) * 0.05)
    
      
#Get new parameter and put in its generator dictionary
def sniffing_parameters():
    request = listener.read().hex()
    global response
    if request in ['01', '02', '03', '04']:
        request += listener.read().hex()
        if request in ['0103', '0203', '0303', '0403']:
            request += listener.read(2).hex()
            if request in ['0103008c', '0203008c', '0303008c', '0403008c']:
                request = request + listener.read(4).hex()
                response = listener.read(245).hex()
                if response[:2] =='01':   
                    parsing_response_for_generator(generator_1_parameters)
                    write_log(generator_1_parameters)
                elif response[:2] =='02':   
                    parsing_response_for_generator(generator_2_parameters)
                    write_log(generator_2_parameters)
                elif response[:2] =='03':   
                    parsing_response_for_generator(generator_3_parameters)
                    write_log(generator_3_parameters)
                elif response[:2] =='04':   
                    parsing_response_for_generator(generator_4_parameters)
                    write_log(generator_4_parameters)

                    
start_time = time.time()
time_step = 5
create_dir()

while True:
    current_time = time.time()
    if current_time >= start_time + time_step:
        print('Get')
        start_time = current_time
        create_dir()
    sniffing_parameters()
