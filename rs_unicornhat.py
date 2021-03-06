# RedSqaure
# unicornhat.device handler
# this one uses the Pimoroni standard library and Pillow
# 8x8 16K RGB LED Matrix
# Copyright (c) 2017 full phat products
#

import threading
import time
import sos

unicorn = None
unicornLib = None

# number of concurrent threads (matches detected devices)
maxThread = None

# list of queued requests
queue = None
RotationOffset = 0

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# flash: alternate between the two given images
#
def flash_image(unicorn, statusIcon, imageIcon, repeat=3):
	for i in range(repeat):
		show_image(unicorn, 'icons/' + statusIcon + '.png')
		time.sleep(1.0)
		show_image(unicorn, 'icons/' + imageIcon + '.png')
		time.sleep(1.0)


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# init: try to load up luma.led_matrix
#
def init():
	global unicorn
	global Image
	global ImageDraw
	global ImageFont

	global unicornlib

	try:
		import unicornlib
		sos.sos_print("Got unicornlib...'")

	except:
		sos.sos_fail("Couldn't load unicornlib")
		return False

	try:
		import unicornhat as unicorn
		sos.sos_print("Got unicornhat...'")

	except:
		sos.sos_fail("Couldn't load unicornhat")
		sos.sos_print("To install the support library, see:")
		sos.sos_print("https://github.com/pimoroni/unicorn-hat-hd")
		return False


	global queue
	queue = []

	# initialise the HAT
	sos.sos_print("Configuring device...")

	fBright = 0.7
	global RotationOffset

	import ConfigParser
	config = ConfigParser.RawConfigParser(allow_no_value=True)
	files = config.read('etc/unicorn.rc')
	if len(files) == 1:
		# got config...
		sos.sos_print("Configuration file found...")
		success,f = sos.ConfigTryGetFloat(config, "general", "brightness")
		if success:
			fBright = f

		success,i = sos.ConfigTryGetInt(config, "general", "rotation")
		if success:
			RotationOffset = i

	else:
		# no config
		sos.sos_info("No configuration file: using defaults")

	sos.sos_info("Brightness: " + str(fBright))
	sos.sos_info("Rotation:   " + str(RotationOffset))

	#unicorn.set_layout(unicorn.HAT)
	unicorn.brightness(fBright)
	#show_image(unicorn, "./icons/save.png")
	#time.sleep(0.5)
	unicorn.off()


	unicornlib.scroll_text(unicorn, RotationOffset, "RSOS 2.07", "info")

	return True

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# device handler
# return bool,string (True,"OK") if query was handled, or false otherwise
#
def handle(queryDict, apiVersion=0, unit=0):

	# queue the request...

	global queue
	queue.append(queryDict)

	global maxThread
	if maxThread:
		if maxThread.is_alive():
			print '    [unicornhat] busy: added to queue...'
			return (True, "Request queued")

	# start a thread to display the message

	#maxThread = threading.Thread(target=device_thread, args=(queryDict,))
	maxThread = threading.Thread(target=device_thread)
	maxThread.daemon = True
	maxThread.start()
	return (True, "OK")


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# thread that talks to the unicornhat
#
def device_thread():

	global queue

	while len(queue) > 0:
		# pop from top of list
		dict = queue[0]
		del queue[0]
		# process it
		process(dict)



#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# thread that talks to the unicornhat
#
def process(queryDict):

	global unicorn
	global unicornlib

	global RotationOffset

	# set defaults

	_device = '0'
	mode = 'text'
	icon = ''

	# read variables...

	if 'icon' in queryDict:
		icon = queryDict['icon'][0]

	if 'mode' in queryDict:
		mode = queryDict['mode'][0]


	# process based on mode...

	if mode == "off":
		unicorn.off()
		return (True, "Device turned off")

	elif mode == "icon":
		# get supplied info
		priority = 0

		# required elements...
		if icon == '':
			print '    [unicornhat]: no icon supplied!'
			return (False, "No icon provided")

#	if 'device' in queryDict:
#		_device = queryDict['device'][0]

	elif mode == "text":
		_font = ''
		_invert = '0'
		text = ''
		if 'text' in queryDict:
			text = queryDict['text'][0]

		if text != "":
			# good to go!
			global RotationOffset
			sos.sos_print("Displaying '" + text + "'")
			unicornlib.scroll_text(unicorn, RotationOffset, text, icon)

		else:
			sos.sos_fail("No text to display")
			return (False, "Nothing to do")

	return (True, "OK")


#	if 'invert' in queryDict:
#		_invert = queryDict['invert'][0]
#	if 'font' in queryDict:
#		_font = queryDict['font'][0]

#	if 'priority' in queryDict:
#		_priority = queryDict['priority'][0]

	# determine status icon to use

#	pri = 0
#	try:
#		pri = int(_priority)

#	except:
#		print '    [unicornhat]: bad priority: ' + _priority

#	if pri > 1:
#		_statusIcon = 'alert'

#	elif pri == 1:
#		_statusIcon = 'warn'

#	else:
#		_statusIcon = 'info'


	# good to go!

#	flash_image(unicorn, _statusIcon, _icon)

#	if _text == "":
#		return (False, "Nothing to display")

if __name__ == '__main__':
	init()


