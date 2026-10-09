# 🤖 RobotOS mini for BBC micro:bit v2

[English](#-english) | [Русский](#-русский)

---

## 🇷🇺 Русский

[![micro:bit](https://img.shields.io/badge/Плата-micro:bit%20v2-blue.svg)](https://microbit.org/)
[![MicroPython](https://img.shields.io/badge/Код-MicroPython-brightgreen.svg)](https://micropython.org/)
[![License: MIT](https://img.shields.io/badge/Лицензия-MIT-yellow.svg)](LICENSE)

Автономный робот на базе бортовой системы **RobotOS mini** для платы BBC micro:bit v2, оснащенный OLED-дисплеем и «виртуальным бампером» на акселерометре.

---

### 📋 Аппаратная спецификация (Железо)

* **Мозг робота:** BBC micro:bit v2 (чип nRF52833, 128 KB RAM)
* **Экран:** OLED 1.3 дюйма I2C (128x64 точек, контроллер SH1106)
* **Плата расширения:** IO:BIT V2 с разъемом внешнего питания DC 6–12V
* **Приводы:**
  * **Серво 1 (Ковш):** Стандартный сервопривод (поворот на 90°)
  * **Серво 2 (Левое колесо):** Сервопривод постоянного вращения (360°)
  * **Серво 3 (Правое колесо):** Сервопривод постоянного вращения (360°)
* **Питание:** Повербанк или сборка аккумуляторов

---

### 🔌 Схема подключения проводов

Все элементы подключаются к разъемам шилда **IO:BIT V2**:

| Компонент | Пин на шилде | Назначение | Особые указания |
| :--- | :---: | :--- | :--- |
| **Серво ковша** | `P0` | Подъём/спуск (0°..90°) | ⚠️ **Выключить тумблер зуммера рядом с пином!** |
| **Левое колесо** | `P1` | Ходовой привод | 3-проводной кабель (Син-Красн-Черн) |
| **Правое колесо** | `P2` | Ходовой привод | 3-проводной кабель (Син-Красн-Черн) |
| **Дисплей SDA** | `SDA (P20)` | Шина данных I2C | Правая группа разъемов I2C |
| **Дисплей SCL** | `SCL (P19)` | Шина тактирования I2C | Правая группа разъемов I2C |
| **Питание OLED**| `3.3V / GND` | Питание экрана | Группа разъемов I2C |

> ⚠️ **ВАЖНО ПО ПИТАНИЮ:**  
> Питание 6–12V подключается строго в круглый разъем DC **на шилде**. Тумблер на шилде перевести в положение **ON**. **Запрещено питать сервоприводы напрямую от micro:bit через USB — плата будет зависать!**

---

### 📁 Структура файлов в памяти платы (MicroPython)

### 📁 Структура файлов в памяти платы (MicroPython)

Файлы загружаются в память micro:bit через среду **Thonny IDE**: https://thonny.org/

```text
📁 microbit/
├── 📄 main.py      # Главный цикл, меню и алгоритм объезда препятствий
├── 📄 sh1106.py    # Драйвер дисплея 1.3" со встроенным шрифтом 5x8
├── 📄 eyes.py      # Физика и анимация глаз робота (радиус 3)
├── 📄 motors.py    # Управление сервоприводами ковша и колес через ШИМ
└── 📄 apps.py      # Модули: уровень (G-сенсор) и градусник процессора
```

> **Прошивка платы:** Если Thonny не видит плату, перепрошейте интерфейс micro:bit файлом `0257_nrf52820_microbit_if_crc_c782a5ba90_gcc.hex`.

---

### 🎮 Руководство по управлению

* **При включении:** Звучит приветственный сигнал, робот моргает глазами и ждет команду.
* **Кнопка [A] (Режим движения):**
  * `1-е нажатие` ➔ Старт автономного движения вперед.
  * `2-е нажатие` ➔ Остановка робота.
* **Кнопка [B] (Главный стоп и меню):**
  * Мгновенная остановка моторов и вход в бортовое меню настроек.

---

### 🛡️ Интеллектуальный «Виртуальный бампер»

Робот чувствует столкновения со стенами с помощью встроенного акселерометра:

1. **1-й удар:** Грустные глазки ➔ подъем ковша ➔ откат назад 1 сек ➔ поворот **налево на 90°** ➔ спуск ковша ➔ движение дальше.
2. **2-й удар подряд (в течение 2.5 сек):** Значит робот в углу/тупике — делает полный **разворот на 180°**!
3. **Свободный путь:** Если робот проехал прямо без ударов более 2.5 секунд, память тупика обнуляется, возвращая легкий поворот на 90°.

---

### ⚙️ Бортовое меню (RobotOS)

* **Управление:** `Кнопка [A]` = Листать пункт вниз (`>`), `Кнопка [B]` = Выбрать / Войти.

| Пункт меню | Что делает приложение | Управление внутри |
| :--- | :--- | :--- |
| **EYES** | Просмотр всех 9 эмоций и анимаций лица | `A` — след. эмоция, `B` — выход |
| **SERVO** | Тест ковша (0° ⇄ 90°) и моторов колес | `A` — выбор серво, `B` — старт теста |
| **G-SENSOR** | Электронный уровень: шарик 5x5 катается при наклоне | Наклоняй робота, `B` — выход |
| **TEMP** | Температура процессора nRF52833 в реальном времени | `B` — выход |
| **EXIT** | Выход из меню к живым глазкам и готовности к езде | `B` — подтвердить |

---

<img width="3840" height="2160" alt="IMG_0626" src="https://github.com/user-attachments/assets/579094f6-6071-4b2c-8e12-2a4b563d291a" />
<img width="3840" height="2160" alt="IMG_0629 (3)" src="https://github.com/user-attachments/assets/b1edac7c-60f5-457c-8867-a9d782c896c4" />
<img width="3840" height="2160" alt="IMG_0629" src="https://github.com/user-attachments/assets/cb18fd46-cf28-4280-81a2-940c23c61138" />
<img width="3840" height="2160" alt="IMG_0629 (1)" src="https://github.com/user-attachments/assets/505f3689-007c-470a-854c-1cdefccdb54c" />
<img width="3840" height="2160" alt="IMG_0629 (2)" src="https://github.com/user-attachments/assets/32f0d277-f9a4-4bb8-a2ca-2bdfca71bc22" />


### 👨‍💻 Автор проекта

Разработано: **Кирилл Дмитриев** (`nitroline@mail.ru`) для **Роберта Дмитриева**.  
Распространяется по открытой лицензии


## 🇬🇧 English

[![micro:bit](https://img.shields.io/badge/Board-micro:bit%20v2-blue.svg)](https://microbit.org/)
[![MicroPython](https://img.shields.io/badge/Code-MicroPython-brightgreen.svg)](https://micropython.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An autonomous mini-robot powered by **RobotOS mini** on BBC micro:bit v2 with an OLED display and an intelligent accelerometer-based "Virtual Bumper".

---

### 📋 Hardware Specification

* **Microcontroller:** BBC micro:bit v2 (nRF52833, 128 KB RAM)
* **Display:** 1.3" OLED I2C (128x64, SH1106 controller)
* **Expansion Board:** IO:BIT V2 shield with external DC 6–12V input
* **Actuators:**
  * **Servo 1 (Bucket):** Standard servo (0°–90° angle)
  * **Servo 2 (Left Wheel):** 360° continuous rotation servo
  * **Servo 3 (Right Wheel):** 360° continuous rotation servo
* **Power Supply:** External PowerBank (USB) or battery pack connected to shield

---

### 🔌 Pinout & Wiring

All modules connect directly to the **IO:BIT V2** shield:

| Component | Shield Pin | Purpose | Special Notes |
| :--- | :---: | :--- | :--- |
| **Bucket Servo** | `P0` | Bucket UP/DOWN (0°..90°) | ⚠️ **Turn off buzzer switch next to it!** |
| **Left Wheel** | `P1` | Drive motor | 3-wire cable (Blue/Red/Black) |
| **Right Wheel** | `P2` | Drive motor | 3-wire cable (Blue/Red/Black) |
| **OLED SDA** | `SDA (P20)` | I2C Data line | Right I2C connector block |
| **OLED SCL** | `SCL (P19)` | I2C Clock line | Right I2C connector block |
| **OLED Power** | `3.3V / GND` | Display power | I2C block power pins |

> ⚠️ **POWER WARNING:**  
> External 6–12V power must be connected to the **DC barrel jack on the expansion board**. Set the shield power switch to **ON**. **NEVER power the servos solely through the micro:bit USB port!**

---

### 📁 Project Structure (MicroPython)

All `.py` files must be uploaded to the root file system of the micro:bit via **Thonny IDE**: https://thonny.org/

```text
📁 microbit/
├── 📄 main.py # Main loop, system menu, autonomous drive logic
├── 📄 sh1106.py # Display driver (1.3" OLED SH1106) with 5x8 font
├── 📄 eyes.py # Animated expressive robot eyes (radius = 3)
├── 📄 motors.py # PWM control for continuous wheels and bucket servo
└── 📄 apps.py # Integrated tools: G-Sensor spirit level & Temperature
```

> **Firmware Note:** If Thonny cannot detect the board, reflash the micro:bit interface with `0257_nrf52820_microbit_if_crc_c782a5ba90_gcc.hex`.

---

### 🎮 Controls

* **Power ON:** Welcome sound plays, blinking eyes appear on the display, robot waits for command.
* **Button [A] (Drive Mode):**
  * `1st Press` ➔ Start autonomous driving forward.
  * `2nd Press` ➔ Stop robot.
* **Button [B] (Emergency Stop & Menu):**
  * Immediately stops all motors and opens the onboard OS menu.

---

### 🛡️ Smart "Virtual Bumper" Algorithm

The robot has no distance sensors, but detects collisions using the onboard accelerometer:

1. **1st Collision:** Shows sad eyes ➔ raises the bucket ➔ reverses for 1 sec ➔ turns left 90° ➔ lowers the bucket ➔ resumes driving.
2. **2nd Collision in a row (< 2.5 sec):** Indicates the robot is trapped in a corner. It immediately reverses and performs a full **180° U-turn**!
3. **Clear Path:** If the robot drives freely for > 2.5 seconds, collision history resets back to default (90° turn).

---

### ⚙️ RobotOS System Menu

* **Navigation:** `Button [A]` = Move cursor down (`>`), `Button [B]` = Select / Confirm.

| Menu Item | Description | Controls Inside |
| :--- | :--- | :--- |
| **EYES** | Preview all 9 face emotions and animations | `A` = Next emotion, `B` = Exit |
| **SERVO** | Test bucket (0° ⇄ 90°) and wheel rotation | `A` = Switch servo, `B` = Toggle test |
| **G-SENSOR** | Digital spirit level (5x5 ball moves with tilt) | Tilt robot, `B` = Exit |
| **TEMP** | Real-time nRF52833 CPU temperature monitor | `B` = Exit |
| **EXIT** | Return to alive eyes and readiness mode | `B` = Confirm |

---

### 👨‍💻 Author & Credits

Developed by **Kirill Dmitriev** (`nitroline@mail.ru`) for **Robert Dmitriev**.  

<br>

---
---

<br>
