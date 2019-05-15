poda
====

Poda is a set of scripts that aid at finding duplicate content between
different storage systems. It is slower than fdupes because it needs
to have previously indexed all content from each storage. Once this
is done, the report is created from the indexes only. Reindexing
is as efficient as possible.

Example usage:

1. Place all the poda-\* under /usr/local/bin or any other place in
   the $PATH.

2. Set yourself in the home directory with "cd".

3. Run poda-reindex. It *will* take a while. Leave it running. If
   it is too much data, leave it overnight. The index will be
   created as .poda/index.

4. This is confusing but: if you created an index for another storage
   then download it and you will need to import it. If not, just
   import it specifying .poda/index as the file:

   poda-import <label> <file>

   If it is the index from your local laptop:
   * poda-import laptop .poda/index 

   If it is the index you downloaded from another storage, say your NAS:
   * poda-import nas index # if you downloaded it as "index".

5. Run poda-create-reports. Find it under .poda.

A sample run can be found in the doc/sample-run.txt. Quick links:
* Gitlab: <https://gitlab.com/alvarezp2000/poda/blob/master/doc/sample-run.txt>

I hope you find this program useful. I am open to suggestions.
