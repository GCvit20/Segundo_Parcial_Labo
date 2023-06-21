import pygame, random, colores, json
from funciones_juego import *
from constantes import * 
import sqlite3

pygame.init() #Inicilizamos el juego
pygame.mixer.init() #Inicializamos el sonido

laser_sonido = pygame.mixer.Sound('Juego/Sonido/laser.wav')
explosion_sonido = pygame.mixer.Sound('Juego/Sonido/explosion.wav')
sonido_golpe = pygame.mixer.Sound('Juego/Sonido/golpe.wav')
 
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Galaxy 2.0')

running = True
bandera_primera_bala_jugador = False
bandera_primera_bala_enemigo = False

#Caja de texto
font_input = pygame.font.SysFont("Arial", 30)
texto = ""
texto_rect = pygame.Rect(LEFT_CAJA_TEXTO,TOP_CAJA_TEXTO,LARGO_CAJA_TEXTO,ANCHO_CAJA_TEXTO) #Creamos la superficie de un rectangulo donde ingresaremos el texto


grupo_enemigo = []
grupo_balas_jugador = []
grupo_balas_enemigas = []

#Cremos el objeto jugador de la clase jugador 
jugador1 = Jugador(imagen.convert_alpha(),velocidad,vida,posicion)


#Creamos enemigos 
for i in range(5):
    velocidad_enemigo = random.randint(1,3)
    enemigo = Enemigos(imagen_enemigo.convert_alpha(),velocidad_enemigo,50,[i*80+100,80]) #Utilizamos la i para que no nos ubique todos los enemigos en la misma fila. En primero se ubica en la posicion 100 (el segundo en la 180... etc) 
    enemigo_2 = Enemigos(imagen_enemigo.convert_alpha(),velocidad_enemigo,50,[i*80+80,150])

    grupo_enemigo.append(enemigo)
    grupo_enemigo.append(enemigo_2)

#Creamos la tabla
crear_tabla("bd_juego.db")

