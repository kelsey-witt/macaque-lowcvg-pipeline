"""
This script was written by Kelsey Witt in March 2018. This file takes an angsd .pos.gz file
(generated using the command angsd -doCounts 1 -dumpCounts 1), filters out all SNPs that do not have
a minimum number of samples represented (minInd), and converts it into a sites file (chromosome position) 
for use with realSFS using the -sites flag.

Usage: python3 angsd_snp_windows_selection.py

The variable "infile" must be changed to the name of your .pos.gz file, and you can change the name of variable "outfile"
to whatever you wish. The "minInd" variable specifies the number of individuals who must have a genotype at that position
for it to be included in the sites file - if you wish to include all SNPs, set it to 0.

Contact: kelsey_witt_dillon@brown.edu
"""
import gzip
infile = "coverage_summary_min5_1mil_1p.pos.gz"
outfile = "1mil_1p_min38_sites.txt"
minInd = 38

with gzip.open(infile, 'rt') as f:
    with open(outfile, 'w') as g:
        next(f)
        for line in f:
            line_split = line.split()
            chrom, pos, tot_depth = line_split[0:3]
            if int(tot_depth) > minInd:
                out_line = chrom + " " + pos + "\n"
                g.write(out_line)
