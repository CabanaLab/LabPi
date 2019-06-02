import logging
log = logging.getLogger(__name__)


class BaseLCD():
    def __init__(self):
        raise NotImplementedError()
    
    def print_message(self, msg, color):
        raise NotImplementedError()


class I2CRGBLCD(BaseLCD):
    pass


class GPIOLCD(BaseLCD):
    def __init__(self):
        from labpi import lcd_16x2
        self._lcd = lcd_16x2
        self._lcd.lcd_init()
        self._lcd.GPIO.cleanup()
    
    def print_message(self, msg, color):
        line0, line1 = msg.split('\n')[:2]
        self._lcd.lcd_string(line0, self._lcd.LCD_LINE_1)
        self._lcd.lcd_string(line1, self._lcd.LCD_LINE_2)
    
    def exit(self):
        self._lcd.GPIO.cleanup()
