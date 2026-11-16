#!/usr/bin/env python3
"""Targeted x86 scans with Capstone for questions a decompiler view answers slowly.

Read-only: opens the input file, prints findings, writes nothing.

  dos-int   16-bit code: every INT instruction with the AH value set before it
  vcalls    32/64-bit code: every `call [reg + disp]`, reported as a vtable slot
  disasm    plain listing of a byte range

Results are a linear sweep from the offset you give. Start at a known function
entry; a sweep that begins in data, or runs across data, decodes nonsense and
can swallow the instructions that follow. Treat hits as leads to confirm.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterator

try:
    from capstone import (
        CS_ARCH_X86, CS_GRP_CALL, CS_GRP_JUMP, CS_GRP_RET,
        CS_MODE_16, CS_MODE_32, CS_MODE_64, Cs,
    )
    from capstone.x86 import (
        X86_INS_CALL, X86_INS_INT, X86_INS_MOV,
        X86_OP_IMM, X86_OP_MEM, X86_OP_REG,
        X86_REG_AH, X86_REG_AX, X86_REG_INVALID,
    )
except ImportError:  # pragma: no cover
    sys.exit("capstone is not installed for this Python (pip install capstone)")

MODES = {16: CS_MODE_16, 32: CS_MODE_32, 64: CS_MODE_64}


def dos_interrupts(code: bytes, base: int) -> Iterator[tuple[int, int, int | None]]:
    """Yield (address, interrupt number, AH or None) for each INT in 16-bit code."""
    md = Cs(CS_ARCH_X86, CS_MODE_16)
    md.detail = True
    md.skipdata = True  # do not stop at bytes that fail to decode
    ah: int | None = None
    for insn in md.disasm(code, base):
        if insn.id == 0:  # skipdata placeholder for undecodable bytes
            ah = None
            continue
        if insn.id == X86_INS_MOV and len(insn.operands) == 2:
            dst, src = insn.operands
            if dst.type == X86_OP_REG and src.type == X86_OP_IMM:
                if dst.reg == X86_REG_AH:
                    ah = src.imm & 0xFF
                elif dst.reg == X86_REG_AX:
                    ah = (src.imm >> 8) & 0xFF
            elif dst.type == X86_OP_REG and dst.reg in (X86_REG_AH, X86_REG_AX):
                ah = None  # loaded from somewhere this scan does not follow
        elif insn.id == X86_INS_INT:
            yield insn.address, insn.operands[0].imm & 0xFF, ah
            ah = None
        elif insn.group(CS_GRP_JUMP) or insn.group(CS_GRP_CALL) or insn.group(CS_GRP_RET):
            ah = None  # control flow: the tracked value may not reach the next INT


def vtable_calls(code: bytes, base: int, bits: int = 32) -> Iterator[tuple[int, str, int]]:
    """Yield (address, base register, slot index) for `call [reg + disp]`."""
    pointer_size = bits // 8
    md = Cs(CS_ARCH_X86, MODES[bits])
    md.detail = True
    md.skipdata = True
    for insn in md.disasm(code, base):
        if insn.id != X86_INS_CALL:
            continue
        op = insn.operands[0]
        if (
            op.type == X86_OP_MEM
            and op.mem.base != X86_REG_INVALID
            and op.mem.index == X86_REG_INVALID
            and op.mem.disp >= 0
            and op.mem.disp % pointer_size == 0
        ):
            yield insn.address, insn.reg_name(op.mem.base), op.mem.disp // pointer_size


def listing(code: bytes, base: int, bits: int) -> Iterator[str]:
    md = Cs(CS_ARCH_X86, MODES[bits])
    md.skipdata = True
    for insn in md.disasm(code, base):
        yield f"{insn.address:08x}  {insn.bytes.hex():<20}  {insn.mnemonic} {insn.op_str}".rstrip()


def self_test() -> int:
    dos = bytes.fromhex("b409ba1001cd21b8004ccd21")
    assert list(dos_interrupts(dos, 0x100)) == [(0x105, 0x21, 0x09), (0x10A, 0x21, 0x4C)]
    jumped = bytes.fromhex("b409eb00cd21")  # a jump between the load and the INT
    assert list(dos_interrupts(jumped, 0x100)) == [(0x104, 0x21, None)]
    com = bytes.fromhex("8b0850ff5128ff9280000000ffd0")
    assert list(vtable_calls(com, 0x401000)) == [(0x401003, "ecx", 10), (0x401006, "edx", 32)]
    assert next(listing(b"\xc3", 0, 32)).endswith("ret")
    print("self-test passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("mode", choices=("dos-int", "vcalls", "disasm", "self-test"))
    parser.add_argument("file", nargs="?", type=Path)
    parser.add_argument("--offset", type=lambda v: int(v, 0), default=0, help="file offset to start at")
    parser.add_argument("--length", type=lambda v: int(v, 0), default=None, help="bytes to read (default: to end)")
    parser.add_argument("--base", type=lambda v: int(v, 0), default=None, help="address of the first byte (default: the offset)")
    parser.add_argument("--bits", type=int, choices=(16, 32, 64), default=None, help="default 16 for dos-int, else 32")
    args = parser.parse_args(argv)

    if args.mode == "self-test":
        return self_test()
    if args.file is None:
        parser.error("a file is required for this mode")

    data = args.file.read_bytes()
    code = data[args.offset: None if args.length is None else args.offset + args.length]
    base = args.offset if args.base is None else args.base

    if args.mode == "dos-int":
        for address, number, ah in dos_interrupts(code, base):
            print(f"{address:08x}  int {number:02x}h  ah={'?' if ah is None else f'{ah:02x}h'}")
    elif args.mode == "vcalls":
        for address, register, slot in vtable_calls(code, base, args.bits or 32):
            print(f"{address:08x}  call [{register} + slot {slot}]")
    else:
        for line in listing(code, base, args.bits or 32):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
