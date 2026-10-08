from microbit import i2c, sleep, button_a, button_b, accelerometer, running_time
import sh1106
import eyes
import motors
import apps

oled = sh1106.SH1106_I2C(128, 64, i2c, addr=0x3c)
eyes.init(oled)

MENU = ["EYES", "SERVO", "G-SENSOR", "TEMP", "EXIT"]
menu_idx = 0
state = 0  # 0: DRIVE, 1: MENU
driving = False

CRASH_THRESHOLD = 450
last_hit_time = 0
hit_count = 0
last_x, last_y, last_z = 0, 0, 0

motors.stop()
motors.bucket_down()
eyes.happy()
sleep(800)
eyes.wakeup()

def draw_menu():
    oled.fill(0)
    oled.fill_rect(0, 0, 128, 11, 1)
    oled.text("-- ROBOT OS --", 20, 2, 0)
    start = max(0, min(menu_idx - 1, len(MENU) - 4))
    for i in range(start, min(len(MENU), start + 4)):
        p = "> " if i == menu_idx else "  "
        oled.text(p + MENU[i], 10, 16 + (i - start) * 12)
    oled.show()

def handle_collision(is_double_hit):
    global hit_count, last_hit_time
    motors.stop()
    eyes.sad()
    motors.bucket_smooth(90, delay_ms=8)
    
    # Откат назад
    motors.backward(80)
    sleep(1000)
    motors.stop()

    # Поворот: 1000мс (180°) при повторном ударе, 500мс (90°) при первом
    turn_ms = 1000 if is_double_hit else 500
    motors.turn_left(85)
    sleep(turn_ms)
    motors.stop()

    motors.bucket_smooth(0, delay_ms=8)
    eyes.center()
    motors.forward(80)
    last_hit_time = running_time()

while True:
    if state == 0:
        if button_a.was_pressed():
            driving = not driving
            if driving:
                eyes.center()
                motors.forward(80)
                last_x = accelerometer.get_x()
                last_y = accelerometer.get_y()
                last_z = accelerometer.get_z()
                last_hit_time = running_time()
                hit_count = 0
            else:
                motors.stop()
                eyes.center()

        elif button_b.was_pressed():
            driving = False
            motors.stop()
            state = 1
            menu_idx = 0
            draw_menu()
            sleep(300)

        if driving:
            ax = accelerometer.get_x()
            ay = accelerometer.get_y()
            az = accelerometer.get_z()
            delta = abs(ax - last_x) + abs(ay - last_y) + abs(az - last_z)
            last_x, last_y, last_z = ax, ay, az

            now = running_time()
            if hit_count > 0 and (now - last_hit_time > 2500):
                hit_count = 0

            # Засекли удар о препятствие!
            if delta > CRASH_THRESHOLD or accelerometer.was_gesture('shake'):
                if hit_count == 0:
                    hit_count = 1
                    handle_collision(False) # 90 град
                else:
                    hit_count = 0
                    handle_collision(True)  # 180 град
        else:
            eyes.idle_tick()

    elif state == 1:
        if button_a.was_pressed():
            menu_idx = (menu_idx + 1) % len(MENU)
            draw_menu()
            sleep(150)
        elif button_b.was_pressed():
            item = MENU[menu_idx]
            if item == "EXIT":
                state = 0
                eyes.wakeup()
            elif item == "EYES":
                eyes.run_app()
                draw_menu()
            elif item == "SERVO":
                motors.run_app(oled)
                draw_menu()
            elif item == "G-SENSOR":
                apps.run_gsensor(oled)
                draw_menu()
            elif item == "TEMP":
                apps.run_temp(oled)
                draw_menu()
            sleep(200)

    sleep(40)