import MySQLdb
import sys
import time
from PIL import ImageFont

import configuration

# Luma.LED_Matrix requirements
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# LED Matrix Setup
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=12, block_orientation=-90)

device.contrast(configuration.LED['CONTRAST'])
device.clear()

# Show Startup Messages
if len(configuration.STARTUP_MESSAGE):
	for m in configuration.STARTUP_MESSAGE:
		show_message(device, m, fill="white", font=proportional(CP437_FONT),scroll_delay=0.02)

# Setup DB connection
SQLcon = MySQLdb.connect(configuration.DATABASE['HOST'], configuration.DATABASE['USER'], configuration.DATABASE['PASSWORD'], configuration.DATABASE['NAME'])
SQLcon.set_character_set('utf8')

with SQLcon:
	while(1):
		# Setup DB cursor
		SQLcur = SQLcon.cursor()
		SQLcur.execute('SET NAMES utf8;')
		SQLcur.execute('SET CHARACTER SET utf8;')
		SQLcur.execute('SET character_set_connection=utf8;')

		# Grab unshown messages from DB
		SQLcur.execute("SELECT `message_id`, `provider_name`, `message_text`, `message_from` FROM `message` JOIN `provider` ON `message`.`provider_id` = `provider`.`provider_id` WHERE `message_shown` = 0 ORDER BY `message_id` ASC;")

		# Grab one message after another
		for i in range(SQLcur.rowcount):
			# Fetch and prepare date
			SQLrow = SQLcur.fetchone()
			if SQLrow:
				for i in range(0, len(SQLrow)):
					if type(SQLrow[i]) is str:
						SQLrow[i].decode("utf-8")

				# Prepare device + message
				device.show()
				message = SQLrow[2] + " // " + SQLrow[3] + " // " + SQLrow[1]
				print "Started showing message id=" + str(SQLrow[0]) + ", time=" + str(SQLrow[3]) + ", message=" + message

				# Show message
				show_message(device, message, fill="white", font=proportional(CP437_FONT), scroll_delay=0.02)

				# Turn Off and clear device
				device.hide()
				device.clear()
				print "Stopped showing message id=" + str(SQLrow[0]) + ", time=" + str(SQLrow[3]) + ", message=" + message

				# Set state of message to shown
				SQLcur.execute("UPDATE `message` SET `message_shown` = 1 WHERE `message_id` = " + str(SQLrow[0]) + ";")

		# Commit to DB and prepare to restart
		SQLcon.commit()
		time.sleep(1)
