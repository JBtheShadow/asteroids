import pygame
from globals import *

class Text:
    def __init__(self, text, x, y, *,
                 font_size = SIZE_P,
                 text_align = ALIGN_LEFT,
                 wrap_width = WIN_WIDTH,
                 fade_in = False,
                 fade_out = False,
                 color = WHITE,
                 opacity = 255):
        self.text = text
        self.x = x
        self.y = y
        self.font_size = font_size
        self.text_align = text_align
        self.wrap_width = wrap_width
        self.fade_in = fade_in
        self.fade_out = fade_out
        self.color = color
        self.opacity = opacity

        if self.fade_in:
            self.opacity = 25

    def set_color(self, new_color):
        self.color = new_color

    def draw(self, win, dt):
        if self.opacity > 0:
            if self.fade_in:
                if self.opacity < 255:
                    self.opacity = min(self.opacity + 255 / TEXT_FADE_DUR * dt, 255)
                else:
                    self.fade_in = False
            elif self.fade_out:
                self.opacity = max(0, self.opacity - 255 / TEXT_FADE_DUR * dt)

            font = fonts[self.font_size]

            words = self.text.split()
            lines = []
            while len(words) > 0:
                line_words = []
                while len(words) > 0:
                    line_words.append(words.pop(0))
                    fw, fh = font.size(' '.join(line_words + words[:1]))
                    if fw > self.wrap_width:
                        break

                line = ' '.join(line_words)
                lines.append(line)

            y_offset = 0
            for line in lines:
                fw, fh = font.size(line)

                tx = self.x
                ty = self.y + y_offset
                if self.text_align == ALIGN_CENTER:
                    tx = self.x + (self.wrap_width - fw) / 2.0
                if self.text_align == ALIGN_RIGHT:
                    tx = self.x + self.wrap_width - fw

                text = font.render(self.text, 1, self.color)
                r_text = text
                if self.opacity < 255:
                    r_text = pygame.Surface((fw, fh))
                    r_text.fill(BLACK)
                    r_text.blit(text, (0, 0, fw, fh))
                    r_text.set_alpha(self.opacity)
                win.blit(r_text, (tx, ty, fw, fh))

                y_offset += fh
            
            return True
        else:
            return False
