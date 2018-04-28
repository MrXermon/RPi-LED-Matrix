# RPi-LED-Matrix
RPi-LED-Matrix is a project at the HS Mainz to display messages from different sources on a 8x8 LED Matrix.
## Components
![Info about the developed components](/docs/Komponenten.jpg)
### Database
* Stores the messages
    * Text
    * Author
    * Scrollspeed
* Flags messages that are already shown
* Maps Messages to Providers
### daemon.py
* Runs as daemon
* Connects to the LED Matrix via SPI by using the [luma.led_matrix](https://github.com/rm-hull/luma.led_matrix) framework
* Grabs messages from the database, formats and displays them
* 2s pause to preserve the databse
### cron_telegram.py
* Triggerd by Cronjob (every minute)
* Connects to the Telegram Bot API (REST)
* Grabs the messages
* Inserts them into the Database
### cron_twitter.py
* Triggerd by Cronjob (every minute)
* Connects to the Twitter API using the [python-twitter](https://github.com/bear/python-twitter) framework
* Grabs mentions and tweets of specific accounts
* Inserts them into the Database
* Likes and retweets them
## Requirements
### Twitter API
* Create twitter app via [apps.twitter.com](https://apps.twitter.com/)
* Insert app details to the configuration file
### Telegram API
* Create a bot via [Botfather](https://core.telegram.org/bots#6-botfather)
* Insert the bot-token to the configuration file
### Python
* Python 2.7
* pip install [python-twitter](https://github.com/bear/python-twitter)
* pip install [luma.core](https://github.com/rm-hull/luma.core) [luma.led_matrix](https://github.com/rm-hull/luma.led_matrix)
    * [HowTo install the framework](https://luma-led-matrix.readthedocs.io/en/latest/install.html)
### Cronjobs
    @reboot         screen -AmdS LED-Daemon /opt/led/start.sh
    * * * * *       cd /opt/led/; /usr/bin/python2.7 cron_telegram.py
    * * * * *       cd /opt/led/; /usr/bin/python2.7 cron_twitter.py
