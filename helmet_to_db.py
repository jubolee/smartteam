'''
This file is used to populated the database. It is not used in the main program,
and should only be used for single use test purpose when adding db classes. 

NOTE: All connections use relative path
'''
import sqlite3
import datetime
from database import Data
import random
import serial
import json
import time
import subprocess
import csv
import math
import signal

SENSOR_DATA_PATH = 'sensor_data.csv'

# Code was written to handle shutdowns with keyboardinterrupt, so make it happy.
def shutdown (signal, frame):
    raise KeyboardInterrupt()

###################################
# MAIN LOOP
###################################
def main():
    signal.signal(signal.SIGTERM, shutdown)

    # Read data from bluetooth port 0, populate data into database.db
    try:
        ser = serial.Serial(port='/dev/rfcomm0', baudrate=9600)
    except Exception:
        print("Bluetooth device not available")
        exit()
    error_count = 0
    print("ENTERING LOOP")
    while True:
        try:
            bt=ser.read_until(b'\x3B').decode("utf-8").replace(';', '') .split(',')
            assert(8 == len(bt))
            bt = [float(x) for x in bt]
            bt_data = Data(bt[0], bt[1], bt[2], bt[3], 0, bt[4], bt[5], bt[6])
            bt_data.write()
        except KeyboardInterrupt:
            print('KeyboardInterrupt found, exiting')
            exit()
        except Exception as e:
            print(f'error with reading bt_data: {e}')
            error_count += 1
            if error_count == 10:
                print('connection not found, exiting')
                exit()
