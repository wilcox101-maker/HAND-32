#!/usr/bin/env python3
"""Overlay HAND-32 onto a cloned ducalex/retro-go tree.

Not a fork. Retro-Go stays upstream:
  https://github.com/ducalex/retro-go
  (c) Alex Duchesne (@ducalex) and contributors, GPLv2

GPIO-only input. Does not patch rg_input.c or rg_i2c.c.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKER = "RG_TARGET_HILETGO_WS2_NS4168"
APPS = "launcher retro-core prboom-go gwenesis fmsx"

CONFIG_ELIF = '''#elif defined(RG_TARGET_HILETGO_WS2_NS4168)
#include "targets/hiletgo-ws2-ns4168/config.h"
#elif defined(RG_TARGET_REDROID_GO)
'''

PROJECT_APPS_OLD = """PROJECT_APPS = {
    # Project name  Type, SubType, Size
    'launcher':     [0, 16, 1048576],
    'retro-core':   [0, 16, 1048576],
    'prboom-go':    [0, 16, 786432],
    'gwenesis':     [0, 16, 1048576],
    'fmsx':         [0, 16, 589824],
}"""

PROJECT_APPS_NEW = """PROJECT_APPS = {
    # Project name  Type, SubType, Size  (HAND-32 16MB, 64K aligned)
    'launcher':     [0, 16, 1179648],
    'retro-core':   [0, 16, 1179648],
    'prboom-go':    [0, 16, 917504],
    'gwenesis':     [0, 16, 1179648],
    'fmsx':         [0, 16, 786432],
}"""


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def apply(root: Path) -> None:
    tgt = root / "components" / "retro-go" / "targets" / "hiletgo-ws2-ns4168"
    if not (root / "rg_tool.py").is_file():
        die(f"{root} is not a retro-go tree (missing rg_tool.py)")

    tgt.mkdir(parents=True, exist_ok=True)
    for name in ("config.h", "sdkconfig", "env.py"):
        shutil.copy2(HERE / name, tgt / name)

    cfg = root / "components" / "retro-go" / "config.h"
    text = cfg.read_text(encoding="utf-8")
    if MARKER not in text:
        old = "#elif defined(RG_TARGET_REDROID_GO)\n"
        if old not in text:
            die("components/retro-go/config.h: unexpected format, cannot insert target")
        cfg.write_text(text.replace(old, CONFIG_ELIF, 1), encoding="utf-8")

    inp = root / "components" / "retro-go" / "rg_input.c"
    if inp.is_file() and "HAND32-I2C-BEGIN" in inp.read_text(encoding="utf-8"):
        print("note: leftover HAND32 I2C block in rg_input.c is inactive (no RG_GAMEPAD_I2C_MAP)")
    print("GPIO-only: skipped rg_input.c / rg_i2c.c patches")

    tool = root / "rg_tool.py"
    rt = tool.read_text(encoding="utf-8")
    if "1179648" not in rt and PROJECT_APPS_OLD in rt:
        tool.write_text(rt.replace(PROJECT_APPS_OLD, PROJECT_APPS_NEW, 1), encoding="utf-8")
        print("patched rg_tool.py PROJECT_APPS (16MB HAND-32 slots)")
    elif "1179648" in rt:
        print("rg_tool.py PROJECT_APPS already bumped")
    else:
        print("note: rg_tool.py PROJECT_APPS layout unexpected; mkfw will grow slots")

    print(f"ok: target hiletgo-ws2-ns4168 installed in {root}")
    print("firmware: Retro-Go by ducalex  https://github.com/ducalex/retro-go")
    print("  Flags BEFORE the command (Windows argparse):")
    print("  python rg_tool.py --no-networking --target hiletgo-ws2-ns4168 build-fw " + APPS)
    print("  python rg_tool.py --no-networking --target hiletgo-ws2-ns4168 build-img")
    print("  python rg_tool.py --target hiletgo-ws2-ns4168 --port COM3 install")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    apply(root)


if __name__ == "__main__":
    main()
