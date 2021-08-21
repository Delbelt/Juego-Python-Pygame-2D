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

    def __init__(self, x, y, grupo_plataforma, grupo_portal, grupo_proyectil): #Iniciar el jugador
        
        super().__init__()

        #CONSTANTES DEL JUGADOR:
        self.VELOCIDAD_HORIZONTAL = 2 #VELOCIDAD DEL JUGADOR
        self.FRICCION_HORIZONTAL = 0.15 #FRICCION EN EL DESPLAZAMIENTO (RESBALON)
        self.ACELERACION_VERTICAL = 0.8 #GRAVEDAD
        self.FUERZA_SALTO = 18 #QUE TAN ALTO SE PUEDE SALTAR
        self.VIDA_INICIAL = 100 #VIDA DEL PERSONAJE
        self.CADENCIA = 100 #VELOCIDAD DE DISPARO - MILISEGUNDOS

        #ANIMACION DE LOS FOTOGRAMAS - LISTAS VACIAS:
        self.movimiento_derecho_sprites = [] #MOVIMIENTO DERECHO
        self.movimiento_izquierdo_sprites = [] #MOVIMIENTO IZQUIERDO

        self.inactivo_derecho_sprites = [] #INACTIVIDAD DERECHO 
        self.inactivo_izquierdo_sprites = [] #INACTIVIDAD IZQUIERDO

        self.salto_derecho_sprites = [] #SALTO DERECHO
        self.salto_izquierdo_sprites = [] #SALTO IZQUIERDO

        self.ataque_derecho_sprites = [] #ATAQUE DERECHO
        self.ataque_izquierdo_sprites = [] #ATAQUE IZQUIERDO

        #### ANIMACIONES ####

        #MOVIMIENTOS: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (1).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (2).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (3).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (4).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (5).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (6).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (7).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (8).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (9).png"), (64,64)))
        self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
        for sprite in self.movimiento_derecho_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.movimiento_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

        #INACTIVO: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (1).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (2).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (3).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (4).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (5).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (6).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (7).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (8).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (9).png"), (64,64)))
        self.inactivo_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (10).png"),(64,64)))
        

       #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
        for sprite in self.inactivo_derecho_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.inactivo_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

        #SALTO: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (1).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (2).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (3).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (4).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (5).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (6).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (7).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (8).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (9).png"), (64,64)))
        self.salto_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
        for sprite in self.salto_derecho_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.salto_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

        #ATAQUE: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (1).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (2).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (3).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (4).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (5).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (6).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (7).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (8).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (9).png"), (64,64)))
        self.ataque_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
        for sprite in self.ataque_derecho_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.ataque_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

        #SE USARA COMO INDICE DE LA LISTA - INDEX
        self.indice_sprite = 0

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.inactivo_derecho_sprites[self.indice_sprite] 

        #OBTENGO LA RECTA (get.rect): Es el recorrido del objeto - En este caso el jugador
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #GRUPOS SPRITES:
        self.grupo_plataforma = grupo_plataforma
        self.grupo_portal = grupo_portal
        self.grupo_proyectil = grupo_proyectil

        #BANDERAS PARA LOS EVENTOS DISPARADORES (DISPARAR Y SALTAR)
        self.animacion_salto = False
        self.animacion_disparo = False

        #CARGA DE SONIDOS
        self.sonido_salto = pygame.mixer.Sound("sounds/jump_sound.wav") #SONIDO AL SALTAR
        self.sonido_disparo = pygame.mixer.Sound("sounds/slash_sound.wav") #SONIDO AL DISPARAR
        self.sonido_portal = pygame.mixer.Sound("sounds/portal_sound.wav") #SONIDO PORTAL
        self.sonido_daño = pygame.mixer.Sound("sounds/player_hit.wav") #SONIDO AL DAÑARSE

        #VECTORES DE CINEMATICAS - AUXILIARES
                
        self.posicion = vector(x,y) #VECTOR DE POSICION
        self.velocidad = vector(0,0) #VELOCIDAD INICIAL Y VELOCIDAD DE ARRESTRE (NO SE DESPLAZA SOLO)
        self.aceleracion = vector(0, self.ACELERACION_VERTICAL) #ACELERACION Y GRAVEDAD

        #VALORES INICIALES DEL JUGADOR - INICIO - REINICIO

        self.vida = self.VIDA_INICIAL
        self.posicion_inicial_x = x #POSICION COORDENADA X
        self.posicion_inicial_y = y #POSICION COORDENADA Y
        self.ultimo_disparo = 0 #TIEMPO INICIAL DE DISPARO


    def update(self): #Actualizar el jugador

        #SE ELIGE SEPARAR LAS FUNCIONES PARA TENER UN MEJOR CONTROL DE CADA UNA:

        self.mover() #MOVIMIENTO DEL JUGADOR
        self.chequear_colisiones() #CHEQUEA LAS COLISIONES
        self.chequear_animaciones() #CHEQUEA LAS ANIMACIONES (SI TIENE QUE DISPARAR EVENTO)

        #CREACION DE LA MASCARA PARA MEJORAR LA PRECISION DE LAS COLISIONES
        self.mascara = pygame.mask.from_surface(self.image)
    

    def mover(self): #Movimiento del jugador
        
        #VECTOR DE ACELERACION
        self.aceleracion = vector(0, self.ACELERACION_VERTICAL)

        #PULSACION DE TECLAS: ESTABLECE EL COMPONENTE DE ACELERACION != DE CERO

        teclas = pygame.key.get_pressed() #TECLAS = VERIFICA SI SE TOCO UNA TECLA

        if teclas[pygame.K_LEFT]: #SE PULSO LA IZQUIERDA? SI:

            self.aceleracion.x = -1 * self.VELOCIDAD_HORIZONTAL
            self.animacion(self.movimiento_izquierdo_sprites, 0.5) #AGREGO LA ANIMACION AL MOVIMIENTO

        elif teclas[pygame.K_RIGHT]: #SE PULSO LA DERECHA? SI:

            self.aceleracion.x = self.VELOCIDAD_HORIZONTAL
            self.animacion(self.movimiento_derecho_sprites, 0.5) #AGREGO LA ANIMACION AL MOVIMIENTO

        else: #SI NO ESTOY TOCANDO NINGUNA TECLA ENTONCES: (REPOSO)

            if self.velocidad.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animacion(self.inactivo_derecho_sprites, 0.5) #MOVIMIENTO INACTIVO DERECHO

            else: #Entonces se estaba moviendo hacia la izquierda <--
                self.animacion(self.inactivo_izquierdo_sprites, 0.5) #MOVIMIENTO INACTIVO IZQUIERDO

        #CALCULAR LOS VALORES DE LAS CINEMATICAS:        

        #CUANTO MAS RAPIDO NOS MOVEMOS MAS FRICCION RECIBIMOS:
        self.aceleracion.x -= self.velocidad.x * self.FRICCION_HORIZONTAL #AÑADIMOS FRICCION
        
        #MATEMATICA VECTORIAL (5, 2) + (6, 1) = (11, 3)
        
        self.velocidad += self.aceleracion #ACTUALIZA EL VECTOR DE VELOCIDAD

        self.posicion += self.velocidad + 0.5 * self.aceleracion #ACTUALIZA EL VECTOR DE POSICION        

        #ACTUALIZAR LA RECTA (rect) BASADA EN LOS CALCULOS CINEMATICOS:
        
        #CONDICIONES PARA QUE EL JUGADOR PASE DE UN LADO A OTRO DE LA PANTALLA        

        if self.posicion.x < 0: #Posicion Jugador menor a 0

            self.posicion.x = WIDTH

        elif self.posicion.x > WIDTH: #Posicion Jugador mayor a la pantalla

            self.posicion.x = 0

        #SE PUEDE CAMBIAR PARA QUE EL JUGADOR NO PUEDA SALIR DE LA PANTALLA - INVIRTIENDO LOS COMPARADORES < >

        #DESPUES DE QUE SE ACTUALICEN TODOS LOS VECTORES CORREGIMOS LA POSICION:

        self.rect.bottomleft = self.posicion


    def chequear_colisiones(self): #Chequea las colisiones del jugador con el entorno
        
        if self.velocidad.y > 0:
            #spritecollide(Grupo a comprobar, Grupo A Colisionar, Desaparecer objeto al chocar?, + mascara)
            colision_plataforma = pygame.sprite.spritecollide(self, self.grupo_plataforma, False, pygame.sprite.collide_mask) #COMPRUEBA COLISION
            #pygame.sprite.collide_mask = MASCARA DE PRECISION FRENTE A LAS COLISIONES - CONECTADO CON CLASE: MOSAICO

            #Tambien se puede usar para dañar al objeto colisionado
            if colision_plataforma: #SI LA LISTA >> NO << ESTA VACIA:
                
                #IGUALA LA POSICION AL OBJETO QUE CHOCA + NUMERO: DE REBOTE AL CHOCAR.
                self.posicion.y = colision_plataforma[0].rect.top + 7 #+ NUMERO = VIBRACION DE COLISION
                self.velocidad.y = 0 #ASEGURA QUE SE DEJE DE MOVER 

        #Chequea las colisiones cuando el jugador esta saltando:
        if self.velocidad.y < 0:
            colision_plataforma = pygame.sprite.spritecollide(self,self.grupo_plataforma, False, pygame.sprite.collide_mask)    

            if colision_plataforma: #Si colisiona:
                self.velocidad.y= 0 #ASEGURA QUE SE DEJE DE MOVER
                
                # BUCLE - MOVIMIENTO INCREMENTAL DE LA POSICION DEL JUGADOR:
                # While: Mientras el jugador colisione con algun objeto de la plataforma:
                while pygame.sprite.spritecollide(self, self.grupo_plataforma, False, pygame.sprite.collide_mask):
                    
                    self.posicion.y += 1 #POSICION DEL JUGADOR + N PIXEL
                    self.rect.bottomleft = self.posicion #SALTA, COLISIONA, Y LUEGO CAE
        
        #Chequea las colisiones con los portales:
        if pygame.sprite.spritecollide(self, self.grupo_portal, False, pygame.sprite.collide_mask):

            self.sonido_portal.play() #Activa el sonido del portal

            #Una vez que colisiona, determinar a que portal se movera:

            #IZQUIERDA Y DERECHA:

            #Si es mayor a la mitad HORIZONTAL, estas en el LADO DERECHO
            if self.posicion.x > WIDTH / 2: #Centro de la pantalla Horizontalmente
                #Desde ABAJO a la DERECHA (Portal verde) a IZQUIERDA ARRIBA
                #Desde ARRIBA a la DERECHA (Portal violeta) a IZQUIERDA ABAJO 
                self.posicion.x = 86 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas en el LADO IZQUIERDO
                self.posicion.x = WIDTH - 150 #150 Pixeles
                #Desde ARRIBA a la IZQUERDA (Portal verde) a DERECHA ABAJO
                #Desde ABAJO a la IZQUIERDA (Portal violeta) a ARRIBA DERECHA

            #ARRIBA Y ABAJO:

            #Si es mayor a la mitad VERTICAL, estas ARRIBA
            if self.posicion.y > HEIGHT / 2: #Centro de la pantalla Verticalmente
                self.posicion.y = 64 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas ABAJO
                self.posicion.y = HEIGHT - 132 #132 Pixeles

            self.rect.bottomleft = self.posicion #Guarda la posicion en la recta


    def chequear_animaciones(self): #Chequea las animaciones de salto y disparo
        
        #CHEQUEO DE SALTO:
        if self.animacion_salto: #La animacion de SALTO esta activada? SI:

            if self.velocidad.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animacion(self.salto_derecho_sprites, 0.1) #MOVIMIENTO SALTO DERECHO

            else: #Significa que el movimiento era hacia la izquierda <--
                self.animacion(self.salto_izquierdo_sprites, 0.1) #MOVIMIENTO SALTO IZQUIERDO

        #CHEQUEO DE DISPARO:
        if self.animacion_disparo: #La animacion de DISPARO esta activada? SI:

            if self.velocidad.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animacion(self.ataque_derecho_sprites, 0.25) #MOVIMIENTO SALTO DERECHO

            else: #Significa que el movimiento era hacia la izquierda <--
                self.animacion(self.ataque_izquierdo_sprites, 0.25) #MOVIMIENTO SALTO IZQUIERDO


    def salto(self): #Salto del jugador
        
        #El jugador esta colisionando con algun objeto de la plataforma?
        if pygame.sprite.spritecollide(self, self.grupo_plataforma, False): #SI:
            
            self.sonido_salto.play() #Reproduce el sonido del salto
            #Para saltar: nuestra velocidad de salto VERTICAL tiene que ser negativa:
            self.velocidad.y = -1 * self.FUERZA_SALTO
            #Activo la animacion de salto:
            self.animacion_salto = True


    def disparar(self): #Disparo del jugador
        
        self.sonido_disparo.play() #Reproduce el sonido del disparo
        #Le paso a la clase: las coordenadas del jugador, el grupo y el jugador
        Proyectil(self.rect.centerx, self.rect.centery, self.grupo_proyectil, self)
        self.animacion_disparo = True #Activa la bandera de disparo


    def reiniciar(self): #Restablece la posicion del jugador
        
        self.velocidad = vector(0,0) #REINICIO LA VELOCIDAD
        self.posicion = vector(self.posicion_inicial_x, self.posicion_inicial_y) #GUARDO LA POSICION CON LOS VALORES INICIALES
        self.rect.bottomleft = self.posicion #LLEVO AL JUGADOR A LA POSICION INICIAL


    def animacion(self, sprite_lista, velocidad): #Animaciones del jugador

        #sprite_list[]: Lista que contiene las animaciones correspondientes

        if self.indice_sprite < len(sprite_lista) -1: #RESTA EN UNO PARA QUE COINCIDA CON INDICE
            self.indice_sprite += velocidad #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.indice_sprite = 0 #PARA QUE VUELVA A EMPEZAR

            #COMPROBAR QUE TERMINO LA ANIMACION DE SALTO:
            if self.animacion_salto: #SI ESTA ACTIVADO LA ANIMACION:
                self.animacion_salto = False #LA DESACTIVA PORQUE O SINO TIENDE AL INFINITO

            #COMPROBAR QUE TERMINO LA ANIMACION DE DISPARO:
            if self.animacion_disparo: #SI ESTA ACTIVADO LA ANIMACION:
                self.animacion_disparo = False #LA DESACTIVA PORQUE O SINO TIENDE AL INFINITO                     

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_lista[int(self.indice_sprite)]

