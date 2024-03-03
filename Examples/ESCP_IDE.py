#!/usr/bin/env python
"""
Script to build an ArduBridge environment
To customize the environment to your needs. You will need to change
he parameters in the "PARAMETER BLOCK" in the __main__ section

By: Guy Soffer
Date: 08/Mar/2021
"""

#Basic modules to load
import time
from GSOF_ArduBridge_RPI import ArduBridge_RPI as ArduBridge
from Modules import ESS_ESCP_lib
from Modules import DS3231_lib
from TestScripts import testScripts

escp_dev = 0x28
pin_escpON = 7 #9

def close():
    ardu.OpenClosePort(0)
    print('COM port is closed')

### Helper function for encoder read/write
def escpON(on):
    ardu.gpio.pinMode(pin_stpON, 0)
    ardu.gpio.digitalWrite(pin_escpON, on&1)

### Helper function for encoder read/write
def escpRW(vDat):
    if ardu.spi.mode != 3:
        ardu.spi.setMode(3)  #< Clock is normally high (CPOL = 1).
                          #< Data is sampled on the transition from low to high (trailing edge) (CPHA = 1)
    return ardu.spi.write_read(vDat)

if __name__ == "__main__":
    #\/\/\/ CHANGE THESE PARAMETERS \/\/\/
    port = 'COM6'       #<--Change to the correct COM-Port to access the Arduino
    baudRate = 115200*2  #<--Leave as is
    #/\/\/\   PARAMETERS BLOCK END  /\/\/\
    
    print('Using port %s at %d'%(port, baudRate))
    ardu = ArduBridge.ArduBridge( COM=port, baud=baudRate )
    escp = ESS_ESCP_lib.ESCP(i2c=ardu.i2c, dev=escp_dev, units='psi')
    t = DS3231_lib.DS3231(i2c=ardu.i2c)
    test = testScripts.test(sns=escp)

    print('Discovering ArduBridge on port %s'%(port))
    if ardu.OpenClosePort(1):
        print('ArduBridge is ON-LINE.')
    else:
        print('ArduBridge is not responding.')
        
    test.printHelp()
    test.config()
