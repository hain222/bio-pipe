# File: setBuild.py
# Author: Harrison Inocencio
# Date: 07-17-18 
# Purpose: Used for building the sampleSet array in bioPipe

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

from readFile import readFile
from sampleSet import sampleSet

# build_sets func
# build the master list of sampleSets from a list of fastq paths
def build_sets(fastq_list):
	# Build readFile objs and sort
	rf_pile = []
	for fpath in fastq_list:
		rf_obj = readFile(fpath)
		rf_pile.append(rf_obj)

	rf_pile.sort(key=lambda s: s.sample)

	# group readFile objs and construct sampleSets from sorted pile
	sample_sets = []
	cur_samp = rf_pile[0].sample
	cur_samp_list = []
	for item in rf_pile:
		if item.sample == cur_samp:
			cur_samp_list.append(item)
		else:
			samp_set = sampleSet(cur_samp_list)
			sample_sets.append(samp_set)
			cur_samp_list = [item]
			cur_samp = item.sample
		
	# Append trailing sampleSet
	samp_set = sampleSet(cur_samp_list)
	sample_sets.append(samp_set)

	return sample_sets
