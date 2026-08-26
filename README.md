# HAND-32

ESP32-S3 retro handheld overlay for [ducalex/retro-go](https://github.com/ducalex/retro-go).

**Hardware**

- HiLetgo ESP32-S3-DevKitC **N16R8**
- Waveshare 2" ST7789T3 320×240 (shared SPI TF, no touch)
- NullLab I2C joystick `0x5A`
- NullLab NS4168 I2S Class-D amp + 3W speaker
- NullLab LiPo pack (3.3 V + 5 V headers)

This repo is the **target overlay only**. Retro-Go itself stays upstream. Build with **ESP-IDF 5.3.x** (5.3.5 is fine). Do not use IDF 6.

## Pin map

| Function | GPIO |
|---|---|
| SPI CLK / MOSI / MISO | 12 / 11 / 13 |
| LCD CS / DC / RST / BL | 10 / 14 / 9 / 21 |
| SD CS | 4 |
| I2C SDA / SCL | 17 / 18 |
| I2S BCLK / WS / DIN | 41 / 42 / 40 |
| NS4168 CTRL | 8 HIGH |

Never: 19–20 USB, 26–37 flash/PSRAM, 0/3/45/46 strap, 48 RGB.

Power: pack 5 V → DevKit 5 V + amp VCC. Pack 3.3 V → LCD + stick. Common GND. Unplug pack 5 V from the DevKit while USB supplies 5 V.

## Build

```
git clone --recursive https://github.com/ducalex/retro-go.git
python hiletgo-ws2-ns4168/apply.py retro-go
cd retro-go
python rg_tool.py -h
```

`--target` must list `hiletgo-ws2-ns4168`. Then (ESP-IDF 5.3 PowerShell on Windows):

```
python rg_tool.py build-fw launcher retro-core --target hiletgo-ws2-ns4168
python rg_tool.py build-img launcher retro-core --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168
```

S3 has no `.fw` packer. First flash is `build-img` then `install` (full image at 0x0). UART USB-C; hold BOOT if the port is missing. Always `python rg_tool.py` on Windows.

ROMs on FAT32: `roms/nes`, `roms/gb`, `roms/gbc`, `roms/sms`.

## Panel / stick tweaks

- Negative image → drop `ILI9341_CMD(0x21)` in `config.h`
- Portrait / mirrored → `ST7789_MADCTL_MV` / `BGR`
- Stick Y inverted → swap UP/DOWN in the HILETGO block of `rg_input.c`

## License

Overlay files in this repo: MIT. Retro-Go cores remain under their upstream licenses. Do not distribute copyrighted ROMs.