############################################################################################

class Proyectil(pygame.sprite.Sprite): #PROYECTIL DISPARADO POR EL JUGADOR

    def __init__(self, x, y, grupo_proyectil, jugador):

        super().__init__()

        #VARIABLES CONSTANTES DE LA MUNICION TESTEAR
        self.velocidad = 20 #VELOCIDAD NO AFECTADA POR LA GRAVEDAD
        self.RANGO = 500 #RANGO <= LUEGO SE DESTRUYE
        
        #ANIMACION DEL PROYECTIL:

        #CONDICIONES PARA ASEGURAR QUE LA ANIMACION SEA LA CORRECTA + CARGA DE LA MISMA

        if jugador.velocidad.x > 0: #Significa que el movimiento es hacia la derecha -->
            
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"),(32,32))

        else: #Significa que el movimiento es hacia la izquierda <--

            #Reutilizo la misma imagen, y la reverso con FLIP: (PRIMER BOOLEAN: "DAR VUELTA HORIZONTALMENTE", SEGUNDO BOOLEAN: "DAR VUELTA VERTICALMENTE")
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/player/slash.png"), True, False), (32,32))
            self.velocidad = -1 * self.velocidad #Garantiza que el disparo tenga orientacion izquierda

        #RECORRIDO DE LA RECTA (rect):

        self.rect = self.image.get_rect() #OBTENGO LA DIRECCION DE PROYECTIL
        self.rect.center = (x,y) #SALDRA DESDE EL CENTRO DE LA POSICION QUE ESTE

        self.posicion_inicial_x = x #POSICION INICIAL DE LA BALA

        grupo_proyectil.add(self)#Lo agrego al grupo de las municiones

    def update(self):        
        
        self.rect.x += self.velocidad #Acumulo en el recorrido el movimiento de la bala
        #self.chequear_colision() TESTEAR           

        #DESTRUCCION de la bala si supera el RANGO

        #ABS: Devuelve el valor absoluto del número dado = DISTANCIA = MODULO |abs|
        if abs(self.rect.x - self.posicion_inicial_x) > self.RANGO:

            self.kill() #destruye el objeto - en este caso la bala

    def chequear_colision(self):
        #SI EL PROYECTIL COLISIONA CON EL PORTAL: (CONTINUAR...) TESTEAR
        lista_colision = pygame.sprite.groupcollide(grupo_proyectil, grupo_portal, False, False) #Diccionario que guarda las colisiones        

        if lista_colision: #SI HAY COLISION: 

            for proyectiles in lista_colision.values():
                for proyectil in proyectiles:

                    if jugador.posicion.x > WIDTH / 2:                        
                        jugador.sonido_portal.play() #Activa el sonido del portal
                        #Una vez que colisiona, determinar a que portal se movera 
       
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
            #(32 - 25 = POSICION IZQUIERDA) ---- (32 + 35 = POSICION ARRIBA O ABAJO)    
            jugador = Jugador(j*32 - 25, i*32 + 32, grupo_plataforma, grupo_portal, grupo_proyectil) 
            grupo_jugador.add(jugador)
            #GRUPO JUGADOR

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

        if evento.type == pygame.KEYDOWN:
        #El evento KEYDOWN se produce cuando se presiona una tecla:    

            if evento.key == pygame.K_SPACE: #BARRA ESPACIADORA
                jugador.salto() #SALTAR
  
            if evento.key == pygame.K_x: #TECLA X 

                primer_disparo = pygame.time.get_ticks()
                
                #CONTROLA LA VELOCIDAD DE LAS RAFAGAS
                if primer_disparo - jugador.ultimo_disparo > jugador.CADENCIA: 
                    #TESTEAR: SE HACE CADA VEZ MAS LENTO DISPARAR POR LA CADENCIA AUMENTADA
                    jugador.disparar() #DISPARAR
                    jugador.ultimo_disparo = primer_disparo #IMPORTANTE MODIFICAR EL VALOR

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