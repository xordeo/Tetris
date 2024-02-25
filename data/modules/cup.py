import pygame


class TetrisCup:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.cup = [[0] * self.width for _ in range(self.height)]
        self.left = 490
        self.top = 90
        self.cell_size = 30
        self.score = 0

    def render(self, screen):
        # отрисовка стакана
        pygame.draw.line(screen, "white",
                         (self.left, self.top + self.cell_size * self.height),
                         (self.left, self.top),
                         3)
        pygame.draw.line(screen, "white",
                         (self.left, self.top + self.cell_size * self.height),
                         (self.left + self.cell_size * self.width, self.top + self.cell_size * self.height),
                         3)
        pygame.draw.line(screen, "white",
                         (self.left + self.cell_size * self.width, self.top + self.cell_size * self.height),
                         (self.left + self.cell_size * self.width, self.top),
                         3)

        s = pygame.Surface((self.cell_size * self.width, self.cell_size * self.height))
        s.set_alpha(225)
        s.fill("black")

        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, "white", (x * self.cell_size + self.left,
                                                   y * self.cell_size + self.top,
                                                   self.cell_size, self.cell_size), 1)
        screen.blit(s, (self.left, self.top))

        # отрисовка поля HOLD
        pygame.draw.rect(screen, "white",
                         (self.left - self.cell_size * 5, self.top, self.cell_size * 5, self.cell_size - 10))
        font = pygame.font.Font(None, 30)
        text = font.render("HOLD", True, (0, 0, 0))
        screen.blit(text, (self.left - self.cell_size * 5 + 3, self.top + 2))

        s1 = pygame.Surface((self.cell_size * 5 - 2, self.cell_size * 3))
        s1.set_alpha(225)
        s1.fill("black")
        screen.blit(s1, (self.left - self.cell_size * 5, self.top + self.cell_size - 10))

        pygame.draw.line(screen, "white", (self.left - self.cell_size * 5, self.top + self.cell_size - 10),
                         (self.left - self.cell_size * 5, self.top + self.cell_size * 4 - 10), 2)
        pygame.draw.line(screen, "white", (self.left - self.cell_size * 5, self.top + self.cell_size * 4 - 10),
                         (self.left - 1, self.top + self.cell_size * 4 - 10), 2)

        # отрисовка поля NEXT
        pygame.draw.rect(screen, "white",
                         (self.left + self.cell_size * self.width, self.top, self.cell_size * 5, self.cell_size - 10))
        font = pygame.font.Font(None, 30)
        text = font.render("NEXT", True, (0, 0, 0))
        screen.blit(text, (self.left + self.cell_size * self.width + 3, self.top + 2))

        pygame.draw.line(screen, "white", (self.left + self.cell_size * (self.width + 5), self.top),
                         (self.left + self.cell_size * (self.width + 5),
                          self.top + self.cell_size - 10 + self.cell_size * 15), 3)
        pygame.draw.line(screen, "white",
                         (self.left + self.cell_size * self.width, self.top + self.cell_size * 16 - 10),
                         (self.left + self.cell_size * 15, self.top + self.cell_size * 16 - 10), 3)

        s2 = pygame.Surface((self.cell_size * 5 - 3, self.cell_size * 15))
        s2.set_alpha(225)
        s2.fill("black")
        screen.blit(s2, (self.left + self.cell_size * self.width + 3, self.top + self.cell_size - 10))

        # отрисовка SCORE
        font = pygame.font.Font("data/fonts/CyberPrincess.ttf", 17)
        text = font.render("SCORE", True, (255, 255, 255))
        screen.blit(text, (self.left + self.cell_size * self.width + 10, self.top + 2 + self.cell_size * 16))

        font = pygame.font.Font("data/fonts/Constance-7BLXE.otf", 30)
        text = font.render(str(self.score), True, (255, 255, 255))
        screen.blit(text, (self.left + self.cell_size * self.width + 10, self.top + 12 + self.cell_size * 16))
