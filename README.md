# HAND-32

ESP32-S3 retro handheld overlay for [ducalex/retro-go](https://github.com/ducalex/retro-go).

**Hardware** (DuPont harness, pin map, power): **[HARDWARE.md](HARDWARE.md)**  
**Firmware** (apps, partitions, SD layout): **[FIRMWARE.md](FIRMWARE.md)**

- HiLetgo ESP32-S3-DevKitC **N16R8** (16 MB flash, 8 MB octal PSRAM)
- Waveshare 2" ST7789T3 320×240 (shared SPI TF, no touch)
- NullLab I2C joystick `0x5A`
- NullLab NS4168 I2S Class-D amp + 3W speaker
- NullLab LiPo pack (3.3 V + 5 V headers)

Overlay only. Upstream Retro-Go stays ducalex. **ESP-IDF 5.3.x** (5.3.5 OK). Do not use IDF 6 (`esp_adc_cal` is gone).

## Wiring

Four DuPont harnesses — not a rat’s nest. Full schedule in [HARDWARE.md](HARDWARE.md).

![HAND-32 DuPont wiring](wiring.svg)

| Harness | GPIOs |
|---|---|
| Power | Pack 5 V → DevKit 5V + NS4168 VCC. Pack 3.3 V → LCD **3V3** + stick VCC. Star GND |
| SPI2 | 12/11/13 CLK MOSI MISO · 10 LCD_CS · 4 SD_CS · 14/9/21 DC RST BL |
| I2C | 17 SDA · 18 SCL |
| I2S | 41 BCLK · 42 WS · 40 DIN · 8 CTRL HIGH |

LCD power is the **3V3** pin (module **VCC** = NC). Touch `TP_*` = NC. Never: 19–20 USB, 26–37 flash/PSRAM, 0/3/45/46 strap, 48 RGB. Unplug pack 5 V from the DevKit while UART USB-C supplies 5 V.

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

Cores are **in the firmware**. FAT32: `roms/nes`, `roms/gb`, `roms/gbc`, `roms/sms`, `roms/gg`, `roms/md`. Doom IWAD. MSX needs `retro-go/bios/msx/`.

## License

Overlay: MIT. Retro-Go cores: upstream licenses. Do not distribute copyrighted ROMs.
