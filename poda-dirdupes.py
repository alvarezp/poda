#!/usr/bin/env python3

# Doesn't even work yet...

import os.path
import fileinput
import itertools
import sys

dirname = os.path.dirname
combinations = itertools.combinations

def dprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def similarity(dir1totalsize, dir2totalsize, equalcontentsize):
    try:
        return (equalcontentsize + equalcontentsize) / (dir1totalsize + dir2totalsize)
    except ZeroDivisionError:
        return 1

def processclass(direquals, dirsizes, pathamounts, filesize):
    #dprint("!!! Entering processclass...")
    pathlist = list()
    for path in pathamounts:
        splitpath = path.split('/')
        pathlist.extend(map("/".join, [splitpath[:i+1] for i in range(len(splitpath))]))
        amount = pathamounts[path]
        for p in map("/".join, [splitpath[:i+1] for i in range(len(splitpath))]):
            try:
                dirsizes[p] += amount * filesize
                #dprint("!!! dirsizes['%s'] += %d * %d" % (path, amount, filesize))
            except KeyError:
                dirsizes[p] = amount * filesize

    pathset = sorted(set(pathlist))
    #dprint("!!! generated path set: %s" % (str(pathset)))

    tuplelist = [(d1, d2) for (d1, d2) in combinations(pathset, 2) if not d2[0:len(d1)] == d1]
    #dprint("tuplelist: %s" % (str(tuplelist)))

    for t in tuplelist:
        # 1. Find out how many times the file occurs in each of the
        #    directories in the tuple
        # 2. Consider the minimum of the two to be the "common" amount for
        #    direquals (similarity).
        t0 = 0
        t1 = 0
        for p in paths:
            if p.startswith(t[0]):
                t0 = t0 + paths[p]
            if p.startswith(t[1]):
                t1 = t1 + paths[p]
        common = min(t0, t1)
        #dprint("! == common: %d %d %d" % (t0, t1, common))

        try:
            direquals[t] += common * filesize
        except KeyError:
            direquals[t] = common * filesize
        #dprint("!!! -- -- direquals[%s] += %d * %d = %d" % (str(t), common, filesize, direquals[t]))

dirsizes = dict()
direquals = dict()

paths = dict()

filesize = 0

prevline = "================================ 000000000000 xxxx-xx-xx xx:xx:xx +xxxx xxx xxx ./whatever\n"
n = 0

with open(0, 'r', errors='replace') as f:
    for line in f:
        # - The equal pool will be processed once a
        #   **differing-content** line is found.
        if line[0:51] != prevline[0:51]:
            processclass(direquals, dirsizes, paths, filesize)
            paths.clear()

        #dprint("+ " + line.rstrip())

        try:
            filesize = int(line.split(" ")[1])
        except:
            print("BAD LINE: " + line)
            raise
        #dprint("! filesize: %d" % (filesize))

        # Converts "host hamper ./path to/somedir/file.txt"
        # ..... to "host:hamper:./path to/somedir"
        path = ":".join([line.split(" ")[5], line.split(" ")[6], dirname(" ".join(line.split(" ")[7:]))])
        #dprint("! path: %s" % (path))

        try:
            paths[path] += 1
        except KeyError:
            paths[path] = 1

        prevline = line

    else:
        processclass(direquals, dirsizes, paths, filesize)


for p in direquals:
    ##print("! p = %s" % (str(p)))
    ##print("! dirsizes[p[0]] = %s" % (dirsizes[p[0]]))
    ##print("! dirsizes[p[1]] = %s" % (dirsizes[p[1]]))
    ##print("! direquals[p[1]] = %s" % (direquals[p]))
    s=similarity(dirsizes[p[0]], dirsizes[p[1]], direquals[p])
    if s >= 0.5:
        print("%18.0f  %6.2f%% %18s: %s %s" % (0.5 * s * direquals[p], 100 * s, direquals[p], p[0], p[1]))
