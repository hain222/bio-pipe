# File: readFile.py
# Author: Harrison Inocencio
# Date: 07-17-18
# Purpose: 

# Usage:

# Notes:
# 1. Doesn't check file is correctly formatted, or a fastq. 
# 2.
# 3.
# 4.
# 5.

# TODO:
# 1. Remove hardcoded "_" etc... (42, 49)
# 2. Add 'purpose' description
# 3.
# 4.
# 5.

# -------------------------------------------------------------------

import os

# readFile class
class readFile:
	"""
	readFile class is a container for read files that parses the 
	information found in the file names and stores them in it's 
	attributes

	ATR:
		fpath = full path to file
		fname = base file name
		run_id = contains run number "4560"
		sample = sample number "S1"
		lane = lane number "L001"
		direction = read direction "R1"
		gzip = gzip status "T/F"

	FUNC:
		tprint = print all atrs, for testing ...

	"""

	# __init__ func
	# call func to set attributes
	def __init__(self, fpath):
		self.__set_atr(fpath)

	# __set_atr func
	# sets the class attributes
	def __set_atr(self, fpath):
		# set fpath/fname
		self.fpath = fpath
		self.fname = os.path.basename(fpath)
		
		# Extract additional info from fname
		spl_name = self.fname.split("_")
		self.run_id = spl_name[0].split("-")[0]
		self.sample =  spl_name[1]
		self.lane = spl_name[2]
		self.direction = spl_name[3]
		
		# Check if gzipped
		if self.fname.split(".")[-1] == "gz":
			self.gzip = True
		else:
			self.gzip = False

	# tprint func
	# prints all attributes (for testing)
	def tprint(self):
		print(self.fpath)
		print(self.fname)
		print(self.run_id)
		print(self.sample)
		print(self.lane)
		print(self.direction)
		print(self.gzip)
		print()
