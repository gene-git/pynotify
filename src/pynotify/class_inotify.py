# SPDX-License-Identifier: MIT
# DX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Wrap around the standard libc library inotify.

 See also standard man pages for inotify for more detail.
"""
# pylint: disable=invalid-name
from typing import (Dict, Iterator, List)
import os
import ctypes
import ctypes.util
import errno
from .class_mask import InotifyMask
from .events import (InotifyEvent, get_inotify_events)


def _load_libc():
    """
    Load the standard c-library
    """
    libc_so = ctypes.util.find_library("c")
    if not libc_so:
        libc_so = 'libc.so.6'
    libc = ctypes.cdll.LoadLibrary(libc_so)
    return libc


class Inotify:
    """
    Python inotify class.

    Uses *inotify* from the standard C-library.

    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        self.libc = _load_libc()

        # timeout in secs: 0 => returns immediately (polls), -1 waits forever
        self.timeout: int = 5

        # fd is handle to this inotify instance
        self.fd: int = -1
        self.buf: bytes = b''

        # Keep track of each watched item by (wd, path)
        self.watch_path: Dict[int, str] = {}
        self.watch_wd: Dict[str, int] = {}

        # Can save one errno via self.save_errno()
        self.errno_code: int = 0
        self.errno_str: str = ''

        #
        # Wrap the inotify functions:
        #  - Each (fd, path, mask) -> wd aka a watch descriptor
        #
        self.inotify_add_watch = self.libc.inotify_add_watch
        self.inotify_add_watch.argtypes = [ctypes.c_int,
                                           ctypes.c_char_p,
                                           ctypes.c_uint32]

        # fd, wd -> 0 (or -1 for error)
        self.inotify_rm_watch = self.libc.inotify_rm_watch
        self.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]

        #
        # init this inotify instance
        #
        self.fd = self.libc.inotify_init()

    def add_watch(self, path: str,
                  mask: int = InotifyMask.IN_ALL_EVENTS) -> int:
        """
        Adds a watch to filesystem path.

        Args:
            path (str):
            The filesystem path on which to set the watch
            path must exist as can only use inotify existing file.

            mask (InotifyMask):
            The mask specifies which events to watch for.

            A mask is made by bitwise OR of one or more masks. 
            Each mask item is taken from *InotifyMask*. 

            For example:

                mask =  (InotifyMask.OPEN | InotifyMask.CLOSE ).
            
            See InotifyMask for the full list.

        Returns:
            int:
            Watch descriptor, wd.
            If non-existent file then returns -1

        """
        #
        # Speak bytes to C-code
        # - we dont seem to need to null terminate
        # - wd < 0 if file doesn't exist (see errno)
        #
        path_bytes = path.encode()
        wd = self.inotify_add_watch(self.fd, path_bytes, mask)

        #
        # A watch on non-existent path will never do anything - skip it
        #
        if wd >= 0:
            self.watch_wd[path] = wd
            self.watch_path[wd] = path
        else:
            self.save_errno()
        return wd

    def save_errno(self):
        """
        Keep the last errno
        """
        err = ctypes.get_errno()
        self.errno_code = err
        err_name = errno.errorcode.get(err)
        self.errno_str = f'{err_name}: ' + os.strerror(err)

    def rm_watch(self, path: str):
        """
        Remove watch on this path.

        Args:
            path (str):
            The filesystem path to remove the watch for.
        """

        wd = self.watch_wd.get(path)
        if not wd:
            return

        del self.watch_path[wd]
        del self.watch_wd[path]

        self.inotify_rm_watch(self.fd, wd)

    def rm_all_watches(self):
        """
        Remove all current watches.
        """
        for (wd, _path) in self.watch_path.items():
            self.inotify_rm_watch(self.fd, wd)
        self.watch_path = {}
        self.watch_wd = {}

    def get_events(self) -> Iterator[List[InotifyEvent]]:
        """
        Wait for events.

        Args:

        Returns:
            Iterator[List[InotifyEvent]]:
            Provides an iterater until fd is closed.
            fd is closed when the inotify event says so.
            if timeout < 0, wait forever.
        """
        return get_inotify_events(self)
