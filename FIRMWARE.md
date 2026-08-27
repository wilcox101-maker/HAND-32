# HAND-32 firmware

Hardware port of [Retro-Go](https://github.com/ducalex/retro-go) by [ducalex](https://github.com/ducalex) (Alex Duchesne) and contributors. Not a fork. [CREDITS.md](CREDITS.md).

Target: `hiletgo-ws2-ns4168`. GPIO tactiles only (`RG_GAMEPAD_GPIO_MAP`). No I2C joystick in firmware. No GBA on ESP32-S3.

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

## Overlay tunables (`hiletgo-ws2-ns4168/config.h`)

| Define | Value | Why |
|---|---|---|
| `RG_STORAGE_SDSPI_SPEED` | `SDMMC_FREQ_DEFAULT` (20 MHz) | Shared SPI2 with LCD. Was `PROBING` (400 kHz). |
| `RG_SCREEN_SPEED` | `SPI_MASTER_FREQ_40M` | Stable on Dupont. |
| Amp enable | **undefined** | `RG_GPIO_SND_AMP_ENABLE -1` panics. |

If the TF slot CRC-fails, set SD back to `SDMMC_FREQ_PROBING`.

## Build / flash (one `.img`)

Apps **before** `--target`. `--no-networking` keeps CPU/RAM on the cores.

```
python C:\Users\d.wilcox\HAND-32\hiletgo-ws2-ns4168\apply.py C:\Users\d.wilcox\retro-go
cd C:\Users\d.wilcox\retro-go
python rg_tool.py clean --target hiletgo-ws2-ns4168
python rg_tool.py build-fw --no-networking launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py build-img --no-networking launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168
```

`install` writes **0x0**. UART USB-C. Hold BOOT, tap RST if needed.

## SD card (FAT32)

Unzip ROMs. BIOS under `/retro-go/bios/`. Doom IWADs in `/roms/doom/`.

In-game: **MENU** (GPIO 39) → Options → Speed (turbo), Overclock, Scaling Fit, Filter Off.
