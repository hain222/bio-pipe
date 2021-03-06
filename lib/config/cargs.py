# File: cargs.py
# Author: Harrison Inocencio
# Date: 07-18-18
# Purpose: Contains consts/arg parsing for the config class and the 
#		   configQuery script

# Notes:
# 1.
# 2.
# 3.
# 4.
# 5.

# TODO:
# 1. Renovate error messages/headers 
# 2.
# 3.
# 4.
# 5.

# -------------------------------------------------------------------

# Config path
config_path = "bioPipe_config.ini"

# Config contents
config_header = "# This is an automatically generated configuration file\n"
	# Trimmomatic
trim_section = 'TRIMMOMATIC'
trim_jar_path_key = 'trimJarPath'
	# Velvet
velvet_section = 'VELVET'
vread_type_key = 'vReadType'

# Errors
key_error = 'ERROR: INI Key error encountered'
