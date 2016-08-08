import glob
from collections import defaultdict
import cPickle as pickle

def readFiles(asType, agg="AS", path="/usr/home/julien/prefix-deaggregation/dumped_results/one-month-intervall/2016.07/AS3356*prefixes*.txt"):
    count = defaultdict(lambda : defaultdict(int)) 
    nbUnknown = 0
    for fi in glob.glob(path):
        prefixType = None
        for t in ["deaggregated", "delegated", "top", "lonely"]:
            if t in fi:
                prefixType = t
                break

        for line in open(fi,"r"):
            _, path, _ = line.split(" - ")
            asn = path.rpartition(" ")[2]
            if asn in asType:
                if agg == "AS":
                    count[asn][prefixType]+=1
                else:
                    count[asType[asn]][prefixType]+=1
            else:
                nbUnknown += 1
 
    print "%s unknown AS" % nbUnknown
    return count 


def getASclassification():
    asType = {}
    nbAsn = defaultdict(int)

    for line in open("results/classifiedAS.txt"):
        asn, label = line.split(" ")
        label = label[:-1]
        #if label == "LargeTransit":
            #asType[asn] = "T1_"+asn
        #else:
        asType[asn] = label
        nbAsn[label] += 1

    return asType, nbAsn


if __name__ == "__main__":
    agg = "AS"
    asType, nbAsnperClass = getASclassification()
    count = readFiles(asType, agg=agg)
    
    if agg!="AS":
        for business, bcount in count.iteritems():
            nbPrefix = sum(bcount.values())
            print "%s (%s ASN, %s prefixes)" % (business, nbAsnperClass[business], nbPrefix)
            for ptype, val in bcount.iteritems():
                print "\t%s %02.2f%%" % (ptype, val*100.0/nbPrefix)
    else:
        ratioPerBusiness = defaultdict(lambda: defaultdict(list)) 
        for asclas in [set(asType.values())]:
            for asn, acount in count.iteritems():
                nbPrefix = sum(acount.values())
                for t in [ "delegated", "lonely", "top","deaggregated"]:
                    if t in acount:
                        ratioPerBusiness[asType[asn]][t].append(acount[t]*100.0/nbPrefix)
                    else:
                        ratioPerBusiness[asType[asn]][t].append(0.0)


        for business, ratioPerCat in ratioPerBusiness.iteritems():
            print business
            for ptype, val in ratioPerCat.iteritems():
                print "\t%s %02.2f%% (median=%02.2f%%)" % (ptype, sum(val)/len(val), sorted(val)[len(val)/2])


        print ratioPerBusiness["LargeTransit"]
       
        #for asn, acount in count.iteritems():
            #nbPrefix = float(sum(acount.values()))
            #if "deaggregated" in acount and acount["deaggregated"]/nbPrefix > 0.75:
                #print "%s %s %s" % ( asn, asType[asn],acount["deaggregated"]/nbPrefix)

        pickle.dump([agg, asType, dict(nbAsnperClass), dict(count)], open("countsPerAS.pickle", "w"))
