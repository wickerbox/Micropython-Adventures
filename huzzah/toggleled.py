from machine import Pin
from time import sleep

def toggleled():
  p0 = Pin(0, Pin.OUT)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
  p0.high()
  sleep(1)

