# File: formatter.py
# Author: Harrison Inocencio
# Date: 07-24-18
# Purpose: Contains helper functions for any formatting operations that
#		   are needed for the pipeline

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

from Bio import SeqIO

# seq_parse func
# Parses the targeted file into seq recs using
# Biopython
def seq_parse(path):
	seq_recs = []
	for rec in SeqIO.parse(path, "fasta"):
		seq_recs.append(rec)

	return seq_recs

# rename func
# renames ids and descriptions given a set of seq records
def rename(sball, seq_recs):
	if sball.strain_id == None:
		prefix = "%s_%s_%s_contig" % (sball.run_id, sball.sample_id,
									sball.sample_id)
	else:
		prefix = "%s_%s_%s_contig" % (sball.run_id, sball.sample_id,
									sball.strain_id)
	contig_cnt = 1
	for rec in seq_recs:
		cur_name = prefix+str(contig_cnt)
		rec.id = cur_name
		rec.description = cur_name
		contig_cnt += 1

	return seq_recs

# format_head func
# Helper func that replaces fasta headers in the target file
# with generic replicated ones. Takes a sample ball as input.
def format_head(sball):
	orig_recs = seq_parse(sball.export_fasta)
	rename_recs = rename(sball, orig_recs)
	SeqIO.write(rename_recs, sball.export_fasta, "fasta")
