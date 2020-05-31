import sys
import time
from datetime import datetime
import serial
import math
from tkinter import *

size=900

#command for getting GPS satellites info
command  = [0x40, 0x40, 0x42, 0x62, 0x00, 0x20, 0x0D, 0x0A]

#buffer
resp=[0]*92

#configure the serial connection
ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    #timeout=1
)

master = Tk()

canvas_width = size+5
canvas_height = size+5

w = Canvas(master, 
           width=canvas_width,
           height=canvas_height)
w.pack()

if not ser.isOpen():
    ser.open()

w.delete("all")
w.create_oval(5, 5, size+5, size+5, fill="black", outline="white", width=1)
w.create_line(5, size/2+5, size+5, size/2+5, fill="white")
w.create_line(size/2+5, 5, size/2+5, size+5, fill="white")

while True:
    ser.write(command)

    for i in range(92):
        resp[i]=int.from_bytes(ser.read(1), "little")

    print("Module reported %d sats above the horizon" % resp[4])
    for sat in range(6):
        d=resp[6+sat*14]*256+resp[7+sat*14]
        if(d & 0x8000):
            d = -0x10000 + d
        az=resp[9+sat*14]*256+resp[10+sat*14]
        elev=resp[8+sat*14]
        print("id=%d\taz=%d\telev=%d\tdoppler=%d" % (resp[5+sat*14], az, elev, d))
        x=size/2+5+(math.cos(((az-90)/180.0)*math.pi)*(90.0-elev))*(size/2)/90.0
        y=size/2+5+(math.sin(((az-90)/180.0)*math.pi)*(90.0-elev))*(size/2)/90.0
        w.create_line(x-1, y, x+2, y, fill="red")
        w.create_line(x, y-1, x, y+2, fill="red")
        w.update()

    #time.sleep(1)

ser.close()
sys.exit()
