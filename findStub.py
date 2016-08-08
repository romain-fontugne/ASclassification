import glob
from collections import defaultdict

def readFiles(path="/usr/home/julien/prefix-deaggregation/dumped_results/one-month-intervall/2016.07/AS3356*prefixes*.txt"):
    stubas = {}
    for fi in glob.glob(path):
        for line in open(fi,"r"):
            _, path, _ = line.split(" - ")

            path = path.split(" ")
            lastas = path[-1]
            if not lastas in stubas:  
                stubas[lastas] = True

            for asn in path:
                # In the case of prepending
                if asn != lastas:
                    stubas[asn] = False

    return stubas

if __name__ == "__main__":

    stubas = readFiles()

    #output results
    fi = open("keywords/80_Stub.txt", "w")
    for asn, val in stubas.iteritems():
        if val:
            fi.write("^AS%s \n" % asn)

    fi.close()

