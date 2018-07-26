# File: sampleBall.py
# Author: Harrison Inocencio
# Date: 07-23-18
# Purpose: Contains the sampleBall class, used to contain data and
#		   functionality related to post-read processing operations 
#		   (assembly, SNPs, etc ...)

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

import shutil
import subprocess
import lib.args as args
import lib.formatter as formatter
from lib.config.config import config

# sampleBall class
class sampleBall:
	"""
	Contains all metadata/functionality realted to post-read processing
	operations.
	"""

	# __init__ func
	# Define class atr using passed readBall
	def __init__(self, rball, key_file=None):
		self.run_id = rball.run_id
		self.sample_id = rball.sample_id
		self.inter_rf = rball.inter_rf
		self.cbox = config()

		# Check that config obj loaded correctly
		try:
			self.cbox.check_path()
		except FileNotFoundError:
			raise(RuntimeError("Missing Config"))

		# Set strain_id if key_file provided
		if key_file != None:
			self.strain_id = self.__get_strain_id(key_file)
		self.assemble_path = None
		self.export_fasta = None

	# __get_strain_id func
	# Searches the provided key_file for a corresponding strain_id
	# If it can't be located, returns None
	def __get_strain_id(self, key_file):
		with open(key_file) as kf:
			dat = kf.readlines()
		key_mtx = []
		for line in dat:
			if line[0] != "#" and line.strip() != "":
				sline = line.strip().split("\t")
				key_mtx.append(sline)

		#print(key_mtx)
		for row in key_mtx:
			if row[0] == self.sample_id:
				return row[1]
		
		return None

	# __gen_assem_name func
	# Generates the vevlet assembly dir name
	def __gen_assem_name(self):
		if self.strain_id != None:
			return "%s-%s_assembly/" % (self.run_id, self.strain_id)
		else:
			return "%s-%s_assembly/" % (self.run_id, self.sample_id)

	# assemble func
	# Calls velvetoptimiser using the passed kmer args and assemble dir
	# sets the appropriate assemble atrs after the assembly is complete
	def assemble(self, assemble_dir, vkmer_args):
		self.assemble_path = assemble_dir + self.__gen_assem_name()
		#print(assemble_path)
		assem_cmd = [args.velvet_name]
		file_args = "%s -fastq %s" % (self.cbox.vread_type,
										self.inter_rf.fpath)
		for param in vkmer_args.split(" "):
			assem_cmd.append(param)
		assem_cmd += ["-d", self.assemble_path, "-f", file_args]
		#print(assem_cmd)
		try:
			assem_ret = subprocess.run(assem_cmd, stdout=subprocess.PIPE,
								stderr=subprocess.PIPE, check=True,
								universal_newlines=True)
		except subprocess.CalledProcessError as perror:
			raise(RuntimeError("ERROR: assembly failed!"))
	
	# export_assembly func
	# Copies the assembly fasta in assemble_path, into the exp_path
	# dir and renames the fasta according to the strain_id or sample_id
	def export_assembly(self, exp_path):
		if self.strain_id == None:
			cpy_dst = "%s%s-%s_%s.fasta" % (exp_path, self.run_id, 
											self.sample_id, self.sample_id)
		else:
			cpy_dst = "%s%s-%s_%s.fasta" % (exp_path, self.run_id, 
											self.sample_id, self.strain_id)

		shutil.copy("%scontigs.fa" % self.assemble_path, cpy_dst, 
					follow_symlinks=True)
		self.export_fasta = cpy_dst

	# format_headers func
	# Formats all of the sequence headers in the export_fasta file
	# to be usable with Dr. Farman's SNP caller program. 
	def format_headers(self):
		formatter.format_head(self)

	# tprint func
	# Prints all class atrs (for testing ...)
	def tprint(self):
		print(self.run_id)
		print(self.strain_id)
		print(self.sample_id)
		print(self.assemble_path)
		print(self.export_fasta)
		self.inter_rf.tprint()
