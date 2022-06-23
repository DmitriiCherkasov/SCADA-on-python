import sqlite3 as database
import serial
from datetime import datetime

listener = serial.Serial(port='COM4', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                             bytesize=serial.EIGHTBITS, timeout=None)
response = ''
request = ''

generator_data = [] 

def parsing_response_for_generator():
    generator_data.append(datetime.now())
    generator_data.append(response[1:2])# Generator_number
    generator_data.append(int(int(response[138:142], 16) * 0.0078125 - 251)) # Generator_Total_Percent_Current
    generator_data.append(int(int(response[238:242], 16) * 0.03125 - 273)) # Engine_Oil_Temperature
    generator_data.append(int(int(response[242:246], 16) * 0.125)) # Engine Oil Pressure
    generator_data.append(int(int(response[246:250], 16) * 0.03125 - 273))# Engine_Coolant_Temperature
    generator_data.append(int(int(response[254:258], 16) * 0.125)) # Engine_rpm
    generator_data.append(int(int(response[258:266], 16) * 0.05)) # Engine_operating_hours
    generator_data.append(int(int(response[406:410], 16) * 0.03125 - 273)) # Exhaust_Left_Temperature
    generator_data.append(int(int(response[410:414], 16) * 0.03125 - 273)) # Exhaust_Right_Temperature
    generator_data.append(int(int(response[430:434], 16) * 0.125)) # Fuel_Pressure
    generator_data.append(int(int(response[446:450], 16) * 0.125)) # Oil_Filter_Diff
    generator_data.append(int(int(response[450:454], 16) * 0.125)) # Fuel_Filter_Diff
    generator_data.append(int(int(response[466:470], 16) * 0.05)) # Fuel_Consumption

    
     

#Get new data and put in its generator_data and then in database
def sniffing_parameters():
    request = listener.read().hex()
    global response
    global generator_data
    generator_data = []
    if request in ['01', '02', '03', '04']:
        request += listener.read().hex()
        if request in ['0103', '0203', '0303', '0403']:
            request += listener.read(2).hex()
            if request in ['0103008c', '0203008c', '0303008c', '0403008c']:
                request = request + listener.read(4).hex()
                response = listener.read(245).hex()

                if response[:2] =='01':   
                    parsing_response_for_generator()
                    with database.connect("scada.db") as con:
                        cur = con.cursor()
                        cur.execute("""INSERT INTO generator_1 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                    generator_data)
                print('Get new parameters')
                elif response[:2] =='02':   
                    parsing_response_for_generator()
                    with database.connect("scada.db") as con:
                        cur = con.cursor()
                        cur.execute("""INSERT INTO generator_2 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                    generator_data)
                print('Get new parameters')
                elif response[:2] =='03':   
                    parsing_response_for_generator()
                    with database.connect("scada.db") as con:
                        cur = con.cursor()
                        cur.execute("""INSERT INTO generator_3 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                    generator_data)
                print('Get new parameters')
                elif response[:2] =='04':   
                    parsing_response_for_generator()
                    with database.connect("scada.db") as con:
                        cur = con.cursor()
                        cur.execute("""INSERT INTO generator_4 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                    generator_data)
                print('Get new parameters')
while True: 
    sniffing_parameters()
                    
