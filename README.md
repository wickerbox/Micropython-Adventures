# Teensy-Micropython-Adventures
Have Teensy and Micropython, will strive to make blinky.

### Resources

1. [Micropython.org](https://micropython.org/)
1. [Micropython/Teensy](https://github.com/micropython/micropython/tree/master/teensy)

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

