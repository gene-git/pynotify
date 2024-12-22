.. SPDX-License-Identifier: MIT

########
pynotify
########

Overview
========

pynotify : Python inotify implementation built atop standard C-library.

Key features
============

* Provides a python class to monitor 1 or more file paths for inotify events.

New / Interesting
==================

* Arch PKGBUILD add missing dependency on python-installer

###############
Getting Started
###############

A simple test program is available in the examples directory. The program
monitors */tmp/xxx* - this can be a file or a directory.  To get a quick idea
in one terminal do:

.. code-block:: bash

   mkdir /tmp/xxx
   ./examples/test_inotify.py

In another terminal do something like:

.. code-block:: bash

    touch /tmp/xxx/A
    touch /tmp/xxx/B
    rm /tmp/xxx/*
    rmdir /tmp/xxx


What the code does is essentialy:

.. code-block:: bash

   from pynotify import Inotify
   inotify = Inotify()
   inotify.add_watch('/tmp/xxx')

   for events in inotify.get_events():
        for event in events:
            if event:
                print(..)


The first loop uses get_events() method which is an iterator that returns a list of events.
Each even in the list provides for:

.. code-block:: bash

    event.wd            # the watch descriptor
    event.mask          # the event mask
    event.event_types   # list of event type enums from the mask
    event.path          # the path being watched (/tmp/xxx)
    event.file          # Possible suppordinate file (/tmp/xxx/A)

Thats it in a nutshell. add_watch takes one optional argument:

.. code-block:: bash

    Inotify.add_watch(*path*, mask=xxx)

*add_watch()* returns the watched descriptor, *wd*. If successful wd is >= 0.
If < 0 then it means the path is non-existent.

If not provided then the watch is for all possible event types.
Where mask are event types from the enum *InotifyMask.IN_xxx*. These event elements are the same 
as provided in */usr/include/sys/inotify.h*.

Before calling get_events() there is one additionl attribute that can be set on an instance
of Inotify which is a select timeout which defaults to 5 seconds.

.. code-block:: bash

    inotify.timeout

The timeout is passed down to *select()* which waits on the inotify file desriptor for events to provided.
If its negative then the select will wait forever, if no events occur.
Otherwise the select loop will break after the timeout. A value of zero causes select to return
immediately. The default value should provide reasonable behaviour.

Mask Flags
==========

You can get the full list of possible mask flags reading code, which has comments, or using:

.. code-block:: python

   from pynotify import InotifyMask, Inotify
   for item in InotifyMask.mask_to_events(0xFFFFFFFF):
        item

This currently outputs the following where we have manually added comments:

.. code::

    <InotifyMask.IN_ACCESS: 1>              # File was accessed
    <InotifyMask.IN_MODIFY: 2>              # File was modified.
    <InotifyMask.IN_ATTRIB: 4>              # Metadata changed.
    <InotifyMask.IN_CLOSE_WRITE: 8>         # Writtable file was closed.
    <InotifyMask.IN_CLOSE_NOWRITE: 16>      # Unwrittable file closed.
    <InotifyMask.IN_CLOSE: 24>              # File closed
    <InotifyMask.IN_OPEN: 32>               # File was opened.
    <InotifyMask.IN_MOVED_FROM: 64>         # File was moved from X.
    <InotifyMask.IN_MOVED_TO: 128>          # File was moved to Y.
    <InotifyMask.IN_MOVE: 192>              # File was moved
    <InotifyMask.IN_CREATE: 256>            # Subfile was created.
    <InotifyMask.IN_DELETE: 512>            # Subfile was deleted.
    <InotifyMask.IN_DELETE_SELF: 1024>      # Self was deleted.
    <InotifyMask.IN_MOVE_SELF: 2048>        # Self was moved.
    <InotifyMask.IN_UNMOUNT: 8192>          # Backing fs was unmounted.
    <InotifyMask.IN_Q_OVERFLOW: 16384>      # Event queue overflowed.
    <InotifyMask.IN_IGNORED: 32768>         # File was ignored.
    <InotifyMask.IN_ONLYDIR: 16777216>      # Only watch the path if it is a directory.
    <InotifyMask.IN_DONT_FOLLOW: 33554432>  # Do not follow a sym link.
    <InotifyMask.IN_EXCL_UNLINK: 67108864>  # Exclude events on unlinked objects.
    <InotifyMask.IN_MASK_CREATE: 268435456> # Only create watches.
    <InotifyMask.IN_MASK_ADD: 536870912>    # Add to the mask of an already existing watch.
    <InotifyMask.IN_ISDIR: 1073741824>      # Event occurred against dir.
    <InotifyMask.IN_ONESHOT: 2147483648>    # Only send event once.
    <InotifyMask.IN_ALL_EVENTS: 4095>       # All events which that can be waited on.


########
Appendix
########

Installation
============

Available on
 * `Github`_
 * `Archlinux AUR`_

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
To build manually, clone the repo and :

 .. code-block:: bash

        rm -f dist/*
        /usr/bin/python -m build --wheel --no-isolation
        root_dest="/"
        ./scripts/do-install $root_dest

When running as non-root then set root_dest a user writable directory

Dependencies
============

**Run Time** :

* python          (3.11 or later)

**Building Package** :

* git
* hatch           (aka python-hatch)
* wheel           (aka python-wheel)
* build           (aka python-build)
* installer       (aka python-installer)
* rsync

**Optional for building docs** :

* sphinx
* texlive-latexextra  (archlinux packaguing of texlive tools)

Philosophy
==========

We follow the *live at head commit* philosophy. This means we recommend using the
latest commit on git master branch. We also provide git tags. 

This approach is also taken by Google [1]_ [2]_.

License
=======

Created by Gene C. and licensed under the terms of the MIT license.

* SPDX-License-Identifier: MIT
* SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>


.. _Github: https://github.com/gene-git/pynotify
.. _Archlinux AUR: https://aur.archlinux.org/packages/python-pynotify

.. [1] https://github.com/google/googletest  
.. [2] https://abseil.io/about/philosophy#upgrade-support

