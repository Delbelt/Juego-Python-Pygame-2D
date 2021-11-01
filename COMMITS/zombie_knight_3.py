import pygame, random

#VECTOR 2D PARA LOS MOVIMIENTOS DE PLATAFORMA
vector = pygame.math.Vector2 #math.Vector2 = VECTOR de 2 DIMENSIONES

#INICIALIZAR PYGAME Y TODOS SUS MODULOS:
pygame.init()

#BALDOSAS DE 32 X 32: CALCULO PARA ASIGNAR LOS ESPACIOS EN EL MAPA MATRIZ:
#SUPERFICIE DE VISUALIZACION: (32 X 32: 1280/32 = 40 ancho, 736/32 = 23 alto)

WIDTH = 1280 # ANCHO
HEIGHT = 736 # ALTO

#TESTEAR: Crear CONSTANTES para asignar el tamaño de los objetos CON LOS DATOS (ANCHO Y HEIGHT) PARA QUE REPRESENTE CORRECTAMENTE LAS IMAGENES

#INICIA LA PANTALLA PARA SU VISUALIZACION CON LOS VALORES QUE ASIGNAMOS ARRIBA:

display = pygame.display.set_mode((WIDTH, HEIGHT)) #NOMBRE DE LA PANTALLA Y DIMENSIONES
pygame.display.set_caption("Zombie Knight") #TITULO DE LA PANTALLA
icono = pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"), (100,100)) #ICONO DEL JUEGO
pygame.display.set_icon(icono) #LO AGREGO

#ESTABLECE LOS FPS Y RELOJ:
FPS = 60
clock = pygame.time.Clock() #CREA EL OBJETO DEL TIEMPO PARA CONTROLARLO

#DEFINICION DE CLASES:

    # Sprite es una imagen bidimensional que forma parte de una escena gráfica.
    # Sprite es cierto tipo de objeto que interactúa. 
    # Rect es el recorrido del objeto

#CLASES:

############################################################################################

class Juego():

    #pass = declaracion NULL de la implementacion

    def __init__(self): #INIT DEL JUEGO
        pass

    def update(self): #ACTUALIZAR JUEGO
        pass

    def dibujar(self): #HUD (Head-UP Display) = BARRA DE ESTADO
        pass        
       
    def chequear_colisiones(self): #CHEQUEA LAS COLISIONES DENTRO DEL JUEGO 
        pass  
    
    def add_enemigo(self):
        pass       

    def chequear_ronda_terminada(self): #CHEQUEA SI SOBREVIVIO A UNA NOCHE
        pass   

    def chequear_juego_terminado(self): #CHEQUEA SI EL JUGADOR PERDIO EL JUEGO
        pass
    
    def iniciar_nueva_ronda(self): #INICIA UNA NUEVA RONDA
        pass       

    def pausar_juego(self, texto_principal, texto_secundario): #PAUSA EL JUEGO - GIU
        pass

    def reiniciar_juego(self): #REINICIA EL JUEGO
        pass    

############################################################################################

class Mosaico(pygame.sprite.Sprite): #Clase que representa el MAPA MOSAICO de 32 x 32 px

    def __init__(self, x, y, imagen_numero, grupo_principal, grupo_secundario=""): #DA INICIO A LA MATRIZ DEL MAPA DE MOSAICO - EN CASO DE NO TENER SUB-GRUPO LO PASA COMO NULL O VACIO
        super().__init__()

        #CARGAR LA IMAGEN CORRECTA Y AGREGARLA AL SUB-GRUPO CORRESPONDIENTE:

        #TIERRA:
        if imagen_numero == 1:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (1).png"), (32,32))
       
        #PLATAFORMA:
        elif imagen_numero == 2:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (2).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            grupo_secundario.add(self)

        elif imagen_numero == 3:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (3).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            grupo_secundario.add(self)

        elif imagen_numero == 4:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (4).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            grupo_secundario.add(self)

        elif imagen_numero == 5:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (5).png"), (32,32)) 
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            grupo_secundario.add(self)

        #SIN IMPORTAR QUE NUMERO DE IMAGEN SEA (imagen_numero)
        #SE AGREGA AL GRUPO PRINCIPAL POR DEFECTO:

        grupo_principal.add(self)

        #OBTIENE EL RESTO DE LA IMAGEN Y LA POSICION DENTRO DE LA MATRIZ:

        self.rect = self.image.get_rect() #OBTIENE LA COORDENADA DE LA RECTA
        self.rect.topleft = (x,y) #UBICA DESDE ARRIBA-IZQUIERDA EN LAS COORDENADAS: (x,y)

        #MASCARA PARA MEJORAR LAS COLISIONES CON EL JUGADOR
        self.mascara = pygame.mask.from_surface(self.image) 
        #De esta forma la "imagen" es solo 32x32 y no tiene "Paredes invisibles"
        #El jugador (U otros objetos tambien) tambien necesita aplicarlo en sus clases.

