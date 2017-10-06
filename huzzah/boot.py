# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import toggleled, logging
import machine, sdcard, os

toggleled.toggleled()

webrepl.start()
gc.collect()

sd = sdcard.SDCard(machine.SPI(1), machine.Pin(15))
os.umount()
vfs = os.VfsFat(sd, "")
