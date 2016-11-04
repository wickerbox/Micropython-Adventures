from pyb import LED
from pyb import delay
led = LED(1)
while (True):     
    led.toggle()    
    delay(1000) 
