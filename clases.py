# Librerias usadas
import random
import pygame
import math

# Inicializador
pygame.init()

# Constantes
ancho, alto = 1280, 960
pantalla = pygame.display.set_mode((ancho, alto))
fondo = pygame.image.load("campo.jpg")
fondo = pygame.transform.scale(fondo, (ancho, alto))
pygame.display.set_caption("bloque Breaker")
pygame.mixer.init()
musica_fondo = pygame.mixer.Sound("champions.wav")
rebote = pygame.mixer.Sound("rebote.wav")
pygame.mixer.Sound.play(musica_fondo)
fps = 60
barra_ancho = 200
barra_alto = 20
pelota_radio = 15

vidas_texto = pygame.font.SysFont("comicsans", 100)

class Barra:
    VEL = 7

    def __init__(self, x, y, ancho, alto, color):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.color = color

    def draw(self, pantalla):
        pygame.draw.rect(
            pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

    def move(self, direccion=1):
        self.x = self.x + self.VEL * direccion


class Pelota:
    VEL = random.randint(4,8)

    def __init__(self, x, y, radio, color):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.x_vel = 0
        self.y_vel = -self.VEL

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def draw(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (self.x, self.y), self.radio)


class Bloque_indestrucitble:
    def __init__(self, x, y, ancho, alto, colors):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.colors = colors
        self.color = colors[0]

    def draw(self, pantalla):
        pygame.draw.rect(
            pantalla, self.color, (self.x, self.y, self.ancho, self.alto))

    def colision(self, pelota):
        if not (pelota.x <= self.x + self.ancho and pelota.x >= self.x):
            return False
        if not (pelota.y - pelota.radio <= self.y + self.alto):
            return False

        pelota.set_vel(pelota.x_vel, pelota.y_vel * -1)
        return True

    @staticmethod
    def interpolate(color_a, color_b, t):
        return tuple(int(a + (b - a) * t) for a, b in zip(color_a, color_b))

class Bloque(Bloque_indestrucitble):
    def __init__(self, x, y, ancho, alto, colors, golpes):
        super().__init__(x, y, ancho, alto, colors)
        self.golpes = golpes
        self.max_golpes = golpes

    def hit(self):
        self.golpes -= 1
        self.color = self.interpolate(
            *self.colors, self.golpes/self.max_golpes)

    def colision(self, pelota):
        if not (pelota.x <= self.x + self.ancho and pelota.x >= self.x):
            return False
        if not (pelota.y - pelota.radio <= self.y + self.alto):
            return False

        self.hit()
        pelota.set_vel(pelota.x_vel, pelota.y_vel * -1)
        return True

def draw(pantalla, barra, pelota, bloques, vidas, bloques_indestucitbles):

    pantalla.blit(fondo, (0,0))
    barra.draw(pantalla)
    pelota.draw(pantalla)

    for bloque in bloques:
        bloque.draw(pantalla)

    for bloque1 in bloques_indestucitbles:
        bloque1.draw(pantalla)

    vidas_text = vidas_texto.render(f"vidas: {vidas}", 1, "black")
    pantalla.blit(vidas_text, (10, alto - vidas_text.get_height() - 10))

    pygame.display.update()


def colisiones_laterales(pelota):
    if pelota.x - pelota_radio <= 0 or pelota.x + pelota_radio >= ancho:
        pelota.set_vel(pelota.x_vel * -1, pelota.y_vel)
    if pelota.y + pelota_radio >= alto or pelota.y - pelota_radio <= 0:
        pelota.set_vel(pelota.x_vel, pelota.y_vel * -1)


def colision_barra(pelota, barra):
    if not (pelota.x <= barra.x + barra.ancho and pelota.x >= barra.x):
        return
    if not (pelota.y + pelota.radio >= barra.y):
        return

    barra_center = barra.x + barra.ancho/2
    distance_to_center = pelota.x - barra_center

    percent_ancho = distance_to_center / barra.ancho
    angle = percent_ancho * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * pelota.VEL
    y_vel = math.cos(angle_radians) * pelota.VEL * -1
    pelota.VEL += random.randint(-2, 2)
    if  pelota.VEL < 4:
        pelota.VEL = 4
    if pelota.VEL < 9:
        pelota.VEL = 9
    print(pelota.VEL)
    pelota.set_vel(x_vel, y_vel)
    pygame.mixer.Sound.play(rebote)

def generador_bloques_indestructibles(rows, cols):
    gap = 2
    bloque_ancho = ancho // cols - gap
    bloque_alto = 35

    bloques = []
    bloques_indestructibles = []
    for row in range(rows):
        for col in range(cols):
            if row == rows-1 and (col == 0 or col == 1 or col == cols-2 or col == cols-1 ):
                bloque_indestructibles = Bloque_indestrucitble(col * bloque_ancho + gap * col, row * bloque_alto +
                              gap * row, bloque_ancho, bloque_alto, [(128, 128, 128), (255, 0, 0)])

                bloques_indestructibles.append(bloque_indestructibles)
            else:
                bloque = Bloque(col * bloque_ancho + gap * col, row * bloque_alto +
                                               gap * row, bloque_ancho, bloque_alto,
                                                [(255, 255, 0), (255, 0, 0)], random.randint(1,3))

                bloques.append(bloque)

    return bloques, bloques_indestructibles
