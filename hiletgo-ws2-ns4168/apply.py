#!/usr/bin/env python3
"""Overlay HAND-32 onto a cloned ducalex/retro-go tree.

Not a fork. Retro-Go stays upstream:
  https://github.com/ducalex/retro-go
  (c) Alex Duchesne (@ducalex) and contributors, GPLv2
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARKER = "RG_TARGET_HILETGO_WS2_NS4168"
APPS = "launcher retro-core prboom-go gwenesis fmsx"
BEGIN = "/* HAND32-I2C-BEGIN */"
END = "/* HAND32-I2C-END */"

INNER = r'''    /* HAND32-I2C-BEGIN */
    {
        uint8_t d[6] = {0};
        bool ok = rg_i2c_read(0x5A, 0, d, 6);
        if (!ok)
            ok = rg_i2c_read(0x5A, -1, d, 6);
        if (ok)
        {
            const int dead = 50;
            static int cx = -1, cy = -1;
            if (cx < 0) { cx = d[0]; cy = d[1]; }
            if (d[0] < cx - dead) state |= RG_KEY_LEFT;
            if (d[0] > cx + dead) state |= RG_KEY_RIGHT;
            if (d[1] < cy - dead) state |= RG_KEY_UP;
            if (d[1] > cy + dead) state |= RG_KEY_DOWN;
            uint8_t b = d[2];
            if (b && b != 0xFF)
            {
                if (b & 1)  state |= RG_KEY_A;
                if (b & 2)  state |= RG_KEY_B;
                if (b & 4)  state |= RG_KEY_X;
                if (b & 8)  state |= RG_KEY_Y;
                if (b & 16) state |= RG_KEY_MENU;
            }
        }
    }
    /* HAND32-I2C-END */
'''

INPUT_FIRST = (
    "#if defined(RG_GAMEPAD_I2C_MAP)\n"
    "#if defined(RG_TARGET_HILETGO_WS2_NS4168)\n"
    + INNER
    + "#else\n    uint32_t buttons = 0;\n"
)

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
    src = inp.read_text(encoding="utf-8")
    if BEGIN in src and END in src:
        pre, rest = src.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        src = pre + BEGIN + INNER.split(BEGIN, 1)[1].split(END, 1)[0] + END + post
        inp.write_text(src, encoding="utf-8")
        print("refreshed I2C analog calibration + button mask")
    elif MARKER not in src:
        needle = "#if defined(RG_GAMEPAD_I2C_MAP)\n    uint32_t buttons = 0;\n"
        if needle not in src:
            die("rg_input.c: I2C map block not found; Retro-Go version mismatch")
        src = src.replace(needle, INPUT_FIRST, 1)
        close = "        }\n    }\n#endif\n\n#if defined(RG_GAMEPAD_KBD_MAP)"
        close_new = "        }\n    }\n#endif\n#endif\n\n#if defined(RG_GAMEPAD_KBD_MAP)"
        if close not in src:
            die("rg_input.c: could not close HILETGO I2C branch")
        src = src.replace(close, close_new, 1)
        inp.write_text(src, encoding="utf-8")
        print("installed I2C joystick block")
    else:
        pat = re.compile(
            r"#if defined\(RG_TARGET_HILETGO_WS2_NS4168\)\s*\{.*?\}\s*#else\s*uint32_t buttons = 0;",
            re.S,
        )
        repl = (
            "#if defined(RG_TARGET_HILETGO_WS2_NS4168)\n"
            + INNER
            + "#else\n    uint32_t buttons = 0;"
        )
        src2, n = pat.subn(repl, src, count=1)
        if n != 1:
            die("rg_input.c: could not migrate unmarked I2C block")
        inp.write_text(src2, encoding="utf-8")
        print("migrated I2C block to calibrated analog")

    i2c = root / "components" / "retro-go" / "rg_i2c.c"
    it = i2c.read_text(encoding="utf-8")
    if ".master.clk_speed = 400000" in it:
        i2c.write_text(it.replace(".master.clk_speed = 400000", ".master.clk_speed = 100000", 1), encoding="utf-8")
        print("I2C clock set to 100 kHz (STM32 joystick)")
    elif ".master.clk_speed = 100000" in it:
        print("I2C clock already 100 kHz")

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
    print("  python rg_tool.py build-fw " + APPS + " --target hiletgo-ws2-ns4168")
    print("  python rg_tool.py build-img " + APPS + " --target hiletgo-ws2-ns4168")
    print("  python rg_tool.py install --target hiletgo-ws2-ns4168")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    apply(root)


if __name__ == "__main__":
    main()
