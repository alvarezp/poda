#!/usr/bin/env python3

import os.path
import fileinput
import itertools
import sys

dirname = os.path.dirname
combinations = itertools.combinations

def dprint(*args, **kwargs):
    #print(*args, file=sys.stderr, **kwargs)
    pass

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def recombine_next_parents(pathamounts):
    dprint("RECOMBINING FROM: %s" % (pathamounts))
    npa = dict();
    for p in pathamounts:
        newpath = dirname(p)
        if newpath == "":
            continue
        npa[newpath] = npa.get(newpath, 0) + pathamounts[p]
    dprint("...           TO: %s" % (npa))
    return npa

def processclass(direquals, dirsizes, pathamounts, filesize):
    dprint("\n\n!!! Entering processclass for size %d with pathamounts: " % (filesize), pathamounts)

    while len(pathamounts) != 0:

        for p in pathamounts:
            dirsizes[p]  = dirsizes.get(p, 0) + pathamounts[p] * filesize
            dprint("+ dirsizes[%s] += %s" % (p, pathamounts[p] * filesize))

        dirpairs = list(combinations(sorted(pathamounts), 2))
        dprint("+ list of dirpairs: ", dirpairs)
        for p in dirpairs:
            minamount = min(pathamounts[p[0]], pathamounts[p[1]])
            direquals[p]  = direquals.get(p, 0) + minamount * filesize
            dprint("+ direquals['%s'] += %d * %d" % (p, minamount, filesize))

        pathamounts = recombine_next_parents(pathamounts)


dirsizes = dict()
direquals = dict()

paths = dict()

filesize = 0

prevline = "================================ 000000000000000000 xxxx-xx-xx xx:xx:xx +xxxx xxx xxx ./whatever\n"
n = 0

with open(0, 'r', errors='replace') as f:
    for line in f:
        # - The equal pool will be processed once a
        #   **differing-content** line is found.
        
        # 51 is the length of the hash plus the size on the line.
        if line[0:51] != prevline[0:51]:
            try:
                processclass(direquals, dirsizes, paths, int(prevline.split(" ")[1]))
            except:
                eprint("BAD LINE: " + prevline)
                raise
            paths.clear()


        # Converts "host hamper ./path to/somedir/file.txt"
        # ..... to "host:hamper:./path to/somedir"
        path = ":".join([line.split(" ")[5], line.split(" ")[6], dirname(" ".join(line.split(" ")[7:]))])
        #dprint("! path: %s" % (path))

        paths[path] = paths.get(path, 0) + 1

        prevline = line

    else:
        try:
            processclass(direquals, dirsizes, paths, int(prevline.split(" ")[1]))
        except:
            eprint("BAD LAST LINE: " + prevline)
            raise


for p in direquals:
    dprint("! dirsizes = %3s, %3s; direquals = %3s for the pair %s" % (dirsizes[p[0]], dirsizes[p[1]], direquals[p], str(p)))
    try:
        #Calculate similarity
        s = 2 * direquals[p] / (dirsizes[p[0]] + dirsizes[p[1]])
        if s >= 0.5:
            print("%18s %6.2f%% %s %s" % (direquals[p], 100 * s, p[0], p[1]))
    except ZeroDivisionError:
        pass
