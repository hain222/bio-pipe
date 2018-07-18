# File: merge.py
# Author: Harrison Inocencio
# Date: 07-17-18
# Purpose: 

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

import gzip
from lib.readFile import readFile

# merge_name_generator func
# Generates merged read file names from readFile obj
# names are assumed to be unzipped, so 'gzip' suffix not added
def merge_name_generator(rf_obj):
	return "%s-%s_%s_all_%s_001.fastq" % (rf_obj.run_id, rf_obj.sample,
									 rf_obj.sample, rf_obj.direction)
# comp_merge func
# Used by merge_helper, given an rf obj and output fd, uses 'gzip.open'
# to open a comp readfile and write it to the outpath
def comp_merge(rf, opath):
	with gzip.open(rf.fpath, 'rt') as inpath:
		for line in inpath:
			opath.write(line)
		#opath.write("\n") Debug nl

# uncomp_merge func
# Same as comp_merge, but uses 'open' instead of 'gzip.open' for use with
# uncomp files
def uncomp_merge(rf, opath):
	with open(rf.fpath) as inpath:
		for line in inpath:
			opath.write(line)
		#opath.write("\n") Debug nl

# merge_helper func
# Merges a given set of readFile objects and writes them out to
# merge_dir, returns a readFile obj containing of the new
# merged file 
def merge_helper(rset, merge_dir):
	# Set merge_path
	merge_path = merge_dir+merge_name_generator(rset[0])
	#print("merge_path=", merge_path)
	#for item in rset:
	#	print(item.fname)
	with open (merge_path, 'w') as opath:
		for rf in rset:
			if rf.gzip == True:
				comp_merge(rf, opath)
			else:
				uncomp_merge(rf, opath)

	ret_rf = readFile(merge_path)
	return ret_rf
