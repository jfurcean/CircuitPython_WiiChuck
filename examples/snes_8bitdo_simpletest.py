# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

import board
import time
from wiichuck.snes_8bitdo import SNES8BitDo

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# controller = SNES8BitDo(i2c)

controller = SNES8BitDo(board.I2C)

while True:
    buttons, dpad = controller.values

    if buttons.A:
        print("button A")
    if buttons.B:
        print("button B")
    if buttons.X:
        print("button X")
    if buttons.Y:
        print("button Y")
    if buttons.R:
        print("button R")
    if buttons.L:
        print("button L")

    if buttons.start:
        print("button start")
    if buttons.select:
        print("button select")

    if dpad.up:
        print("dpad up")
    if dpad.down:
        print("dpad down")
    if dpad.right:
        print("dpad right")
    if dpad.left:
        print("dpad left")
