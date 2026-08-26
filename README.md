# HAND-32

Hardware port of **[Retro-Go](https://github.com/ducalex/retro-go)** — the ESP32 retro firmware by **[ducalex](https://github.com/ducalex)** (Alex Duchesne) and contributors.

This repo is **not a fork**. It is a target overlay: pins, display init, Nulllabs I2C Joystick, Nulllabs NS4168 3W Audio amp w/Speaker. Clone Retro-Go, run `apply.py`, build with Retro-Go's `rg_tool.py`. Full attribution: **[CREDITS.md](CREDITS.md)**.

**Hardware** (DuPont harness, pin map): **[HARDWARE.md](HARDWARE.md)**  
**Firmware** (apps, partitions, SD): **[FIRMWARE.md](FIRMWARE.md)**

- HiLetgo ESP32-S3-DevKitC **N16R8** (16 MB flash, 8 MB octal PSRAM)
- Waveshare 2" ST7789T3 320×240 (shared SPI TF, no touch)
- **Nulllabs I2C Joystick** `0x5A`
- **Nulllabs NS4168 3W Audio amp w/Speaker** (I2S DAC AMP + 2-wire 3 W speaker)
- Nulllabs LiPo pack (3.3 V + 5 V headers)

Build with **ESP-IDF 5.3.x** (5.3.5 OK). Do not use IDF 6 (`esp_adc_cal` is gone).

## Wiring

Five harnesses. Full schedule in [HARDWARE.md](HARDWARE.md).

![HAND-32 DuPont wiring](wiring.svg)

| Harness | Run |
|---|---|
| Power | Pack 5 V → DevKit 5V + amp Power V. Pack 3.3 V → LCD **3V3** + Nulllabs I2C Joystick VCC. Star GND |
| SPI2 | 12/11/13 CLK MOSI MISO · 10 LCD_CS · 4 SD_CS · 14/9/21 DC RST BL |
| I2C | 17 SDA · 18 SCL → Nulllabs I2C Joystick |
| I2S | 41 **BCL** · 42 **LRC** · 40 **DIN** (kit silkscreen; no CTRL on this cable) |
| Speaker | Amp **+** red / **−** black → 3 W speaker. Not a GPIO |

LCD power is the **3V3** pin (module **VCC** = NC). Touch `TP_*` = NC. GPIO 8 unused on this SKU. Never: 19–20 USB, 26–37 flash/PSRAM, 0/3/45/46 strap, 48 RGB. Unplug pack 5 V from the DevKit while UART USB-C supplies 5 V.

## Single flash image

One `.img` at `0x0`: launcher + retro-core + Mega Drive + Doom + MSX.

```
git clone --recursive https://github.com/ducalex/retro-go.git
python hiletgo-ws2-ns4168/apply.py retro-go
cd retro-go
```

ESP-IDF **5.3** PowerShell. Apps **before** `--target`:

```
python rg_tool.py build-fw launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py build-img launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168
```

S3 has no `.fw` packer. Use `install` (or `esptool write_flash 0x0 *.img`). UART USB-C; hold BOOT if the port is missing. Always `python rg_tool.py` on Windows.

## After flash

Cores are **in the firmware** (Retro-Go apps). FAT32: `roms/nes`, `roms/gb`, `roms/gbc`, `roms/sms`, `roms/gg`, `roms/md`. Doom IWAD. MSX needs `retro-go/bios/msx/`.

## License

See **[LICENSE](LICENSE)** and **[CREDITS.md](CREDITS.md)**.

- Retro-Go (launcher, cores, `rg_tool.py`): **GPLv2**, © ducalex and contributors. fMSX is non-commercial; handy is zlib.
- This overlay's original files (target config, docs, wiring, `apply.py`): MIT, when distributed on their own.
- A flashed HAND-32 image is a modified Retro-Go and follows Retro-Go's licenses. Do not distribute copyrighted ROMs.
