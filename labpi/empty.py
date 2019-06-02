"""Used in conjunction with https://github.com/m3wolf/professor_oak
(Professor Oak Lab Management System). Script to run on a Raspberry Pi
that will send a HTTPrequest to the main inventory server to mark a
certain container_id as empty and output a success/failure message to a GPIO LCD
display. Questions? Comments? email michael.plews@gmail.com"""

# Setup logging
import logging
logging.basicConfig(filename='labpi.log', level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger('emptypi')
logging.getLogger("requests").setLevel(logging.WARNING)

import re
import datetime
import requests
import json
import configparser
import os

import labpi.lcd


# Variables
barcode_digit_length = 6


def load_config(configfile='~/labpi.conf'):
    """Create a configuration from a .conf file.
    
    Returns
    =======
    config : configparser.ConfigParser
      The configuration loaded from disk.
    
    """
    # Create a default configuration
    config = configparser.ConfigParser()
    config.read_dict({
        'server': {
            'username': '',
            'password': '',
            'base_url': 'http://example.com/container/{id}'
        },
        'pi': {
            'lcd_panel': 'dummy',
        }
    })
    # Load the configuration from disk
    config.read(os.path.expanduser(configfile))
    return config


def lcd_factory(panel_name):
    panels = {
        'i2c_rgb': labpi.lcd.I2CRGBLCD,
        'gpio': labpi.lcd.GPIOLCD,
        'dummy': labpi.lcd.BaseLCD,
    }
    LCD = panels[panel_name]
    return LCD()


def login():
    config = load_config()
    username = config['server']['username']
    password = config['server']['password']
    auth = requests.auth.HTTPBasicAuth(username, password)
    log.debug("Logged in with user %s", username)
    return auth


def validate(input):
    """Check that the input specified is a container barcode.
    
    Returns
    -------
    is_valid : bool
      True if the input is a valid barcode ID, False otherwise.
    
    """
    regex = re.compile(r'(UL)?\d{1,' + re.escape(str(barcode_digit_length)) + '}$', flags=re.IGNORECASE)
    if regex.match(input):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def check_if_empty(id_number):
    # Stubbed for development
    raise NotImplementedError()


def mark_as_empty(id_number):
    """Hit the server and tell it the this container is now empty."""
    base_url = load_config()['server']['base_url']
    url = base_url.format(id=id_number)
    log.debug("Url is '%s'", url)
    payload = {
        'is_empty': True,
        }
    log.debug('Payload is %s', str(payload))
    auth = login()
    
    r = requests.patch(url, json=payload, auth=auth)
    log.debug("Received response status code: %s", r.status_code)
    log.debug("Received response text: %s", r.text)
    
    r = requests.patch(url, json=payload, auth=auth)
    return r.status_code


def process_input(lcd, server):
    lcd.GPIO.cleanup()
    lcd.lcd_init()
    lcd.lcd_string("Ready:", lcd.LCD_LINE_1)
    barcode = str(input('input:'))
    log.debug("Input received: %s", barcode)
    if barcode == 'EXIT':
        log.info("Received 'EXIT' signal. Exiting.")
        exit()
    if validate(barcode):
        barcode = barcode.lstrip('0')
        # Send the request to the server
        msg = "Container {}:\nSending...".format(barcode)
        lcd.print_message(msg, lcd.C_WARNING)
        status_return = server.mark_as_empty(barcode)
        barcode_string = str(barcode).zfill(barcode_digit_length)
        log.info("ID# %s %s", str(barcode).zfill(barcode_digit_length), status_return)
        # Handle the return status code
        if status_return == 200:
            msg = "Container {}:\nMarked as Empty!".format(barcode)
            lcd.print_message(msg, lcd.C_SUCCESS)
        elif status_return == 404:
            log.error("Container %s 404.", barcode)
            msg = "Container {}:\nNot Found!".format(barcode)
            lcd.print_message(msg, lcd.C_ERROR)
        else:
            msg = "Container {}:\nError! ({})".format(barcode, status_return)
            lcd.print_message(msg, lcd.C_ERROR)
    else:
        # Invalid barcode, so let the user know
        log.warning("Invalid input: %s", barcode)
        lcd.lcd_string("Invalid", lcd.LCD_LINE_1)
    lcd.GPIO.cleanup()
    lcd.time.sleep(2)


def main():
    lcd = lcd_factory(load_config()['pi']['lcd_panel'])
    try:
        while True:
            process_input(lcd=lcd)
    except (KeyboardInterrupt, SystemExit):
        lcd.print_message("Goodbye!", lcd.C_INFO)
        lcd.exit()
        exit()


if __name__ == "__main__":
    main()
