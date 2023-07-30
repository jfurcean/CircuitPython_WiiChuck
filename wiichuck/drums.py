# SPDX-FileCopyrightText: 2023 David Glaude + 2021 John Furcean (for Guitar original code)
# SPDX-License-Identifier: MIT

"""
`wiichuck.drums`
================================================================================

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


* Author(s): John Furcean and David Glaude

Implementation Notes
--------------------

**Hardware:**

* Guitar Hero World Tour (Wii) Drums
* `Adafruit Wii Nunchuck Breakout Adapter <https://www.adafruit.com/product/4836>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

** Drums/Bass positions

This code assume you connected the Yellow Cymbal on the left and the Orange Cymbal on the right.
If this is not the default/standard in game/library, we can adapt the library.

Physical setup assumed:
Yellow - Orange
Red - Blue - Green
Joystick - Minus- Plus
Bass

**Not implemented yet**
* "Softness" is how hard or soft you hit the pad. It ranges from 0 = Very hard to 6 = very soft,
#  with 7 = not hit at all == bits 7+6+5 of byte 3
* "HHP" is 0 if the velocity data is for the hi-hat pedal (unmarked 3.5mm jack above bass pedal jack),
#  and 1 otherwise.
* "Which" (another way to identify the presence or origin of the velocity data?)

See http://wiibrew.org/wiki/Wiimote/Extension_Controllers/Guitar_Hero_World_Tour_(Wii)_Drums
"""
from collections import namedtuple
from wiichuck import WiiChuckBase

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Nunchuk.git"


class Drums(WiiChuckBase):
    """
    Class which provides interface to Nintendo Wii Guitar Hero World Tour (Wii) Drums.

    :param i2c: The `busio.I2C` object to use.
    :param address: The I2C address of the device. Default is 0x52.
    :type address: int, optional
    :param i2c_read_delay: The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    :type i2c_read_delay: float, optional
    """

    _Values = namedtuple("Values", ("joystick", "buttons"))
    _Joystick = namedtuple("Joysticks", ("x", "y"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "orange",
            "red",
            "yellow",
            "green",
            "blue",
            "bass",
            "plus",
            "minus",
        ),
    )

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joystick(do_read=False),
            self._buttons(do_read=False),
        )

    @property
    def joystick(self):
        """The current joystick position."""
        return self._joystick()

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    def _joystick(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Joystick(
            self.buffer[0] & 0x3F,
            self.buffer[1] & 0x3F,
        )

    def _buttons(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Buttons(
            not bool(self.buffer[5] & 0x80),  # orange (right cymbals)
            not bool(self.buffer[5] & 0x40),  # red
            not bool(self.buffer[5] & 0x20),  # yellow (left cymbals)
            not bool(self.buffer[5] & 0x10),  # green
            not bool(self.buffer[5] & 0x8),  # blue
            not bool(self.buffer[5] & 0x4),  # bass
            not bool(self.buffer[4] & 0x4),  # plus
            not bool(self.buffer[4] & 0x10),  # minus
        )