############################################################################################

class Jugador(pygame.sprite.Sprite): #JUGADOR

    def __init__(self): #Iniciar el jugador
        pass        
       
    def update(self): #Actualizar el jugador
        pass

    def mover(self): #Movimiento del jugador
        pass

    def chequear_colisiones(self): #Chequea las colisiones del jugador con el entorno
        pass

    def chequear_animaciones(self): #Chequea las animaciones de salto y disparo
        pass

    def salto(self): #Salto del jugador
        pass

    def disparar(self): #Disparo del jugador
        pass

    def reiniciar(self): #Restablece la posicion del jugador
        pass

    def animacion(self): #Animaciones del jugador
        pass

############################################################################################

class Proyectil(pygame.sprite.Sprite): #PROYECTIL DISPARADO POR EL JUGADOR

    def __init__(self):
        pass
       
    def update(self):
        pass             

    def chequear_colision(self):
        pass
       
############################################################################################    

class Enemigo(pygame.sprite.Sprite): #ENEMIGO

    def __init__(self): #Iniciar el enemigo
        pass

    def update(self): #Actualizar el enemigo
        pass

    def mover(self): #Movimiento del enemigo       
        pass

    def chequear_colisiones(self): #Chequea las colisiones del enemigo con el entorno
        pass

    def chequear_animaciones(self): #Chequea las animaciones de muerte y ascenso
        pass

    def animacion(self, sprite_lista, speed): #Animaciones del enemigo
        pass

############################################################################################

class RubyLogo(pygame.sprite.Sprite): #Animacion del LOGO del juego - PODRIA SER OTRA COSA

    #QUIZAS PODRIA SER OTRO OBJETO O SIMPLEMENTE QUITARLO
    #PERO SE PODRIA AAGREGAR UN LOGO O ALGO EN SU REEMPLAZO

    def __init__(self, x, y, grupo_principal):
        
        super().__init__()

        #ANIMACION DE LOS FRAMES DEL RUBY
        self.logo_sprites = []

        #ANIMACION GIRATORIA:

        #ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"),(54,54)))
        self.logo_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"),(54,54)))
        
        #SE USARA COMO INDICE DE LA LISTA - INDEX
        self.indice_sprite = 0

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.logo_sprites[self.indice_sprite] 

        #OBTENGO LA RECTA (get.rect):
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        grupo_principal.add(self)        


    def update(self):

        self.animacion(self.logo_sprites, 0.25) # 0.25 ANIMACION GIRATORIA
        # .25 O 0.25 = 1/4 ---> TOMARA 4 BUCLES PARA MOVERSE HACIA EL SIGUIENTE FOTOGRAMA


    def animacion(self, sprite_list, speed): #Animacion del Ruby
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.indice_sprite < len(sprite_list) -1: #RESTA EN UNO PARA QUE COINCIDA CON INDICE
            self.indice_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.indice_sprite = 0 #PARA QUE VUELVA A EMPEZAR

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_list[int(self.indice_sprite)]

############################################################################################

class Ruby(pygame.sprite.Sprite): #Ruby: Da puntos y aumenta la salud del jugador

    def __init__(self):
        pass

    def update(self):
        pass

    def mover(self): #Movimiento del Ruby    
        pass

    def chequear_colisiones(self): #Chequea las colisiones del Ruby con el entorno
        pass

    def animacion(self, sprite_list, speed):
        pass      
 
############################################################################################

