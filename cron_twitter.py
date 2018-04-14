import MySQLdb
import twitter
import json

import configuration

if configuration.TWITTER['ACTIVE'] is "true":
	# Setup DB connection
	SQLcon = MySQLdb.connect(configuration.DATABASE['HOST'], configuration.DATABASE['USER'], configuration.DATABASE['PASSWORD'], configuration.DATABASE['NAME'])
	SQLcon.set_character_set('utf8')

	SQLcur = SQLcon.cursor()
        SQLcur.execute('SET NAMES utf8;')
        SQLcur.execute('SET CHARACTER SET utf8;')

	# Setup TwitterAPI
	TWITTERapi = twitter.Api(consumer_key=configuration.TWITTER['C_KEY'],
                      consumer_secret=configuration.TWITTER['C_SECRET'],
                      access_token_key=configuration.TWITTER['A_TOKEN'],
                      access_token_secret=configuration.TWITTER['A_SECRET'],
		      sleep_on_rate_limit=True)

	# Grab messages and convert to array
	TwitterMetions = TWITTERapi.GetMentions()
	for Status in TwitterMetions:
		SQLcur.execute("SELECT COUNT(*) FROM `message` WHERE `provider_id` = 2 AND `message_id_external` = '" + str(Status.id_str) + "';")
                if SQLcur.fetchone()[0] == 0:
                        # Insert message to database
			SQLcur.execute("INSERT INTO `message` (`message_text`, `message_from`, `message_id_external`, `provider_id`) VALUES ('" + (Status.text) + "', '" + (Status.user.screen_name) + "', " + str(Status.id_str) + ", '2');")

        # Commit SQL transaction
        SQLcon.commit()

