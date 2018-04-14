cd /opt/led/
/usr/bin/python2.7 daemon.py
renice -n -15 -p $(pgrep python2.7)
