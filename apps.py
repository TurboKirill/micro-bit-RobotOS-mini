from microbit import accelerometer, temperature, button_b, sleep

def run_gsensor(oled):
    button_b.was_pressed()
    while True:
        ax = accelerometer.get_x()
        ay = accelerometer.get_y()
        oled.fill(0)
        oled.fill_rect(0, 0, 128, 11, 1)
        oled.text("-- G-SENSOR --", 20, 2, 0)
        oled.fill_rect(34, 35, 60, 1, 1)
        oled.fill_rect(63, 16, 1, 40, 1)
        bx = max(36, min(88, 62 + int((ax / 1024.0) * 26)))
        by = max(18, min(50, 34 + int((ay / 1024.0) * 16)))
        oled.fill_rect(bx - 2, by - 2, 5, 5, 1)
        oled.text("X:" + str(int(ax/10)) + " Y:" + str(int(ay/10)), 10, 56)
        oled.show()
        if button_b.was_pressed():
            break
        sleep(40)

def run_temp(oled):
    button_b.was_pressed()
    while True:
        t = temperature()
        oled.fill(0)
        oled.fill_rect(0, 0, 128, 11, 1)
        oled.text("-- TEMPERATURE --", 12, 2, 0)
        oled.text("SENSOR: CPU NRF", 10, 20)
        oled.text("TEMP: " + str(t) + " C", 10, 34)
        stat = "STATUS: COLD" if t < 18 else ("STATUS: WARM" if t > 28 else "STATUS: COMFORT")
        oled.text(stat, 10, 46)
        oled.text("B: EXIT", 10, 56)
        oled.show()
        if button_b.was_pressed():
            break
        sleep(300)