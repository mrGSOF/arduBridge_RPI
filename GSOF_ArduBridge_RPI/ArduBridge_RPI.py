#!/usr/bin/env python
"""
Class that emulates the ArduBridge API over the RPI hardware

By: Guy Soffer
Date: 04/June/2021
"""

import smbus
import spidev
import gpiozero
#import RPi.GPIO as GPIO

class ArduBridge():
    def __init__(self, COM, baud):
        self.i2c = arduBridgeI2C( bus=smbus.SMBus(1) )
        self.spi = arduSPI( bus=spidev(0,0) )
        self.spi.setFreq(1000000) #< Default clock frequency is 1 Mhz
#        self.spi = arduSPI( bus=spidev.SpiDev() )
#        self.spi.open(0,0)
        self.gpio = arduBridgeGPIO( gpiozero.pins.rpigpio.GPIO )

    def OpenClosePort(self, val):
        return
    
class arduBridgeI2C():
    def __init__(self, bus):
        self.i2c = bus

    def readRegister(self, dev, reg, N):
        return self.i2c.read_i2c_block_data(dev, reg, N)
    
    def writeRegister(self, dev, reg, vDat):
        return self.i2c.write_i2c_block_data(dev, reg, vDat)
    
    def setFreq(self, freq):
        #self.i2c. = freq
        return

class arduBridgeSPI():
    MODE0 = 0
    MODE1 = 1
    MODE2 = 2
    MODE3 = 3
    OFF   = 4

    def __init__(self, bus):
        self.spi = spi

    def setMode(self, mode, v=False):
        modeDesc = ("SPI_MODE0:\nClock is normally low (CPOL = 0)\nData is sampled on the transition from low to high (leading edge) (CPHA = 0)",
                    "SPI_MODE1:\nClock is normally low (CPOL = 0)\nData is sampled on the transition from high to low (trailing edge) (CPHA = 1)",
                    "SPI_MODE2:\nClock is normally high (CPOL = 1)\nData is sampled on the transition from high to low (leading edge) (CPHA = 0)",
                    "SPI_MODE3:\nClock is normally high (CPOL = 1)\nData is sampled on the transition from low to high (trailing edge) (CPHA = 1)")
        self.spi.mode = mode&0b11
        if v:
            if mode < self.OFF:
                print(modeDesc[mode])
            else:
                print("SPI-OFF")
        self.spi.mode = mode

    def setFreq(self, freq):
        self.spi.max_speed_hz = freq
        
    def write_read(self, vByte):
        reply = self.spi.writebytes2(vByte) #Read the recevied bytes
  
        if self.v:
            print('SPI-Tx: %s', par=(dev, vByte))
            print('SPI-Rx: %s', par=(dev, reply))
        return reply

class arduBridgeGPIO():
    OUTPUT = 0 #< To set the pin to digital output mode
    INPUT = 1  #< To set the pin to digital input mode

    def __init__(self, gpio):
        self.gpio = gpio

    def digitalWrite(self, pin, val):
        self.gpio.output(pin, val)
        return 1
    
    def digitalRead(self, pin):
        return self.gpio.input(pin)
    
    def setMode(self, pin, mode, init=0):
        self.pinMode(pin, mode, init)

    def pinMode(self, pin, mode, init=0):
        if mode == self.OUTPUT:
            self.digitalWrite(pin, init):
            self.gpio.setup(pin, self.gpio.OUT)
        else:
            self.gpio.setup(pin, self.gpio.IN)

    def pinPulse(self, pin, onTime):
        """
        Pulse the the specific pin# on the arduino GPO
        """
        self.digitalWrite(pin, 1)
        time.sleep(onTime)
        self.digitalWrite(pin, 0)
        return 1

    def servoWrite(self, val):
        return
##        val = int(val)
##        vDat = [ord('S'), val]
##        self.comm.send(vDat)
##        reply = self.comm.receive(1)
##        CON_prn.printf('SERVO: %d - %s', par=(val, self.RES[reply[0]]), v=self.v)
##        return 1
