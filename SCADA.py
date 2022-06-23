from tkinter import *
import sqlite3 as database


result = []



def get_last_values_from_database(generator_table):
    global result
    with database.connect("scada.db") as connection:
        query = """SELECT
        Time,
        Generator_number,
        Generator_Total_Percent_Current,
        Engine_Oil_Temperature,
        Engine_Coolant_Temperature,
        Engine_rpm,
        Engine_operating_hours,
        Exhaust_Left_Temperature,
        Exhaust_Right_Temperature,
        Fuel_Pressure,
        Oil_Filter_Diff,
        Fuel_Filter_Diff,
        Fuel_Consumption
        FROM {table} ORDER BY rowid DESC LIMIT 1"""
        cur = connection.cursor()
        cur.execute(query.format(table=generator_table))
        result = cur.fetchall()
        
class Generator:
       
    def __init__(self, master, generator_number, row, column):

        self.generator_number = Label(root, text=generator_number, width=18, height=2,font=("Arial", 14, "bold"), bg='yellow', relief=RIDGE)
        self.generator_number.grid(row=row, column=column)
        self.engine_speed = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.engine_speed.grid(row=row + 1, column=column)
        self.fuel_pressure = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.fuel_pressure.grid(row=row + 2, column=column)
        self.fuel_diff = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.fuel_diff.grid(row=row + 3, column=column)
        self.oil_pressure = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.oil_pressure.grid(row=row + 4, column=column)
        self.oil_diff = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.oil_diff.grid(row=row + 5, column=column)
        self.oil_temp = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.oil_temp.grid(row=row + 6, column=column)
        self.coolant_temp = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.coolant_temp.grid(row=row + 7, column=column)
        self.right_exhaust = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.right_exhaust.grid(row=row + 8, column=column)
        self.left_exhaust = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.left_exhaust.grid(row=row + 9, column=column)
        self.fuel_consumption = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.fuel_consumption.grid(row=row + 10, column=column)
        self.load = Label(root, text='None', height=2, font="Calibri 12", bg='yellow')
        self.load.grid(row=row + 11, column=column)
        
    def label_refresh(self):
        self.engine_speed['text'] = result[0][5]
        self.fuel_pressure['text'] = result[0][9]
        self.fuel_diff['text'] = result[0][11]
        self.oil_pressure['text'] = 0
        self.oil_diff['text'] = result[0][10]
        self.oil_temp['text'] = result[0][3]
        self.coolant_temp['text'] = result[0][4]
        self.right_exhaust['text'] = result[0][8]
        self.left_exhaust['text'] = result[0][7]
        self.fuel_consumption['text'] = result[0][12]
        self.load['text'] = 0
        
root = Tk()
root.title('ДЭС "Крабозаводское"')
root.geometry('1024x800')
root['background']='yellow'

    
first_generator = Generator(root, 'ДГУ №1', 0, 1)
second_generator = Generator(root, 'ДГУ №2', 0, 2)
third_generator = Generator(root, 'ДГУ №3', 0, 3)
fourth_generator = Generator(root, 'ДГУ №4', 0, 4)


def refresh_parameters():
    get_last_values_from_database('generator_1')
    first_generator.label_refresh()
    get_last_values_from_database('generator_2')
    second_generator.label_refresh()
    root.after(1, refresh_parameters)

label_1 = Label(root, text='Скорость вращения, об/мин', height=2, font="Calibri 12", bg='yellow')
label_1.grid(row=1, column=0)
label_2 = Label(root, text='Давление топлива, кПа\t', height=2, font="Calibri 12", bg='yellow')
label_2.grid(row=2, column=0)
label_3 = Label(root, text='Дифферент топлива, кПа\t', height=2, font="Calibri 12", bg='yellow')
label_3.grid(row=3, column=0)
label_4 = Label(root, text='Давление масла, кПа\t', height=2, font="Calibri 12", bg='yellow')
label_4.grid(row=4, column=0)
label_5 = Label(root, text='Дифферент масла, кПа\t', height=2, font="Calibri 12", bg='yellow')
label_5.grid(row=5, column=0)
label_6 = Label(root, text='Температура масла, С\t', height=2, font="Calibri 12", bg='yellow')
label_6.grid(row=6, column=0)
label_7 = Label(root, text='Температура антифриза, С\t', height=2, font="Calibri 12", bg='yellow')
label_7.grid(row=7, column=0)
label_8 = Label(root, text='Температура пр. турбины, С', height=2, font="Calibri 12", bg='yellow')
label_8.grid(row=8, column=0)
label_9 = Label(root, text='Температура лв. турбины, С', height=2, font="Calibri 12", bg='yellow')
label_9.grid(row=9, column=0)
label_10 = Label(root, text='Расход топлива, л/ч\t', height=2, font="Calibri 12", bg='yellow')
label_10.grid(row=10, column=0)
label_11 = Label(root, text='Загрузка генератора, кВт\t', height=2, font="Calibri 12", bg='yellow')
label_11.grid(row=11, column=0)

###########Main programm loop################

refresh_parameters()

root.mainloop()

