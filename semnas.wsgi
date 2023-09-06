#! /opt/rh/rh-python38/root/usr/bin/python

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/woundapi')
#sys.stdout = open('output.logs', 'w')
from wound import create_app
application = create_app()