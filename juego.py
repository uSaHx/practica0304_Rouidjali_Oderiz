from clases import *

def main():
    clock = pygame.time.Clock()

    barra_x = ancho/2 - barra_ancho/2
    barra_y = alto - barra_alto - 5
    barra = Barra(barra_x, barra_y, barra_ancho, barra_alto, "white")
    pelota = Pelota(ancho/2, barra_y - pelota_radio, pelota_radio, "black")

    bloques, bloques_indestructibles = generador_bloques_indestructibles(6, 10)
    vidas = 3

    def reset():
        barra.x = barra_x
        barra.y = barra_y
        pelota.x = ancho/2
        pelota.y = barra_y - pelota_radio


    def display_text(text):
        text_render = vidas_texto.render(text, 1, "red")
        pantalla.blit(text_render, (ancho/2 - text_render.get_width() /
                               2, alto/2 - text_render.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)

    jugando = True
    while jugando:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jugando = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and barra.x - barra.VEL >= 0:
            barra.move(-1)
        if keys[pygame.K_RIGHT] and barra.x + barra.ancho + barra.VEL <= ancho:
            barra.move(1)

        pelota.move()
        colisiones_laterales(pelota)
        colision_barra(pelota, barra)

        # Colisiones con los bloques
        for bloque in bloques_indestructibles[:]:
            bloque.colision(pelota)

        for bloque in bloques[:]:
            bloque.colision(pelota)
            if bloque.golpes <= 0:
                bloques.remove(bloque)

        # Vidas
        if pelota.y + pelota.radio >= alto:
            vidas -= 1
            pelota.x = barra.x + barra.ancho/2
            pelota.y = barra.y - pelota_radio
            pelota.set_vel(0, pelota.VEL * -1)

        if vidas <= 0:
            bloques = generador_bloques_indestructibles(3, 10)
            vidas = 3
            reset()
            display_text("DERROTA...")

        if len(bloques) == 0:
            bloques = generador_bloques_indestructibles(3, 10)
            vidas = 3
            reset()
            display_text("¡¡VICTORIA!!")

        draw(pantalla, barra, pelota, bloques, vidas, bloques_indestructibles)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()