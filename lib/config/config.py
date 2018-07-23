# File: config.py
# Author: Harrison Inocencio
# Date: 07-18-18
# Purpose: Contains the config class, a container for r/w to the config file
#		   and storing it's parameters.

# Notes:
# 1.
# 2.
# 3.
# 4.
# 5.

# TODO:
# 1. 
# 2.
# 3.
# 4.
# 5.

# -------------------------------------------------------------------

import os
import configparser
import lib.config.cargs as cargs

# config class
class config():
	"""
	Contains the parameters read from the config file, but can also
	Write out it's own attributes into a new file. Attributes will
	be set to 'None' if the initial read was unsuccessful, but this can
	also be checked using the 'check_path' func
	"""

	trim_jar_path = None
	vread_type = None

	# __init__ func
	# By default, will automatically try to load ini file
	def __init__(self):
		try:
			self.ini_read()
		except FileNotFoundError:
			pass	
			
	# __parse_ini func
	# Parses init configuration file and sets attributes
	def __parse_ini(self):
		config = configparser.ConfigParser()
		config.read(cargs.config_path)
		self.trim_jar_path = config[cargs.trim_section][(
												cargs.trim_jar_path_key)]
		self.vread_type = config[cargs.velvet_section][(
												cargs.vread_type_key)]

	# __check_path func
	# Attempts to locate config file path
	# If not found, raises a FileNotFound exception
	def check_path(self):
		if not os.path.isfile(cargs.config_path):
			raise(FileNotFoundError)

	# ini_read func
	# Attempts to update its attributes from the ini file
	# Will riase a FileNotFoundError if the file could not be located
	# Will raise a KeyError if a the file experiences a key formatting 
	# issue
	def ini_read(self):
		self.check_path()
		try:
			self.__parse_ini()
		except KeyError:
			raise(RuntimeError(cargs.key_error))

	# config_write func
	# The object will write out its current attributes into the config file
	# Will overwrite current config file
	def config_write(self):
		config = configparser.ConfigParser()
		config[cargs.trim_section] = {}
		config[cargs.trim_section][cargs.trim_jar_path_key] = (
														self.trim_jar_path)
		config[cargs.velvet_section] = {}
		config[cargs.velvet_section][cargs.vread_type_key] = (
														self.vread_type)

		#config[cargs.section_name][cargs.trim_section][(
		#		cargs.trim_jar_path_key)] = self.trim_jar_path
		with open(cargs.config_path, 'w') as fh:
			fh.write(cargs.config_header+'\n')
			config.write(fh)
	
	# tprint func
	# Print out all attributes (for testing)
	def tprint(self):
		print(self.trim_jar_path)
		print(self.vread_type)
