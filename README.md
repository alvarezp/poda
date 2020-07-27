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

2. Initialize poda by using ``poda-init [hostname]``. If a hostname is
   ommitted, it will be taken from your system's ``hostname -s``.

3. Declare a hamper. A hamper is a location unit for poda. For example,
   I declare a hamper to be my home directory. Another hamper can be a
   USB pendrive. A hamper in Poda is any location that stores data. The
   syntax is:
   
   ``poda-hamper-add <hampername> <basedir> <find_expr>``
   
   For example, this is how I ad my home directory as a hamper:
   
   ``poda-hamper-add home $HOME .``
   
   And this is how I declare my USB drieve as a hamper:
   
   ``poda-hamper-add -n blue-usb /media/alvarezp/1234-ABCD .``
   
   ``find_expr`` is important. Poda will search for files by doing this:
   
   ``find ${FINDEXPR} -name '.poda' -type d -prune -o -type f -size +0 -print0``
   
   So, for the whole directory just use ``.`` but if you want to exclude a
   directory, you can do it by using ``. -name <dirname> -prune -o`` instead.
   If it sounds hackish, it's because it is.

4. Run poda-reindex <hampername>. It *will* take a while. Leave it running.
   If it is too much data, leave it overnight. The index will be
   created as ``.poda/indexes/hostname/hampername/index``.

5. The following steps must be done manually for now. Download indexes from
   other hosts (for example, your NAS) and copy it to your .poda directory.
   Say you downloaded the index for host ``mynas``, hampername ``home``, and
   you downloaded it to your laptop as ``index``:
   
   ``mkdir -p ~/.poda/indexes/mynas/home``
   ``cp index ~/.poda/indexes/mynas/home``
   
6. Generate the similar directories report:

   ``cat ~/.poda/indexes/\*/\*/index | poda-dirdupes.py | sort -n > dirdupes.txt``

A sample run can be found in the doc/sample-run.txt. Quick links:
* Gitlab: <https://gitlab.com/alvarezp2000/poda/blob/master/doc/sample-run.txt>

I hope you find this program useful. I am open to suggestions.
