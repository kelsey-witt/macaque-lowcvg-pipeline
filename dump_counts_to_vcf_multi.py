"""
This script was written by Kelsey Witt in March 2018. This file takes an angsd .mafs.gz file (generated 
using the command angsd -doMajorMinor 4 -doMaf 2) and an angsd .counts.gz file (generated using the command 
angsd -doCounts 1 -dumpCounts 4), and generates haploid "pseudoautosomal" vcf files (one or many) where the 
SNP is randomly selected for each individual from all reads that mapped to that position.

Usage: python3 dump_counts_to_vcf_multi.py

The "ind" list determines the sample names in the vcf, and must be in the same order that is in the angsd
files. Please change these to reflect the names of your samples.

The variables "pos_infile" and "counts_infile must be changed to the name of your .mafs.gz and .counts.gz files, 
respectively, and you can change the name of variable "outfile" to whatever you wish. The "filename_start" and 
"filename_end" numbers specify how many replicate vcfs you wish to generate, and these numbers are added on to 
the outfile name. If you wish to only generate 1 vcf, set start to 1 and end to 2.

Contact: kelsey_witt_dillon@brown.edu
"""

import gzip
import random

filename_start = 1
filename_end = 101

ind=["002", "003", "006", "007", "008", "009", "010", "011", "013", "014", "015", "016", "025", "026", "028", \
"029", "030", "031", "032", "033", "037", "040", "045", "047", "048", "049", "050", "051", "052", "053", "054", \
"055", "058", "061", "065", "068", "073", "074", "075", "076", "077", "079", "081", "082", "083", "084", "088", \
"089", "090", "092", "095", "096", "106", "107", "109", "115", "116", "117", "118", "119", "123", "124", "125", \
"129", "131", "133", "137", "138", "139", "140", "141", "143", "144", "145", "149"]

pos_infile = "sites_pulled.mafs.gz"
counts_infile = "sites_pulled.counts.gz"
for i in range(filename_start, filename_end):
    print("file num:",str(i))
    outfile = "macaque_pseudoautosomal_snps_run" + i + ".vcf"

    posTracker = {}
    posCounter = 0

    with gzip.open(pos_infile, 'rt') as g:
        next(g)
        for line in g:
            line_split = line.split()
            chrom, pos, _, _, ref = line_split[0:5]
            posTracker[posCounter] = [chrom, pos, ref]
            posCounter += 1

    lineCounter = 0
    with gzip.open(counts_infile, 'rt') as f:
        with open(outfile, 'w') as h:
            h.write("##fileformat=VCFv4.1" + "\n")
            h.write('##INFO=<ID=.,Number=1,Type=Character,Description="description">' + "\n")
            h.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">' + "\n")
            vcf_header = ["#CHROM",	"POS", "ID", "REF", "ALT", "QUAL","FILTER", "INFO", "FORMAT"] + ind
            vcf_header_print = "\t".join(vcf_header)
            h.write(vcf_header_print + "\n")
            next(f)
            for line in f:
                ind_counter = 0
                line_split = line.split()
                snp_set = set()
                ind_snps = []
                print(line_split)
                for i in range(0,len(line_split),4):
                    snp = 0
                    A_count = int(line_split[i])
                    C_count = int(line_split[i+1])
                    G_count = int(line_split[i+2])
                    T_count = int(line_split[i+3])
                    SNPs_for_ind = "A" * A_count + "C" * C_count + "G" * G_count + "T" * T_count
                    #print(SNPs_for_ind)
                    if len(SNPs_for_ind) == 0:
                        snp = "."
                    else:
                        snp = random.choice(SNPs_for_ind)
                        snp_set.add(snp)
                    ind_snps.append(snp)
                ref_snp = posTracker[lineCounter][2]
                snp_list = list(snp_set)
                print(snp_list)
                if ref_snp in snp_list and len(snp_list) == 2: #must be biallelic including reference
                    print("true")
                    if snp_list[0] == ref_snp:
                        alt_snp = snp_list[1]
                    else:
                        alt_snp = snp_list[0]
                    chrom, pos = posTracker[lineCounter][0:2]
                    vcf_line = [chrom, pos, ".", ref_snp, alt_snp, ".", "PASS", ".", "GT"]
                    for snp in ind_snps:
                        if snp == ref_snp:
                            vcf_line.append("0")
                        elif snp == alt_snp:
                            vcf_line.append("1")
                        elif snp == ".":
                            vcf_line.append(".")
                    vcf_line_print = "\t".join(vcf_line)
                    h.write(vcf_line_print + "\n")
                lineCounter += 1