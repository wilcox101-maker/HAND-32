/* HAND-32 target overlay for Retro-Go (ducalex/retro-go).
 * Not a fork. Pins and panel init only.
 * Retro-Go (c) Alex Duchesne (@ducalex) and contributors, GPLv2.
 * https://github.com/ducalex/retro-go
 *
 * Nulllabs I2C Joystick 0x5A: analog XY, PB, A, B, C, D (no Start/Select).
 * START/SELECT are two active-low tactiles on GPIO 5 / 6.
 *
 * Waveshare 2inch ST7789VW/T3 is natively 240x320. Landscape 320x240 uses
 * MADCTL 0x70 (MX|MV|ML) per Waveshare LCD_2inch HORIZONTAL. INVON 0x21.
 */
#pragma once

#define RG_TARGET_NAME             "HILETGO-WS2-NS4168"

#define RG_STORAGE_ROOT             "/sd"
#define RG_STORAGE_SDSPI_HOST       SPI2_HOST
#define RG_STORAGE_SDSPI_SPEED      SDMMC_FREQ_PROBING

#define RG_AUDIO_USE_INT_DAC        0
#define RG_AUDIO_USE_EXT_DAC        1

#define RG_SCREEN_DRIVER            0   /* ili9341.h path also drives ST7789 */
#define RG_SCREEN_HOST              SPI2_HOST
#define RG_SCREEN_SPEED             SPI_MASTER_FREQ_40M
#define RG_SCREEN_BACKLIGHT         1
#define RG_SCREEN_WIDTH             320
#define RG_SCREEN_HEIGHT            240
#define RG_SCREEN_ROTATE            0
#define RG_SCREEN_VISIBLE_AREA      {0, 0, 0, 0}
#define RG_SCREEN_SAFE_AREA         {0, 0, 0, 0}

/* Waveshare 2inch landscape. If still mirrored, try 0xA0, 0x60, 0xE0, 0x00. */
#define RG_SCREEN_INIT() \
    ILI9341_CMD(0x36, 0x70); \
    ILI9341_CMD(0xB2, 0x0C, 0x0C, 0x00, 0x33, 0x33); \
    ILI9341_CMD(0xB7, 0x35); \
    ILI9341_CMD(0xBB, 0x1F); \
    ILI9341_CMD(0xC0, 0x2C); \
    ILI9341_CMD(0xC2, 0x01); \
    ILI9341_CMD(0xC3, 0x12); \
    ILI9341_CMD(0xC4, 0x20); \
    ILI9341_CMD(0xC6, 0x0F); \
    ILI9341_CMD(0xD0, 0xA4, 0xA1); \
    ILI9341_CMD(0xE0, 0xD0, 0x08, 0x11, 0x08, 0x0C, 0x15, 0x39, 0x33, 0x50, 0x36, 0x13, 0x14, 0x29, 0x2D); \
    ILI9341_CMD(0xE1, 0xD0, 0x08, 0x10, 0x08, 0x06, 0x06, 0x39, 0x44, 0x51, 0x0B, 0x16, 0x14, 0x2F, 0x31); \
    ILI9341_CMD(0x21);

#define RG_GPIO_LCD_MISO            GPIO_NUM_13
#define RG_GPIO_LCD_MOSI            GPIO_NUM_11
#define RG_GPIO_LCD_CLK             GPIO_NUM_12
#define RG_GPIO_LCD_CS              GPIO_NUM_10
#define RG_GPIO_LCD_DC              GPIO_NUM_14
#define RG_GPIO_LCD_BCKL            GPIO_NUM_21
#define RG_GPIO_LCD_RST             GPIO_NUM_9

#define RG_GPIO_SDSPI_MISO          GPIO_NUM_13
#define RG_GPIO_SDSPI_MOSI          GPIO_NUM_11
#define RG_GPIO_SDSPI_CLK           GPIO_NUM_12
#define RG_GPIO_SDSPI_CS            GPIO_NUM_4

#define RG_GPIO_I2C_SDA             GPIO_NUM_17
#define RG_GPIO_I2C_SCL             GPIO_NUM_18

#define RG_GPIO_SND_I2S_BCK         41
#define RG_GPIO_SND_I2S_WS          42
#define RG_GPIO_SND_I2S_DATA        40
#define RG_GPIO_SND_AMP_ENABLE      8

#define RG_BATTERY_DRIVER           0

#define RG_GAMEPAD_I2C_MAP { \
    {RG_KEY_A, .num = 31, .level = 1}, \
}

#define RG_GAMEPAD_GPIO_MAP { \
    {RG_KEY_START,  .num = GPIO_NUM_5, .pullup = 1, .level = 0}, \
    {RG_KEY_SELECT, .num = GPIO_NUM_6, .pullup = 1, .level = 0}, \
}

#define RG_NULLLAB_JOY_ADDR         0x5A
#define RG_NULLLAB_JOY_DEAD         40
