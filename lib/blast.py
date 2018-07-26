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
from lib.qSeq import qSeq

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
		self.db_bucket = []
		self.qSeq_list = []

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
	
		query_list = []
		query_path = self.base_blast_path + args.query_dir
		plumber.force_dir(query_path)
		for rec in query_recs:
			write_out = [rec]
			write_path = query_path+self.__format_id(rec.id)+".fasta"
			SeqIO.write(write_out, write_path, "fasta")
			query_list.append(write_path)
			
		return query_list

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
			print("\t\tMaking database for sample", sball.sample_id)
			out_path = self.__gen_db_path(sball, bucket_path)
			blast_cmd = ["makeblastdb", "-in", sball.export_fasta,
						"-dbtype", "nucl", "-out", out_path]
			try:
				blast_ret = subprocess.run(blast_cmd, 
										stdout=subprocess.PIPE,
										stdin=subprocess.PIPE, check=True,
										universal_newlines=True)
			except subprocess.CalledProcessError as perror:
				raise(RuntimeError("ERROR: makeblastdb failed!"))

			self.db_bucket.append(out_path)

	# __build_qSeqs func
	# Builds a list of all qSeq objects using query_list and the db_bucket
	def __build_qSeqs(self, query_list):
		for query_path in query_list:
			new_qSeq = qSeq(query_path, self.db_bucket)
			self.qSeq_list.append(new_qSeq)

	# __blast_all func
	# Calls the bucket_blast function on each qSeq obj in qSeq_list
	def __blast_all(self):
		archive_path = self.base_blast_path + args.archive_dir
		plumber.force_dir(archive_path)
		for query in self.qSeq_list:
			print("\t\tBlasting %s against bucket ..." % query.query_name)
			query.bucket_blast(archive_path)

	# __gen_hr_reports func
	# Converts the archive to human readable reports
	def __gen_hr_reports(self):
		reports_path = self.base_blast_path + args.report_dir
		plumber.force_dir(reports_path)
		for query in self.qSeq_list:
			print("\t\tBuilding reports for %s ..." % query.query_name)
			query.convert_hr_reports(reports_path)

	# Extracts the hit subject sequences and writes them
	# to their own fastas
	def __extract_sub_seqs(self):
		sub_seq_path = self.base_blast_path + args.sub_seq_dir
		plumber.force_dir(sub_seq_path)
		for query in self.qSeq_list:
			print("\t\tBuilding reports for %s ..." % query.query_name)
			query.get_sub_seqs(sub_seq_path)

	# run func
	# Starts the blast branch
	def run(self):
		print("\tBLASTER alive and running ...")
		print("\tSplitting queries ...")
		query_list = self.__split_queries()
		print("\tBuiding database bucket ...")
		self.__build_bucket()
		self.__build_qSeqs(query_list)
		print("\tBeginning bucket blasts ...")
		self.__blast_all()
		print("\tBuilding HR reports ...")
		self.__gen_hr_reports()
		print("\tExtracting subject seq fastas ...")
		self.__extract_sub_seqs()
