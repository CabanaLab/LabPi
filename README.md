# LabPi
[![GitHub tag](https://img.shields.io/github/tag/CabanaLab/LabPi.svg?style=flat-square)](https://github.com/CabanaLab/LabPi/releases)

Scripts running on the Raspberry Pi in 4163SES.

## Installation
In the pi's /home/pi/ directory:

```bash
git clone git@github.com:CabanaLab/LabPi.git
```

### `empty.py`
Setup `empty.py` to run on startup in a headless commandline environment (no GUI). This script is designed to await input from a barcode scanner on a forever-loop. 

### `lcs_16x2.py`
Prints output to a [16x2 character LCD screen](https://www.adafruit.com/products/198). This item has been modified for the purposes here. [The original creator and file can be found here.](http://www.raspberrypi-spy.co.uk/)
