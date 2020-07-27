#!/usr/bin/env python3

# Doesn't even work yet...

import os.path
import fileinput
import itertools
import sys

def similarity(dir1totalsize, dir2totalsize, equalcontentsize):
    if dir1totalsize + dir2totalsize == 0:
        return 1
    return 2 * equalcontentsize / (dir1totalsize + dir2totalsize)

def dir1_contains_or_is_dir2(dir1, dir2):
    return dir2[0:len(dir1)] == dir1

dirsizes = dict()
direquals = dict()
equalpathpool = list()
nextdirequals = set()
equalpathtotals = dict()

with open(0, 'r', errors='replace') as f:

    prevline = "================================ 000000000000 xxxx-xx-xx xx:xx:xx +xxxx xxx xxx ./whatever\n"
    n = 0
    while True:

        line = f.readline()
        if line != "":
            n = n + 1
            #print(n)
            #print("+ " + line.rstrip())

            try:
                size = int(line.split(" ")[1])
            except:
                print("BAD LINE: " + line)
                raise
                
            path = ":".join([line.split(" ")[5], line.split(" ")[6], os.path.dirname(" ".join(line.split(" ")[7:]))])
            
            while True:
                if path in dirsizes:
                    dirsizes[path] += size
                else:
                    dirsizes[path] = size
                #print("! dirsizes['%s'] += %s" % (path, size))
                path = os.path.dirname(path)
                if path == "/" or path == "":
                    break

        prevsize = int(prevline.split(" ")[1])
        prevpath = ":".join([prevline.split(" ")[5], prevline.split(" ")[6], os.path.dirname(" ".join(prevline.split(" ")[7:]))])

        # add the path from prevline to an "equal pool"
        if prevpath not in equalpathpool:
            equalpathpool.append(prevpath)
            #print("! equalpathpool.append('%s')" % (prevpath))
            while True:
                if prevpath in equalpathtotals:
                    equalpathtotals[prevpath] += prevsize
                else:
                    equalpathtotals[prevpath] = prevsize
                ##print("! equalpathtotals['%s'] += %s" % (prevpath, prevsize))
                prevpath = os.path.dirname(prevpath)
                if prevpath == "/" or prevpath == "":
                    break

        # - The equal pool will be processed once a
        #   **differing-content** line is found.
        # When the equal pool is processed:
        # - equal[./a/b][./c/d] += size per path combination
        #   from the equal pool, but if c and d are
        #   subdirs, then the parent dirs will also
        #   have the size added, thus:
        #   - equal[./a][/c] += size, also.
        if line[0:51] != prevline[0:51]:
            #print("! processing equalpathpool: " + str(equalpathpool))
            combs = itertools.combinations(sorted(equalpathpool), 2)
            for combelems in combs:
                path1 = combelems[0]
                path2 = combelems[1]
                while True:
                    dirtuple = tuple(sorted(list((path1, path2))))
                    if dir1_contains_or_is_dir2(dirtuple[0], dirtuple[1]):
                        break
                    nextdirequals.add(dirtuple)
                    path1 = os.path.dirname(dirtuple[0])
                    path2 = os.path.dirname(dirtuple[1])
                    if path1 == "/" or path1 == "" or \
                        path2 == "/" or path2 == "":
                        break
            for p in nextdirequals:
                if p in direquals:
                    direquals[p] += min(equalpathtotals[p[0]], equalpathtotals[p[1]])
                else:
                    direquals[p] = min(equalpathtotals[p[0]], equalpathtotals[p[1]])
                #print("! direquals[%s] += %s" % (str(p), min(equalpathtotals[p[0]], equalpathtotals[p[1]])))

            #print("! equalpathpool.clear()")
            equalpathpool.clear()
            nextdirequals.clear()
            equalpathtotals.clear()

        prevline = line
        if line == "":
            break

for p in direquals:
    ##print("! p = %s" % (str(p)))
    ##print("! dirsizes[p[0]] = %s" % (dirsizes[p[0]]))
    ##print("! dirsizes[p[1]] = %s" % (dirsizes[p[1]]))
    ##print("! direquals[p[1]] = %s" % (direquals[p]))
    s=similarity(dirsizes[p[0]], dirsizes[p[1]], direquals[p])
    if s >= 0.5:
        print("%18.0f  %6.2f%% %18s: %s %s" % (0.5 * s * direquals[p], 100 * s, direquals[p], p[0], p[1]))
