# File: qSeq.py
# Author: Harrison Inocencio
# Date: 07-26-18
# Purpose: Contains the qSeq class, contains a query sequence, a list
# 		   of subject sequences, and serves as a unit of orginization in 
#		   the blast branch. Provides blast functionalities

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
import lib.plumber as plumber

# qSeq class
class qSeq:
	"""
	Contains a query sequence path, a list of subject sequence paths, and 
	provides functionalities for blasting and storing output
	"""

	# __init__ func
	# initializes passed values and empty variables
	def __init__(self, query_path, bucket):
		self.query = query_path
		self.query_name = os.path.basename(query_path).split(".")[0]
		self.bucket = bucket
		self.archives = []
		self.reports = []

	# __gen_out_name func
	# Given a query and database, creates a blast report file name
	# i.e KT772.4560-S5-KY155_genomeBLASTn11
	def __gen_out_name(self, db_path):
		query_string = self.query_name
		subj_string = os.path.basename(db_path).split(".")[0]
		blast_name = "%s.%sBLASTn11" % (query_string, subj_string)

		return blast_name

	# __gen_archive_subdir func
	# Returns a name for the archive subdir needed to store the qSeq 
	# objs archive reports
	def __gen_archive_subdir(self):
		query_name = self.query_name
		return query_name + "_archives/"

	# bucket_blast func
	# Blasts the objs query against the databases in bucket. All
	# archive paths are stored in self.archives, and all the files
	# are written to the base archive_path plus a sub dir according to
	# query
	def bucket_blast(self, archive_path):
		blast_path = archive_path + self.__gen_archive_subdir()
		plumber.force_dir(blast_path)
		for db_path in self.bucket:
			out_path = blast_path + self.__gen_out_name(db_path)
			blast_cmd = ["blastn", "-db", db_path, "-query", self.query,
						"-out", out_path, "-evalue",
						"1e-20", "-outfmt", "11"]
			try:
				blast_ret = subprocess.run(blast_cmd, 
											stdout=subprocess.PIPE,
											stderr=subprocess.PIPE,
											check=True, 
											universal_newlines=True)
			except subprocess.CalledProcessError as perror:
				raise(RuntimeError("ERROR: BLAST failed!"))

			self.archives.append(out_path)

			#print(blast_cmd)

	# __gen_report_subdir func
	# Generates the subdir name for the reports step of the branch
	def __gen_report_subdir(self):
		return self.query_name + "_reports/"

	# __gen_report_name func
	# Generates the report file name for the reports step of the branch
	def __gen_report_name(self, arch_path):
		prefix = os.path.basename(arch_path)[:-3]
		return prefix + "n0"

	# convert_hr_reports func
	# Converts the all archives present in self.archives into
	# hr reports. Sets the self.reports atr.
	def convert_hr_reports(self, reports_path):
			convert_path = reports_path + self.__gen_report_subdir()
			plumber.force_dir(convert_path)
			for arch_path in self.archives:
				out_path = convert_path + self.__gen_report_name(arch_path)
				bconvert_cmd = ["blast_formatter", "-archive", arch_path,
								"-outfmt", "0", "-out", out_path]
				#print(bconvert_cmd)
				try:
					convert_ret = subprocess.run(bconvert_cmd,
											stdout=subprocess.PIPE,
											stderr=subprocess.PIPE, 
											check=True,
											universal_newlines=True)
				except subprocess.CalledProcessError as perror:
					raise(RuntimeError("ERROR: Report conversion failed!"))

				self.reports.append(out_path)
