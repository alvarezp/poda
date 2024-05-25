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
        try:
            npa[newpath] += pathamounts[p]
        except KeyError:
            npa[newpath]  = pathamounts[p]
    dprint("...           TO: %s" % (npa))
    return npa

def processclass(direquals, dirsizes, pathamounts, filesize):
    dprint("\n\n!!! Entering processclass for size %d with pathamounts: " % (filesize), pathamounts)

    while len(pathamounts) != 0:

        for p in pathamounts:
            try:
                dirsizes[p] += pathamounts[p] * filesize
            except KeyError:
                dirsizes[p]  = pathamounts[p] * filesize
            dprint("+ dirsizes[%s] += %s" % (p, pathamounts[p] * filesize))

        dirpairs = list(itertools.combinations(sorted(pathamounts), 2))
        for (dir1, dir2) in list(dirpairs):
            amount = min(pathamounts[dir1], pathamounts[dir2])
            try:
                direquals[(dir1, dir2)] += amount * filesize
            except KeyError:
                direquals[(dir1, dir2)]  = amount * filesize
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
            processclass(direquals, dirsizes, paths, filesize)
            paths.clear()

        try:
            filesize = int(line.split(" ")[1])
        except:
            eprint("BAD LINE: " + line)
            raise

        # Converts "host hamper ./path to/somedir/file.txt"
        # ..... to "host:hamper:./path to/somedir"
        path = ":".join([line.split(" ")[5], line.split(" ")[6], dirname(" ".join(line.split(" ")[7:]))])
        dprint("! path: %s" % (path))

        try:
            paths[path] += 1
        except KeyError:
            paths[path]  = 1

        prevline = line

    else:
        processclass(direquals, dirsizes, paths, filesize)


for p in direquals:
    dprint("! dirsizes = %3s, %3s; direquals = %3s for the pair %s" % (dirsizes[p[0]], dirsizes[p[1]], direquals[p], str(p)))
    try:
        #Calculate similarity
        s = 2 * direquals[p] / (dirsizes[p[0]] + dirsizes[p[1]])
        if s >= 0.5:
            print("%18s %6.2f%% %s %s" % (direquals[p], 100 * s, p[0], p[1]))
    except ZeroDivisionError:
        pass
