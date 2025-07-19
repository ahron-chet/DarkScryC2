# Attack modules

The `execution` library provides platform specific shell functionality. On
Windows it uses the Win32 API while on Linux it spawns `/bin/sh` and communicates
via pipes. Modules are organized under `execution/<platform>`.
