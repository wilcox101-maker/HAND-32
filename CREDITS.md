# Credits

HAND-32 is **not a fork**. It is a hardware target overlay that ports [Retro-Go](https://github.com/ducalex/retro-go) onto a HiLetgo ESP32-S3-DevKitC N16R8, Waveshare 2" ST7789T3, GPIO tactile pad, and NS4168 amp.

Clone Retro-Go. Apply this overlay. Build with Retro-Go's `rg_tool.py`. All launcher, cores, and tooling remain upstream.

## Retro-Go

**[Retro-Go](https://github.com/ducalex/retro-go)** by **[ducalex](https://github.com/ducalex)** (Alex Duchesne) and contributors.

Firmware for ESP32 handhelds: launcher, save states, cover art, and the emulator apps. Officially aimed at ODROID-GO and MRGC-G32; other boards exist as in-tree targets. HAND-32 adds one more target the same way.

- License: **GPLv2** ([COPYING](https://github.com/ducalex/retro-go/blob/master/COPYING)), with the exceptions listed in Retro-Go's README
- If you use HAND-32, you are using Retro-Go. Credit belongs there first.

## Cores (via Retro-Go)

| System | Origin |
|---|---|
| NES, GB/GBC, SMS/GG/SG-1000/Coleco | Go-Play / Triforce (crashoverride, Nemo1984, and others) |
| SNES | [Snes9x 2005](https://github.com/libretro/snes9x2005) |
| Mega Drive | [Gwenesis](https://github.com/bzhxx/gwenesis) by bzhxx |
| Game & Watch | [lcd-game-emulator](https://github.com/bzhxx/lcd-game-emulator) by bzhxx |
| Doom | [PrBoom 2.5.0](http://prboom.sourceforge.net/) |
| MSX | [fMSX](https://fms.komkon.org/fMSX/) by Marat Fayzullin (non-commercial) |
| Lynx | [libretro-handy](https://github.com/libretro/libretro-handy) (zlib) |
| PC Engine | as bundled in Retro-Go `retro-core` |

## This overlay

Pin map, `config.h`, NS4168 glue, GPIO pad schedule, and `apply.py` only. Those files: MIT. Combined firmware after `apply.py`: Retro-Go's licenses (GPLv2 + the exceptions above).

Do not vendor or re-publish Retro-Go source in this repo. Point people at [ducalex/retro-go](https://github.com/ducalex/retro-go).
