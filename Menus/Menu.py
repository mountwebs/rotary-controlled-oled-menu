import os

from Adafruit import SSD1306
from RPi import GPIO
from PIL import Image, ImageDraw, ImageFont


class Menu:

    def __init__(self, options):
        self.options = options
        self.highlightOption = None
        self.rowCount = 3

        self.oled = SSD1306.SSD1306_128_32(rst=None, gpio=GPIO)
        self.oled.begin()
        self.oled.clear()
        self.oled.display()

        self.image = Image.new('1', (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(os.path.dirname(__file__) + '/pixel_arial_11.ttf', 8)

    def blank(self, draw=False):
        self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        if draw:
            self.oled.image(self.image)
            self.oled.display()

    def render(self, highlight=None):
        self.blank()
        self.__build(highlight)
        self.oled.image(self.image)
        self.oled.display()

    def __build(self, highlight):
        # sanity check the highlight value
        if highlight is None:
            self.highlightOption = None
        elif highlight < 0:
            self.highlightOption = 0
        elif highlight >= len(self.options):
            self.highlightOption = len(self.options) - 1
        else:
            self.highlightOption = highlight

        # adjust the start/end positions of the range
        if self.highlightOption >= (len(self.options) - self.rowCount):
            end = len(self.options)
            start = end - self.rowCount
        elif self.highlightOption is None or self.highlightOption <= self.rowCount:
            start = 0
            end = start + self.rowCount
        else:
            start = self.highlightOption
            end = start + self.rowCount

        # draw the menu options
        top = 0
        for x in range(start, end):
            fill = 1
            if self.highlightOption is not None and self.highlightOption == x:
                at_row_height = 0 if top == 0 else top
                self.draw.rectangle([0, at_row_height, self.oled.width, at_row_height + 11], outline=0, fill=1)
                fill = 0
            self.draw.text((3, top + 1), self.options[x], font=self.font, fill=fill)
            top += 10
