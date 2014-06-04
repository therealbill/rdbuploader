#!/usr/bin/env python


import datetime
import gitconfig
import logging
import sys
import os

import argparse

parser = argparse.ArgumentParser(description='Upload Dump file to Remote server')
parser.add_argument("-config", help="Config file to use", default="/etc/redis/rdbuploader.cfg")
args = parser.parse_args()

"""

try:
	cfg_filename = sys.argv[1]
except IndexError:
	cfg_filename = "/etc/redis/rdbuploader.cfg"
"""

print args.config
cfg_filename = args.config
config = gitconfig.config(cfg_filename)

if not config.exists:
	print "Unable to open config file, which means whatever I do will fail. Aborting"
	sys.exit(-1)

logger = logging.getLogger("RDB Uploader")

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

if not os.path.isfile(config.redis.dumpfile):
	logger.error("No dump file '{}' found, nothing to do".format(config.redis.dumpfile) )
	sys.exit(0)


filesize = os.stat(config.redis.dumpfile).st_size


logger.info("Target file size: {} bytes".format(filesize) )

if filesize >= int(config.main.maxfilesize):
		logger.error("Dump file is larger than configured limits ({} bytes), bailing".format(config.main.maxfilesize) )
		sys.exit(-1)

destination_module = config.main.driver

try:
	driver = __import__("drivers.{}".format(destination_module), globals(), locals(), fromlist = ['upload_redis_dump'] )
except ImportError:
	logger.error("Was unable to import driver '{}', perhaps config is incorrect?".format(destination_module) )
	sys.exit(-1)


remote = driver.Driver(config)

remote.connect()
remote.getContainer()
remote.uploadFile()


