#!/usr/bin/env

import Base
import logging
import datetime


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger("RDBUploader")
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)


try:
	import cloudfiles
	logger.info("imported cloudfiles library.")
except ImportError:
	logger.critical("unable to import cloudfiles library. Is it installed?")
	import sys
	sys.exit(-1)

class Driver(Base.Driver):

	def connect(self):
		message = "Not connected"
		return_code = False
		try:
			self.connection = cloudfiles.get_connection(self.user, self.apikey)
			logger.info("connected to cloudfiles successfully")
			message = "connected"
			return_code = True
		except cloudfiles.errors.AuthenticationFailed:
			logger.critical("Unable to establish connection due to invalid credentials" )
			print self.user
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
			self.container = self.connection.get_container( self.containername )
			logger.info("found container from ")
			message = "found container"
			return_code = True
		except Exception as err:
			logger.warn( "No container '{}' found".format(self.containername) )
			try:
				self.container = self.connection.create_container( destination['containername']  )
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
			message = "No container set"
			return (return_code,message)

		# Now we have a container to upload to
		logger.info("Creating remote object")
		now = datetime.datetime.now()
		remote_name =  now.strftime(self.destination_file_format)
		logger.info( "Uploading to '{}'".format(remote_name) )
		try:
			self.container.create_object( remote_name )
			message = "Dump uploaded"
			logger.info( message )
			return_code = True
		except Exception as err:
			message = "Unhandled Exception:"
			self.critical( "{}: '{}'".format(message, err) )

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
