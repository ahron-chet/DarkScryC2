# Attack modules

The `Execution` library provides platform specific shell functionality. On
Windows it uses the Win32 API while on Linux it spawns `/bin/sh` and communicates
via pipes. Modules are organized under `Execution/<platform>`.

Common alias headers like `Execution/Shell.hpp` and `Collection/sysinfo.hpp`
provide platform-agnostic interfaces so core modules can simply use
`execution::Shell` and `sysinfo::get_basic_machine_info()` without conditional
includes.
