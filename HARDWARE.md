# HAND-32 hardware

Target `hiletgo-ws2-ns4168`. All jumpers are **2.54 mm DuPont** (female–female onto module headers, female–male onto the DevKit). One color per net. Touch header **NC**.

![HAND-32 DuPont wiring](wiring.svg)

## Bill of materials

| Qty | Part | Notes |
|---|---|---|
| 1 | HiLetgo ESP32-S3-DevKitC **N16R8** | 16 MB flash, 8 MB octal PSRAM, 240 MHz. Flash on **UART USB-C** |
| 1 | Waveshare **2 inch** ST7789T3 320×240 + TF | Header names below. Power the **3V3** pin; leave module **VCC** open (Waveshare wiki) |
| 1 | NullLab I2C joystick **0x5A** | VCC / GND / SDA / SCL |
| 1 | NullLab NS4168 + 3 W speaker | VCC 3.0–5.5 V. Use pack **5 V** for 3 W |
| 1 | NullLab LiPo pack | 3.3 V and 5 V headers |
| — | DuPont FF / FM 20 cm | Colors in the schedule |

## DuPont colors

Hobby / Adafruit / Qwiic convention:

| Color | Net |
|---|---|
| Red | +5 V |
| Orange | +3.3 V |
| Black | GND |
| Yellow | clocks (SCLK, SCL, WS) |
| Green | data out (MOSI, SDA, DIN) |
| Blue | data in / bit clock (MISO, BCLK) |
| White | chip-select / CTRL |
| Violet | LCD DC / RST / BL |

## Harness 1 — power (star GND)

| Color | From | To |
|---|---|---|
| Red | Pack **5V** | DevKit **5V** |
| Red | Pack **5V** | NS4168 **VCC** |
| Orange | Pack **3V3** | LCD **3V3** (not VCC) |
| Orange | Pack **3V3** | Stick **VCC** |
| Black | Pack **GND** | DevKit GND, LCD GND, stick GND, NS4168 GND |

Unplug pack 5 V from the DevKit whenever UART USB-C is supplying 5 V (do not parallel two 5 V sources).

## Harness 2 — SPI2 (shared LCD + TF)

Same CLK / MOSI / MISO. **Two chip-selects.**

| Color | DevKit GPIO | Waveshare pin |
|---|---|---|
| Yellow | **12** | SCLK |
| Green | **11** | MOSI |
| Blue | **13** | MISO (required for SD) |
| White | **10** | LCD_CS |
| White | **4** | SD_CS |
| Violet | **14** | LCD_DC |
| Violet | **9** | LCD_RST |
| Violet | **21** | LCD_BL (active high) |

SPI host `SPI2_HOST`. LCD 40 MHz. SD probing speed. Do **not** use Waveshare’s ESP32-S3 example GPIOs (1/2/38/39/40/41/42) — those collide with this I2S map.

## Harness 3 — I2C stick (Qwiic colors)

| Color | DevKit GPIO | Stick |
|---|---|---|
| Green | **17** | SDA |
| Yellow | **18** | SCL |

100 kHz, address `0x5A`. Leave **TP_SDA / TP_SCL / TP_INT / TP_RST** unconnected. If you ever attach touch: CST816D is not `0x5A`, but **TP_INT on GPIO 4 fights SD_CS** and **TP_RST on GPIO 9 fights LCD_RST**.

## Harness 4 — I2S amp

| Color | DevKit GPIO | NS4168 |
|---|---|---|
| Blue | **41** | BCLK |
| Yellow | **42** | LRCLK / WS |
| Green | **40** | DIN |
| White | **8** | CTRL |

CTRL is **channel select**. Firmware holds GPIO 8 **HIGH** (right). Speaker on SPK+ / SPK− only — no DuPont there.

## Pin map vs forbidden

Used: **4, 8, 9, 10, 11, 12, 13, 14, 17, 18, 21, 40, 41, 42**. No duplicates. Shared SPI is two CS, not a short.

| GPIO | Why unused |
|---|---|
| 19, 20 | USB D+/D− |
| 26–32 | WROOM-1 flash |
| 33, 34 | Not broken out |
| 35, 36, 37 | Octal PSRAM |
| 0, 3, 45, 46 | Strapping |
| 43, 44 | UART0 console |
| 48 | Onboard RGB |

GPIO 17/18 are S3 default UART1 — Retro-Go console is UART0. Fine unless you enable UART1 on the defaults.

## Electrical

| Rail | Destinations |
|---|---|
| 5 V | DevKit `5V`, NS4168 `VCC` |
| 3.3 V | LCD `3V3`, stick `VCC` |
| GND | All four boards, one star |

`RG_BATTERY_DRIVER` is 0 — no cell ADC. Stick XY center 128, deadzone 40. Start+Select = Menu.
