# Micropython on the Adafruit ESP8266 Huzzah

Have Huzzah and Micropython, will strive to make blinky.

### Resources

1. [Micropython.org](https://micropython.org/)
1. [Micropython Source](https://github.com/micropython/micropython)
1. [GCC-arm-embedded](https://launchpad.net/gcc-arm-embedded)
1. [Micropython Official ESP8266 Howto](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware)

### Acquire Parts

1. ESP8266 Huzzah
1. Jumper wires
1. Blue LED
1. 1K resistor
1. Pushbutton
1. Micro-USB cable
i
### Acquire Micropython ESPtool

```
sudo pip install esptool
```

I downloaded the newest firmware from [Micropython.org](http://micropython.org/download/#esp8266), which was esp8266-20161017-v1.8.5.bin, and saved it to my ~/tools directory.

The HUZZAH is a special board that has buttons for GPIO0 and RESET. Hold GPIO0 down, press and release RESET, and release GPIO0 to tell the module to boot up into its firmware flashing mode. 

If this doesn't work or isn't done, you'll get the following error:

```
wicker@surface:~$ esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py v1.1
Connecting...

A fatal error occurred: Failed to connect to ESP8266
```

If it works, it looks like this:
```
esptoolcker@surface:~$ esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py v1.1
Connecting...
Erasing flash (this may take a while)...
```

Next, after again using GPIO0 and RESET to boot the board into firmware flashing mode, I changed the directory to ~/tools where I saved the firmware file. Then I flashed the board:

```
wicker@surface:~/tools$ esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=8m 0 esp8266-20161017-v1.8.5.bin 
esptool.py v1.1
Connecting...
Running Cesanta flasher stub...
Flash params set to 0x0020
Writing 565248 @ 0x0... 565248 (100 %)
Wrote 565248 bytes at 0x0 in 14.5 seconds (312.5 kbit/s)...
Leaving...
```

### Access Serial REPL

I opened a serial connection to the board using Minicom.

```
minicom -D /dev/ttyUSB0 -s
```

The -s is to enter setup, where I selected Serial Port Setup and made sure both Hardware and Software Flow Control were set to No. Otherwise, I found I couldn't enter any characters with my keyboard.

I saved that to my profile and selected Exit.

In the console, nothing happened. I tried to hit enter a couple of times, but no luck, so I hit 'reset' on the board and that did the trick. I got some garbage in Minicom and then the REPL terminal.

```
�ll`�ll��l�#4 ets_task(40100384, 3, 3fff6300, 4)
Performing initial setup
#5 ets_task(4020e374, 29, 3fff7090, 10)
WebREPL daemon started on ws://192.168.4.1:8266
Started webrepl in setup mode
could not open file 'main.py' for reading

MicroPython v1.8.5-10-g0e69e6b on 2016-10-17; ESP module with ESP8266
Type "help()" for more information.
>>> 
```

### Blink an LED

The onboard LED is pin 0 and it's an active low pin.

Success! Unlike the Teensy, the standard ESP8266 just uses pin numbers with no 'D' or 'A' prefixes.

```
>>> from machine import Pin
>>> p0 = Pin(0, Pin.OUT)
>>> p0.low()
>>> p0.high()
```

### Using ampy to load a blinky script

The [Adafruit MicroPython Tool](https://github.com/adafruit/ampy) has installation instructions.

I installed it with

```
sudo pip install adafruit-ampy
```

At this point, I'm really fuzzy about file structures. Not only what I have access to on the remote board, but what I should have for which tool here on my laptop. So, using Ampy, I ran `ampy --help` to see what my options were.

```
wicker@surface:~$ ampy --help
Usage: ampy [OPTIONS] COMMAND [ARGS]...

  ampy - Adafruit MicroPython Tool

  Ampy is a tool to control MicroPython boards over a serial connection.
  Using ampy you can manipulate files on the board's internal filesystem and
  even run scripts.

Options:
  -p, --port PORT  Name of serial port for connected board.  Can optionally
                   specify with AMPY_PORT environemnt variable.  [required]
  -b, --baud BAUD  Baud rate for the serial connection (default 115200).  Can
                   optionally specify with AMPY_BAUD environment variable.
  --version        Show the version and exit.
  --help           Show this message and exit.

Commands:
  get    Retrieve a file from the board.
  ls     List contents of a directory on the board.
  mkdir  Create a directory on the board.
  put    Put a file on the board.
  reset  Perform soft reset/reboot of the board.
  rm     Remove a file from the board.
  run    Run a script and print its output.
```

Okay, so what's currently on the board. Should there be a boot.py and a main.py, like in the Teensy?

```
wicker@surface:~$ ampy -p /dev/ttyUSB0 ls
boot.py
```

Let's get that file and see what's in it... but first, let's move into the working directory for this project on my computer.

```
wicker@surface:~$ cd proj/Micropython-Adventures/huzzah/ 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 get boot.py# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
webrepl.start()
gc.collect()
```

Doesn't look like we copied it, just that we read it so I can copy it down if I wanted to. Did we copy it locally?

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ls
README.md  toggle-led.py
```

I decided to try and run my blinky script locally, using `run` and it worked, but it didn't get added to the Huzzah or anything.

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 run toggle-led.py 
```

Let's try putting it on the board, but first, let's try adding time and delay to it. I went back in to the REPL to test out a delay script.

```
minicom -D /dev/ttyUSB0
```

I'm not able to import pyb, but I was able to import time. I added a sleep to my existing toggle-led script, but I'm cheating by using a Pin instead of an LED object.

```
from machine import Pin
from time import sleep
p0 = Pin(14, Pin.OUT)
p0.high()
sleep(1)
p0.low()
sleep(1)
p0.high()
sleep(1)
p0.low()
sleep(1)
```

This works on the REPL and it should slowly blink the LED twice when run on the board. I ran it using the same `run` command:

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 run toggle-led.py
```

But I really want to upload the file and run it whenever I hit the reset button.

First, I uploaded toggle-led.py to the board. Success!

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put toggle-led.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
toggle-led.py
```

But it doesn't yet run on startup, because `boot.py` has no idea `toogle-led.py` exists. I copied the contents of the `boot.py` on the board to my computer's local folder.

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 get boot.py > boot.py
```

Then I removed the toggle-led file from the board with `rm` and tested the asterisk for uploading using `put`.


```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
toggle-led.py

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm toggle-led.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
```

It's gone, now I'm going to try to put all \*.py on the board. Boot.py still doesn't know about toggle-led.py. I'm trying not to make any assumptions about how this works.

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put *.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
toggle-led.py
```

Success!

Now, to link boot.py to toggle-led.py.

First, I adjusted toggle-led.py to contain a function:

```
from machine import Pin
from time import sleep

def toggleled():
  p0 = Pin(14, Pin.OUT)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
```

Then I edited the boot.py to import toggle-led and realized that, of course, this needs to be rnamed toggleled instead of toggle-led, since Python doesn't like dashes in module names...

```
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import toggleled

webrepl.start()
toggleled()
gc.collect()
```

And now, to remove the old toggle-led.py, put both files on the board, and see if it works.

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ls
boot.py  README.md  toggleled.py

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
toggle-led.py

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm toggle-led.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put *.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 reset

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
boot.py
toggleled.py
```

That totally didn't work. Have I forgotten how to call modules in Python? Shoot, let's just throw this in boot.py directly.

```
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from machine import Pin
from time import sleep

p0 = Pin(14, Pin.OUT)
p0.high()
sleep(1)
p0.low()
sleep(1)
p0.high()
sleep(1)
p0.low()
sleep(1)

webrepl.start()
gc.collect()
```

Putting that on the board didn't work either... wait... what's ON the boot.py right now? 

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 get boot.py 
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
webrepl.start()
gc.collect()
```

Wait a minute... What?! We're not affecting boot.py? Do we have not have overwrite capability?

I removed the two .py files, verified they were gone, added the new edited boot.py by itself, and ran it. And it worked!

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm toggleled.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm boot.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put boot.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls 
boot.py

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 get boot.py 
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
from machine import Pin
from time import sleep

p0 = Pin(14, Pin.OUT)
p0.high()
sleep(1)
p0.low()
sleep(1)
p0.high()
sleep(1)
p0.low()
sleep(1)

webrepl.start()
gc.collect()
```

Okay, I made one edit and tried to put boot.py but it apparently can't overwrite. I also played around with adding multiple files at one time. Basically, it looks like you have to put each file individually, and remove each file before putting a new one. But that's okay.

... after some more messing around with it: success!

Boot.py looks like this:

```
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import toggleled

toggleled.toggleled()

webrepl.start()
gc.collect()
```

Toggleled..py looks like this:

```
from machine import Pin
from time import sleep

def toggleled():
  p0 = Pin(14, Pin.OUT)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
  p0.high()
  sleep(1)
  p0.low()
  sleep(1)
```

I remove everything from the board, upload each file individually, and hit the physical reset button on the board, then the light blinks twice as the script runs successfully.

```
wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
toggleled.py
boot.py

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm toggleled.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 rm boot.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put toggleled.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 put boot.py 

wicker@surface:~/proj/Micropython-Adventures/huzzah (master)$ ampy -p /dev/ttyUSB0 ls
toggleled.py
boot.py
```

### Talking to Accelerometer over I2C

Using the MMA7660 3-axis accelerometer.

I'll need to: 

- collect and hold the x, y, z info in an accelerometer object in the ESP8266
- talk I2C to the accelerometer from the ESP8266

I opened and kept open the [Quick Ref guide for the ESP8266 Micropython libraries](http://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html), along with the [MicroPython ESP8266](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/index.html) tutorial.  

I know from a previous project that the MMA7660 default address is 0x4C. Also:

|Variable|Address|
|--------|-------|
|MMA7660_ADDR  |0x4c|
|MMA7660_X     |0x00|
|MMA7660_Y     |0x01|
|MMA7660_Z     |0x02|
|MMA7660_TILT  |0x03|
|MMA7660_SRST  |0x04|
|MMA7660_SPCNT |0x05|
|MMA7660_INTSU |0x06|
|MMA7660_MODE  |0x07|
|MMA7660_SR    |0x08|
|MMA7660_PDET  |0x09|
|MMA7660_PD    |0x0A|

What do I need to talk I2C to this accelerometer? There's an I2C in `machine`.

from machine import Pin, I2C

# construct an I2C bus
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)

i2c.readfrom(0x4c, 4)   # read 4 bytes from slave device with address 0x3a
i2c.writeto(0x4c, '12') # write '12' to slave device with address 0x3a

buf = bytearray(10)     # create a buffer with 10 bytes
i2c.writeto(0x3a, buf)  # write the given buffer to the slave
```

```

Next, is I2C (the serial protocol to talk to the accelerometer chip) already supported automatically? How do I call it? 


