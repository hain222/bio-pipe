# File: sampleSet.py
# Author: Harrison Inocencio
# Date: 07-17-18
# Purpose: 

# Notes:
# 1. If the sampleSet contains readFile's that are not of the same sample,
#	 grp_sample will be set to 'None'
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

# sampleSet class
class sampleSet:
	"""
	Container for readFile objects. Should be used to group related
	sample read files, so that ops can be performed on them.

	ATRS:
		set_sample = shared sample number of all reads in the set, set to
					 'None' if members of the group differ in sample number
		fwd_set = lane sorted list of the R1 files in the set
		rev_set = lane sorted list of the R2 files in the set

	"""

	# __init__ func
	# reads in a list of readFile objects grped by sample
	def __init__(self, laned_reads):
		self.__set_atr(laned_reads)

	# __set_atr func
	# sets the overall attributes of the sampleSet
	def __set_atr(self, laned_reads):
		# if their is a != sample in laned_reads, set set_sample to 'None'
		if all(x.sample == laned_reads[0].sample for x in laned_reads):
			self.set_sample = laned_reads[0].sample
		else:
			self.set_sample = None
		# Set fwd and rev sets
		self.fwd_set, self.rev_set = self.__sort(laned_reads)	

	# __sort func
	# groups objs by direction and sorts them by lane
	def __sort(self, laned_reads):
		fwd_set = []
		rev_set = []
		for obj in laned_reads:
			if obj.direction == "R1":
				fwd_set.append(obj)
			else:
				rev_set.append(obj)
		fwd_set.sort(key=lambda f: f.lane)
		rev_set.sort(key=lambda r: r.lane)

		return fwd_set, rev_set
	
	# tprint func
	# print various info on attributes (for testing ...)
	# 1. set_sample :
	# 2. fwd_set: prints the fname of each readFile ele
	# 3. rev_set: ...
	def tprint(self):
		print(self.set_sample)
		for obj in self.fwd_set:
			print(obj.fname)
		for obj in self.rev_set:
			print(obj.fname)
		print()
