from time import sleep
from widgetlords.pi_spi import *
import numpy as np
from widgetlords import *
import concurrent.futures
from pynput import mouse
import pandas
import time
import sys
import threading
import RPi.GPIO as GPIO
from pymodbus.client.sync import ModbusSerialClient
import serial.tools.list_ports as portlist


init()
output = Mod2AO(False)
output2=Mod2AO(True)
minSpeed=745
maxSpeed=(int)((3723+745)/2)
inputs=Mod8AI()

pump = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=5,
    parity='N',
    stopbits=1,
    bytesize=8
)
flowmeter = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyACM0',
    baudrate=38400,
    timeout=5,
    parity='N',
    stopbits=1,
    bytesize=8
)

pump.connect()
flowmeter.connect()

def setPumpSpeed(speed):
    pump.write_register(1, speed, unit=1)

def runPump():
    pump.write_register(0,1,unit=1)

def stopPump():
    pump.write_register(0,0,unit=1)
    
def getFlowrate():
    try:
        flowrate=flowmeter.read_holding_registers(address = 4,count=1,unit=1).registers[0]
        flowratescale=flowmeter.read_holding_registers(address = 31,count=1,unit=1).registers[0]
        return flowrate/flowratescale
    except:
        return 0

def getDensity():
    density=flowmeter.read_holding_registers(address = 2,count=1,unit=1).registers[0]
    densityscale=flowmeter.read_holding_registers(address = 29,count=1,unit=1).registers[0]
    return density/densityscale

def getTemp():
    temp=flowmeter.read_holding_registers(address = 3,count=1,unit=1).registers[0]
    tempscale=flowmeter.read_holding_registers(address = 30,count=1,unit=1).registers[0]
    return temp/tempscale

def addWater(time):  #opens water valve for time seconds
    stopAdd = threading.Timer(time, stopWater)
    output2.write_single(1,1750)
    print("Adding water for "+ str(time)+ " seconds.")
    stopAdd.start()
    
def stopWater():
    output2.write_single(1,0)
    print("Done")

def dumpMud(time):  #opens water valve for time seconds
    stopAdd = threading.Timer(time, stopDump)
    output2.write_single(0,1750)
    print("Dumping Mud for "+ str(time)+ " seconds.")
    stopAdd.start()
    
def stopDump():
    output2.write_single(0,0)
    print("Done")
    
def distancethread():
    GPIO.setmode(GPIO.BCM)
    trigger=23
    echo=24
    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trigger, True)
    time.sleep(.00001)
    GPIO.output(trigger, False)
    starttime=time.time()
    while GPIO.input(echo)==0:
        starttime=time.time()
    while GPIO.input(echo)==1:
        endtime=time.time()
    return (endtime-starttime)*34300/2
#     start=time.time()
#     arrived=False
#     while time.time()-start<1:
#         if GPIO.input(echo)==0 and not arrived:
#             start=time.time()
#         elif GPIO.input(echo)==0:
#             bouncetime=time.time()-start
#             GPIO.cleanup()
#             #print(bouncetime*34300/2)
#             return bouncetime*34300/2
#         if GPIO.input(echo)==1:
#             arrived=True

def distance ():
    with concurrent.futures.ThreadPoolExecutor()as executor:
        future = executor.submit(distancethread)
        return future.result()

def getpH(): #returns pH and temp
    return((counts_to_value(inputs.read_single(1), 745, 3723, 4, 20 )+.03)*.875-3.5, (counts_to_value(inputs.read_single(0), 745, 3723, 4, 20)+.03)*6.25-25)

# outFile=open("30Lpumponmixeron.txt", "w")
# while True:
#     d=distance()
#     print(d)
#     print(d, file = outFile)
#     outFile.flush()
#     time.sleep(1)
