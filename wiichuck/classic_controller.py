# SPDX-FileCopyrightText: 2021 John Furcean

# SPDX-License-Identifier: MIT

"""
`wiichuck.classic_controller`
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


_THIRD_PARTY_SIGNATURE = bytearray((0x00, 0x00))


class ClassicController(WiiChuckBase):
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

    _Values = namedtuple("Values", ("joysticks", "buttons", "dpad", "triggers"))
    _Joysticks = namedtuple("Joysticks", ("rx", "ry", "lx", "ly"))
    _Buttons = namedtuple(
        "Buttons",
        (
            "A",
            "B",
            "X",
            "Y",
            "R",
            "L",
            "ZR",
            "ZL",
            "start",
            "select",
            "home",
            "plus",
            "minus",
        ),
    )
    _Dpad = namedtuple("Dpad", ("up", "down", "right", "left"))
    _Triggers = namedtuple("Trigers", ("right", "left"))

    def __init__(self, i2c, address=0x52, i2c_read_delay=0.002):
        super().__init__(i2c, address=address, i2c_read_delay=i2c_read_delay)

    @property
    def values(self):
        """The current state of all values."""
        self._read_data()
        return self._Values(
            self._joysticks(do_read=False),
            self._buttons(do_read=False),
            self._dpad(do_read=False),
            self._triggers(do_read=False),
        )

    @property
    def joysticks(self):
        """The current joysticks positions."""
        return self._joysticks()

    @property
    def buttons(self):
        """The current pressed state of all buttons."""
        return self._buttons()

    @property
    def dpad(self):
        """The current pressed state of the dpad."""
        return self._dpad()

    @property
    def triggers(self):
        """The current readding from the triggers (0-31 for Pro) (0 or 31 non-Pro)."""
        return self._triggers()

    def _joysticks(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Joysticks(
            (
                (self.buffer[0] & 0xC0) >> 3
                | (self.buffer[1] & 0xC0) >> 5
                | (self.buffer[2] & 0x80) >> 7
            ),  # rx
            self.buffer[2] & 0x1F,  # ry
            self.buffer[0] & 0x3F,  # lx
            self.buffer[1] & 0x3F,  # ly
        )

    def _buttons(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Buttons(
            not bool(self.buffer[5] & 0x10),  # A
            not bool(self.buffer[5] & 0x40),  # B
            not bool(self.buffer[5] & 0x8),  # X
            not bool(self.buffer[5] & 0x20),  # Y
            not bool(self.buffer[4] & 0x2),  # R
            not bool(self.buffer[4] & 0x20),  # L
            not bool(self.buffer[5] & 0x4),  # ZR
            not bool(self.buffer[5] & 0x80),  # ZL
            not bool(self.buffer[4] & 0x4),  # start
            not bool(self.buffer[4] & 0x10),  # select
            not bool(self.buffer[4] & 0x8),  # home
            not bool(self.buffer[4] & 0x4),  # plus
            not bool(self.buffer[4] & 0x10),  # minus
        )

    def _dpad(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Dpad(
            not bool(self.buffer[5] & 0x1),  # UP
            not bool(self.buffer[4] & 0x40),  # DOWN
            not bool(self.buffer[4] & 0x80),  # RIGHT
            not bool(self.buffer[5] & 0x2),  # LEFT
        )

    def _triggers(self, do_read=True):
        if do_read:
            self._read_data()
        return self._Triggers(
            self.buffer[3] & 0x1F,  # right
            (self.buffer[2] & 0x60) >> 2 | (self.buffer[3] & 0xE0) >> 5,  # left
        )

    def _read_data(self):
        """Overides the ``_read_data()`` function.

        Checks to see if the data looks like it is comming from a thrid party remote
        and modifies it.
        """

        super()._read_data()

        if self._check_third_party():
            self.buffer[4] = self.buffer[6]
            self.buffer[5] = self.buffer[7]
        return self.buffer

    def _check_third_party(self):
        """Checks if it is a thrid party controller.

        Some third party NES/SNES devices do not work properly with decryption enabled and the
        correct button information is stored in bytes 7 and 8. All ones are stored in
        bytes 4 and 5. Therefore, if the data in bytes 4 and 5 look like all buttons are
        pressed (all 0s), then it is safe to assume this is a thrid party remote.
        """
        return self.buffer[4:6] == _THIRD_PARTY_SIGNATURE
