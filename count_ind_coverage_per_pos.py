"""
This script was written by Kelsey Witt in March 2018. This file takes an angsd .counts.gz file
(generated using the command angsd -doCounts 1 -dumpCounts 2) and the number of samples in the dataset as input and outputs an
_indDepth.txt file, a tab-separated file where each value is the number of positions called for x 
individuals, from x=1 to x=n. The values are in ascending order (ie x=1  x=2  x=3).

Usage: python3 count_ind_coverage_per_pos.py file.counts.gz sample_size

Contact: kelsey_witt_dillon@brown.edu
"""

import sys
import gzip

infile = sys.argv[1]
numSamples = sys.argv[2]

outfile = infile[:-10] + "_indDepth.txt"

outLine = ""

indDepthCounter = [0]*int(numSamples)

with gzip.open(infile, 'rt') as f:
    next(f)
    for line in f:
        indDepth = 0
        line_split = line.split()
        for readCount in line_split:
            if int(readCount) > 0:
                indDepth += 1
        counterPos=indDepth - 1
        indDepthCounter[counterPos] += 1
with open(outfile, 'w') as g:
    for depth in indDepthCounter:
        outLine += str(depth) + "\t"
    outLine = outLine[:-1]
    g.write(outLine)
