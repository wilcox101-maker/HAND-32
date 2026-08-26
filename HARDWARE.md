# HAND-32 hardware

Target `hiletgo-ws2-ns4168` for **[Retro-Go](https://github.com/ducalex/retro-go)** by [ducalex](https://github.com/ducalex) (Alex Duchesne) and contributors. Port overlay, not a fork. [CREDITS.md](CREDITS.md).

GPIO nets: **2.54 mm DuPont**. Speaker: **2-wire** on the amp. Touch **NC**.

![HAND-32 DuPont wiring](wiring.svg)

## Photos

MCU is a **YD-ESP32-S3 2022-V1.3** N16R8 (DevKitC-1 clone). Flash on the **UART USB-C** (back silkscreen **USB / COM**), not **USB-OTG**.

<img src="docs/hardware/esp32-s3.jpg" width="560" alt="YD-ESP32-S3 N16R8 both sides">

<img src="docs/hardware/esp32-s3-front.jpg" width="420" alt="YD-ESP32-S3 chip side">

**Nulllabs Mini-Joystick** `0x5A`. Header **SCL SDA V G**. Stick 0–255 XY, **PB** (press), **A B C D**. No Start/Select on the module.

<img src="docs/hardware/joystick.jpg" width="560" alt="Nulllabs Mini-Joystick I2C 0x5A">

**Nulllabs LiPo pack** 1200 mAh. Headers **VBAT / 5V / 3V3**. USB-C charge (max 5 V 1.2 A). USB-A output 5 V 1 A. Use the **5V** and **3V3** headers, not USB-A, for the handheld.

<img src="docs/hardware/lipo-pack.jpg" width="520" alt="Nulllabs 1200mAh LiPo pack">

Start/Select: two **6×6 mm 4-pin tactiles** on a 400-point breadboard (or fly leads). Opposite pins are the switch; adjacent pins on one side are already shorted inside.

<img src="docs/hardware/tactile.jpg" width="360" alt="6x6 mm 4-pin tactile Start/Select">

<img src="docs/hardware/breadboard.jpg" width="360" alt="400-point breadboard for Start/Select tactiles">

Still needed: **NS4168 amp + speaker** (one photo).

## Bill of materials

| Qty | Part | Notes |
|---|---|---|
| 1 | **YD-ESP32-S3** / HiLetgo **N16R8** | Dual USB-C. Flash **UART/COM**, not OTG |
| 1 | Waveshare **2 inch** ST7789T3 + TF | Power **3V3**; module **VCC** = NC |
| 1 | **Nulllabs I2C Joystick** `0x5A` | Header **SCL SDA V G**. XY, PB, A B C D. No Start/Select |
| 2 | 6×6 mm tactile (4-pin OK) | GPIO **5** Start, GPIO **6** Select, other side GND |
| 1 | **Nulllabs NS4168 3W Audio amp w/Speaker** | I2S **G V BCL LRC DIN** + speaker +/− |
| 1 | Nulllabs LiPo pack | Headers **VBAT / 5V / 3V3**. USB-C charge. USB-A is 5 V 1 A |
| 1 | 400-point breadboard (optional) | Holds the two tactiles |

## Button map

| Control | Retro-Go |
|---|---|
| Joystick XY | D-pad (deadzone 40) |
| A / B | A / B |
| C / D | X / Y |
| PB (stick click) | Menu |
| Tactile GPIO **5** | **Start** (active-low, internal pull-up) |
| Tactile GPIO **6** | **Select** (active-low, internal pull-up) |

## Harness 1 — power

Pack **5V** → DevKit 5V and amp Power V. Pack **3V3** → LCD 3V3 and joystick V. Star GND. Unplug pack 5 V from the DevKit while UART USB-C supplies 5 V. Do not feed DevKit from pack USB-A and the 5V header at the same time.

## Harness 2 — SPI2

12 SCLK, 11 MOSI, 13 MISO, 10 LCD_CS, 4 SD_CS, 14 DC, 9 RST, 21 BL.

## Harness 3 — Nulllabs I2C Joystick

17 SDA, 18 SCL, 100 kHz, `0x5A`. Module header order **SCL SDA V G**.

## Harness 4 — Nulllabs NS4168 amp I2S

41 **BCL**, 42 **LRC**, 40 **DIN**, G to GND. Power V/G from harness 1. No CTRL on this cable. GPIO 8 unused.

## Harness 5 — speaker

Amp **+** red → speaker +. Amp **−** black → speaker −.

## Harness 6 — Start / Select tactiles

GPIO **5** and GPIO **6** each to one side of a tactile; other side **GND**. Internal pull-up. No resistor. On a 4-pin 6×6, use **opposite** pins (adjacent pins on one side are already shorted inside the switch).

Breadboard: GPIO 5 → row, switch across the ditch to GND rail. Same for GPIO 6.

## Forbidden

Used: **4, 5, 6, 9, 10, 11, 12, 13, 14, 17, 18, 21, 40, 41, 42**. Leave **8** open.

Never: 0, 3, 19–20 (USB), 26–37 (flash/PSRAM), 43–46 (UART0/strap), 48 (RGB).
