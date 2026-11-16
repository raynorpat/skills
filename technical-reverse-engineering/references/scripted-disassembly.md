# Scripted disassembly with Capstone

Capstone is a disassembly library. Use it to ask one narrow question of many
bytes: where is every `INT 21h` and what function does it request, which
virtual-method slots does this module call, does this region decode as code at
all. It complements a decompiler; it does not replace one.

Capstone is not part of REA. Anything it produces is your own observation.
Report it as such, with the script and the byte range, and do not present it as
REA Evidence.

## When it is the right tool

- The connected server does not support the format (see
  [DOS and 16-bit Windows](dos-and-win16.md)), so there is no function list or
  pseudocode to query.
- The region is not a recognized function: an unpacker stub, an overlay, a
  payload after a DOS-extender stub, code copied to memory at run time, or a
  dump taken from an emulator.
- The question is a census, not a reading: every interrupt, every port access,
  every call through a table, every use of an instruction.
- You need to check a claim about bytes independently of the tool that made it.

Use the decompiler view instead when the question is what a function does.

## Availability

Check before relying on it, and do not install it as a side effect of an
investigation:

```bash
python -c "import capstone; print(capstone.__version__)"
```

If it is missing, say so and ask before installing (`pip install capstone`).
The examples here use the Python binding and were run against Capstone 5.

## The bundled scanner

`scripts/capstone_scan.py` wraps the three most common scans. It reads the
file and prints; it writes nothing.

```bash
python <skill-directory>/scripts/capstone_scan.py self-test
python <skill-directory>/scripts/capstone_scan.py dos-int GAME.COM --base 0x100
python <skill-directory>/scripts/capstone_scan.py vcalls game.exe --offset 0x400 --length 0x20000 --base 0x401000
python <skill-directory>/scripts/capstone_scan.py disasm stub.bin --bits 16 --offset 0x1C0 --length 0x80
```

| Mode | Output | Use |
|---|---|---|
| `dos-int` | Each `INT` with the `AH` value loaded before it, or `?` | Map a DOS program's use of DOS and BIOS services |
| `vcalls` | Each `call [reg + disp]` as a slot index | Find COM and C++ virtual calls; see [games and graphics](games-and-graphics.md) |
| `disasm` | Plain listing | Read a stub or confirm a range is code |

`--offset` and `--length` select file bytes; `--base` sets the address printed
for the first byte. Get all three from the format's headers (section or segment
tables) so addresses match the other tools you are using.

## Writing your own scan

```python
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86 import X86_INS_IN, X86_INS_OUT, X86_OP_IMM

md = Cs(CS_ARCH_X86, CS_MODE_16)   # CS_MODE_32 / CS_MODE_64 for later targets
md.detail = True                   # required for insn.operands and insn.groups
md.skipdata = True                 # emit a placeholder for bytes that do not decode

for insn in md.disasm(code, base_address):
    if insn.id in (X86_INS_IN, X86_INS_OUT):
        port = next((op.imm for op in insn.operands if op.type == X86_OP_IMM), None)
        print(hex(insn.address), insn.mnemonic, insn.op_str, "port", port)
```

Points that matter:

- **Mode is not detected.** 16-bit real-mode, 16-bit protected-mode, and
  32-bit code decode differently from the same bytes. Take the mode from the
  format (COM, MZ, and NE are 16-bit; LE objects carry a 32-bit flag; PE is 32
  or 64). A DOS extender's stub and payload need different modes.
- **`detail` costs time.** Leave it off for a plain listing over a large range.
- **Skipdata placeholders have `insn.id == 0`.** Reset any state you are
  tracking when you see one.
- **Other architectures** use the same pattern with a different `Cs(...)`
  pair, such as `CS_ARCH_ARM`/`CS_MODE_THUMB`, `CS_ARCH_ARM64`/`CS_MODE_ARM`,
  `CS_ARCH_M68K`, or `CS_ARCH_MIPS`.

## Limits of a linear sweep

Capstone decodes whatever bytes it is given, in order. It does not follow
control flow, find function boundaries, or know code from data.

- **Data desynchronizes it.** Old x86 code keeps jump tables, strings, and
  lookup tables between functions. A sweep that crosses them decodes garbage,
  and the garbage can swallow the first real instructions after it. Start each
  sweep at a known entry point (the program entry, an export, a relocation
  target, a call target from a previous sweep) and stop at a return or an
  unconditional jump.
- **A variable-length instruction set resynchronizes by luck.** A sweep begun
  one byte off usually falls back into step within a few instructions, which
  makes wrong output look plausible. A hit in the first few instructions of an
  arbitrary range is weak evidence.
- **Register tracking is local.** The `AH` value reported by `dos-int` is the
  last immediate loaded in straight-line code. A value set before a jump,
  loaded from memory, or shared by several paths shows as `?`. Resolve those
  by reading the function.
- **A vtable slot is not a method name.** `vcalls` reports an index. Which
  interface it belongs to depends on what object the register holds, which
  the scan does not know.
- **Self-modifying and relocated code.** File bytes may differ from what
  executes (see the pitfalls in [DOS and 16-bit Windows](dos-and-win16.md)).
  Scan a memory dump when the question is about run-time code.

Confirm any hit that a conclusion depends on by reading the surrounding
function, in the decompiler when the format is supported.

## Related libraries

Use these only when the task needs them and they are already available, or the
user agrees to install them.

- **Unicorn** emulates CPU instructions without an operating system. It suits
  a self-contained routine such as a decompression or decryption loop: map the
  bytes, set the registers, run to the return. It has no DOS, BIOS, or Windows
  services, so anything that makes a call or raises an interrupt needs a hook
  that you write, and the result is only as good as that hook.
- **Keystone** assembles text to bytes, for checking what an instruction
  encodes to or preparing a byte pattern to search for.
- **Format parsers** (`pefile`, `lief`, `pyelftools`) give the section offsets
  and bases to pass to a scan. For MZ and NE, read the header fields directly;
  they are short and documented in [DOS and 16-bit Windows](dos-and-win16.md).

Emulating code from an untrusted binary in Unicorn does not touch the host
system, but run it with a step or time limit so a loop cannot hang the session.
