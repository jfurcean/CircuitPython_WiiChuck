# SPDX-FileCopyrightText: Copyright (c) 2023 David Glaude + 2021 John Furcean (for Guitar original code)
#
# SPDX-License-Identifier: MIT
import board
from wiichuck.drums import Drums

drums = Drums(board.I2C())

while True:

    joystic, buttons = drums.values

    # Joystick: (0-63,0-63), middle is (32,32)
    if joystic != (31, 32):  # My joystic is sending 31,32
        print(f"Joystick (x,y): {joystic}")

    # Drums and Pedal Buttons
    if buttons.orange:
        print("Button Pressed: ORANGE")
    if buttons.blue:
        print("Button Pressed: BLUE")
    if buttons.yellow:
        print("Button Pressed: YELLOW")
    if buttons.red:
        print("Button Pressed: RED")
    if buttons.green:
        print("Button Pressed: GREEN")
    if buttons.bass:
        print("Button Pressed: BASS (Pedal)")
    if buttons.plus:
        print("Button Pressed: PLUS")
    if buttons.minus:
        print("Button Pressed: MINUS")
