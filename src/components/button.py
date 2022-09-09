from globals import *
from utils import *
from components.text import Text

class Button:
    def __init__(self, text, btn_x, btn_y, *,
                 func = None,
                 text_color = WHITE,
                 hover_color = FADED_RED,
                 btn_color = BLACK,
                 width = 100,
                 height = 50,
                 text_align = ALIGN_LEFT,
                 font_size = SIZE_P,
                 text_x = 0,
                 text_y = 0):
        func = func or (lambda: print(f"No function attached to button '{self.text}'"))

        self.func = func
        self.text_color = text_color
        self.hover_color = hover_color
        self.btn_color = btn_color
        self.width = width
        self.height = height
        self.text = text
        self.text_x = text_x
        self.text_y = text_y
        self.btn_x = btn_x
        self.btn_y = btn_y
        self.text_component = Text(text, text_x + btn_x, text_y + btn_y,
            color = text_color,
            font_size = font_size,
            wrap_width = width,
            text_align = text_align
        )

    def set_btn_color(self, new_color):
        self.btn_color = new_color

    def set_text_color(self, new_color):
        self.text_color = new_color

    def set_hover_color(self, new_color):
        self.hover_color = new_color

    def click(self):
        self.func()

    def get_bounds(self):
        return self.btn_x, self.btn_y, self.width, self.height

    def check_hover(self, mouse_xy, mouse_radius):
        return does_circle_overlap_rect(mouse_xy, mouse_radius, self.get_bounds())

    def draw(self, win, mouse_xy, mouse_radius, dt):
        pygame.draw.rect(win, self.btn_color, self.get_bounds())

        if self.check_hover(mouse_xy, mouse_radius):
            self.text_component.set_color(self.hover_color)
        else:
            self.text_component.set_color(self.text_color)

        self.text_component.draw(win, dt)

    def get_pos(self):
        return self.btn_x, self.btn_y

    def get_text_pos(self):
        return self.text_x, self.text_y