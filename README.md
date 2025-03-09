# 74th の使う KiCad Parts

- symbols: KiCad のシンボル
- footprints: KiCad のフットプリント
- 3d-models: ダウンロードした 3D モデルを置くディレクトリ
- pcb-default: 基板の設定の標準データ。最初にインポートして使う

## 他によく使う KiCad Parts

- Espressif KiCad Library https://github.com/espressif/kicad-libraries

## あるもの（一例）

### シンボル

- 74th_ApplicationIC
  - CH224K: USB PD Sink Controller
  - CH334R: USB2.0 Hub Controller
  - CH340C, CH340G, CH340X: USB UART
  - CH9329: USB to USBHID Keyboard/Mouse
  - W25Q32JVSS, W25Q32JVUU: Flash
- 74th_Board
  - M5Stack Core2 M-BUS
- 74th_Display
  - OSL01561-LW: 7seg LED
  - I2C OLED Module
- 74th_Interface
  - AudioJack_4_TRRS
  - ESP-Prog_ProgramCOM_Recv
  - Grove Device-Side/Host-Side
  - I2C Breakout
  - I2C Grove Device-Side/Host-Side
  - JoyStick b10k
  - Jumper 2/3
  - Pin 1~20
  - Pin 4 PokaYoke
  - Pin 2 GND
  - ProMicro Left/Right/Left-NoGND
  - Qwiic DeviceSide/HostSide
  - RaspberryPiPico PinOut
  - SWD 3Pin
  - SWD 10Pin Debuger-Side/MCU-Side
  - SWD WCH 1Wire/With VCC/With TXD-VCC
  - SWD LinkE header
  - SW Push
  - SW Push Pin-4
  - SW Slide
  - UART Grove Device-Side/Host-Side
  - UART TX
  - USB TypeA 2.0 Plug
  - USB TypeA 2.0 Receptacle
  - USB TypeC 2.0 Plug
  - USB TypeC 2.0 Receptacle
  - USB TypeC 2.0 Receptacle Simple
  - USB TypeC 3.0 Plug
  - USB TypeC 3.0 Plug 24Pin
- 74th_MCU
  - CH32V002F4P6/F4U6/J4M6
  - CH32V003F4P6/F4U6/J4M6
  - CH32V006K8U6
  - CH32V203CxT6/F6T6
  - CH32V305FBP6
  - CH32X035G8U6
  - RP2040
  - RP2350A
  - RP2350B
  - STM32F103C8T6
  - STM32G030F6P6
- 74th_Passive
  - AMS117-3.3: Regulator
  - AP7333-LDO: Regulator
  - CH213K: USB電源保護IC
  - CH217K: USB電源保護IC
  - IRLM6402: Pch MOSFET
  - MT2492: DCDC Converter
  - SK6812MINI-E : RGB LED
  - MT2492: DCDC COnverter
- 74th_PassiceCommon
  - Crystal_GND24
  - L Directed
  - MOSFET Dural Pch

### footprint

- BatteryHolder CR2034
- Basic
  - Capacitor 0402in_1005M/0603in_1608M/0805in_2012M/1206_3216M
  - Capacitor 0603in_1608M/0805in_2012M WithSizeText
  - Register 0402in_1005M/0603in_1608M/0805in_2012M/1206_3216M
  - Register 0603in_1608M/0805in_2012M WithSizeText
  - Inductor 4.1x4.5mm
  - Inductor 0806in 2016M
- Connector
  - BoxPinHeader 2x03 P1.27 (ESP-Prog)
  - BoxPinHeader 2x05 P1.27 (SWD)
  - Grove or Qwiic Socket
  - HY-2.0 SMD 4Pin/TH-Surface 4Pin/TH Versical 4Pin
  - HalfPinHeader SWD
  - MJ-4PP-9 (TRRSジャック)
  - PH-2.0
  - SH-1.0 SMD 2Pin/4Pin(Qwiic)
  - USB-A Plug TH
  - USB-A Receptacle SMT 4-Pin
  - USB-C Plug 2.0 for 24 Pin
  - USB-C Plug 2.0 24Pin
  - USB-C Receptacle SMT 12-PIn Midmount
  - USB-C Receptacle SMT 12-PIn Midmount Simple
  - USB-C Receptacle SMT 12-PIn Simple
  - USB-Micro Plug SMD
  - USB3-A-Receptacle SMT 9-Pin
- Crystal
  - SMD 2012 2-Pin 2.0x1.2mm HandSoldering
  - SMD 2012 2-Pin 3.2x1.5mm
  - SMD 2012 4-Pin 3.2x1.5mm HandSoldering
- Display
  - OSL10561-LW
- Hole
  - M1.6
  - M2
  - M5Dial/M5Dial Stopper
  - M5StackCore2
  - OLED 0.96inch
- LED
  - 0805in_2016M
  - Reverse Mount 0805in_2016M
  - SK6812MINI-E back side light
  - SK6812MINI-E silk side light
- Mousebite
- Package
  - Fuse 1812in 4532m
  - LQFP-48 7x7mm P0.5 EP1.7x1.7mm
  - QFN-20-1EP 3x3mm P0.5 EP2.6x2.6mm Handsolder
  - QFN-24-1EP 4x4mm P0.4 EP2.8x2.8mm Handsolder
  - QFN-28-1EP 4x4mm P0.4 EP2.7x2.7mm
  - QFN-32-1EP 4x4mm P0.4 EP2.7x2.7mm
  - QFN-32-1EP 4x4mm P0.4 EP2.7x2.7mm Handsolder
  - QFN-54-1EP 7x7mm P0.4 EP3.1x3.1mm Handsolder
  - QFN-60-1EP 7x7mm P0.4 EP3.4x3.4mm Handsolder
  - QFN-80-1EP 10x10mm P0.4 EP3.4x3.4mm Handsolder
  - SOD23 Diode
  - SOD23 Diode No-Reference
  - SOD123W
  - SOIC-8 3.9x4.9mm P1.27mm
  - SOIC-8 3.25x5.23mm P1.27mm
  - SOIC-16 3.8x8.8mm P1.27mm
  - SOT-23
  - SOT-23-5
  - SOT-23-6
  - SOT-89-3
  - SOT233-3
  - TSSOP-20 4.4x6.5mm P0.65mm
  - USON-8 3.4mm P0.8mm
- Pad 1/4
- PinOut
  - Pin 1~20
  - PokeYoke
  - Raspberry Pi Pico
  - ProMicro LIKE LEFT/RIGHT
- SolderJumper-2/3
- Switch
  - MXChocSwap 1Side 1.0u
  - MXChoc 1.0u
  - MXSwapChoc 1.0u
  - MXSwap 1.0u
  - MXSwap 1.25u
  - SKRPABE010
  - SK-12D02-G020
  - TactileSwitch4Foot 6x6

## LICENSE

明記のないものは CC0 (Creative Commons Public License) とします。

いくつかのパーツは KiCad ライブラリーからコピーして使っています。それぞれのディレクトリの README を参照してください。

## Links

- 74thのOpen Source Hardwareのプロジェクト https://github.com/74th/74th-open-source-hardware-projects