class Portal(pygame.sprite.Sprite): #Portal de teletransportacion

    def __init__(self,x,y, color, grupo_portal):  
        
        super().__init__()

        #ANIMACION DE LOS FRAMES DEL PORTAL
        self.portal_sprites = []

        #ANIMACION DEL PORTAL:

        #EN CASO DE QUE EL PORTAL SEA VERDE:        
        if color == "green":

            #ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS:            
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile000.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile001.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile002.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile003.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile004.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile005.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile006.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile007.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile008.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile009.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile010.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile011.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile012.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile013.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile014.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile015.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile016.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile017.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile018.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile019.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile020.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/green/tile021.png"),(72,72)))
        
        #EN CASO DE QUE EL PORTAL NO SEA VERDE:
        else:

            #ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS:
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile000.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile001.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile002.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile003.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile004.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile005.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile006.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile007.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile008.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile009.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile010.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile011.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile012.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile013.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile014.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile015.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile016.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile017.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile018.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile019.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile020.png"),(72,72)))
            self.portal_sprites.append(pygame.transform.scale(pygame.image.load("images/portals/purple/tile021.png"),(72,72)))

        #SE USARA COMO INDICE DE LA LISTA - INDEX
        self.indice_sprite = random.randint(0,len(self.portal_sprites)-1) #INDEX RANDOM

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.portal_sprites[self.indice_sprite] #EMPIEZA SIEMPRE DIFERENTE

        #OBTENGO LA RECTA (get.rect):
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        grupo_portal.add(self) 


    def update(self):

        self.animacion(self.portal_sprites, .2)


    def animacion(self, sprite_lista, speed):
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.indice_sprite < len(sprite_lista) -1: #RESTA EN UNO PARA QUE COINCIDA CON INDICE
            self.indice_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.indice_sprite = 0 #PARA QUE VUELVA A EMPEZAR

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_lista[int(self.indice_sprite)]

############################################################################################

#ALMACENAMIENTO DE LOS GRUPOS DE SPRITE
#(DONDE VAN TODOS LOS OBJETOS) LOS ALMACE EN UN CONTENEDOR

grupo_Mosaico = pygame.sprite.Group() #GRUPO PRINCIPAL DE SPRITES
grupo_plataforma = pygame.sprite.Group() #GRUPO DE LOS OBJETOS DENTRO DE LA PLATAFORMA
grupo_jugador = pygame.sprite.Group() #GRUPO JUGADOR
grupo_proyectil = pygame.sprite.Group() #GRUPO DE LAS RAFAGAS
grupo_enemigo = pygame.sprite.Group() #GRUPO ENEMIGO
grupo_portal = pygame.sprite.Group() #GRUPO DEL PORTAL DE TELETRANSPORTACION
grupo_ruby = pygame.sprite.Group() #GRUPO DE POTENCIADORES - BUFFERS

# MAPA DE MOSAICO: TILE MAP -  MAPA DEL JUEGO, EN SIMPLES PALABRAS O MATRIZ DEL MAPA

#REFERENCIAS:

# 0 -> NO REPRESENTA NINGUN AZULEJO (TILE) - ESPACIO VACIO
# 1 -> TIERRA
# 2-5 -> PLATAFORMAS
# 6 -> RUBI MAKER - POTENCIADOR
# 7-8 -> PORTALES 7 = VERDE ---- 8 = VIOLETA
#9 -> JUGADOR

# (23) BALDOSAS (FILAS) - (40) BALDOSAS (FILAS) COLUMNAS

#MATRIZ DEL MAPA (MAPA DE MOSAICO): EN DONDE LOS NUMEROS YA DEFINIDOS ARRIBA SERAN ASIGNADOS EN CADA POSICION
#CADA POSICION DE LA MATRIZ REPRESENTA UN AZULEJO EN EL MAPA

#Tile_map

mapa_mosaico = [

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0], #3
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #5
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10

    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4], #11
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #12
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #13
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #14
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #15
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #16
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #17
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #18
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #19
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #20

    [8, 0, 0, 0, 0, 0, 0, 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], #21
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],   #22
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]    #23

            ]

#GENERAR LOS OBJETOS DEL MAPA DE MOSAICO

#RECORRER LAS 23 FILAS:

