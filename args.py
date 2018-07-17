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

# parser HELPS
read_dir_help = "read_dir HELP"

# parse func
# parses arguments from the command line
def parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('read_dir', help=read_dir_help)
	args = parser.parse_args()

	return args
