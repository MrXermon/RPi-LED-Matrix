# RPi-LED-Matrix
## Components
![Uebersicht der Komponenten](/docs/Komponenten.jpg)
## Requirements
### Python
* Python 2.7
* pip install python-twitter // https://github.com/bear/python-twitter
* pip install --upgrade luma.led_matrix // https://luma-led-matrix.readthedocs.io/en/latest/install.html
### Cronjobs
    @reboot         screen -AmdS LED-Daemon /opt/led/start.sh
    * * * * *       cd /opt/led/; /usr/bin/python2.7 cron_telegram.py
    * * * * *       cd /opt/led/; /usr/bin/python2.7 cron_twitter.py
### Twitter API

### Telegram API
