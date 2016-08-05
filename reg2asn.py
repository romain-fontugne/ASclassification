import re
import sys

asnFile = "uniqASN.txt"
regexp = {}
#regexp["Academic/Research"] = re.compile(".*research.*|.*university.*|.*college.*|.*school.*|.*research.*|.*institute of technology.* |.*univerzita.*|.*universidad.*|.*universiteet.*|.*universite.*|.*faculte.*|.*egyetem.*| .*universita.*|.*ateneo.*|.*uniwersitet.*|.*universitate.*|.*augstskola.*|.*universiteit.*| .*hogeschool.*|.*academie.*|.*uniwersytet.*|.*universidade.*|.*universitate.*|.*univerzitet.*| .*univerzita.*|.*universitet.*|.*universitet.*|.*akademi.*", re.IGNORECASE)
regexp["Academic/Research"] = re.compile("research|university|college|school|research|institute of technology|univerzita|universidad|universiteet|universite|faculte|egyetem|universita|ateneo|uniwersitet|universitate|augstskola|universiteit|hogeschool|academie|uniwersytet|universidade|universitate|univerzitet|univerzita|universitet|universitet|akademi", re.IGNORECASE)
count = 0

for line in open(asnFile, "r"):
    asn, _, name = line.partition(" ")

    for label, reg in regexp.iteritems():
        if reg.search(name):
            count += 1
            sys.stdout.write("%s %s\n" % (asn[2:], label))


sys.stderr.write("Found %s ASs\n" % count)
