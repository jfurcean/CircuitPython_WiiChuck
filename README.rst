Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-wiichuck/badge/?version=latest
    :target: https://circuitpython-wiichuck.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/jfurcean/CircuitPython_WiiChuck/workflows/Build%20CI/badge.svg
    :target: https://github.com/jfurcean/CircuitPython_WiiChuck/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython driver for Nintento WiiMote I2C Accessory Devices


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.


Usage Example
=============

.. code-block:: python

    import time
    import board
    from wiichuck.nunchuk import Nunchuk

    nc = Nunchuk(board.I2C())

    while True:
        x, y = nc.joystick
        ax, ay, az = nc.acceleration
        print("joystick = {},{}".format(x, y))
        print("accceleration ax={}, ay={}, az={}".format(ax, ay, az))

        buttons = nc.buttons
        if buttons.C:
            print("button C")
        if buttons.Z:
            print("button Z")
        time.sleep(0.5)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/jfurcean/CircuitPython_WiiChuck/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
