#!/usr/bin/python
# test inotify class
#
import sys
from pynotify import Inotify

def main():
    """ test inotify """
    path = '/tmp/xxx'

    #breakpoint()
    inot = Inotify()
    inot.add_watch(path)
    inot.timeout = 120

    try:
        for events in inot.get_events():
            num = len(events)
            print(f'Got {num} events')
            for event in events:
                if event:
                    print(f'wd           = {event.wd}')
                    print(f'mask         = 0x{event.mask:08x}')
                    print(f'event_types  = {event.event_types}')
                    print(f'path         = {event.path}')
                    print(f'file         = {event.file}')

                #inot.rm_watch(path)

    except (IOError, KeyboardInterrupt):
        print('Interrupted')
        sys.exit()

    #inot.rm_watch(path)


if __name__ == '__main__':
    main()