while running:
    time.tick(fps)
    pantalla.blit(fondo, (0,0)) #Establecemos el fondo de la ventana 
    jugador1.update()


    if JUGANDO == 0:
        pantalla.blit(imagen_play,rect_boton) #Mostramos los botones por pantalla
        pantalla.blit(imagen_ranking,rect_ranking)
        pygame.display.flip() #Escuchamos los cambios 

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                lista_click = list(evento.pos)
                if lista_click[0] > rect_boton[0] and lista_click[0] < (rect_boton[0] + rect_boton[2]): #Chequeamos el largo del boton (rect[0] = left, rect[1] = top, rect[2] = ancho, rect[3] = alto)(lista_click[0] = fila y lista_click[1] = columna)
                    if lista_click[1] > rect_boton[1] and lista_click[1] < (rect_boton[1] + rect_boton[3]): #Chequeamos el alto del boton 
                        JUGANDO = 1 
                if lista_click[0] > rect_ranking[0] and lista_click[0] < (rect_ranking[0] + rect_ranking[2]):
                    if lista_click[1] > rect_ranking[1] and lista_click[1] < (rect_ranking[1] + rect_ranking[3]): 
                        JUGANDO = 2 
            if evento.type == pygame.KEYDOWN:  
                if evento.key == pygame.K_BACKSPACE:
                    texto = texto[0:-1] #Si se presiona el backspace volvera hacia atras en el texto (desde 0 hasta la posicion donde esta -1)
                else:
                    if len(texto) < 13:
                        texto += evento.unicode #Unicode tiene almacenados todos los caracteres con los cuales nosotros trabajamos (depende del idioma). Entoces ira acumulando todas las letras que ingresemos por teclado

        #Dibujamos el rectangulo
        pygame.draw.rect(pantalla,colores.ALICEBLUE,texto_rect,2) #2 = borde 
        #Utilizamos el .render() para convertir el texto en una imagen para asi colocarla en la pantalla
        font_input_surface = font_input.render(texto,True,colores.WHITE)
        #Mostramos en pantalla 
        pantalla.blit(font_input_surface,(texto_rect.x+5, texto_rect.y+5))

    elif JUGANDO == 2:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT: 
                running = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                JUGANDO = 0
        
        mostrar_ranking("bd_juego.db", pantalla)
 
    elif JUGANDO == 1:
                
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                add_jugador("bd_juego.db",texto,score)

                running = False
            if evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_SPACE:
                
                    bala_jugador = Balas(list(jugador1.arma), imagen_bala, velocidad, laser_sonido) 
                    grupo_balas_jugador.append(bala_jugador)

                    if bandera_primera_bala_jugador == False:
                        bandera_primera_bala_jugador = True
                elif evento.key == pygame.K_ESCAPE:
                    add_jugador("bd_juego.db",texto,score)
                    JUGANDO = 0 
                    
            
        if bandera_primera_bala_jugador == True:
            bala_jugador.blit_and_update(grupo_balas_jugador, pantalla)
    
        pantalla.blit(jugador1.imagen, jugador1.posicion)
        enemigo.blit_and_update(grupo_enemigo, pantalla)


        #Coliciones entre balas jugador y enemigo
        try:
            if len(grupo_balas_jugador) > 0:
                for i in grupo_balas_jugador:
                    for j in grupo_enemigo:
                        if i.obtener_rectangulo().colliderect(j.obtener_rectangulo()):
                            if j.colision == False: #Si hay una colisión, se verifica si el enemigo (j) ya ha tenido una colisión previa
                                j.colision = True #Si es la primera colisión. Se establece j.colision en True para indicar que el enemigo ha tenido una colisión
                                posicion_enemigo_x = random.randint(1, 100) #Se generan nuevas coordenadas aleatorias para el nuevo enemigo que se cree.
                                posicion_enemigo_y = random.randint(1, 100)
                                score += 10
                                velocidad_enemigo = random.randint(1, 3) #Se generan una velocidad aleatorias para el nuevo enemigo que se crea.
                                enemigo = Enemigos(imagen_enemigo,velocidad_enemigo,50,[posicion_enemigo_x,posicion_enemigo_y]) #Cuando ocurre una colision se generarn nuevos enemigos 
                                grupo_enemigo.append(enemigo) #Se agrega a la lista de enemigos
                                explosion_sonido.set_volume(0.3)
                                explosion_sonido.play()
                                grupo_balas_jugador.remove(i) 
                                grupo_enemigo.remove(j)
                            else:
                                if j.tiempo_colision < 21: #Se verifica si el tiempo de colisión es menor que 21 milisegundos
                                    j.tiempo_colision += 1 #De ser asi se incrementa en 1
                                else:
                                    j.colision = False #Si el tiempo de colisión ha alcanzado 21 o más, se establece j.colision en False para permitir futuras colisiones
        except ValueError:
            print("ERROR") 

        #Colisiones entre jugador y balas enemigas
        
        tiempo_actual = pygame.time.get_ticks()
        tiempo_disparo = random.randint(1000,3000)

        for enemigo in grupo_enemigo:
            if tiempo_actual - enemigo.tiempo_disparo >= tiempo_disparo: # 2 disparos por segundo 
                enemigo.tiempo_disparo = tiempo_actual

                if random.random() < 0.4:

                    bala_enemigo = Balas_enemigas(imagen_bala, list(enemigo.arma), velocidad_disparo_enemigo, laser_sonido)
                    grupo_balas_enemigas.append(bala_enemigo)

                    if bandera_primera_bala_enemigo == False:
                        bandera_primera_bala_enemigo = True 
                

        
        for i in grupo_balas_enemigas:
              
            if i.obtener_rectangulo().colliderect(jugador1.obtener_rectangulo()):
                if i.colision == False:
                    i.colision = True
                    jugador1.vida -= 10

                    if jugador1.vida <= 0:
                        add_jugador("bd_juego.db",texto,score)
                        running = False
                        

                    sonido_golpe.set_volume(0.3)
                    sonido_golpe.play()
                else:
                    
                    if jugador1.tiempo_colision < 21: 
                        jugador1.tiempo_colision += 1 
                    else:
                        i.colision = False 

                grupo_balas_enemigas.remove(i)

        if bandera_primera_bala_enemigo == True:
            bala_enemigo.blit_and_update(grupo_balas_enemigas, pantalla)
            
             

        #Score y barra de vida
        puntuacion(pantalla,(' SCORE: ' + str(score)+ '   '),30,ANCHO_VENTANA-790,2)
        barra_vida(pantalla, ANCHO_VENTANA-110, ALTO_VENTANA-25, jugador1.vida)
        

    pygame.display.flip()
pygame.quit()