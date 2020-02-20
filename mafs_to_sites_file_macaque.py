import gzip

def decode_split_line(line):
    line = str(line.decode('utf-8'))
    line = line.split(sep="\t")
    return line

infile = "macaque_gl_1p_50_01.mafs.gz"
outfile = "macaque_gl_1p_50_01.sites.txt"

of = open(outfile, 'r')
with gzip.open(infile, 'r') as f:
    next(f)
    for line in f:
        spline = decode_split_line(line)
        chromo,pos = spline[0:2]
        outLine = chromo + "\t" + pos + "\n"
        of.write(outLine)
of.close()