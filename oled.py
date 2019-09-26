# import machine
# import ssd1306
# i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
# oled = ssd1306.SSD1306_I2C(128, 32, i2c)

import machine, ssd1306
import time
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
#oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
# oled.fill(0)
# oled.text("Hello World", 0, 0)
# oled.text("Hello World 2", 0, 10)
# oled.show()

oled.fill(0)
# oled.setTextSize(3)
oled.text('MicroPython on', 0, 0)
oled.text('an ESP8266 with an', 0, 10)
oled.text('attached SSD1306', 0, 20)
oled.text('OLED display', 0, 30)
oled.show()

time.sleep(5)
oled.invert(1)
time.sleep(5)
oled.poweroff()


# oled.rect(5, 5, 100, 20, 1)
# oled.show()
# oled.scroll(-10, 0)

# import urandom

# ICON = [
#     [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
#     [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
#     [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
#     [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
#     [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
#     [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
#     [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
# ]


# def random_heart():
#     xofs = urandom.getrandbits(8)
#     yofs = urandom.getrandbits(5)
#     for y, row in enumerate(ICON):
#         for x, c in enumerate(row):
#             oled.pixel(x + xofs, y + yofs, c)

# for n in range(100):
#     random_heart()
# oled.show()