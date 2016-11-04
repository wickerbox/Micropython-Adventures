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
minicom -D /dev/ttyUSB0
```

I tried to hit enter a couple of times, but nothing happened, so I hit 'reset' on the board and that did the trick. I got some garbage in Minicom and then the REPL terminal.

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

Success! Unlike the Teensy, the standard ESP8266 just uses pin numbers with no 'D' or 'A' prefixes.

```
>>> from machine import Pin
>>> p0 = Pin(14, Pin.OUT)
>>> p0.high()
>>> p0.low()
```

