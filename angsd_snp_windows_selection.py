"""
This script was written by Kelsey Witt in March 2018. This file takes an angsd .mafs file
(generated using the command angsd -doMajorMinor 1 -doMaf 2) and outputs a text file containing
a randomized set of unlinked SNPs, where each window (default size 50 kB, but can be changed)
contains only one SNP. This file can then be used as the input file for "filter_angsd_beagle_snps.py".

Usage: python3 angsd_snp_windows_selection.py

The variable "infile" must be changed to the name of your .mafs file, and you can change the variable "outfile"
to have whatever suffix you wish. Other optional variables that can be changed include window_size (window size, 
to control for linkage), indCutoff (if the selected snps need to have a minimum number of individuals represented, 
otherwise set to 1), and minAlleleFreq(if you want the minor allele frequency to be above a certain value, otherwise 
set to 0)

Contact: kelsey_witt_dillon@brown.edu
"""

import random
infile = "macaque_gl_1p_50_01.mafs"
outfile = infile[:-5] + "_unlinked_snps.txt"
window_size = 50000
indCutoff = 56
minAlleleFreq = 0.1

window = 0
curr_window_position = 0-window_size
curr_chromosome = "0"
output_chromosome = "0"
window_max_pos = []

g = open(outfile, 'w')
with open(infile) as f:
    next(f)
    for line in f:
        Hi_Cvg_hi_maf = False
        chrom_shift = False
        line_split = line.split()
        chromosome, pos = line_split[0:2]
        if chromosome != curr_chromosome:
            curr_window_position = 0-window_size
            output_chromosome = curr_chromosome
            curr_chromosome = chromosome
            chrom_shift = True
        position = int(pos)
        if position < curr_window_position + window_size: #If position is in the same window specified:
            nInd = int(line_split[7])
            maf = float(line_split[5])
            if nInd > indCutoff and maf > minAlleleFreq:
                Hi_Cvg_hi_maf = True
            if Hi_Cvg_hi_maf:
                if float(window_max_pos[0][2])<minAlleleFreq or int(window_max_pos[0][1])<=indCutoff:
                    window_max_pos = [[position,str(nInd),str(maf)]]
                else:
                    window_max_pos.append([position,str(nInd),str(maf)])
            else:
                max_pos, max_nind, max_maf = window_max_pos[0][0:3]
                if maf > float(max_nind) or nInd > int(max_nind):
                    window_max_pos = [[position,str(nInd),str(maf)]]
        else:
            if window >= 1:
                if len(window_max_pos) > 1:
                    position_picked = random.randint(0,(len(window_max_pos)-1))
                    pos, snp_ind, snp_maf = window_max_pos[position_picked][0:3]
                else:
                    pos, snp_ind, snp_maf = window_max_pos[0][0:3]
                if chrom_shift:
                    chromosome = output_chromosome
                out_line = str(window) + "\t" + chromosome + "\t" + str(pos) + "\t" + str(snp_ind) + "\t" + str(snp_maf) + "\n"
                g.write(out_line)
            window += 1
            window_max_pos = []
            nInd = int(line_split[7])
            maf = float(line_split[5])
            window_max_pos.append([position,str(nInd),str(maf)])
            curr_window_position = position
    if len(window_max_pos) > 1:
        position_picked = random.randint(0,(len(window_max_pos)-1))
        pos, snp_ind, snp_maf = window_max_pos[position_picked][0:3]
    else:
        pos, snp_ind, snp_maf = window_max_pos[0][0:3]
    out_line = str(window) + "\t" + chromosome + "\t" + str(pos) + "\t" + str(snp_ind) + "\t" + str(snp_maf) + "\n"
    g.write(out_line)
g.close()
print(str(window))