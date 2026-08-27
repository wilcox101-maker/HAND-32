# HAND-32 firmware

Hardware port of [Retro-Go](https://github.com/ducalex/retro-go) by [ducalex](https://github.com/ducalex) and contributors. Not a fork. [CREDITS.md](CREDITS.md).

Target: `hiletgo-ws2-ns4168`. GPIO tactiles only. No I2C joystick. No GBA on ESP32-S3.

IDF **5.3.x only**. IDF 6.x fails (`esp_adc_cal`).

## Apps in the image

| App | Systems |
|---|---|
| `launcher` | Menu |
| `retro-core` | NES, GB, GBC, GW, SG-1000, SMS, GG, Coleco, PCE, Lynx |
| `gwenesis` | Mega Drive |
| `prboom-go` | Doom |
| `fmsx` | MSX |

Cores are compiled in. They are not files on the SD card.

## Overlay (`hiletgo-ws2-ns4168/config.h`)

| Define | Value |
|---|---|
| `RG_STORAGE_SDSPI_SPEED` | `SDMMC_FREQ_DEFAULT` (20 MHz) |
| `RG_SCREEN_SPEED` | `SPI_MASTER_FREQ_40M` |
| Amp enable | **undefined** (do not set -1) |
| Input | `RG_GAMEPAD_GPIO_MAP` |

If the TF slot CRC-fails, set SD back to `SDMMC_FREQ_PROBING`.

## Build / flash

Windows argparse: **all flags before the command**. `build-img` takes **no** app names. Do not put `--no-networking` between `build-fw` and the app list — that is the `unrecognized arguments` error.

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

UART USB-C, not OTG. Unplug pack **5V** from the DevKit while flashing. If `No serial data received`: hold **BOOT**, tap **RST**, keep BOOT until Connecting.

```
python -m esptool --chip esp32s3 --port COM3 --before no_reset write_flash --flash_size detect 0x0 retro-go_*_hiletgo-ws2-ns4168.img
```

## SD card

ESP32 SDSPI wants **MBR + one FAT32 primary**. Not exFAT. Not GPT.

| Card | Do this |
|---|---|
| **16–32 GB** Class 10 | Best. Full-card FAT32, 32 KB clusters. |
| **128 GB** | Do **not** FAT32 the whole card. **MBR**, first partition **32 GB FAT32 32 KB**, rest unallocated. |

Windows will not FAT32 anything >32 GB in Explorer. Use Disk Management (MBR + 32 GB simple volume, FAT32).

Copy unzipped ROMs after format:

```
roms\nes  roms\gb  roms\gbc  roms\sms  roms\gg  roms\md
roms\doom  roms\pce  roms\lnx  roms\col  roms\gw  roms\msx
retro-go\bios\gb_bios.bin
retro-go\bios\gbc_bios.bin
retro-go\bios\fds_bios.bin
retro-go\bios\msx\
```

Eject the reader before pulling the card. Play on **battery**. LCD **VCC = NC**, **3V3** from pack.

In-game: **MENU** (GPIO 39) → Options → Speed (turbo), Overclock, Scaling Fit, Filter Off.
