# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Wrap the standard libc library inotify using ctypes
- See also man pages for inotify for more detail.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
import os
import ctypes
import ctypes.util
import errno


def _load_libc():
    """
    Load the standard c-library.
    """
    libc_so = ctypes.util.find_library("c")
    if not libc_so:
        libc_so = 'libc.so.6'
    libc = ctypes.cdll.LoadLibrary(libc_so)
    return libc


class InotifyBase:
    """
    Python inotify class.

    Uses *inotify* from the standard C-library via ctypes.
    """
    def __init__(self):
        """
        Notes:
            .timeout = seconds where 0 returns immediately (polls), -1 waits forever
            .fd = handle to inotify instance.
        """
        self.libc = _load_libc()

        self.timeout: int = 5
        self.fd: int = -1
        self.buf: bytes = b''

        self.watch_path: dict[int, str] = {}
        self.watch_wd: dict[str, int] = {}

        self.errno_code: int = 0
        self.errno_str: str = ''

        # Wrap inotify_init
        self.inotify_init_func = self.libc.inotify_init
        self.inotify_init_func.argtypes = []
        self.inotify_init_func.restype = ctypes.c_int

        # Wrap inotify_add_watch
        self.inotify_add_watch = self.libc.inotify_add_watch
        self.inotify_add_watch.argtypes = [ctypes.c_int,
                                           ctypes.c_char_p,
                                           ctypes.c_uint32]
        self.inotify_add_watch.restype = ctypes.c_int

        # Wrap inotify_rm_watch
        self.inotify_rm_watch = self.libc.inotify_rm_watch
        self.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_int]
        self.inotify_rm_watch.restype = ctypes.c_int

        # init this inotify instance
        self.fd = self.inotify_init_func()
        if self.fd < 0:
            self.save_errno()
            raise OSError(self.errno_code, f"Failed to initialize inotify: {self.errno_str}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        """
        Safely close the file descriptor to avoid resource leaks.
        """
        if hasattr(self, 'fd') and self.fd >= 0:
            try:
                os.close(self.fd)
            except OSError:
                pass
            finally:
                self.fd = -1

    def save_errno(self):
        """
        Keep the last errno
        """
        err = ctypes.get_errno()
        self.errno_code = err
        err_name = errno.errorcode.get(err, "UNKNOWN")
        self.errno_str = f'{err_name}: ' + os.strerror(err)
