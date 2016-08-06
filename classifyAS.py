import re
import sys
import glob

def readKeywordFiles(path="./keywords/*.txt"):
    regexp = [] 
    files = glob.glob(path)
    files.sort()

    for fi in files:
        label = fi.rpartition("/")[2].split(".")[0].partition("_")[2]
        sys.stderr.write("Loading %s keywords...\n" % label)
        
        keywords = "|".join(open(fi,"r").read().splitlines())
        regexp.append((label, re.compile(keywords, re.IGNORECASE)))

    return regexp


def classify(regexp, asnFile="./asNames0.txt", output="results/classifiedAS.txt"):
    count = 0
    outFile = open(output, "w")

    for line in open(asnFile, "r"):
        if " " in line:
            asn, _, _ = line.partition(" ")
        else:
            asn = line

        for (label, reg) in regexp:
            if reg.search(line):
                count += 1
                outFile.write("%s %s\n" % (asn[2:], label))
                break

    sys.stderr.write("Found %s ASs\n" % count)


if __name__ == "__main__":
    regexp = readKeywordFiles()
    classify(regexp) 
