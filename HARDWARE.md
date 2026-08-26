# HAND-32 hardware

Target `hiletgo-ws2-ns4168` for **[Retro-Go](https://github.com/ducalex/retro-go)** by [ducalex](https://github.com/ducalex) (Alex Duchesne) and contributors. This overlay is a **port, not a fork**. See [CREDITS.md](CREDITS.md).

GPIO nets use **2.54 mm DuPont**. The speaker is a **2-wire** red/black pair on the amp, not a DevKit GPIO. Touch header **NC**.

![HAND-32 DuPont wiring](wiring.svg)

## Bill of materials

| Qty | Part | Notes |
|---|---|---|
| 1 | HiLetgo ESP32-S3-DevKitC **N16R8** | 16 MB flash, 8 MB octal PSRAM. Flash on **UART USB-C** |
| 1 | Waveshare **2 inch** ST7789T3 320×240 + TF | Power the **3V3** pin; leave module **VCC** open |
| 1 | **Nulllabs I2C Joystick** `0x5A` | VCC / GND / SDA / SCL |
| 1 | **Nulllabs NS4168 3W Audio amp w/Speaker** | Orange NS4168 I2S DAC AMP + 3 W speaker. VCC 3.0–5.5 V. Use pack **5 V** |
| 1 | Nulllabs LiPo pack | 3.3 V and 5 V headers |
| — | DuPont FF / FM 20 cm | GPIO harnesses only |

## DuPont colors (GPIO)

| Color | Net |
|---|---|
| Red | +5 V |
| Orange | +3.3 V |
| Black | GND |
| Yellow | clocks (SCLK, SCL, LRC) |
| Green | data (MOSI, SDA, DIN) |
| Blue | MISO / BCL |
| White | chip-select |
| Violet | LCD DC / RST / BL |

Speaker pair (on the amp, not DuPont GPIO): **red = +**, **black = −**.

## Harness 1 — power

| Color | From | To |
|---|---|---|
| Red | Pack **5V** | DevKit **5V** |
| Red | Pack **5V** | Amp **Power V** |
| Orange | Pack **3V3** | LCD **3V3** (not VCC) |
| Orange | Pack **3V3** | **Nulllabs I2C Joystick** VCC |
| Black | Pack **GND** | DevKit GND, LCD GND, joystick GND, amp **Power G** |

Unplug pack 5 V from the DevKit whenever UART USB-C is supplying 5 V.

## Harness 2 — SPI2 (LCD + TF)

| Color | DevKit GPIO | Waveshare pin |
|---|---|---|
| Yellow | **12** | SCLK |
| Green | **11** | MOSI |
| Blue | **13** | MISO |
| White | **10** | LCD_CS |
| White | **4** | SD_CS |
| Violet | **14** | LCD_DC |
| Violet | **9** | LCD_RST |
| Violet | **21** | LCD_BL (active high) |

Two chip-selects, same CLK/MOSI/MISO. Do not use Waveshare’s sample S3 GPIOs (they collide with I2S 40/41/42).

## Harness 3 — Nulllabs I2C Joystick

| Color | DevKit GPIO | Joystick |
|---|---|---|
| Green | **17** | SDA |
| Yellow | **18** | SCL |

100 kHz, address `0x5A`. Leave **TP_SDA / TP_SCL / TP_INT / TP_RST** unconnected.

## Harness 4 — Nulllabs NS4168 3W Audio amp (I2S)

This kit’s I2S plug is silkscreened **G  V  BCL  LRC  DIN** (5 wires). There is **no CTRL** on that cable.

| Color | DevKit GPIO | Amp I2S pin |
|---|---|---|
| Blue | **41** | **BCL** (bit clock) |
| Yellow | **42** | **LRC** (word select / LRCLK) |
| Green | **40** | **DIN** |
| Black | GND | **G** |

Amp **Power V** / **Power G** are harness 1 (5 V / GND). You can leave the I2S **V** pin open if Power V is already fed. Firmware still drives GPIO **8** HIGH (legacy CTRL); **leave GPIO 8 unconnected** on this SKU.

## Harness 5 — speaker (2-wire)

On the amp, not the DevKit. Same as the kit photo: screw / JST **+** and **−** to the 3 W speaker.

| Color | From | To |
|---|---|---|
| Red | Amp **+** | Speaker **+** |
| Black | Amp **−** | Speaker **−** |

Do not land the speaker on any ESP32 pin.

## Pin map vs forbidden

Used: **4, 9, 10, 11, 12, 13, 14, 17, 18, 21, 40, 41, 42**. GPIO **8** unused on this SKU.

| GPIO | Why unused |
|---|---|
| 8 | No CTRL wire on this Nulllabs I2S cable |
| 19, 20 | USB D+/D− |
| 26–32 | WROOM-1 flash |
| 33, 34 | Not broken out |
| 35, 36, 37 | Octal PSRAM |
| 0, 3, 45, 46 | Strapping |
| 43, 44 | UART0 console |
| 48 | Onboard RGB |

## Electrical

| Rail | Destinations |
|---|---|
| 5 V | DevKit `5V`, amp Power **V** |
| 3.3 V | LCD `3V3`, Nulllabs I2C Joystick VCC |
| GND | All boards, one star |

`RG_BATTERY_DRIVER` is 0. Joystick XY center 128, deadzone 40. Start+Select = Menu.
