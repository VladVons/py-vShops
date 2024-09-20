# Created: 2024.09.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# WatchDog = TWatchDog()
# WatchDog.AddFile('vCrawler.sh')
# await WatchDog.Run()

import os
import ctypes
import ctypes.util
import struct
import asyncio

IN_MODIFY = 0x00000002
IN_DELETE = 0x00000200
IN_CREATE = 0x00000100

libc = ctypes.CDLL(ctypes.util.find_library('c'), use_errno=True)

class TWatchDog():
    def __init__(self):
        inotify_init = libc.inotify_init
        inotify_init.restype = ctypes.c_int
        self.inotify_fd = inotify_init()
        if (self.inotify_fd == -1):
            raise OSError("Failed to initialize inotify")

    def AddFile(self, aPath: str, aMode = IN_MODIFY):
        inotify_add_watch = libc.inotify_add_watch
        inotify_add_watch.restype = ctypes.c_int
        watch_descriptor = inotify_add_watch(self.inotify_fd, aPath.encode(), aMode)
        if (watch_descriptor == -1):
            raise OSError(f'Failed to add watch for file: {aPath}')

    async def Run(self):
        event_size = struct.calcsize('iIII')  # Event struct size
        loop = asyncio.get_running_loop()

        while True:
            await loop.run_in_executor(None, os.read, self.inotify_fd, event_size + 512)

            buffer = os.read(self.inotify_fd, event_size + 512)  # Buffer to hold event data
            wd, mask, cookie, name_len = struct.unpack('iIII', buffer[:event_size])

            if mask & IN_MODIFY:
                print("File modified")
            elif mask & IN_DELETE:
                print(f"File deleted")
            elif mask & IN_CREATE:
                print(f"File created")
