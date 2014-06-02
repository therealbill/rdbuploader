#!/usr/bin/env

import Base
import logging
import datetime

logger = logging.getLogger("RDBUploader")

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


try:
	import boto
except ImportError:
	logger.critical("unable to import boto library. Is it installed?")

class Driver(Base.Driver):

	def connect(self):
		message = "Not connected"
		return_code = False
		try:
			self.connection = boto.connect_s3(self.user, self.apikey)
			logger.info("connected to S3 successfully")
			message = "connected"
			return_code = True
		except Exception as err:
			logger.critical("Unable to establish connection due to '{}'".format(err) )
		return (return_code,message)


	def getContainer(self,create=True):

		message = "No container"
		return_code = False

		if not self.connection:
			message = "Not connected"
			return (return_code,message)

		try:
			self.container = self.connection.get_bucket( self.containername )
			logger.info("pulled bucket from S3")
			message = "retrieved bucket"
			return_code = True
		except Exception as err:
			logger.warn( "No container '{}' found".format(self.containername) )
			try:
				self.container = self.connection.create_bucket( destination['containername']  )
				logger.info( "Created container '{containername}'".format(**destination) )
				message = "Container created"
			except boto.exception.S3ResponseError as err:
				logger.critical("Unable to create container due to policy limitations" )
			except Exception as err:
				logger.critical("Unable to create container due to exception '{}".format(err) )

		return (return_code,message)

	def uploadFile(self):

		message = "No container"
		return_code = False

		if not self.connection:
			message = "Not connected"
			return (return_code,message)

		if not self.container:
			message = "No bucket set"
			return (return_code,message)

		# Now we have a container to upload to
		logger.info("Creating remote object")
		now = datetime.datetime.now()
		remote_name =  now.strftime(self.destination_file_format)
		k = boto.s3.key.Key(self.container)
		k.key = remote_name
		logger.info( "Uploading to '{}'".format(remote_name) )
		try:
			res = k.set_contents_from_filename(self.dumpfile)
			message = "Dump uploaded"
			return_code = True
		except boto.exception.S3ResponseError as err:
			if err.error_code == "AccessDenied":
				message = "Unable to upload dump file due to policy configuration"
				logger.critical(message)
			else:
				print "Unhandled Exception:"
				print err.error_code
				print err.reason

		return (return_code,message)


if __name__ == '__main__':
	import gitconfig
	cfg = gitconfig.config("../redis-remote-copy.cfg")
	if not cfg.exists:
		logger.critical( "Unable to load file:",cfg.filename )
		import sys
		sys.exit(-1)
	d = Driver(cfg)
	d.connect()
	d.getContainer()
	d.uploadFile()
