# The C pack's traps

What cost time when the first C projects ran in the factory (an ESP32 template and a fork of an ESP8266 firmware; November 2026), and what the pack does about each.

- **Only the host build is checked.** A stage has no device and no vendor toolchain. The logic must therefore build with the host's compiler: keep platform headers out of it (ports and adapters), and let a cross build be a target of its own, outside `check`.
- **An existing firmware repository keeps its own build.** Name the factory's makefile in the pipeline definition (`make_file: factory/Makefile`) and leave the root build files as they are; the write paths then name only the folders the fork adds.
- **Fetched sources need the network once.** What `CMakeLists.txt` fetches is fetched by `make sync`; pin it by hash, so that a sync of another day builds the same.
- **clang-format differs between versions.** The stage image's version is the one that counts; a developer formats with the same version or lets the check say what differs.
- **Line ends.** A checkout made on Windows with converted line ends fails shell scripts with "required file not found". Keep `* text=auto eol=lf` in `.gitattributes`.
- **The sanitizers' leak check** needs a permission a stage's container does not have; the makefile switches it off (`ASAN_OPTIONS=detect_leaks=0`) and keeps the others.
- **A big stage image is slow to build, not to use.** A vendor toolchain in the stage file adds gigabytes; add it only when a check really needs it.
