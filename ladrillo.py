import pygame
class Brick:
    def __init__(self, x, y, imagen):
        self.image = pygame.image.load(imagen)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect(x=x,y=y)
        pass
class Brickvida(Brick):
    def __init__(self, x, y, imagen, hits):
        super().__init__(x, y, imagen)
        self.hits = hits
