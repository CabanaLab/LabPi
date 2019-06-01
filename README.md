# LabPi
[![GitHub tag](https://img.shields.io/github/tag/CabanaLab/LabPi.svg?style=flat-square)](https://github.com/CabanaLab/LabPi/releases)

Scripts running on the Raspberry Pi in 4163SES.

## Installation
In the pi's /home/pi/ directory:

```bash
$ git clone git@github.com:CabanaLab/LabPi.git
$ pip install -e LabPi/
```

### `run-empty`
Setup `empty.py` to run on startup in a headless commandline environment (no GUI). This script is designed to await input from a barcode scanner on a forever-loop. 

### `lcd_16x2.py`
Prints output to a [16x2 character LCD screen](https://www.adafruit.com/products/198). This item has been modified for the purposes here. [The original creator and file can be found here.](http://www.raspberrypi-spy.co.uk/)

## Configuration

Create a file in the LabPi/labpi directory title ``LOCALSETTINGS.py``
with installation specific variables.

- **ulon_url** - Base REST url (with trailing slash) for accessing
    ULONS. It will have the ULON ID appended.
- **base_url** - Base REST url (with trailing slash) for accessing
    containers. It will have the container ID appended.
- **username** - Username for logging into the professor_oak server.
- **password** - Password for logging into the professor_oak server.

## Usage

Connect the barcode reader to the PI, then execute ``run-empty`` from
the command line.
