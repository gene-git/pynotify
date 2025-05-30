# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Constants taken from sys/inotify.h
"""
# pylint: disable=superfluous-parens
from enum import IntEnum


class InotifyMask(IntEnum):
    """
    Mask values from /usr/include/sys/inotify.h.

    Masks can be bitwise *OR* together. For example IN_CLOSE
    can be written as (IN_CLOSE_WRITE | IN_CLOSE_NOWRITE).

    Available masks:

    * IN_ACCESS : **File was accessed**
    * IN_MODIFY : **File was modified**
    * IN_ATTRIB : **Metadata changed**

    * IN_CLOSE_WRITE : **Writtable file was closed**
    * IN_CLOSE_NOWRITE : **Unwrittable file closed**
    * IN_CLOSE : **Closed write or nowrite**

    * IN_OPEN : **File was opened**

    * IN_MOVED_FROM : **File was moved from X**
    * IN_MOVED_TO : **File was moved to Y**
    * IN_MOVE : **Moved from or to**

    * IN_CREATE : **Subfile was created**
    * IN_DELETE : **Subfile was deleted**
    * IN_DELETE_SELF :**Self was deleted**
    * IN_MOVE_SELF : **Self was moved**

    # Events sent by the kernel.

    * IN_UNMOUNT : **Backing fs was unmounted**
    * IN_Q_OVERFLOW : **Event queued overflowed**
    * IN_IGNORED : **File was ignored**

    # Special flags.

    * IN_ONLYDIR :         **Only watch the path if it is a directory**
    * IN_DONT_FOLLOW : **Do not follow a sym link**
    * IN_EXCL_UNLINK : **Exclude events on unlinked objects**
    * IN_MASK_CREATE : **Only create watches**
    * IN_MASK_ADD : **Add to mask of an existing watch**
    * IN_ISDIR : **Event occurred against dir**
    * IN_ONESHOT : **Only send event once**

    # All events which a program can wait on.

    * IN_ALL_EVENTS : **All events**

    """

    # Supported events suitable for MASK parameter of INOTIFY_ADD_WATCH.
    IN_ACCESS = 0x00000001     # File was accessed.
    IN_MODIFY = 0x00000002     # File was modified.
    IN_ATTRIB = 0x00000004     # Metadata changed.

    IN_CLOSE_WRITE = 0x00000008                 # Writtable file was closed.
    IN_CLOSE_NOWRITE = 0x00000010                   # Unwrittable file closed.
    IN_CLOSE = (IN_CLOSE_WRITE | IN_CLOSE_NOWRITE)  # Close.

    IN_OPEN = 0x00000020                            # File was opened.

    IN_MOVED_FROM = 0x00000040                      # File was moved from X.
    IN_MOVED_TO = 0x00000080                        # File was moved to Y.
    IN_MOVE = (IN_MOVED_FROM | IN_MOVED_TO)         # Moves.

    IN_CREATE = 0x00000100                          # Subfile was created.
    IN_DELETE = 0x00000200                          # Subfile was deleted.
    IN_DELETE_SELF = 0x00000400                     # Self was deleted.
    IN_MOVE_SELF = 0x00000800                       # Self was moved.

    # Events sent by the kernel.
    IN_UNMOUNT = 0x00002000                     # Backing fs was unmounted.
    IN_Q_OVERFLOW = 0x00004000                  # Event queued overflowed.
    IN_IGNORED = 0x00008000                     # File was ignored.

    # Special flags.
    IN_ONLYDIR = 0x01000000         # Only watch the path if it is a directory.
    IN_DONT_FOLLOW = 0x02000000     # Do not follow a sym link.
    IN_EXCL_UNLINK = 0x04000000     # Exclude events on unlinked objects.
    IN_MASK_CREATE = 0x10000000     # Only create watches.
    IN_MASK_ADD = 0x20000000        # Add to mask of an existing watch.
    IN_ISDIR = 0x40000000           # Event occurred against dir.
    IN_ONESHOT = 0x80000000         # Only send event once.

    # All events which a program can wait on.
    IN_ALL_EVENTS = (IN_ACCESS | IN_MODIFY | IN_ATTRIB | IN_CLOSE_WRITE |
                     IN_CLOSE_NOWRITE | IN_OPEN | IN_MOVED_FROM |
                     IN_MOVED_TO | IN_CREATE | IN_DELETE |
                     IN_DELETE_SELF | IN_MOVE_SELF)

    @classmethod
    def mask_to_events(cls, mask):
        """
        Return list of all events in mask
        """
        return [item for item in cls.__members__.values() if item & mask]
