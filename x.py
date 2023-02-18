import pygame
from random import randint
from ladrillo import Brickvida
from ladrillo import Brick


# Setup del juego
pygame.init()
pygame.mixer.init()
ventana = pygame.display.set_mode((720, 1020))
pygame.display.set_caption("Juego Oussama y Asier")

# Musica
musica_fondo = pygame.mixer.Sound("champions.wav")
pitido = pygame.mixer.Sound("pitido.mp3")
rebote = pygame.mixer.Sound("rebote.wav")
pygame.mixer.Sound.play(musica_fondo)

# Fondo de pantalla
fondo = pygame.image.load("campo.jpg")
fondo = pygame.transform.scale(fondo, (720, 1020))

# Bases del ladrillo
lista_ladrillos = []
columnas = 9
filas = 3
for columna in range(columnas):
    for fila in range(filas):
        if columna == 0:
            espaciox = 0
        else:
            espaciox = 10
        if fila == 0:
            espacioy = 0
        else:
            espacioy = 30
        brick = Brickvida(columna * 70 + espaciox * columna, fila * 100 + espacioy * fila, "messi.png",randint(1,2))
        lista_ladrillos.append(brick)

# Bases de la roca
roca1 = Brick(0, 430, "ronaldo.png")
roca2 = Brick(80, 430, "ronaldo.png")
roca3 = Brick(560, 430, "ronaldo.png")
roca4 = Brick(640, 430, "ronaldo.png")

# Bases de la pelota
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, (50, 50))
ballrect = ball.get_rect()
speed = [randint(2,5),randint(2,5)]
ballrect.move_ip(600,600)

# Bases de la barra
barra = pygame.image.load("botas.png")
barra = pygame.transform.scale(barra, (100, 50))
barrarect = barra.get_rect()
barrarect.move_ip(240,900)
fuente = pygame.font.Font(None, 36)

# Base fin de juego
texto = pygame.image.load("over.png")
texto = pygame.transform.scale(texto, (700, 300))
texto_rect = texto.get_rect()

# Funciones del juego
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
    # Teclas para jugar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        barrarect = barrarect.move(-5,0)
    if keys[pygame.K_RIGHT]:
        barrarect = barrarect.move(5,0)

    # Velocidad al colisionar con la barra
    if barrarect.colliderect(ballrect):
        speed[1] = -speed[1]
        pygame.mixer.Sound.play(rebote)
        if speed[0] < 15 and speed[1] < 15:
            speed[0] += 1
            if speed[1] < 0:
                speed[1] -= 2
            else:
                speed[1] += 2

    ballrect = ballrect.move(speed[0],speed[1])
    if ballrect.left < 0 or ballrect.right > ventana.get_width():
        speed[0] = -speed[0]
    if ballrect.top < 0:
        speed[1] = -speed[1]

    # Colision con Rocas
    if ballrect.colliderect(roca1.rect) or ballrect.colliderect(roca2.rect) \
            or ballrect.colliderect(roca3.rect) or ballrect.colliderect(roca4.rect):
        speed[1] = -speed[1]
    for f in range(len(lista_ladrillos)):
        if ballrect.colliderect(lista_ladrillos[f]):
            speed[1] = -speed[1]

    # Limites Laterales
    if barrarect.right > 724:
        barrarect.right = 723
    if barrarect.left < 0:
        barrarect.left = 1

    # Refresh Ventana
    ventana.blit(fondo, (0,0))
    for x in lista_ladrillos:
        ventana.blit(x.image, x.rect)
    ventana.blit(roca1.image, roca1.rect)
    ventana.blit(roca2.image, roca2.rect)
    ventana.blit(roca3.image, roca3.rect)
    ventana.blit(roca4.image, roca4.rect)
    ventana.blit(ball, ballrect)
    ventana.blit(barra, barrarect)

    # Pantalla de derrota
    if ballrect.bottom > 1010:
        speed = [0, 0]
        ventana.blit(texto, texto_rect)
        pygame.mixer.Sound.play(pitido, 1)
        pygame.mixer.Sound.stop(musica_fondo)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
pygame.quit()
