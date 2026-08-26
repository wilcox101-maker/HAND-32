/* HAND-32 target overlay for Retro-Go (ducalex/retro-go).
 * Not a fork. Pins and panel init only.
 * Retro-Go (c) Alex Duchesne (@ducalex) and contributors, GPLv2.
 * https://github.com/ducalex/retro-go
 *
 * Hardware: HiLetgo ESP32-S3-DevKitC N16R8, Waveshare 2" ST7789T3
 * (shared SPI TF), NullLab I2C stick 0x5A, NS4168.
 */
#pragma once

#define RG_TARGET_NAME             "HILETGO-WS2-NS4168"

#define RG_STORAGE_ROOT             "/sd"
#define RG_STORAGE_SDSPI_HOST       SPI2_HOST
#define RG_STORAGE_SDSPI_SPEED      SDMMC_FREQ_PROBING

#define RG_AUDIO_USE_INT_DAC        0
#define RG_AUDIO_USE_EXT_DAC        1

#define RG_SCREEN_DRIVER            0
#define RG_SCREEN_HOST              SPI2_HOST
#define RG_SCREEN_SPEED             SPI_MASTER_FREQ_40M
#define RG_SCREEN_BACKLIGHT         1
#define RG_SCREEN_WIDTH             320
#define RG_SCREEN_HEIGHT            240
#define RG_SCREEN_ROTATE            0
#define RG_SCREEN_VISIBLE_AREA      {0, 0, 0, 0}
#define RG_SCREEN_SAFE_AREA         {0, 0, 0, 0}

#define ST7789_MADCTL               0x36
#define ST7789_MADCTL_MV            0x20
#define ST7789_MADCTL_RGB           0x00
#define ST7789_MADCTL_BGR           0x08

#define RG_SCREEN_INIT() \
    ILI9341_CMD(0xCF, 0x00, 0xc3, 0x30); \
    ILI9341_CMD(0xED, 0x64, 0x03, 0x12, 0x81); \
    ILI9341_CMD(0xE8, 0x85, 0x00, 0x78); \
    ILI9341_CMD(0xCB, 0x39, 0x2c, 0x00, 0x34, 0x02); \
    ILI9341_CMD(0xF7, 0x20); \
    ILI9341_CMD(0xEA, 0x00, 0x00); \
    ILI9341_CMD(0xC0, 0x1B); \
    ILI9341_CMD(0xC1, 0x12); \
    ILI9341_CMD(0xC5, 0x32, 0x3C); \
    ILI9341_CMD(0xC7, 0x91); \
    ILI9341_CMD(ST7789_MADCTL, (ST7789_MADCTL_MV | ST7789_MADCTL_BGR)); \
    ILI9341_CMD(0x21); \
    ILI9341_CMD(0xB1, 0x00, 0x10); \
    ILI9341_CMD(0xB6, 0x0A, 0xA2); \
    ILI9341_CMD(0xF6, 0x01, 0x30); \
    ILI9341_CMD(0xF2, 0x00); \
    ILI9341_CMD(0xE0, 0xD0, 0x00, 0x05, 0x0E, 0x15, 0x0D, 0x37, 0x43, 0x47, 0x09, 0x15, 0x12, 0x16, 0x19); \
    ILI9341_CMD(0xE1, 0xD0, 0x00, 0x05, 0x0D, 0x0C, 0x06, 0x2D, 0x44, 0x40, 0x0E, 0x1C, 0x18, 0x16, 0x19);

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

#define RG_NULLLAB_JOY_ADDR         0x5A
#define RG_NULLLAB_JOY_DEAD         40
