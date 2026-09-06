//
// Size of struct inotify_event
//
// SPDX-License-Identifier: GPL-2.0-or-later
// SPDX-FileCopyrightText: © 2023-present Gene C <arch@sapience.com>
//
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/inotify.h>

int main()
{
    struct inotify_event event;
    long unsigned ssize = sizeof(struct inotify_event) ;
        
    printf(" total     : %ld\n", ssize) ;
    printf("   wd     : %ld\n", sizeof(event.wd)) ;
    printf("  mask    : %ld\n", sizeof(event.mask)) ;
    printf("cookie    : %ld\n", sizeof(event.cookie)) ;
    printf("   len    : %ld\n", sizeof(event.len)) ;

    return(0);
}
