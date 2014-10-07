#!/usr/bin/env python

import os
from stat import *

def browseDirTree(path):
    """ Traverses a directory recursively.

    This is a template function which you will probably extend to
    some desired functionality; When using as it is you get full paths
    to all subdirectories and files in the dir along with permissions.
    ! Not tested for symlimks.

    Arguments:
    path -- a path string ( default '' )
    """

    for dirname, dirnames, filenames in os.walk(path):
        # print path to all dirs and subdirs
        for subdirname in dirnames:
            full_dir_path = os.path.join(dirname, subdirname)
            print full_dir_path, oct( S_IMODE(os.stat(full_dir_path).st_mode) )

        # print path to all filenames
        for filename in filenames:
            full_file_path = os.path.join(dirname, filename)
            print full_file_path, oct( S_IMODE(os.stat(full_file_path).st_mode) )

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there
        # if '.git' in dirnames:
        #    # don't go into any .git directories.
        #    dirnames.remove('.git')

    return True

def setPermitDownTheTree(path, permit=0770):
    """ Traverses a directory recursively and set permissions.

    The function is based on browseDirTree(). It expands simple traversing
    by setting a specified permissions for each file and subdir within a
    given path.
    ! Not tested for symlimks.

    Arguments:
    path        -- a path string ( default '' )
    permit      -- permissions to be set in oct 
		( default 0770 ) - '?rwxrwx---'
    """

    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            full_dir_path = os.path.join(dirname, subdirname)
            os.chmod(full_dir_path, permit)

        for filename in filenames:
            full_file_path = os.path.join(dirname, filename)
            os.chmod(full_file_path, permit)

    return True
