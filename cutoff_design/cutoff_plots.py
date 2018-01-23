import sys
import glob

sam_files = glob.glob("*magicblast*.sam")

print("alignment\tscore\tlength")
for sfile in sam_files:
    for line in open(sfile):
        la = line.strip().split("\t")
        if (len(la)) == 14:
            length = len(la[9])
            score = la[12].split(":")[-1]
            print("{}\t{}\t{}".format(sfile,score,length))
