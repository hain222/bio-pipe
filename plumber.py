# File: plumber.py
# Author: Harrison Inocencio
# Date: 07-17-18 
# Purpose: Contains a variety of helper functions for the bioPipe class

# Notes:
# 1. Called plumber b/c plumbers maintain 'pipes' har-har
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
import shutil
from readFile import readFile
from readBall import readBall

# build_sets func
# build the master list of readBalls from a list of fastq paths
def build_read_pit(fastq_list):
	# Build readFile objs and sort
	rf_pile = []
	for fpath in fastq_list:
		rf_obj = readFile(fpath)
		rf_pile.append(rf_obj)

	rf_pile.sort(key=lambda s: s.sample)

	# group readFile objs and construct readBalls from sorted pile
	read_pit = []
	cur_samp = rf_pile[0].sample
	cur_ball_list = []
	for item in rf_pile:
		if item.sample == cur_samp:
			cur_ball_list.append(item)
		else:
			rball = readBall(cur_ball_list)
			read_pit.append(rball)
			cur_ball_list = [item]
			cur_samp = item.sample
		
	# Append trailing readBall
	rball = readBall(cur_ball_list)
	read_pit.append(rball)

	return read_pit

# force_dir func
# Forces creation of specified directory by deleting the prexisting
# dir if found.
def force_dir(dpath):
	try:
		os.mkdir(dpath)
	except FileExistsError:
		shutil.rmtree(dpath)
		os.mkdir(dpath)
	
