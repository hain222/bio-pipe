# File: blast.py
# Author: Harrison Inocencio
# Date: 07-24-18
# Purpose: Contains the blastBranch object, which runs all operations
#		   related to the pipes BLAST branch

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
import subprocess
import lib.args as args
import lib.plumber as plumber
from Bio import SeqIO

# blastBranch class
class blastBranch:
	"""
	This class contains all atr/functions needed to execute the blast
	branch portion of the pipeline. Generates BLAST databases, blastn 
	runs, and exports reports
	"""

	# __init__ func
	# Initializes passed attributes
	def __init__(self, blast_path, sample_pit, query_fpath):
		self.base_blast_path = blast_path
		self.sample_pit = sample_pit
		self.query_fpath = query_fpath
		self.query_list = []
		self.db_bucket = []

	# __format_id func
	# Removes periods/spaces from the passed id and returns a the new id
	# Used for creating the listed query file names
	def __format_id(self, rec_id):
		new_id = ""
		for char in rec_id:
			if char != '.' and char != " ":
				new_id+=char
			else:
				new_id+='_'

		return new_id

	# __split_queries func
	# Splits the query fasta entries into individual files for blasting
	# sets the query_list atr
	def __split_queries(self):
		query_recs = []
		for rec in SeqIO.parse(self.query_fpath, "fasta"):
			query_recs.append(rec)
	
		query_path = self.base_blast_path + args.query_dir
		plumber.force_dir(query_path)
		for rec in query_recs:
			write_out = [rec]
			write_path = query_path+self.__format_id(rec.id)+".fasta"
			SeqIO.write(write_out, write_path, "fasta")
			self.query_list.append(write_path)

	# __gen_db_path func
	# creates and the blast database directory for a passe sampleBall
	# returns the complete db name for the makeblastdb process
	def __gen_db_path(self, sball, bucket_path):
		dir_name = os.path.basename(sball.export_fasta).split(".")[0]
		dir_name += "_db/"
		db_name = os.path.basename(sball.export_fasta).split(".")[0]
		db_name += "_genome.fasta"
		dir_path = bucket_path + dir_name
		plumber.force_dir(dir_path)
		
		return dir_path + db_name

	# __build_bucket func
	# builds blast databases from all samples in sample_pit
	# sets the db_bucket atr
	def __build_bucket(self):
		bucket_path = self.base_blast_path + args.bucket_dir
		plumber.force_dir(bucket_path)
		for sball in self.sample_pit:
			print("\tMaking database for sample", sball.sample_id)
			out_path = self.__gen_db_path(sball, bucket_path)
			blast_cmd = ["makeblastdb", "-in", sball.export_fasta,
						"-dbtype", "nucl", "-out", out_path]
			try:
				blast_ret = subprocess.run(blast_cmd, 
										stdout=subprocess.PIPE,
										stdin=subprocess.PIPE, check=True,
										universal_newlines=True)
			except subprocess.CalledProcessError as perror:
				print("ERROR: makeblastdb failed!")

			self.db_bucket.append(out_path)

	# run func
	# Starts the blast branch
	def run(self):
		self.__split_queries()
		self.__build_bucket()
