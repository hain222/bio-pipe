# File: args.py
# Author: Harrison Inocencio
# Date: 07-17-18
# Purpose: Contains const/arg parsing for the bioPipe class

# Notes:
# 1.
# 2.
# 3.
# 4.
# 5.

# TODO:
# 1. Complete HELPS
# 2.
# 3.
# 4.
# 5.

# -------------------------------------------------------------------

import argparse

# Output sub dir names (terminal '/' required)
merge_dir = 'merged_reads/'
trim_dir = 'trimmed/'
inter_dir = 'interleaved/'
assemble_dir = 'assembly/'
assembly_exp_dir = 'fastas/'

# parser HELPS
read_dir_help = "read_dir HELP"
output_dir_help = "output_dir HELP"
trim_args_help = "trim_args HELP"
key_file_help = "key_file HELP"
velvet_kmer_args_help = 'velvet_kmer_args HELP'
blast_help = 'blast HELP'

# Executable names
velvet_name = "VelvetOptimiser.pl"

# parse func
# parses arguments from the command line
def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('read_dir', help=read_dir_help)
	parser.add_argument('output_dir', help=output_dir_help)
	parser.add_argument('velvet_kmer_args', help=velvet_kmer_args_help)
	parser.add_argument('-t', '--trim_args', help=trim_args_help)
	parser.add_argument('-k', '--key_file', help=key_file_help)
	parser.add_argument('-b', '--blast', help=blast_help)
	args = parser.parse_args()

	return args
