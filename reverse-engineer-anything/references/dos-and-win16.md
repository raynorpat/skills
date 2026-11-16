# DOS and 16-bit Windows (3.x / 95) targets

Use this guide when the target is a DOS program, a Windows 3.x application or
driver, or a 16-bit or VxD component shipped with a Windows 95-era product.
These formats predate the assumptions most native tooling makes: code is
segmented, the API is interrupts or ordinal imports, and the file header often
describes a stub in front of the real program.

## What REA covers and what it does not

Stay inside what the connected server reports.

- DOS MZ: open with `open_binary`, then verify the image with
  `inspect_native_load_image` as described in
  [DOS MZ with Ghidra](native-and-artifacts.md#dos-mz-with-ghidra).
- Headerless DOS COM: open with `format: "dos-com"`; see
  [native and artifacts](native-and-artifacts.md).
- NE, LE/LX, and VxD support is not established by this skill. Open the file
  and read what the result reports. If the format is refused, or only the MZ
  stub is analyzed, say so and treat anything learned with other tools as your
  own observation, not REA Evidence.
- Every static result describes the file image. DOS, BIOS, extender, Windows
  loader, and hardware behavior are runtime facts that need an emulator
  observation or documentation, and should be labeled as such.

## Identify the real format first

Read the header bytes before choosing a tool. A wrong guess here wastes the
whole investigation.

| Bytes | Format | Typical target |
|---|---|---|
| No header, file under 64 KB, `.COM` | DOS COM | Loaded at `PSP:0100h`, one segment |
| `MZ` (or `ZM`) at 0, nothing valid at `e_lfanew` | DOS MZ | Real-mode DOS EXE |
| `MZ`, then `NE` at the offset stored at `0x3C` | New Executable | Windows 1.x-3.x apps, DLLs, `.DRV`, fonts; OS/2 1.x |
| `MZ`, then `LE` | Linear Executable | Windows 3.x/9x VxD (`.386`, `.VXD`); DOS/4G and DOS/4GW programs |
| `MZ`, then `LX` | Linear Executable (OS/2 2.x) | OS/2; some DOS extenders |
| `MZ`, then `PE\0\0` | Portable Executable | Win32 (Windows 95/NT). Route as an ordinary PE |
| `FF FF FF FF` at 0, `.SYS` | DOS device driver | Header holds strategy and interrupt entry offsets |
| `W3` / `W4` | VxD container | `WIN386.EXE`, `VMM32.VXD`: a bundle of LE modules, compressed in `W4` |

Then check for a second layer:

- **DOS extenders.** The MZ part is a loader stub and the program follows it.
  Look for `DOS/4G`, `PMODE/W`, `CauseWay` (`3P`), Phar Lap (`MP`, `P2`, `P3`),
  Borland `RTM`/`DPMI16BI`/`32RTM`, or a DJGPP `go32` stub in front of a COFF
  image. Analyze the payload at its own offset as 32-bit (or 16-bit protected
  mode) code, not the stub.
- **Packers.** LZEXE (`LZ09` or `LZ91` at offset `0x1C`), PKLITE (copyright
  string near the start), EXEPACK (`RB` marker and "Packed file is corrupt"),
  DIET, and UPX for DOS are common. A packed file shows a tiny code section, a
  large high-entropy tail, and few readable strings; use `inspect_byte_entropy`
  to confirm. Unpack statically where a known unpacker exists and record which
  one. Do not treat the stub's control flow as the program's.
- **Overlays.** Bytes after the MZ image length may be Borland VROOMM overlays
  (`FBOV`), Microsoft overlays reached through `INT 3Fh`, appended resources,
  or a self-extracting archive. Report the size of the appended region and
  what identifies it before analyzing the main image as if it were complete.

## Real-mode DOS programs

**Addressing.** A real-mode address is `segment * 16 + offset`. Pointers are
near (offset only, relative to a segment register) or far (segment and offset).
Which one a function uses depends on the memory model the program was built
with: tiny and small use near code and data, medium has far code, compact has
far data, large and huge have both. Identify the model early; it decides
whether a 16-bit value is a pointer at all.

**Loading.** The MZ relocation table lists places that hold segment values to
be adjusted by the load segment. Disassemblers pick an arbitrary load segment
(Ghidra commonly uses `1000`), so segment values in listings are relative to
that choice. On entry `DS` and `ES` point at the 256-byte Program Segment
Prefix, not the data segment; startup code loads `DS` with the real data
segment (often called `DGROUP`). The command tail is at `PSP:80h` and the
environment segment at `PSP:2Ch`. Memory beyond the file image up to the
header's minimum allocation is uninitialized BSS.

**The API is interrupts.** There is no import table. Find functionality by
locating `INT` instructions and the register values set before them.

| Interrupt | Purpose | Notes |
|---|---|---|
| `INT 21h` | DOS services, function in `AH` | `09` print `$`-terminated string, `3D`/`3F`/`40`/`3E` open/read/write/close, `4B` exec, `4C` exit, `25`/`35` set/get interrupt vector, `48`-`4A` memory |
| `INT 10h` | Video BIOS | `AH=00` set mode; mode `13h` is 320x200x256 |
| `INT 13h` | Disk BIOS | Raw sector access; also used by disk-based copy protection |
| `INT 16h` | Keyboard BIOS | |
| `INT 33h` | Mouse driver | |
| `INT 2Fh` | Multiplex | Installation checks for TSRs, XMS entry lookup (`AX=4310h`) |
| `INT 31h` | DPMI | Present in extended programs |
| `INT 67h` | EMS | |
| `INT 34h`-`3Dh` | Floating-point emulation | See pitfalls |

Many programs bypass DOS and the BIOS: direct writes to `A000:0000` (VGA
graphics) or `B800:0000` (text), and port I/O such as `3C8h`/`3C9h` (VGA
palette), `3DAh` (retrace), `60h`/`64h` (keyboard), `40h`-`43h` (timer),
`20h`/`21h` (interrupt controller), `220h`-`22Fh` (Sound Blaster), `388h`
(AdLib). Ralf Brown's Interrupt List is the standard reference for functions
and ports; cite the entry you relied on.

**Resident programs.** A TSR hooks vectors with `INT 21h` `AH=25h`/`35h` or by
writing the table at `0000:vector*4`, then stays resident with `INT 27h` or
`INT 21h` `AH=31h`. The interesting code is the handlers, which are reached by
no call in the file. Find them from the vector-setting sites.

**Compiler and runtime.** Identifying the toolchain tells you the calling
convention, the startup code to skip, and the library functions to stop
reading.

- Borland and Turbo C/C++: copyright string in the data segment; `cdecl` by
  default.
- Turbo Pascal: "Runtime error" string, length-prefixed strings (first byte is
  the length, no terminator), 6-byte `Real` type, arguments pushed left to
  right with the callee cleaning the stack.
- Microsoft C: "MS Run-Time Library" string.
- Watcom: `WATCOM C/C++` string; default convention passes arguments in
  registers (`AX`, `DX`, `BX`, `CX`, or their 32-bit forms).
- QuickBASIC, Clipper, and similar: mostly runtime plus tables; look for a
  runtime module name such as `BRUN45` before reading any code.

Library signatures for these compilers exist for IDA (FLIRT) and are sparse
for Ghidra. Without them, identify `printf`-family and file routines from
their `INT 21h` use and format strings, name them, and move on.

## Windows 3.x: the NE format

An NE file is a set of 16-bit protected-mode segments plus tables. Read the
header before the code:

- **Segment table.** Each segment is code or data, and movable, fixed, or
  discardable. One data segment is the automatic data segment (`DGROUP`).
  Segments are addressed by selector at run time, so far pointers in the file
  are not final addresses.
- **Entry table and name tables.** Exports are numbered. The resident and
  non-resident name tables map names to ordinals; the entry table maps
  ordinals to segment and offset.
- **Module reference and imported-names tables.** Imports are by module and
  ordinal far more often than by name. `KERNEL`, `USER`, and `GDI` ordinals
  must be mapped to names from an ordinal list for that Windows version
  before any call makes sense. State which list you used.
- **Per-segment relocations.** Each fixup is an internal reference, an import
  by ordinal, an import by name, or an OS fixup (floating-point emulation).
  Fixups to the same target are often chained through the code bytes
  themselves, so unrelocated operands hold chain links, not addresses.
- **Resource table.** Dialogs, menus, string tables (stored in blocks of 16),
  accelerators, icons, and version information. Dialog and menu resources name
  the control and command IDs that message handlers switch on; read them
  early.

**Conventions.** Win16 API functions and callbacks are `FAR PASCAL`: arguments
pushed left to right, callee cleans the stack, far return. Handles and `WPARAM`
are 16 bits; `LPARAM` and far pointers are 32. Far functions typically open
with `inc bp` / `push bp` / `mov bp, sp` (the odd `BP` marks a far frame).
Exported callbacks open with a short `DS`-loading sequence (`mov ax, ds` /
`nop`, or `push ds` / `pop ax` / `nop`) that the loader or `MakeProcInstance`
rewrites, so the bytes in the file are a template.

**Finding the program.** Startup calls `InitTask`, `WaitEvent`, and `InitApp`
before `WinMain(hInstance, hPrevInstance, lpCmdLine, nCmdShow)`. From there:

- Window procedures are the `lpfnWndProc` values passed to `RegisterClass`.
- Dialog procedures are the callbacks passed to `DialogBox` or `CreateDialog`,
  usually through `MakeProcInstance`.
- A window procedure is a switch on the message number. `WM_COMMAND` (`0111h`)
  dispatches on control and menu IDs from the resources.
- Framework programs hide this: MFC 1.x-2.x uses message maps, Borland OWL
  uses dynamic dispatch tables indexed by message. Identify the framework from
  class-name strings and find the tables instead of the switch.
- Visual Basic 1-3 programs (`VBRUN100`, `VBRUN200`, `VBRUN300`) are p-code or
  thin native stubs over the runtime. Native disassembly of the EXE says
  little; say so and use a VB-specific approach.

Memory idioms: `GlobalAlloc`/`GlobalLock` and `LocalAlloc` return handles that
are locked into pointers; "huge" pointers cross 64 KB by adding `__AHINCR` to
the selector.

## Windows 95-era products

Most Windows 95 applications are ordinary PE files: analyze them as PE. The
16-bit and ring-0 parts are what this guide adds.

- **Mixed 16/32-bit components.** Products often ship a PE DLL paired with an
  NE DLL. They talk through thunks. Flat thunks (thunk-compiler output) show
  `QT_Thunk`, `FT_Prolog`, `SMapLS`/`SUnMapLS`, `ThunkConnect32`, and a
  `*_ThunkData32` export on the 32-bit side, with `ThunkConnect16` on the
  other. Generic thunks use `LoadLibraryEx32W` and `CallProc32W` from 16-bit
  code. Win32s on Windows 3.1 uses universal thunks (`UTRegister`). A call
  that vanishes into one of these continues in the partner module: find the
  pair and follow it across.
- **VxDs.** A VxD is an LE file with one export, the Device Descriptor Block
  (`<NAME>_DDB`), which holds the device ID, the control procedure, and
  service tables. The control procedure dispatches on system control messages
  such as `Sys_Critical_Init`, `Device_Init`, and `W32_DEVICEIOCONTROL`; the
  last is the entry for applications that open `\\.\NAME.VXD` and call
  `DeviceIoControl`. Calls to other VxDs and the VMM are encoded as `INT 20h`
  followed by a 32-bit service identifier (device ID in the high word, service
  number in the low). Disassemblers that do not know this decode the
  identifier as instructions and desynchronize; mark those six bytes as a
  service call before trusting the code that follows.
- **Undocumented imports.** Windows 95 system DLLs export many functions by
  ordinal only. Do not name one from a guess; cite a published ordinal list or
  leave it as an ordinal.

## Tools outside REA

Use these when the connected server does not cover the format. Label results
as coming from them.

| Need | Options |
|---|---|
| Header and table dumps (MZ, NE, LE) | Open Watcom `wdump`, Borland `tdump`, Microsoft `exehdr`, `winedump`, Semblance |
| Disassembly and decompilation | Ghidra loads MZ and NE and decompiles 16-bit x86 (`Real Mode` and `Protected Mode` language variants); LE/LX needs a third-party loader. IDA loads MZ, NE, LE, and LX, but its decompiler does not cover 16-bit code. Reko handles MZ and NE |
| NE resources | `wrestool` (icoutils), or a resource viewer that still reads NE |
| Running and debugging DOS code | DOSBox built with its debugger, DOSBox-X, Bochs with its debugger, Spice86 for real-mode tracing |
| Running Win16 | Windows 3.1 inside DOSBox or 86Box/PCem; winevdm (otvdm) on 64-bit Windows; Wine on Linux |
| Ring-0 and VxD debugging | A full-system emulator (86Box, PCem, Bochs) with a period debugger such as SoftICE or WDEB386 |

Run unknown period software only inside an emulator with no access to host
files or the network.

## Pitfalls

- **Segment registers drive the decompiler.** If `DS` is unknown, every global
  access is wrong. Set the assumed `DS` (and `ES` where it is stable) per
  function to the program's data segment before reading pseudocode.
- **Far pointers arrive in two halves.** `les bx, [mem]` or separate segment
  and offset loads form one pointer. Treat the pair as a unit.
- **Floating-point emulation.** Compilers emitted `INT 34h`-`3Dh` followed by
  operand bytes; at run time the emulator or a fixup turns each into an x87
  instruction. Statically these look like interrupts followed by garbage.
  Translate them (`INT 35h` corresponds to opcode `D9`, and so on through the
  range) before analyzing numeric code.
- **Code and data share segments.** Jump tables, strings, and lookup tables
  sit between functions. A run of nonsense instructions is usually data.
- **Self-modifying code and patched templates.** Period code patches its own
  operands, and loaders rewrite prologues and fixup chains. File bytes are not
  always the bytes that execute.
- **String conventions vary.** `$`-terminated (DOS function `09h`),
  length-prefixed (Pascal), and NUL-terminated strings coexist. Text is
  usually code page 437 or a national code page, not ASCII or UTF-8;
  box-drawing and accented characters decode wrongly otherwise.
- **Timing and hardware assumptions.** Delay loops calibrated to CPU speed and
  reads of retrace or timer ports change behavior under emulation. A
  difference between emulator and expectation may be the emulator's speed
  setting.
- **Copy protection.** Key-disk checks through `INT 13h`, checksum loops, and
  anti-debug tricks (vector checks, timing) are common. Describe them when
  they are in scope and the work is authorized; they also explain code that
  seems to do nothing useful.

## Reporting

Follow [evidence workflows](evidence-workflows.md). For these targets, state in
addition:

- the container format and any second layer (extender, packer, overlay), with
  the bytes or strings that identify it;
- the load segment or base your addresses are relative to;
- the compiler or runtime you identified and how;
- which ordinal list or interrupt reference names came from;
- which facts are static and which were observed in an emulator, naming the
  emulator and its configuration.
