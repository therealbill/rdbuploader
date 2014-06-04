#!/usr/bin/env python


class Driver(object):

	def __init__( self, config_instance ):
		self.driver = config_instance.main.driver
		self.user = config_instance.get( self.driver,'username' )
		self.apikey = config_instance.get( self.driver,'apikey' )
		self.destination_format = config_instance.main.destinationformat
		self.maxsize = config_instance.main.maxfilesize
		self.containername = config_instance.get( self.driver, "containername" )
		self.connection = None
		self.container = None
		self.destination_file_format = config_instance.destinationformat.python
		self.dumpfile = config_instance.redis.dumpfile


	def connect(self):
		"Override this to provide connect mechanism"
		return_code = False
		self.connection = None
		message="NOT IMPLEMENTED"
		if self.connection:
			message = "success"
			return_code = True
		else:
			pass
		return (return_code,message)


	def getContainer(self,create=True):
		"""
		Return the remote container object, creating if necessary
		"""
		return_code = False
		message="NOT IMPLEMENTED"
		return (return_code,message)


	def uploadFile(self,create=True):
		"""
		Upload the file
		"""
		return_code = False
		message="NOT IMPLEMENTED"
		return (return_code,message)


