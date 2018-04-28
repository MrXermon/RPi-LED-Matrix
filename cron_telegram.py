# -*- coding: utf-8 -*-
import MySQLdb
import urllib
import urllib2
import json

import configuration

if configuration.TELEGRAM['ACTIVE'] is "true":
	# Setup DB connection
	SQLcon = MySQLdb.connect(configuration.DATABASE['HOST'], configuration.DATABASE['USER'], configuration.DATABASE['PASSWORD'], configuration.DATABASE['NAME'])
	SQLcon.set_character_set('utf8')

	SQLcur = SQLcon.cursor()
        SQLcur.execute('SET NAMES utf8;')
        SQLcur.execute('SET CHARACTER SET utf8;')

	# Grab messages and convert to array
	TelegramUpdates = urllib2.urlopen("https://api.telegram.org/bot" + configuration.TELEGRAM['A_TOKEN'] + "/getUpdates").read()
	TelegramMessages = json.loads(TelegramUpdates)

	# Do magic for all messages
	for message in TelegramMessages['result']:
		try:
			message['message']['text'] = message['message']['text'].replace('/msg ', '')
			# Check if message already exists
			SQLcur.execute("SELECT COUNT(*) FROM `message` WHERE `provider_id` = 3 AND `message_id_external` = '" + str(message['message']['message_id']) + "';")
			if SQLcur.fetchone()[0] == 0:
				# Insert message to database
				SQLcur.execute("INSERT INTO `message` (`message_text`, `message_from`, `message_id_external`, `provider_id`) VALUES (%s, %s, %s, 3);", (message['message']['text'], message['message']['from']['username'], str(message['message']['message_id'])))
		except KeyError:
			False
	# Commit SQL transaction
	SQLcon.commit()
