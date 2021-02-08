# SPDX-FileCopyrightText: 2021 John Furcean

# SPDX-License-Identifier: MIT

"""
`wiichuck.guitar`
================================================================================

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


* Author(s): John Furcean

Implementation Notes
--------------------

**Hardware:**

* `Wiichuck <https://www.adafruit.com/product/342>`_
* `Adafruit Wii Nunchuck Breakout Adapter <https://www.adafruit.com/product/4836>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
from collections import namedtuple
from wiichuck import WiiChuckBase

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Nunchuk.git"


class Guitar(WiiChuckBase):
    """
    Class which provides interface to Nintendo Wii Classic Controller.

    :param i2c: The `busio.I2C` object to use.
    :param address: The I2C address of the device. Default is 0x52.
    :type address: int, optional
    :param i2c_read_delay: The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    :type i2c_read_delay: float, optional
    """

    _Values = namedtuple(
        "Values", ("joystick", "buttons", "strum", "whammy", "touchbar")
    )
    _Joystick = namedtuple("Joysticks", ("x", "y"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "orange",
            "blue",
            "yellow",
            "red",
            "green",
            "start",
            "select",
            "plus",
            "minus",
        ),
    )
    _Strum = namedtuple("Strum", ("up", "down"))

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joystick(do_read=False),
            self._buttons(do_read=False),
            self._strum(do_read=False),
            self._whammy(do_read=False),
            self._touchbar(do_read=False),
        )

    @property
    def joystick(self):
        """The current joystick position."""
        return self._joystick()

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    @property
    def strum(self):
        """The current pressed state of strum.up and strum.down."""
        return self._strum()

    @property
    def whammy(self):
        """The current whammy position."""
        return self._whammy()

    @property
    def touchbar(self):
        """The current touchbar position. Only available in the Guitar Hero World Tour Guitars"""
        return self._touchbar()

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
            not bool(self.buffer[5] & 0x80),  # orange
            not bool(self.buffer[5] & 0x20),  # blue
            not bool(self.buffer[5] & 0x8),  # yellow
            not bool(self.buffer[5] & 0x40),  # red
            not bool(self.buffer[5] & 0x10),  # green
            not bool(self.buffer[4] & 0x4),  # start
            not bool(self.buffer[4] & 0x10),  # select
            not bool(self.buffer[4] & 0x4),  # plus
            not bool(self.buffer[4] & 0x10),  # minus
        )

    def _strum(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Strum(
            not bool(self.buffer[5] & 0x1),  # up
            not bool(self.buffer[4] & 0x40),  # down
        )

    def _touchbar(self, do_read=True):
        if do_read:
            self._read_data()
        return self.buffer[2] & 0x1F

    def _whammy(self, do_read=True):
        if do_read:
            self._read_data()
        return self.buffer[3] & 0x1F
