"""
This script was written by Kelsey Witt in September 2019. This script adds the outgroup genotype to a phylip file
by pulling the reference genotype from the vcf file for the same SNPs. (M. mulatta was used as the outgroup for this 
analysis, but for all SNPs in this dataset, its genotype was identical to the reference genome for M. fascicularis
and so those alleles were used instead). It requires a vcf_infile and a phy_infile of the same data, and can be 
run on multiple replicates at the same time, where the range controls the file numbers that are modified to add the 
outgroup.

Usage: python3 add_macaque_outgroup.py

Contact: kelsey_witt_dillon@brown.edu
"""
for i in range(0,1):
    vcf_infile = "/home/Kelseywd/macaque_lu/angsd_out/snp_counter/pseudoautosomal_replicates/macaque_pseudoautosomal_snps_run" + \
    str(i) + ".vcf"
    phy_infile = "/home/Kelseywd/macaque_lu/raxml_tree/phylip_reps/macaque_pseudoautosomal_snps_run" + str(i) + ".phy"
    phy_outfile = phy_infile[:-4] + "_outgroup.phy"
    with open(vcf_infile) as f:
        refSequence = ""
        next(f)
        next(f)
        next(f)
        next(f)
        for line in f:
            lineSplit = line.split(sep="\t")
            refAllele = lineSplit[3]
            refSequence += refAllele
    with open(phy_outfile, 'w') as g:
        with open(phy_infile) as h:
            for line in h:
                if "75 " in line:
                    newLine = "76 " + line[3:]
                    g.write(newLine)
                else:
                    g.write(line)
    with open(phy_outfile,"a") as j:
        j.write("MacaqueRef" + "\t" + refSequence + "\n")