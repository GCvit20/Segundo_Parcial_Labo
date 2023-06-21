import pygame, random, colores, re, sqlite3
from constantes import * 

##########################CLASES##############################################

class Jugador():
    def __init__(self, imagen,velocidad,vida, posicion): #Parametros formales del constructor 
        self.imagen = imagen
        pygame.display.set_icon(self.imagen) #Colocamos la imagen como icono del juego
        self.velocidad_x = velocidad #Incializamos la velocidad de movimiento
        self.vida = vida
        self.posicion = posicion
        self.tiempo_colision = 0
        self.arma = [(self.posicion[0] + self.imagen.get_width()) - 80 // 2, self.posicion[1]] 

    def update(self):
        key_state = pygame.key.get_pressed() #Chequeamos si alguna tecla fue presionada

        if True in key_state:

            if key_state[pygame.K_RIGHT]:
                if self.posicion[0] < ANCHO_VENTANA - self.imagen.get_width(): #Establecemos limites para que no se salga de la pantalla
                    self.posicion[0] += self.velocidad_x
                    
            if key_state[pygame.K_LEFT]:
                
                if self.posicion[0] > 0:
                    self.posicion[0] -= self.velocidad_x
        
            self.arma = [(self.posicion[0] + self.imagen.get_width()) - 80 // 2, self.posicion[1]]
            
    
    def obtener_rectangulo(self):
        return self.imagen.get_rect(topleft=self.posicion) 

class Enemigos():
    def __init__(self,imagen,velocidad_x,recorrido_top,posicion):
        self.imagen = imagen
        self.velocidad_x = velocidad_x #Velocidad con la que se mueven las naves enemigas
        self.recorrido = 0
        self.recorrido_top = recorrido_top
        self.posicion = posicion
        self.movimiento = False
        self.colision = False
        self.tiempo_colision = 0
        self.tiempo_disparo = pygame.time.get_ticks()
        self.arma = [(self.posicion[0] + self.imagen.get_width()) - 60 // 2, self.posicion[1]]

    def update(self):
    
        self.recorrido += 1

        if self.posicion[0] < ANCHO_VENTANA - self.imagen.get_width() and self.movimiento == False:
            self.posicion[0] += self.velocidad_x
        elif self.posicion[0] >= ANCHO_VENTANA - self.imagen.get_width() and self.movimiento == False:
            self.movimiento = True
        
        if self.posicion[0] > 0 and self.movimiento == True:
            self.posicion[0] -= self.velocidad_x
        elif self.posicion[0] < 1 and self.movimiento == True:
            self.movimiento = False

        self.arma = [(self.posicion[0] + self.imagen.get_width()) - 60 // 2, self.posicion[1]]


    def blit(self,pantalla):
        pantalla.blit(self.imagen, self.posicion)

    def blit_and_update(self,grupo,pantalla):
        for i in grupo:
            i.update()
            i.blit(pantalla)

    def obtener_rectangulo(self):
        return self.imagen.get_rect(topleft=self.posicion) 

class Balas():
    def __init__(self,posicion, imagen_bala,velocidad,laser_sonido):
        self.imagen_bala = imagen_bala
        self.velocidad = velocidad
        self.posicion = posicion
        laser_sonido.play()
    
    def update(self, lista):
        self.posicion[1] -= self.velocidad #La velocidad sera asignada en el eje y
        if self.posicion[1] < 0:
            lista.remove(self)
            

    def blit(self,pantalla):
        pantalla.blit(self.imagen_bala, self.posicion)

    def blit_and_update(self,grupo,pantalla):
        for i in grupo:
            i.update(grupo)
            i.blit(pantalla)

    def obtener_rectangulo(self):
        return self.imagen_bala.get_rect(topleft=self.posicion)

class Balas_enemigas():
    def __init__(self,imagen_bala,posicion,velocidad,laser_sonido):
        self.imagen_bala = imagen_bala
        self.velocidad = velocidad
        self.posicion = posicion
        self.colision = False
        laser_sonido.play()
    
    def update(self, lista):
        
        self.posicion[1] += self.velocidad #La velocidad sera asignada en el eje y
        if self.posicion[1] > ALTO_VENTANA:
            lista.remove(self)

    def blit(self,pantalla):
        pantalla.blit(self.imagen_bala, self.posicion)

    def blit_and_update(self,lista,pantalla):
        for i in lista:
            i.update(lista)
            i.blit(pantalla)

    def obtener_rectangulo(self):
        return self.imagen_bala.get_rect(topleft=self.posicion)

##########################FUNCIONES##############################################

def puntuacion(screen,text,size,x,y):
    """
    Recibe:
    Screen: pantalla en la que se va a imprimir el texto 
    text: el texto ha imprimir
    size: el tamaño del texto
    x: posicion en el eje x
    y: posiscion en el eje y

    Esta funcion nos permite dibujar en pantalla el score que vamos obteniendo en el juego

    Retorno: Sin retorno 
    """
    
    fuente = pygame.font.SysFont('Small Fonts', size, bold=True) #bold = letra negrita
    texto_screen = fuente.render(text,True,colores.WHITE) #white color que sale y black color de fondo
    texto_rect = texto_screen.get_rect() #Obtenemos el rectangulo de la variable anterior
    texto_rect.midtop = (x,y) #Posicionamos el texto
    screen.blit(texto_screen,texto_rect) #Dibujamos en la ventana el texto y el rectangulo

def barra_vida(screen,x,y,nivel):

    """
    Recibe:
    Screen: pantalla en la que se va a imprimir la barra de vida 
    X: posicion en el eje x
    Y: posiscion en el eje y
    Nivel: nivel de vida que tendra la barra

    Esta funcion nos permite dibujar en pantalla la barra de vida de nuestra nave

    Retorno: Sin retorno 
    """

    largo = 100
    alto = 20
    fill = int((nivel/100)*largo) #El nivel era variando dependiendo de los disparos que reciba
    borde = pygame.Rect(x, y, largo, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(screen, (255,0,55), fill) #Dibujamos en pantalla la barra de vida
    pygame.draw.rect(screen, colores.BLACK, borde,4) #Dibujamos en pantalla el borde de la misma

def mostrar_ranking(archivo:str, pantalla):

    """
    Recibe:
    Archivo: ruta del archivo 
    Pantalla: pantalla en la que se va a imprimir la barra de vida 
    
    Esta funcion nos permite mostrar el ranking con los 10 mejores score ordenados de forma descendente 

    Retorno: Sin retorno 
    """


    with sqlite3.connect(archivo) as conexion:
            cursor = conexion.execute("SELECT * FROM Jugadores ORDER BY Score DESC LIMIT 10")

            encabezado = 'Nombre                   Score'
            font_nombre = pygame.font.SysFont("Arial", TAMAÑO_FUENTE_ENCABEZADO) 
            texto_nombre = font_nombre.render(encabezado, True, colores.WHITE)
            pantalla.blit(texto_nombre, (LEFT_TEXTO, TOP_TEXTO))

            for i, elemento in enumerate(cursor):
                font_nombre = pygame.font.SysFont("Arial", TAMAÑO_FUENTE)
                texto_nombre = font_nombre.render(str(elemento[1]), True, colores.WHITE)
                pantalla.blit(texto_nombre, (LEFT_TEXTO, i*30 + 100))

                font_puntos = pygame.font.SysFont("Arial", TAMAÑO_FUENTE)
                texto_puntos = font_nombre.render(str(elemento[2]), True, colores.WHITE)
                pantalla.blit(texto_puntos, (LEFT_TEXTO * 2, i*30 + 100))

def crear_tabla(archivo:str):

    """
    Recibe:
    Archivo: ruta del archivo 
    
    Esta funcion nos permite crear la tabla en la que se almacenaran los datos del jugador (Nombre y Score)

    Retorno: Sin retorno 
    """


    with sqlite3.connect(archivo) as conexion:
            try:
                sentencia = ''' create  table Jugadores
                                (
                                    Id integer primary key autoincrement,
                                    Nombre text,
                                    Score real
                                )
                            '''
                conexion.execute(sentencia)
                print("Se creo la tabla Jugadores")                       
            except sqlite3.OperationalError:
                print("La tabla Jugadores ya existe")

def add_jugador(archivo:str, texto, score):

    """
    Recibe:
    Archivo: ruta del archivo
    Texto: nombre del jugador
    Score: puntuacion obtenida
    
    Esta funcion nos permite agregar a la base de datos el nombre y la puntuacion obtenida por el jugador

    Retorno: Sin retorno 
    """

    with sqlite3.connect(archivo) as conexion:
                    try:
                        conexion.execute("insert into Jugadores(Nombre,Score) values (?,?)", (texto,score)) #Insertar dentro 
                        conexion.commit()# Actualiza los datos realmente en la tabla
                    except:
                        print("Error")
      