for i in range(len(mapa_mosaico)):

    #RECORRER LAS 40 COLUMNAS:
    for j in range(len(mapa_mosaico[i])):

    #CADA CONDICION MUESTRA LOS OBJETOS CORRESPONDIENTES:

        #TIERRA:        
        if mapa_mosaico[i][j] == 1:

            Mosaico(j*32, i*32, 1, grupo_Mosaico)
            #COMO NO ES PARTE DE LA PLATAFORMA, VA AL GRUPO PRINCIPAL

        #PLATAFORMA:               
        elif mapa_mosaico[i][j] == 2:
            Mosaico(j*32, i*32, 2, grupo_Mosaico, grupo_plataforma)
            #GRUPO PLATAFORMA

        elif mapa_mosaico[i][j] == 3:
            Mosaico(j*32, i*32, 3, grupo_Mosaico, grupo_plataforma)
            #GRUPO PLATAFORMA

        elif mapa_mosaico[i][j] == 4:
            Mosaico(j*32, i*32, 4, grupo_Mosaico, grupo_plataforma)
            #GRUPO PLATAFORMA
            
        elif mapa_mosaico[i][j] == 5:
            Mosaico(j*32, i*32, 5, grupo_Mosaico, grupo_plataforma)
            #GRUPO PLATAFORMA    
        
        #RUBY MAKER:
        elif mapa_mosaico[i][j] == 6:
            RubyLogo(j*32, i*32, grupo_Mosaico)
            #COMO NO ES PARTE DE LA PLATAFORMA, VA AL GRUPO PRINCIPAL       

        #PORTALES: VERDE
        elif mapa_mosaico[i][j] == 7:
            Portal(j*32, i*32 + 35, "green", grupo_portal)
            #GRUPO PORTAL

        #PORTALES: VIOLETA
        elif mapa_mosaico[i][j] == 8:
            Portal(j*32, i*32 + 35, "purple", grupo_portal) 
            #GRUPO PORTAL
        
        #JUGADOR:
        elif mapa_mosaico[i][j] == 9:
            pass 

#FONDO DE PANTALLA - CARGA LA IMAGEN:
background_image = pygame.transform.scale(pygame.image.load("images/background.png"),(WIDTH,HEIGHT))
pygame.display.set_icon(icono) #ICONO

#pygame.transform.scale CAMBIA LA ESCALA DE LA IMAGEN(IMAGEN,(ANCHO, ALTO))
#pygame.image.load CARGA LA IMAGEN

#Superficie para rellenar con la imagen cargada:
backgroud_rect = background_image.get_rect() #RECTA (Rect) DEL SPRITE (0,0)
backgroud_rect.topleft = (0, 0) #POSICIONA DESDE ARRIBA-IZQUIERDA LA RECTA (Rect) DEL SPRITE

#CREACION DEL JUEGO

#AGREGAR EN LOS EVENTOS TECLAS PARA BAJAR O SUBIR EL VOLUMEN

#BUCLE PRINCIPAL DEL JUEGO (CICLO DE VIDA DEL JUEGO):

running = True #VARIABLE BANDERA PARA DETERMINAR SI SE ESTA EJECUTANDO EL CICLO

while running: #Mientras se este corriendo el juego:

    for evento in pygame.event.get(): #Captura los eventos dentro del juego

        if evento.type == pygame.QUIT: #Cuando el evento es igual a X (SALIR)
            running = False #Termina el ciclo del juego

    #Dibujar (blit) el fondo en la pantalla:    
    display.blit(background_image, backgroud_rect) #Superposicion (Fondo, Fondo recta)

    #DIBUJAR AZULEJOS - TILES - GRAFICOS - OBJETOS - ESTRUCTURAS - PLATAFORMA - ETC    
    grupo_Mosaico.draw(display)

    #ACTUALIZAR AZULEJOS - TILES - GRAFICOS - OBJETOS - ESTRUCTURAS - PLATAFORMA - ETC  
    grupo_Mosaico.update()

    #ACTUALIZAR Y DIBUJAR LOS GRUPOS DE SPRITES

    grupo_portal.update() #Actualiza el movimiento ciclo tras ciclo, si no se agrega los objetos quedan estaticos
    grupo_portal.draw(display)

    grupo_jugador.update() #Actualiza el movimiento ciclo tras ciclo, si no se agrega los objetos quedan estaticos
    grupo_jugador.draw(display)

    grupo_proyectil.update() #Actualiza el movimiento ciclo tras ciclo, si no se agrega los objetos quedan estaticos
    grupo_proyectil.draw(display)

    grupo_enemigo.update() #Actualiza el movimiento ciclo tras ciclo, si no se agrega los objetos quedan estaticos
    grupo_enemigo.draw(display)

    grupo_ruby.update() #Actualiza el movimiento ciclo tras ciclo, si no se agrega los objetos quedan estaticos
    grupo_ruby.draw(display)

    #ACTUALIZACION Y DIBUJO DEL JUEGO:

    #Actualiza la pantalla y los frames:
    pygame.display.update() #Actualiza la pantalla
    clock.tick(FPS) #Cuadros por segundos

#### FIN CICLO DEL JUEGO ####

#Terminado el ciclo de vida del juego:
pygame.quit() #Cierra todos los procesos utilizados de la lib Pygame