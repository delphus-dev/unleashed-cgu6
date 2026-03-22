#pragma once

#include <furi_hal_spi_types.h>

#ifdef __cplusplus
extern "C" {
#endif

/** Preset for ST25R916 */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_2edge_low_8m;

/** Preset for CC1101 */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_1edge_low_8m;

/** Preset for ST7567 (Display) */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_1edge_low_4m;

/** Preset for SdCard in fast mode */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_1edge_low_16m;

/** Preset for SdCard in slow mode */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_1edge_low_2m;

/** Preset for Button Shift Register (74HC165) */
extern const LL_SPI_InitTypeDef furi_hal_spi_preset_1edge_low_BTN;

/** Furi Hal Spi Bus (Single bus for all peripherals on SPI1) */
extern FuriHalSpiBus furi_hal_spi_bus;

/** CC1101 on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_subghz;

/** ST25R3916 on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_nfc;

/** External on `furi_hal_spi_bus`
 * Preset: `furi_hal_spi_preset_1edge_low_2m`
 * 
 * miso: pa6
 * mosi: pa7
 * sck: pb3
 * cs:  pa4 (software controlled)
 * 
 * @warning not initialized by default, call `furi_hal_spi_bus_handle_init` to initialize
 * Bus pins are floating on inactive state, CS high after initialization
 * 
 */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_external;

/** ST7567(Display) on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_display;

/** SdCard in fast mode on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_sd_fast;

/** SdCard in slow mode on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_sd_slow;

/** Button Shift Register on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_button_sr;

/** Extra external on `furi_hal_spi_bus` */
extern const FuriHalSpiBusHandle furi_hal_spi_bus_handle_external_extra;

#ifdef __cplusplus
}
#endif
