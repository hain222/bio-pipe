# File: trim.py
# Author: Harrison Inocencio
# Date: 07-19-18
# Purpose: Contains the trim class, which generates parameters for, and 
#		   runs the trim subprocess.

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

import subprocess
from lib.readFile import readFile
import lib.plumber

# trimmer class
class trimmer:
	"""
	This class contains all of the parameters needed for the trim run,
	and includes a function that will run the trim command. 
	Note: the trim object containing the paths to the trim_log/trim_sum
		   will be exported as an attribute to the readBall for later
		   access by a log grabber
	"""

	# __init__ func
	# sets trim_args attribute and call __set_params
	def __init__(self, rball, trim_path, trim_args):
		self.trim_args = trim_args
		self.__set_params(rball, trim_path)

	# __set_params func
	# sets all input output file names using atr from rball
	def __set_params(self, rball, trim_path):
		fwd_rf = rball.fwd_merge_rf
		rev_rf = rball.rev_merge_rf

		# Set paths and logs
		self.sub_path = "%s%s-%s_trimmed/" % (trim_path, rball.run_id,
										rball.sample_id)
		self.trim_log = "%s%s-%s_errorlog.txt" % (self.sub_path, 
			rball.run_id, rball.sample_id)
		self.trim_sum = "%s%s-%s_summary.txt" % (self.sub_path, 
			rball.run_id, rball.sample_id)
		self.jar_path = rball.cbox.trim_jar_path

		# Set input/output files
		self.fwd_in = fwd_rf.fpath
		self.rev_in = rev_rf.fpath
		self.fwd_paired_out = "%s%s-%s_%s_%s_%s_paired.fastq" % (
			self.sub_path, fwd_rf.run_id, fwd_rf.sample, fwd_rf.sample, 
			fwd_rf.lane, fwd_rf.direction)
		self.fwd_unpaired_out = "%s%s-%s_%s_%s_%s_unpaired.fastq" % (
			self.sub_path, fwd_rf.run_id, fwd_rf.sample, fwd_rf.sample, 
			fwd_rf.lane, fwd_rf.direction)
		self.rev_paired_out = "%s%s-%s_%s_%s_%s_paired.fastq" % (
			self.sub_path, rev_rf.run_id, rev_rf.sample, rev_rf.sample, 
			rev_rf.lane, rev_rf.direction)
		self.rev_unpaired_out = "%s%s-%s_%s_%s_%s_unpaired.fastq" % (
			self.sub_path, rev_rf.run_id, rev_rf.sample, rev_rf.sample, 
			rev_rf.lane, rev_rf.direction)

	# run func
	# Starts the trim process. Once completes, checks the return code
	# and returns both fwd and rev paired files
	def run(self):
		lib.plumber.force_dir(self.sub_path)
		trim_cmd = ["java", "-jar", self.jar_path, "PE", '-phred33',
			"-trimlog", self.trim_log, "-summary", self.trim_sum, 
			self.fwd_in, self.rev_in, self.fwd_paired_out, 
			self.fwd_unpaired_out, self.rev_paired_out, 
			self.rev_unpaired_out]
		for param in self.trim_args.split(" "):
			trim_cmd.append(param)

		try:
			trim_ret = subprocess.run(trim_cmd, stdout=subprocess.PIPE, 
									stderr=subprocess.PIPE, check=True, 
									universal_newlines=True)
		except subprocess.CalledProcessError as perror:
			raise(RuntimeError("ERROR: trim run failed!"))
	
		fwd_ret = readFile(self.fwd_paired_out)
		rev_ret = readFile(self.rev_paired_out)

		return fwd_ret, rev_ret

	# tprint func
	# Prints all class atr, (for testing ...)
	def tprint(self):
		print(self.jar_path)
		print(self.trim_args)
		print(self.trim_log)
		print(self.trim_sum)
		print(self.fwd_in)
		print(self.rev_in)
		print(self.fwd_paired_out)
		print(self.fwd_unpaired_out)
		print(self.rev_paired_out)
		print(self.rev_unpaired_out)
		print()
