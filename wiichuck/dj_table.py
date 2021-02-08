# SPDX-FileCopyrightText: 2021 John Furcean

# SPDX-License-Identifier: MIT

"""
`wiichuck.dj_table`
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


class DJTable(WiiChuckBase):
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
        "Values", ("joystick", "buttons", "turntables", "dial", "slider")
    )
    _Joystick = namedtuple("Joysticks", ("x", "y"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "euphoria",
            "start",
            "select",
            "plus",
            "minus",
        ),
    )
    _Turntables = namedtuple("Turntables", ("right", "left"))
    _Turntable = namedtuple("Turntable", ("value", "green", "red", "blue"))

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joystick(do_read=False),
            self._buttons(do_read=False),
            self._turntables(do_read=False),
            self._dial(do_read=False),
            self._slider(do_read=False),
        )

    @property
    def joystick(self):
        """The current joystick position."""
        return self._joystick()

    @property
    def buttons(self):
        """The current pressed state of all buttons that are not on the turntable."""
        return self._buttons()

    @property
    def turntables(self):
        """The current reading from the turntable and it's buttons."""
        return self._turntables()

    @property
    def dial(self):
        """The current dial position."""
        return self._dial()

    @property
    def slider(self):
        """The current slider position."""
        return self._slider()

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
            not bool(self.buffer[5] & 0x10),  # euphoria
            not bool(self.buffer[4] & 0x4),  # start
            not bool(self.buffer[4] & 0x10),  # select
            not bool(self.buffer[4] & 0x4),  # plus
            not bool(self.buffer[4] & 0x10),  # minus
        )

    def _turntables(self, do_read=True):
        if do_read:
            self._read_data()

        rtt = (self.buffer[0] & 0xC0) >> 3
        rtt |= (self.buffer[1] & 0xC0) >> 5
        rtt |= (self.buffer[2] & 0x80) >> 7
        if self.buffer[2] & 0x1:
            rtt = rtt * -1

        ltt = self.buffer[3] & 0x1F
        if self.buffer[4] & 0x1:
            ltt = ltt * -1

        return self._Turntables(
            self._Turntable(
                rtt,
                not bool(self.buffer[5] & 0x20),  # green
                not bool(self.buffer[4] & 0x2),  # red
                not bool(self.buffer[5] & 0x4),  # blue
            ),
            self._Turntable(
                ltt,
                not bool(self.buffer[5] & 0x8),  # green
                not bool(self.buffer[4] & 0x20),  # red
                not bool(self.buffer[5] & 0x80),  # blue
            ),
        )

    def _dial(self, do_read=True):
        if do_read:
            self._read_data()
        return ((self.buffer[2] & 0x60) >> 2) | ((self.buffer[3] & 0xE0) >> 5)

    def _slider(self, do_read=True):
        if do_read:
            self._read_data()
        return (self.buffer[2] & 0x1E) >> 1
