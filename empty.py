"""Used in conjunction with https://github.com/m3wolf/professor_oak
(Professor Oak Lab Management System). Script to run on a Raspberry Pi
that will send a HTTPrequest to the main inventory server to mark a
certain container_id as empty and output a success/failure message to a GPIO LCD
display. Questions? Comments? email michael.plews@gmail.com"""

import re, datetime, requests, json, LOCALSETTINGS as localsettings, lcd_16x2 as lcd

import logging

# Setup logging
logging.basicConfig(filename='~/labpi.log', level=logging.INFO, mode="r+", format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
log = logging.getLogger('emptypi')
logging.getLogger("requests").setLevel(logging.WARNING)

# Variables
barcode_digit_length = 6

ulon_url = localsettings.ulon_url
base_url = localsettings.base_url
username = localsettings.username
password = localsettings.password


def login():
    auth = requests.auth.HTTPBasicAuth(username, password)
    log.debug("Logged in with user %s", username)
    return auth
 

def validate(input):
    """Check that the input specified is either a container barcode or ULON barcode.

    Returns
    -------
    - is_valid : bool
      True if the input is a valid barcode ID, False otherwise.
      """
    regex = re.compile(r'(UL)?\d{1,' + re.escape(str(barcode_digit_length)) + '}$', flags=re.IGNORECASE)
    if regex.match(input):
        is_valid = True
    else:
        is_valid = False
    return is_valid


def send_notification(id_number, note_type):
    """Ask the server to notify the user that the ULON has been
    removed."""
    auth = login()  
    if note_type == 'ULON':
        url = ulon_url + str(id_number)
        r = requests.get(url, auth=auth)
    return r.status_code


def check_if_empty(id_number):
    # Stubbed for development
    raise NotImplementedError()


def mark_as_empty(id_number):
    """Hit the server and tell it the this container is now empty."""
    url = base_url + str(id_number)
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


if __name__ == "__main__":
    lcd.lcd_init()
    lcd.lcd_string("Welcome", lcd.LCD_LINE_1, "c")
    lcd.lcd_string("to LabPi", lcd.LCD_LINE_2, "c")
    lcd.GPIO.cleanup()
    lcd.time.sleep(3)
    while True:
        try:
            lcd.GPIO.cleanup()
            lcd.lcd_init()
            lcd.lcd_string("Ready:", lcd.LCD_LINE_1)
            barcode = str(input('input:'))
            log.debug("Input received: %s", barcode)
            if barcode == 'EXIT':
                log.info("Received 'EXIT' signal. Exiting.")
                exit()
            if validate(barcode):
                lcd.lcd_string("Recieved:", lcd.LCD_LINE_1)
                lcd.lcd_string(barcode, lcd.LCD_LINE_2)
                if barcode[:2] == 'UL':
                    lcd.lcd_string("Sending...", lcd.LCD_LINE_1)
                    status_return = send_notification(barcode[2:], note_type='ULON')
                    barcode_string = str(barcode)
                    log.info("ULON# %s %s", str(barcode).zfill(barcode_digit_length), status_return)
                    if status_return == "200":
                        lcd.lcd_string("Email Sent!", lcd.LCD_LINE_1)
                    else:
                        lcd.lcd_string("Error!", lcd.LCD_LINE_1)
                else:
                    lcd.lcd_string("Sending...", lcd.LCD_LINE_1)
                    status_return = mark_as_empty(barcode)
                    barcode_string = str(barcode).zfill(barcode_digit_length)
                    log.info("ID# %s %s", str(barcode).zfill(barcode_digit_length), status_return)
                    if status_return == 200:
                        lcd.lcd_string("Marked as Empty!", lcd.LCD_LINE_1)
                    elif status_return == 404:
                        lcd.lcd_string("Not Found!", lcd.LCD_LINE_1)
                    else:
                        lcd.lcd_string("Error!", lcd.LCD_LINE_1)
            else:
                log.warning("Invalid input: %s", barcode)
                lcd.lcd_string("Invalid", lcd.LCD_LINE_1)
            lcd.GPIO.cleanup()
            lcd.time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            lcd.lcd_string("Goodbye!",lcd.LCD_LINE_1, "c")
            lcd.time.sleep(1)
            lcd.GPIO.cleanup()
            lcd.lcd_init()
            exit()
