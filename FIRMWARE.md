# HAND-32 firmware

Target name: `hiletgo-ws2-ns4168`. Single flash image (`build-img` + `install`).

## Apps in the image

| App | In firmware | Systems |
|---|---|---|
| `launcher` | yes | Menu |
| `retro-core` | yes | NES, GB, GBC, GW, SG-1000, SMS, GG, Coleco, PCE, Lynx |
| `gwenesis` | yes | Mega Drive |
| `prboom-go` | yes | Doom |
| `fmsx` | yes | MSX |

Cores are compiled in. They are not files on the SD card.

IDF **5.3.x only**. IDF 6.x fails (`esp_adc_cal`).

## Build / flash (one `.img`)

Apps **before** `--target` (Windows argparse).

```
python rg_tool.py build-fw launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py build-img launcher retro-core prboom-go gwenesis fmsx --target hiletgo-ws2-ns4168
python rg_tool.py install --target hiletgo-ws2-ns4168
```

`install` writes the image at **0x0** (bootloader + table + all apps). UART USB-C. `--port COMx` if needed. Hold BOOT, tap RST if the port is missing.

`flash` is per-app after a full image exists. Do not use it for the first write.

Rename if you want:

```
copy retro-go_*_hiletgo-ws2-ns4168.img hand32.img
python -m esptool --chip esp32s3 write_flash --flash_size detect 0x0 hand32.img
```

## Partitions

`partitions.csv` is a dummy so IDF builds. Real sizes are `PROJECT_APPS` in `rg_tool.py`. `apply.py` sets:

| App | Slot |
|---|---|
| launcher | 1.125 MB (`0x120000`) |
| retro-core | 1.125 MB |
| prboom-go | 896 KB (`0xE0000`) |
| gwenesis | 1.125 MB |
| fmsx | 768 KB (`0xC0000`) |

Upstream defaults overflowed on this tree (launcher +1.7K, prboom +49K, fmsx +66K). mkfw can grow slots at pack time; the bumped sizes avoid that. Image is ~4.6 MB in **16 MB** flash. No `--fatsize` — ROMs live on the TF card.

## SD card (FAT32)

```
roms/nes
roms/gb
roms/gbc
roms/sms
roms/gg
roms/md
roms/pce
roms/lnx
roms/col
roms/gw
```

Doom: IWAD on the card (e.g. `doom.wad` / `doom1.wad`).

BIOS (optional except MSX):

```
retro-go/bios/gb_bios.bin
retro-go/bios/gbc_bios.bin
retro-go/bios/fds_bios.bin
retro-go/bios/msx/     MSX.ROM MSX2.ROM …
```

GB/GBC run without BIOS. MSX does not.

Stick = D-pad. **Start+Select = Menu**.
