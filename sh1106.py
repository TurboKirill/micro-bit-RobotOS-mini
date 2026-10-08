# Автономный драйвер SH1106 для BBC micro:bit v2 с поддержкой текста

# Базовый шрифт 5x8 (цифры, латиница, символы)
FONT = {
    ' ': b'\x00\x00\x00\x00\x00', '!': b'\x00\x00\x5f\x00\x00', '"': b'\x00\x07\x00\x07\x00',
    '+': b'\x08\x08\x3e\x08\x08', '-': b'\x08\x08\x08\x08\x08', '.': b'\x00\x60\x60\x00\x00',
    '/': b'\x20\x10\x08\x04\x02', ':': b'\x00\x36\x36\x00\x00', '<': b'\x08\x14\x22\x41\x00',
    '=': b'\x14\x14\x14\x14\x14', '>': b'\x00\x41\x22\x14\x08', '?': b'\x02\x01\x51\x09\x06',
    '0': b'\x3e\x51\x49\x45\x3e', '1': b'\x00\x42\x7f\x40\x00', '2': b'\x42\x61\x51\x49\x46',
    '3': b'\x21\x41\x45\x4b\x31', '4': b'\x18\x14\x12\x7f\x10', '5': b'\x27\x45\x45\x45\x39',
    '6': b'\x3c\x4a\x49\x49\x30', '7': b'\x01\x71\x09\x05\x03', '8': b'\x36\x49\x49\x49\x36',
    '9': b'\x06\x49\x49\x29\x1e', 'A': b'\x7e\x11\x11\x11\x7e', 'B': b'\x7f\x49\x49\x49\x36',
    'C': b'\x3e\x41\x41\x41\x22', 'D': b'\x7f\x41\x41\x22\x1c', 'E': b'\x7f\x49\x49\x49\x41',
    'F': b'\x7f\x09\x09\x09\x01', 'G': b'\x3e\x41\x49\x49\x7a', 'H': b'\x7f\x08\x08\x08\x7f',
    'I': b'\x00\x41\x7f\x41\x00', 'J': b'\x20\x40\x41\x3f\x01', 'K': b'\x7f\x08\x14\x22\x41',
    'L': b'\x7f\x40\x40\x40\x40', 'M': b'\x7f\x02\x0c\x02\x7f', 'N': b'\x7f\x04\x08\x10\x7f',
    'O': b'\x3e\x41\x41\x41\x3e', 'P': b'\x7f\x09\x09\x09\x06', 'Q': b'\x3e\x41\x51\x21\x5e',
    'R': b'\x7f\x09\x19\x29\x46', 'S': b'\x46\x49\x49\x49\x31', 'T': b'\x01\x01\x7f\x01\x01',
    'U': b'\x3f\x40\x40\x40\x3f', 'V': b'\x1f\x20\x40\x20\x1f', 'W': b'\x7f\x20\x18\x20\x7f',
    'X': b'\x63\x14\x08\x14\x63', 'Y': b'\x07\x08\x70\x08\x07', 'Z': b'\x61\x51\x49\x45\x43',
    '[': b'\x00\x7f\x41\x41\x00', ']': b'\x00\x41\x41\x7f\x00', '_': b'\x40\x40\x40\x40\x40'
}

class SH1106_I2C:
    def __init__(self, width=128, height=64, i2c=None, addr=0x3c, rotate=180):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr
        self.rotate = rotate
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.init_display()

    def write_cmd(self, cmd):
        self.i2c.write(self.addr, bytearray([0x80, cmd]))

    def init_display(self):
        cmds = [
            0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
            0xAD, 0x8B, 0x30 | 0x02,
            0xA0 | (0x01 if self.rotate == 180 else 0x00),
            0xC0 | (0x08 if self.rotate == 180 else 0x00),
            0xDA, 0x12, 0x81, 0x80, 0xD9, 0x1F, 0xDB, 0x40,
            0x33, 0xA6, 0xAF
        ]
        for c in cmds:
            self.write_cmd(c)
        self.fill(0)
        self.show()

    def fill(self, color=0):
        val = 0xFF if color else 0x00
        for i in range(len(self.buffer)):
            self.buffer[i] = val

    def pixel(self, x, y, color=1):
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y >> 3) * self.width + x
            bit = 1 << (y & 7)
            if color:
                self.buffer[idx] |= bit
            else:
                self.buffer[idx] &= ~bit

    def fill_rect(self, x, y, w, h, color=1):
        x1 = max(0, x)
        x2 = min(self.width, x + w)
        y1 = max(0, y)
        y2 = min(self.height, y + h)
        if x1 >= x2 or y1 >= y2:
            return
        for cy in range(y1, y2):
            page_offset = (cy >> 3) * self.width
            bit = 1 << (cy & 7)
            if color:
                for cx in range(x1, x2):
                    self.buffer[page_offset + cx] |= bit
            else:
                nbit = ~bit
                for cx in range(x1, x2):
                    self.buffer[page_offset + cx] &= nbit

    def text(self, string, x, y, color=1):
        """Печать строки текста (шрифт 5x8)"""
        cur_x = x
        for char in str(string).upper():
            glyph = FONT.get(char, FONT[' '])
            if cur_x + 6 > self.width:
                break
            for col_idx in range(5):
                byte = glyph[col_idx]
                for bit_idx in range(8):
                    # Рисуем только саму букву нужным цветом
                    if (byte >> bit_idx) & 1:
                        self.pixel(cur_x + col_idx, y + bit_idx, color)
            cur_x += 6

    def show(self):
        for page in range(self.pages):
            self.write_cmd(0xB0 | page)
            self.write_cmd(0x02)
            self.write_cmd(0x10)
            start = page * self.width
            chunk = self.buffer[start : start + self.width]
            self.i2c.write(self.addr, b'\x40' + chunk)