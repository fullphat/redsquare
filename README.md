# Halon

## Synopsis

Python-based micro webserver that controls various LED matricies, LCD displays, LEDs and other nifty widgets in a structured, easily-accessible, and extensible way.

## Concept

Halon supports a modular platform based on a single central webserver, a standard helper library and any number of third-party created device modules that interface with varying physical devices.

## Supported Devices

- Max7219 8x8 LED Matrix
- Thingm Blink(1) USB LED
- Pimoroni UnicornHAT and UnicornHAT HD

## Support Planned

- Nokia 3310/5110 LCD Display
- Pimoroni pHAT

## Examples

The following examples use **curl**, however you could just paste everything but "curl" into the address bar of your favourite browser.  Don't forget to prefix with "http://" of course.

Display "Hello world!" as a scrolling message on a MAX7219 8x8 Matrix:

```curl 127.0.0.1:6789/v1?device=max7219&text=Hello%20world%21```

Glimmer the second Blink(1) device connected to your system a nice shade of magenta:

```curl 127.0.0.1:6789/v1?device=blink1&unit=1&mode=glimmer&rgb=ff00ff```





