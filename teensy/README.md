# Micropython Adventures with Teensy 3.2

Have Teensy and Micropython, will strive to make blinky.

### Resources

1. [Micropython.org](https://micropython.org/)
1. [Micropython Source](https://github.com/micropython/micropython)
1. [Micropython/Teensy](https://github.com/micropython/micropython/tree/master/teensy)
1. [GCC-arm-embedded](https://launchpad.net/gcc-arm-embedded)
1. [catherineh/Getting Started](http://catherineh.github.io/programming/2016/09/18/getting-started-with-micropython-on-the-teensy.html)

### Acquire ARM Embedded Toolchain

I'm using Linux Mint 17 on a Surface Pro 3 because I enjoy pain and suffering.

```
sudo add-apt-repository ppa:team-gcc-arm-embedded/ppa
sudo apt-get update
sudo apt-get install gcc-arm-embedded
```

### Acquire Parts

1. Teensy 3.2
1. Jumper wires
1. Blue LED
1. 1K resistor
1. Pushbutton
1. Micro-USB cable

### Install Teensy Rules file

I cheated and already had this installed from way back, but for future reference, I installed the [49-teensy.rules](http://www.pjrc.com/teensy/49-teensy.rules) file in `/etc/udev/rules.d/49-teensy.rules`. This means I don't have to use `sudo` later.

### Test Teensy 

I already had [Arduino 1.6.12](https://www.arduino.cc/en/Main/Software). 

I downloaded the [Teensyduino installer 1.31 beta version](https://forum.pjrc.com/threads/38599-Teensyduino-1-31-Beta-2-Available) that works with 1.6.12 and ran it. I just had to tell it where I put the Arduino install.

I placed the Teensy on a breadboard and plugged it in. It started blinking, because that's what they do right out of the box. 

In the Arduino IDE, I went to the Tools > Boards > Board Manager. Because I added Teensyduino, the Teensy list was already there. I selected Teensy 3.2 / 3.1.

I left all the Boards settings to default but noticed there's no Port being detected. That's no problem. I opened the Files > Examples > Teensy > Tutorial1 > Blink. I adjusted the duration of the delay so it would blink much faster.

```
  digitalWrite(ledPin, HIGH);   // set the LED on
  delay(200);                  // wait for a second
  digitalWrite(ledPin, LOW);    // set the LED off
  delay(200);                  // wait for a second
```

Then I clicked 'Upload' which compiled, started another little program window from Teensyduino, and automatically uploaded. Next thing I know, my Teensy is blinking rapidly. 

Now I know that everything broken from here on out is probably my fault, not the Teensy's.

### Install Micropython

I cloned the [Micropython repo](https://github.com/micropython/) into ~/tools, where I usually put things like this. I followed the instructions on the [Micropython Teensy page](https://github.com/micropython/micropython/tree/master/teensy), adapting them for my file system.

My arduino install is in ~/tools/arduino-1.6.12.

```
cd ~/tools/micropython/teensy
ARDUINO=~/tools/arduino-1.6.12/ make deploy
```

The first time, I didn't have the Teensy actually attached to my computer, so I got this message:

```
Preparing post_compile for upload
REBOOT
Teensy did not respond to a USB-based request to automatically reboot.
Please press the PROGRAM MODE BUTTON on your Teensy to upload your sketch.
```

Oops. I connected the Teensy and ran the command again.

```
ARDUINO=~/tools/arduino-1.6.12 make deploy
```

Worked great. 

My Teensy is now the proud bearer of Python development environment accesible over serial.

### Serial to the Teensy

I used minicom because I had it, but will probably move to screen in the future. It's been forever since I used screen. Anyway, I ran this command and hit enter a couple of times.

```
minicom -D /dev/ttyACM0
```

Success! That there is a Python prompt!

```
Welcome to minicom 2.7

OPTIONS: I18n 
Compiled on Jan  1 2014, 17:13:19.
Port /dev/ttyACM0, 14:42:50

Press CTRL-A Z for help on special keys


>>> 
```

### Wait, Python 3.4?

Uh, okay. Let's start with [reading up on using the language](http://docs.micropython.org/en/latest/wipy/library/index.html)...

Turns out the Python environment is really called a Micropython Serial REPL, a read, eval, print loop. The tutorials at Micropython are helpful, but definitely figuring stuff out took some trial and error.

The LED is hardwired... the onboard orange LED can be toggled:

```
from pyb import LED
led = LED(1)
led.on()
led.off()
led.toggle()
```

I wanted to treat the LED pin like a standard output pin.

```
from pyb import Pin

led = Pin('D3', Pin.OUT_PP)
led.high()
led.low()
```

### Create and upload Python script 

I want to set up a simple toggling LED script to prove this works, so I logged into the REPL like I did before and tested the script parts to make sure it all works.

```
from pyb import LED
from pyb import delay                                                       
led = LED(1)
while (True):                                                              
    led.toggle()                                                            
    delay(1000)                                                             
```

I used [Catherine's instructions](http://catherineh.github.io/programming/2016/09/18/getting-started-with-micropython-on-the-teensy.html), which said:

```
MicroPython looks for two scripts - boot.py that will execute once on boot (like the setup section of an arduino sketch) and - main.py that executes after boot (like the loop section of an arduino sketch, except that it will not run continously unless you have a while True: loop).
```

I want this code in the loop so I created a new directory called ~/tools/micropython/teensy/scripts and saved these steps in a file called toggle-led.py. Then, from the ~/tools/micropython/teensy directory, I ran the same command as earlier to make and deploy the code.

```
cd ~/tools/micropython/teensy
ARDUINO=~/tools/arduino-1.6.12 make deploy
```

That didn't work, so I added the extra step from Catherine's instructions to add the files to the memzip_files folder:

```
cd ~/tools/micropython/teensy
cp scripts/* memzip_files
ARDUINO=~/tools/arduino-1.6.12 make deploy
```

The LEDs didn't toggle... :(

Oh! I opened up  memzip_files and found two files: `boot.py` and `main.py` and I realized it's only running `main.py` in the loop, so I'd have to call what's in toggle_led.py with a function. Not sure how I thought it was working, but anyway...

I added the code to toggle the LED to the end of main.py and it works!

```
wicker@surface:~/tools/micropython/teensy (master)$ ARDUINO=~/tools/arduino-1.6.12/ make deploy
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
Using toolchain from PATH
Generating build/frozen.c
Generating build/genhdr/mpversion.h
GEN build/genhdr/qstr.i.last
GEN build/genhdr/qstr.split
GEN build/genhdr/qstrdefs.collected.h
QSTR not updated
CC ../py/modsys.c
CC ../py/../extmod/modwebrepl.c
CC build/frozen.c
CC ../lib/utils/pyexec.c
LINK build/micropython.elf
   text    data     bss     dec     hex filename
 188440    1236   20388  210064   33490 build/micropython.elf
HEX build/micropython.elf
Preparing post_compile for upload
REBOOT
```


