# HAND-32

Hardware port of **[Retro-Go](https://github.com/ducalex/retro-go)** by **[ducalex](https://github.com/ducalex)** (Alex Duchesne) and contributors. **Not a fork.** [CREDITS.md](CREDITS.md).

**Hardware:** [HARDWARE.md](HARDWARE.md) · **Firmware:** [FIRMWARE.md](FIRMWARE.md)

- HiLetgo ESP32-S3-DevKitC **N16R8**
- Waveshare 2" ST7789T3 + TF (no touch)
- **Nulllabs I2C Joystick** `0x5A` — XY, PB, A, B, C, D (no Start/Select)
- Two tactiles: **GPIO 5 Start**, **GPIO 6 Select** (to GND)
- **Nulllabs NS4168 3W Audio amp w/Speaker**
- Nulllabs LiPo pack

ESP-IDF **5.3.x** only.

## Wiring

![HAND-32 DuPont wiring](wiring.svg)

| Harness | Run |
|---|---|
| Power | Pack 5 V → DevKit + amp V. Pack 3.3 V → LCD **3V3** + joystick VCC. Star GND |
| SPI2 | 12/11/13 · CS 10 / 4 · 14/9/21 |
| I2C | 17 SDA · 18 SCL |
| I2S | 41 BCL · 42 LRC · 40 DIN |
| Speaker | Amp +/− 2-wire |
| Tactiles | GPIO **5** Start, GPIO **6** Select, both to GND |

Joystick: XY = D-pad, A/B = A/B, C/D = X/Y, PB = Menu.

## Flash

```
git clone --recursive https://github.com/ducalex/retro-go.git
python hiletgo-ws2-ns4168/apply.py retro-go
cd retro-go
python rg_tool.py build-fw launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py build-img launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168
```

Apps **before** `--target`. One `.img` at 0x0. Re-run `apply.py` after pulling this overlay (Start/Select moved to GPIO).

## License

Retro-Go: **GPLv2**. Overlay-only files: MIT. Flashed image follows Retro-Go. No copyrighted ROMs.
