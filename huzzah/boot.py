# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import toggleled

toggleled.toggleled()

webrepl.start()
gc.collect()


