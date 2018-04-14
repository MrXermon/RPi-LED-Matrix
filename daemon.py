import configuration
import MySQLdb
import sys
import time

# Setup DB connection
con = MySQLdb.connect(configuration.DATABASE['HOST'], configuration.DATABASE['USER'], configuration.DATABASE['PASSWORD'], configuration.DATABASE['NAME'])
con.set_character_set('utf8')

with con:
	while(1):
		# Setup DB cursor
		cur = con.cursor()
		cur.execute('SET NAMES utf8;')
		cur.execute('SET CHARACTER SET utf8;')
		cur.execute('SET character_set_connection=utf8;')

		# Grab unshown messages from DB
		cur.execute("SELECT `message_id`, `message_text`, `provider_name` FROM `messages` JOIN `provider` ON `messages`.`provider_id` = `provider`.`provider_id` WHERE `message_shown` = 0 ORDER BY `message_id` ASC;")

		# Grab one message after another
		for i in range(cur.rowcount):
			# Fetch and prepare date
			row = cur.fetchone()
			for i in range(0, len(row)):
				if type(row[i]) is str:
					row[i].decode("utf-8")

			# Do magic to show message
			print row[1] + " via " + row[2]

			# Set state of message to shown
			cur.execute("UPDATE `messages` SET `message_shown` = 1 WHERE `message_id` = "+str(row[0])+";")

		# Commit to DB and prepare to restart
		con.commit()
		time.sleep(2)
