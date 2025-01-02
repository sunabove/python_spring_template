import framebuf
from uctypes import bytearray_at, addressof
from sys import implementation

# Basic Writer class for monochrome displays
class Writer():

    def __init__(self, device, font, verbose=True):
        self.device = device
        
        self.font = font
        if font.height() >= device.height or font.max_width() >= device.width:
            raise ValueError('Font too large for screen')
        # Allow to work with reverse or normal font mapping
        if font.hmap():
            self.map = framebuf.MONO_HMSB if font.reverse() else framebuf.MONO_HLSB
        else:
            raise ValueError('Font must be horizontally mapped.')
        pass
        
        if verbose:
            fstr = 'Orientation: Horizontal. Reversal: {}. Width: {}. Height: {}.'
            print(fstr.format(font.reverse(), device.width, device.height))
            print('Start row = {} col = {}'.format(self._getstate().text_row, self._getstate().text_col))
        
        self.screenwidth = device.width  # In pixels
        self.screenheight = device.height
        self.bgcolor = 0  # Monochrome background and foreground colors
        self.fgcolor = 1
        self.row_clip = False  # Clip or scroll when screen fullt
        self.col_clip = False  # Clip or new line when row is full
        self.wrap = True  # Word wrap
        self.cpos = 0
        self.tab = 4

        self.glyph = None  # Current char
        self.char_height = 0
        self.char_width = 0
        self.clip_width = 0
        
        self.x = 10
        self.y = (device.height - font.height()) // 2
    pass

    def _newline(self):
        height = self.font.height()
        
        self.y += height
        self.x = 0
        
        margin = self.screenheight - (self.y + height)
        y = self.screenheight + margin
        if margin < 0:
            if not self.row_clip:
                self.device.scroll(0, margin)
                self.device.fill_rect(0, y, self.screenwidth, abs(margin), self.bgcolor)
                self.y += margin

    def set_clip(self, row_clip=None, col_clip=None, wrap=None):
        if row_clip is not None:
            self.row_clip = row_clip
        if col_clip is not None:
            self.col_clip = col_clip
        if wrap is not None:
            self.wrap = wrap
        return self.row_clip, self.col_clip, self.wrap

    @property
    def height(self):  # Property for consistency with device
        return self.font.height()

    def print(self, string, x=None, y=None, invert=False):
        if x is not None :
            self.x = x
        pass
    
        if y is not None :
            self.y = y
        pass
    
        # word wrapping. Assumes words separated by single space.
        q = string.split('\n')
        last = len(q) - 1
        for n, s in enumerate(q):
            if s:
                self._printline(s, invert)
            if n != last:
                self._printchar('\n')

    def _printline(self, string, invert):
        rstr = None
        if self.wrap and self.stringlen(string, True):  # Length > self.screenwidth
            pos = 0
            lstr = string[:]
            while self.stringlen(lstr, True):  # Length > self.screenwidth
                pos = lstr.rfind(' ')
                lstr = lstr[:pos].rstrip()
            if pos > 0:
                rstr = string[pos + 1:]
                string = lstr
                
        for char in string:
            self._printchar(char, invert)
        if rstr is not None:
            self._printchar('\n')
            self._printline(rstr, invert)  # Recurse

    def stringlen(self, string, oh=False):
        if not len(string):
            return 0
        
        x = self.x  # Start column
        wd = self.screenwidth
        str_len = 0
        for char in string[:-1]:
            _, _, char_width = self.font.get_ch(char)
            str_len += char_width
            if oh and str_len + x > wd:
                return True  # All done. Save time.
        char = string[-1]
        _, _, char_width = self.font.get_ch(char)
        if oh and str_len + x + char_width > wd:
            str_len += self._truelen(char)  # Last char might have blank cols on RHS
        else:
            str_len += char_width  # Public method. Return same value as old code.
        return str_len + x > wd if oh else str_len

    # Return the printable width of a glyph less any blank columns on RHS
    def _truelen(self, char):
        glyph, ht, wd = self.font.get_ch(char)
        div, mod = divmod(wd, 8)
        gbytes = div + 1 if mod else div  # No. of bytes per row of glyph
        mc = 0  # Max non-blank column
        data = glyph[(wd - 1) // 8]  # Last byte of row 0
        for row in range(ht):  # Glyph row
            for col in range(wd -1, -1, -1):  # Glyph column
                gbyte, gbit = divmod(col, 8)
                if gbit == 0:  # Next glyph byte
                    data = glyph[row * gbytes + gbyte]
                if col <= mc:
                    break
                if data & (1 << (7 - gbit)):  # Pixel is lit (1)
                    mc = col  # Eventually gives rightmost lit pixel
                    break
            if mc + 1 == wd:
                break  # All done: no trailing space
        # print('Truelen', char, wd, mc + 1)  # TEST 
        return mc + 1

    def _get_char(self, char, recurse):
        if not recurse:  # Handle tabs
            if char == '\n':
                self.cpos = 0
            elif char == '\t':
                nspaces = self.tab - (self.cpos % self.tab)
                if nspaces == 0:
                    nspaces = self.tab
                while nspaces:
                    nspaces -= 1
                    self._printchar(' ', recurse=True)
                self.glyph = None  # All done
                return

        self.glyph = None  # Assume all done
        if char == '\n':
            self._newline()
            return
        glyph, char_height, char_width = self.font.get_ch(char)
        
        np = None  # Allow restriction on printable columns
        if self.y + char_height > self.screenheight:
            if self.row_clip:
                return
            self._newline()
        oh = self.x + char_width - self.screenwidth  # Overhang (+ve)
        
        if oh > 0:
            if self.col_clip or self.wrap:
                np = char_width - oh  # No. of printable columns
                if np <= 0:
                    return
            else:
                self._newline()
        self.glyph = glyph
        self.char_height = char_height
        self.char_width = char_width
        self.clip_width = char_width if np is None else np
        
    # Method using blitting. Efficient rendering for monochrome displays.
    # Tested on SSD1306. Invert is for black-on-white rendering.
    def _printchar(self, char, invert=False, recurse=False):
        self._get_char(char, recurse)
        if self.glyph is None:
            return  # All done
        buf = bytearray(self.glyph)
        if invert:
            for i, v in enumerate(buf):
                buf[i] = 0xFF & ~ v
        fbc = framebuf.FrameBuffer(buf, self.clip_width, self.char_height, self.map)
        self.device.blit(fbc, self.x, self.y)
        self.x += self.char_width
        self.cpos += 1

    def tabsize(self, value=None):
        if value is not None:
            self.tab = value
        return self.tab

    def setcolor(self, *_):
        return self.fgcolor, self.bgcolor
    pass
pass

if __name__ == '__main__':
    print("Hello...")

    from machine import Pin, I2C
    import ssd1306

    # Font
    import freesans20

    # OLED 디스플레이 설정 (128x32 해상도)
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
    w = width = 128
    h = height = 32
    oled = ssd1306.SSD1306_I2C(w, h, i2c)
    # 정사각형 그리기
    oled.fill(0)
    oled.rect(0, 0, w, h, 1)

    writer = Writer(oled, freesans20, verbose=0)

    # "Hello World"를 화면 중간에 출력하기 위해 위치 계산
    fw = font_width = writer.font.max_width()  # 폰트의 최대 글자 너비
    fh = font_height = writer.font.height()   # 폰트 높이

    text = "Hello World!"
    text_width = len(text) * font_width
    
    x = 10
    y = (h - fh) // 2  # 화면 가운데 행 계산

    #writer.text_pos( x, y )
    writer.print(text)
    
    oled.show()
pass

