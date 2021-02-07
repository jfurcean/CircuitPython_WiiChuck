# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

# Classic Controller also work with CLV-202.
# But the "Super Nintendo SNES Classic Mini Controller" has less button and not stick.

import board
from wiichuck.classic_controller import ClassicController

controller = ClassicController(board.I2C())

while True:
    _, buttons, dpad, _ = controller.values

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
