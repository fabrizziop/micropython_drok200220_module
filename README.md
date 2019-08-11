# micropython_drok200220_module
Module for DROK 200220 control, tested on an ESP32/microPython1.11

Made with the info collected at:
https://www.droking.com/cs/support/topic/200220-dc-dc-buck-converter-uart/

The module communicates through UART on the ESP32. When any write command is issued, the module expects the correct reply from the DC buck converter, and it also issues the corresponding read command, reading back the written values, to verify them. If an error is detected, the module tries multiple times (configurable), and when reaching the retry limit, an exception is thrown.

The Lock/Load data/Save data commands are NOT implemented, because they aren't useful for me.
