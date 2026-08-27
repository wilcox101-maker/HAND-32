# HAND-32

Hardware port of **[Retro-Go](https://github.com/ducalex/retro-go)** by **[ducalex](https://github.com/ducalex)** (Alex Duchesne) and contributors. **Not a fork.** [CREDITS.md](CREDITS.md).

**Hardware:** [HARDWARE.md](HARDWARE.md) · **Firmware:** [FIRMWARE.md](FIRMWARE.md)

- HiLetgo / YD-ESP32-S3-DevKitC **N16R8**
- Waveshare 2" ST7789T3 + TF (no touch). Module **VCC = NC**, power **3V3**
- GPIO tactile pad: U/D/L/R, A/B/X/Y, Start/Select, Menu
- **Nulllabs NS4168 3W Audio amp w/Speaker**
- Nulllabs LiPo pack (headers **5V / 3V3**)

ESP-IDF **5.3.x** only. Input is **GPIO-only** (no I2C joystick in firmware).

## Flash (IDF 5.3.5 shell)

Windows argparse: **flags before the command**. Apps only on `build-fw`.

```
cd C:\Users\d.wilcox\HAND-32
git pull
python hiletgo-ws2-ns4168\apply.py C:\Users\d.wilcox\retro-go
cd C:\Users\d.wilcox\retro-go
python rg_tool.py --target hiletgo-ws2-ns4168 clean
python rg_tool.py --no-networking --target hiletgo-ws2-ns4168 build-fw launcher retro-core prboom-go gwenesis fmsx
python rg_tool.py --no-networking --target hiletgo-ws2-ns4168 build-img
python rg_tool.py --target hiletgo-ws2-ns4168 --port COM3 install
```

One `.img` at **0x0** on UART USB-C (not OTG). Unplug pack **5V** while flashing.

## License

Retro-Go: **GPLv2**. Overlay-only files: MIT. Flashed image follows Retro-Go. No copyrighted ROMs.
