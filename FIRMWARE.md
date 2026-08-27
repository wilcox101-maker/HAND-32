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

`build-fw` takes the app list. `build-img` does **not**.

```
python C:\Users\d.wilcox\HAND-32\hiletgo-ws2-ns4168\apply.py C:\Users\d.wilcox\retro-go
cd C:\Users\d.wilcox\retro-go
python rg_tool.py clean --target hiletgo-ws2-ns4168
python rg_tool.py build-fw --no-networking launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py build-img --no-networking --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168 --port COM3
```

UART USB-C, not OTG. If `Failed to connect ... No serial data received`:

1. Unplug pack **5V** from the DevKit.
2. Hold **BOOT**, tap **RST**, keep BOOT until esptool says Connecting.
3. Fallback:

```
python -m esptool --chip esp32s3 --port COM3 --before no_reset write_flash --flash_size detect 0x0 retro-go_*_hiletgo-ws2-ns4168.img
```

## SD card (FAT32)

Unzip ROMs. BIOS under `/retro-go/bios/`. Doom IWADs in `/roms/doom/`.

In-game: **MENU** (GPIO 39) → Options → Speed (turbo), Overclock, Scaling Fit, Filter Off.
