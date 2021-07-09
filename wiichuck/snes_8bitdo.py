# SPDX-FileCopyrightText: 2021 John Furcean

# SPDX-License-Identifier: MIT

"""
`wiichuck.8bitdo_snes`
================================================================================

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


* Author(s): John Furcean

Implementation Notes
--------------------

**Hardware:**

* `Adafruit Wii Nunchuck Breakout Adapter <https://www.adafruit.com/product/4836>`_
* `8BitDo Retro Receiver <https://www.8bitdo.com/retro-receiver-snes-sfc-classic>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""
from collections import namedtuple
from wiichuck import WiiChuckBase

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Nunchuk.git"


class SNES8BitDo(WiiChuckBase):
    """
    Class which provides interface to 8BitDo Retro Receiver.

    :param i2c: The `busio.I2C` object to use.
    :param address: The I2C address of the device. Default is 0x52.
    :type address: int, optional
    :param i2c_read_delay: The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    :type i2c_read_delay: float, optional
    """

    _Values = namedtuple("Values", ("buttons", "dpad"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "A",
            "B",
            "X",
            "Y",
            "R",
            "L",
            "start",
            "select",
        ),
    )
    _Dpad = namedtuple("Dpad", ("up", "down", "right", "left"))

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._buttons(do_read=False),
            self._dpad(do_read=False),
        )

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    @property
    def dpad(self):
        """The current pressed state of the dpad."""
        return self._dpad()

    def _buttons(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Buttons(
            not bool(self.buffer[7] & 0x10),  # A
            not bool(self.buffer[7] & 0x40),  # B
            not bool(self.buffer[7] & 0x8),  # X
            not bool(self.buffer[7] & 0x20),  # Y
            not bool(self.buffer[6] & 0x2),  # R
            not bool(self.buffer[6] & 0x20),  # L
            not bool(self.buffer[6] & 0x4),  # start
            not bool(self.buffer[6] & 0x10),  # select
        )

    def _dpad(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Dpad(
            not bool(self.buffer[7] & 0x1),  # UP
            not bool(self.buffer[6] & 0x40),  # DOWN
            not bool(self.buffer[6] & 0x80),  # RIGHT
            not bool(self.buffer[7] & 0x2),  # LEFT
        )
