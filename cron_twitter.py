import MySQLdb
import twitter
import json

import configuration

if configuration.TWITTER['ACTIVE'] is 'true':
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

	# Grab mentions and convert to array
	if configuration.TWITTER['MENTIONS'] is 'true':
		# Fetch Mentions
		TwitterMetions = TWITTERapi.GetMentions()
		# Check if Mentions already shown and insert into db
		for Status in TwitterMetions:
			SQLcur.execute("SELECT COUNT(*) FROM `message` WHERE `provider_id` = 2 AND `message_id_external` = '" + str(Status.id_str) + "';")
	                if SQLcur.fetchone()[0] == 0:
				message = Status.text.encode('ascii',errors='ignore')
                                # Insert message to database
                                SQLcur.execute("INSERT INTO `message` (`message_text`, `message_from`, `message_id_external`, `provider_id`) VALUES (%s, %s, %s, '2');", (message, Status.user.screen_name, str(Status.id_str)))

	if configuration.TWITTER['TWEETS'] is 'true':
		# Loop through all Users
		for User in configuration.TWITTER['TWEETS_USERS']:
			# Fetch User Timeline
			TwitterTimeline = TWITTERapi.GetUserTimeline(screen_name=User)
			# Check if Statuses already shown and insert into db
			for Status in TwitterTimeline:
				SQLcur.execute("SELECT COUNT(*) FROM `message` WHERE `provider_id` = 2 AND `message_id_external` = '" + str(Status.id_str) + "';")
	                        if SQLcur.fetchone()[0] == 0:
					message = Status.text.encode('ascii',errors='ignore')
        	                        # Insert message to database
					SQLcur.execute("INSERT INTO `message` (`message_text`, `message_from`, `message_id_external`, `provider_id`) VALUES (%s, %s, %s, '2');", (message, Status.user.screen_name, str(Status.id_str)))

        # Commit SQL transaction
        SQLcon.commit()

