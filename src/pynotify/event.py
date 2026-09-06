# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Wrap libc inotify
 see man inotify et al for details
"""
# pylint: disable=invalid-name
from dataclasses import (dataclass, field)
from .mask import InotifyMask


@dataclass
class InotifyEvent:
    """
    One inotify event.

    Holds:
        - wd : the watch descriptor
        - mask : the mask for this event.
        - event_types : the list of individual event masks which are or'ed together to make the mask.
        - path : the path to be/being watched..
        - file : the filename.
    """
    wd: int = -1
    mask: int = -1
    event_types: list[InotifyMask] = field(default_factory=list)
    path: str = ''
    file: str = ''
