import pygame, random

#IMAGENES

fondo = pygame.image.load('Juego/Imagenes/fondo.png')
imagen_bala = pygame.image.load('Juego/Imagenes/bola.png')
imagen = pygame.image.load('Juego/Imagenes/principal.png') #Utilizamos el 'convert()' para convertir una imagen a un formato optimizado para su uso en el juego.
imagen = pygame.transform.scale(imagen, (50,70))
imagen_enemigo = pygame.image.load('Juego/Imagenes/enemy3.png')
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (30,50))
imagen_play = pygame.image.load('Juego/Imagenes/play.png')
imagen_ranking = pygame.image.load('Juego/Imagenes/ranking.png')

#CONSTANTES

ANCHO_VENTANA = fondo.get_width() #Toma el ancho de la iamgen de fondo 
ALTO_VENTANA = fondo.get_height()
ANCHO_BOTON = 90
ALTO_BOTON = 50
POS_TOP_BOTON = 100
POS_LEFT_BOTON = 320
POS_TOP_PUNTOS = 230
POS_LEFT_PUNTOS = 320
LEFT_TEXTO = 230
TOP_TEXTO = 50
TAMAÑO_FUENTE = 24
TAMAÑO_FUENTE_ENCABEZADO = 30
TOP_TEXTO_RANKING = 30 + 100
LEFT_CAJA_TEXTO = 330
TOP_CAJA_TEXTO = 380
ANCHO_CAJA_TEXTO = 40
LARGO_CAJA_TEXTO = 180
JUGANDO = 0 
fps = 60
time = pygame.time.Clock()
score = 0
vida = 100
velocidad = 5
velocidad_disparo_enemigo = 3
posicion = [ANCHO_VENTANA // 2, ALTO_VENTANA-100]

#Obtenemos los rectangulos de los botones 
rect_boton = imagen_play.get_rect()
rect_boton.y = POS_TOP_BOTON
rect_boton.x = POS_LEFT_BOTON

rect_ranking = imagen_ranking.get_rect()
rect_ranking.y = POS_TOP_PUNTOS
rect_ranking.x = POS_LEFT_PUNTOS

