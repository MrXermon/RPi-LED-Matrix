import configuration
import MySQLdb
import sys
import time

# Luma.LED_Matrix requirements
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy.font import proportional, LCD_FONT

# LED Matrix Setup
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=12, block_orientation=-90)

device.contrast(10)
device.clear()

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
		SQLcur.execute("SELECT `message_id`, `provider_name`, `message_text`, `message_duration` FROM `message` JOIN `provider` ON `message`.`provider_id` = `provider`.`provider_id` WHERE `message_shown` = 0 ORDER BY `message_id` ASC;")

		# Grab one message after another
		for i in range(SQLcur.rowcount):
			# Fetch and prepare date
			SQLrow = SQLcur.fetchone()
			if SQLrow:
				for i in range(0, len(SQLrow)):
					if type(SQLrow[i]) is str:
						SQLrow[i].decode("utf-8")

				# Prepare device
				device.show()
				print "Started showing message ("+str(SQLrow[3])+"s): " + SQLrow[2] + " via " + SQLrow[1]

				# Show message
				with canvas(device) as draw:
					draw.rectangle(device.bounding_box, outline="white")

				# Wait
				time.sleep(SQLrow[3])

				# Turn Off and clear device
				device.hide()
				device.clear()
				print "Stopped showing message: " + SQLrow[2] + " via " + SQLrow[1]

				# Set state of message to shown
				SQLcur.execute("UPDATE `message` SET `message_shown` = 1 WHERE `message_id` = "+str(SQLrow[0])+";")

		# Commit to DB and prepare to restart
		SQLcon.commit()
		time.sleep(2)
