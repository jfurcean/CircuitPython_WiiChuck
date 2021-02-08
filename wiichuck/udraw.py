# SPDX-FileCopyrightText: 2021 David Glaude
#
# SPDX-License-Identifier: MIT

"""
`wiichuck.udraw`
================================================================================

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


* Author(s): David Glaude

Implementation Notes
--------------------

**Hardware:**

* `Wii Remote Nunchuk <https://en.wikipedia.org/wiki/Wii_Remote#Nunchuk>`_
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


class UDraw(WiiChuckBase):
    """
    Class which provides interface to Nintendo Nunchuk controller.

    :param i2c: The `busio.I2C` object to use.
    :param address: The I2C address of the device. Default is 0x52.
    :type address: int, optional
    :param i2c_read_delay: The time in seconds to pause between the
        I2C write and read. This needs to be at least 200us. A
        conservative default of 2000us is used since some hosts may
        not be able to achieve such timing.
    :type i2c_read_delay: float, optional
    """

    _Values = namedtuple("Values", ("position", "buttons", "pressure"))
    _Position = namedtuple("Position", ("x", "y"))
    _Buttons = namedtuple("Buttons", ("tip", "C", "Z"))
    _Pressure = namedtuple("Pressure", ("pressure"))

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._position(do_read=False),
            self._buttons(do_read=False),
            self._pressure(do_read=False),
        )

    @property
    def position(self):
        """The current pen tip position."""
        return self._position()

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    @property
    def pressure(self):
        """The current pressure reading."""
        return self._pressure()

    def _position(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Position(
            ((self.buffer[2] & 0x0F) << 8 | self.buffer[0]),  # x
            ((self.buffer[2] & 0xF0) << 4 | self.buffer[1]),  # y
        )

    def _buttons(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Buttons(
            bool((self.buffer[5] & 0x04) >> 2),  # tip
            not bool((self.buffer[5] & 0x02) >> 1),  # C
            not bool(self.buffer[5] & 0x01),  # Z
        )

    def _pressure(self, do_read=True):
        if do_read:
            self._read_data()
        return self.buffer[3]
