"""
This script was written by Kelsey Witt in March 2018. This file takes an angsd .counts.gz file
(generated using the command angsd -doCounts 1 -dumpCounts 2), calculates the number of positions
covered by each individual sample and the percentage of the total positions across all samples.
It outputs a .csv file with four columns: Sample Name, Positions (positions covered), Percent_Covered
(the percentage of total positions across all samples present in the one sample), and Total_Depth (the number
of positions mapped across all reads).

Usage: python3 count_ind_coverage_per_pos.py 

The "infile", "outfile", and "totalInd" must be changed to reflect your sample, where totalInd should be set
to the sample size.

Contact: kelsey_witt_dillon@brown.edu
"""

import gzip 
import csv

infile = "./coverage_summary_min5/coverage_summary_min5.counts.gz"
outfile = "coverage_summary_min5_indbreakdown.csv"

totalPositions = 0
totalInd = 147
positionsByInd = [0] * totalInd
depthByInd = [0] * totalInd

def decode_split_line(line):
    line = str(line.decode('utf-8'))
    if '#' not in line:
        line = line.split()
    return line

with gzip.open(infile) as f:
    next(f)
    for line in f:
        totalPositions += 1
        if totalPositions % 500000 == 0:
            print(totalPositions)
        colCounter = 0
        line_split = decode_split_line(line)
        for individual in line_split:
            individual = int(individual)
            if individual > 0:
                depthByInd[colCounter] += individual
                positionsByInd[colCounter] += 1
            colCounter += 1

percentCoverage = []

for individual in positionsByInd:
    percent = individual/totalPositions
    percentCoverage.append(str(percent))

with open(outfile, 'w', newline='') as f:
    csvwriter = csv.writer(f, delimiter=',')
    header_line = ["Sample", "Positions", "Percent_Covered", "Total_Depth"]
    csvwriter.writerow(header_line)
    for sample in range(0,147):
        sampleID = sample + 1
        if sampleID > 72:
            sampleID += 1
        indRow = [sampleID, positionsByInd[sample], percentCoverage[sample], depthByInd[sample]]
        csvwriter.writerow(indRow)