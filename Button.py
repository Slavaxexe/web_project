import pygame


class Button:
    def __init__(self, x, y, size_x, size_y, color, text, text_color, text_size):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.text = text
        self.color = color
        self.text_color = text_color
        self.text_size = text_size

    def draw_button(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size_x, self.size_y))
        self.write_text(screen)

    def write_text(self, surface):
        font_size = self.text_size
        myFont = pygame.font.Font(None, 24)
        myText = myFont.render(self.text, 1, self.text_color)
        surface.blit(myText, ((self.x + self.size_x / 2) - myText.get_width() / 2,
                              (self.y + self.size_y / 2) - myText.get_height() / 2))

    def pressed(self, mouse):
        if self.x + self.size_x > mouse[0] > self.x  and self.y + self.size_y > mouse[1] > self.y:
            return True
        return False

    def change_color(self, color):
        self.color = color