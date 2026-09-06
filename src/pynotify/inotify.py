# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Wrap the standard libc library inotify using ctypes
- See also man pages for inotify for more detail.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-instance-attributes
# pylint disable=too-many-locals
import os
from collections.abc import Iterator
from select import select
import struct

from .inotify_base import InotifyBase
from .mask import InotifyMask
from .event import InotifyEvent


class Inotify(InotifyBase):
    """
    Python inotify class.

    Uses *inotify* from the standard C-library via ctypes.
    """
    def add_watch(self, path: str, mask: int = InotifyMask.IN_ALL_EVENTS) -> int:
        """
        Adds a watch for a filesystem path.

        :param path: The file to watch
        :param mask: The event mask to use
        :returns: The watch descriptor (wd).
        """
        path_bytes = path.encode()
        wd = self.inotify_add_watch(self.fd, path_bytes, mask)

        if wd >= 0:
            self.watch_wd[path] = wd
            self.watch_path[wd] = path
        else:
            self.save_errno()
            raise OSError(self.errno_code, self.errno_str, path)

        return wd

    def rm_watch(self, path: str):
        """
        Remove watch on this path.

        :param path: Remove the watc for this path
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
        for (wd, _path) in list(self.watch_path.items()):
            self.inotify_rm_watch(self.fd, wd)
        self.watch_path.clear()
        self.watch_wd.clear()

    def get_events(self) -> Iterator[list[InotifyEvent]]:
        """
        Wait for events.
        :yields: List of events.
        """
        return get_inotify_events(self)


def mask_to_event_types(mask: int) -> list[InotifyMask]:
    """
    mask => return list of event types (IntFlag members)
    """
    return InotifyMask.mask_to_events(mask)


def _read_inotify_events(inotify: Inotify) -> list[InotifyEvent]:
    """
    read one or more event(s) up to max number of events
    :param inotify: The Inotify instance.
    """
    buf = inotify.buf

    hdr_fmt = 'iIII'
    hdr_size = struct.calcsize(hdr_fmt)

    event_size_max = hdr_size + 256
    max_to_read = 50
    events_size = max_to_read * event_size_max

    events: list[InotifyEvent] = []
    try:
        chunk = os.read(inotify.fd, events_size)
    except OSError:
        return events

    buf += chunk

    while True:
        len_buf = len(buf)
        if len_buf < hdr_size:
            inotify.buf = buf
            return events

        header = struct.unpack(hdr_fmt, buf[:hdr_size])
        [wd, mask, _cookie, len_name] = header

        len_event = hdr_size + len_name

        # Defensive check against malformed event lengths causing infinite loops
        if len_event <= 0:
            inotify.buf = b''
            break

        if len_buf < len_event:
            # partial - wait till next time
            inotify.buf = buf
            return events

        # overflow of event queue - not good - so we bail
        if mask & InotifyMask.IN_Q_OVERFLOW or wd < 0:
            return events

        file = buf[hdr_size:len_event]

        event = InotifyEvent()
        event.wd = wd
        event.path = inotify.watch_path.get(wd, '')
        event.mask = mask

        file = file.rstrip(b'\0')
        if file:
            event.file = file.decode(errors='replace')

        event.event_types = mask_to_event_types(mask)
        events.append(event)

        if len_buf > len_event:
            inotify.buf = buf[len_event:]
        else:
            inotify.buf = b''

        buf = inotify.buf

    return events


def get_inotify_events(inotify: Inotify) -> Iterator[list[InotifyEvent]]:
    """
    wait for events
    """
    if len(inotify.watch_wd) == 0:
        return

    timeout = inotify.timeout
    done = False
    while not done:
        if len(inotify.watch_path) == 0:
            done = True
            break
        try:
            if timeout >= 0:
                (fds, _fwr, _ferr) = select([inotify.fd], [], [], timeout)
            else:
                (fds, _fwr, _ferr) = select([inotify.fd], [], [])

        except (IOError, KeyboardInterrupt):
            inotify.rm_all_watches()
            done = True
            break

        if not fds:
            # Polling mode: yield empty list rather than terminating the generator
            yield []
            continue

        events = _read_inotify_events(inotify)

        # check if watched path deleted
        for event in events:
            if (InotifyMask.IN_DELETE_SELF in event.event_types and
                event.path in inotify.watch_wd):                # noqa: E129
                inotify.rm_watch(event.path)

        yield events

    return
