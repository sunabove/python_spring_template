#!/usr/bin/python
"""
Released under the MIT License
Copyright 2015 MrTijn/Tijndagamer
"""

# Import the MPU6050 class from the MPU6050.py file
from MPU6050 import MPU6050
from time import sleep

# Create a new instance of the MPU6050 class
sensor = MPU6050(0x68)

count = 0 
while 1 :
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    print()
    print(  "-"*40 )
    print( f"Count: {count:d}" )
    print(  "-"*40 )
    print("Accelerometer data")
    print("x: " + str(accel_data['x']))
    print("y: " + str(accel_data['y']))
    print("z: " + str(accel_data['z']))
    print(  "-"*40 )

    print("Gyroscope data")
    print(  "-"*40 )
    print("x: " + str(gyro_data['x']))
    print("y: " + str(gyro_data['y']))
    print("z: " + str(gyro_data['z']))
    print(  "-"*40 )

    print("Temp: " + str(temp) + " C")
    print(  "-"*40 )
    
    sleep(1)
pass