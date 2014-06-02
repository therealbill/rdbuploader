#!/usr/bin/env python


import datetime
import gitconfig
import logging
import sys
import os


try:
	cfg_filename = sys.argv[1]
except IndexError:
	cfg_filename = "/etc/redis/rdbuploader.cfg"


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

destination_module = config.main.targetmodule
print destination_module

driver = __import__("drivers.{}".format(destination_module), globals(), locals(), fromlist = ['upload_redis_dump'] )
print driver

remote = driver.Driver(config)

remote.connect()
remote.getContainer()
remote.uploadFile()


