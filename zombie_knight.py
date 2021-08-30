import pygame, random

#VECTOR 2D PARA LOS MOVIMIENTOS DE PLATAFORMA
vector = pygame.math.Vector2 #math.Vector2 = VECTOR de 2 DIMENSIONES

#INICIALIZAR PYGAME Y TODOS SUS MODULOS:
pygame.init()

#BALDOSAS DE 32 X 32: CALCULO PARA ASIGNAR LOS ESPACIOS EN EL MAPA MATRIZ:
#SUPERFICIE DE VISUALIZACION: (32 X 32: 1280/32 = 40 ancho, 736/32 = 23 alto)
#NOS DA UNA MATRIZ DE [40][23] SE MULTIPLICA POR 32, QUE SON EL TAMAÑO DE LAS TEXTURAS DE LOS MOSAICOS

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

    def __init__(self, jugador, grupo_enemigo, grupo_plataforma, grupo_portal, grupo_proyectil, grupo_ruby): #INIT DEL JUEGO
        
        #VARIABLES CONSTANTES
        self.TIEMPO_RONDA = 15 #Duracion de cada ronda
        self.TIEMPO_SPAM_ENEMIGO = 5 #TIEMPO PARA SPAMEAR UN ENEMIGO

        #VALORES DEL JUEGO:
        self.score = 0 #PUNTUACION INICIAL
        self.ronda_numero = 1 #INICIO DE RONDA
        self.contador_fps = 0 #CONTEO DE FOTOGRAMAS
        self.tiempo_ronda = self.TIEMPO_RONDA #Duracion de la ronda
        self.tiempo_spam_enemigo = self.TIEMPO_SPAM_ENEMIGO #TIEMPO DE SPAM
        self.modo_juego = False #TRUE = MODO ATURDIR - FALSE = MODO DAÑO

        #MODO ATURDIR = CUANDO UN PROYECTIL COLISIONA CON EL ENEMIGO, LO ATURDE Y EL JUGADOR TIENE QUE "PISARLO" PARA ELIMINARLO
        #MODO DAÑO = EL ENEMIGO RECIBE DAÑO POR PROYECTIL, TIENE UN LEVE RETROCESO POR DISPARO - EL ENEMIGO NO SE ATURDE, NI SE PISA.

        #VALORES DE LAS FUENTE

        self.titulo_fuente = pygame.font.Font("fonts/Poultrygeist.ttf", 48) #FUENTE DEL TITULO
        self.HUD_fuente = pygame.font.Font("fonts/Pixel.ttf", 24) #FUENTE DE LA BARRA DE ESTADO

        #SONIDOS:
        self.perdida_ruby_sonido = pygame.mixer.Sound("sounds/lost_ruby.wav") #Choca con un enemigo
        self.agarrar_ruby_sonido = pygame.mixer.Sound("sounds/ruby_pickup.wav") #Choca con nosotros
        pygame.mixer.music.load("sounds/level_music.wav") #MUSICA DE FONDO     

        #GRUPOS Y SPRITES:
        self.jugador = jugador
        self.grupo_enemigo = grupo_enemigo
        self.grupo_plataforma = grupo_plataforma
        self.grupo_portal = grupo_portal
        self.grupo_proyectil = grupo_proyectil
        self.grupo_ruby = grupo_ruby              


    def update(self): #ACTUALIZAR JUEGO
        
        self.contador_fps += 1 #CUENTA LOS FPS

        if self.contador_fps % FPS == 0: #CONDICION PARA IR RESTANDO TIEMPO A LA RONDA

            self.tiempo_ronda -= 1 #Decrece el tiempo
            self.contador_fps = 0

        #CHEQUEAR LAS COLISIONES DEL JUEGO
        self.chequear_colisiones()

        #CREA AL ENEMIGO SI CUMPLE EL TIEMPO DE CREACION:
        self.add_enemigo()

        #TERMINA LA RONDA SI SE CUMPLE EL TIEMPO:
        self.chequear_ronda_terminada()

        #VERIFICA SI EL JUEGO TERMINO:
        self.chequear_juego_terminado()


    def dibujar(self): #HUD (Head-UP Display) = BARRA DE ESTADO
        
        #VALORES DE LOS COLORES:
        WHITE = (255, 255, 255) #BLANCO
        GREEN = (25, 200, 25) #VERDE

        #TEXTOS DENTRO DEL JUEGO - HUD BARRAS DE ESTADO:

        # topleft = ARRIBA A PARTIR DE LA IZQUIERDA
        # topright = ARRIBA A PARTIR DE LA DERECHA
        # center = CENTRO 
        # Render(Texto, Anti-Aliasing, Color)             

        score_texto = self.HUD_fuente.render("Score: " + str(self.score), True, WHITE) #DONDE MUESTRA EL PUNTAJE
        score_rect = score_texto.get_rect() #OBTENGO LA POSICION DE LA RECTA
        score_rect.topleft = (10, HEIGHT - 50) #POSICION DE LOS PUNTOS 

        vida_texto = self.HUD_fuente.render("Vida: " + str(self.jugador.vida), True, WHITE) #VIDA EN PANTALLA
        vida_rect = vida_texto.get_rect() #OBTENGO LA POSICION DE LA RECTA
        vida_rect.topleft = (10, HEIGHT - 25) #POSICION DE LA VIDA  

        titulo_texto = self.titulo_fuente.render("Zombie Knight", True, GREEN) #TITULO      
        titulo_rect = titulo_texto.get_rect() #OBTENGO LA POSICION DE LA RECTA
        titulo_rect.center = (WIDTH // 2, HEIGHT - 25) #POSICION TITULO DEL GIU

        ronda_texto = self.HUD_fuente.render("Noche: " + str(self.ronda_numero), True, WHITE) #NUMERO DE RONDA
        ronda_rect = ronda_texto.get_rect() #OBTENGO LA POSICION DE LA RECTA
        ronda_rect.topright = (WIDTH - 10, HEIGHT - 50) #RONDAS COMPLETADAS

        tiempo_text = self.HUD_fuente.render("Amanece en: " + str(self.tiempo_ronda), True, WHITE) #TIEMPO RESTANTE PARA QUE TERMINE LA NOCHE
        tiempo_rect = tiempo_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        tiempo_rect.topright = (WIDTH - 10, HEIGHT - 25)

        #DIBUJOS DEL HUD - HAY QUE AGREGARLOS PARA QUE APAREZCAN:

        display.blit(score_texto, score_rect) #DIBUJO: PUNTAJE
        display.blit(vida_texto, vida_rect) #DIBUJO: VIDA
        display.blit(titulo_texto, titulo_rect) #DIBUJO: TITULO
        display.blit(ronda_texto, ronda_rect) #DIBUJO: RONDAS
        display.blit(tiempo_text, tiempo_rect) #DIBUJO: TIEMPO


    def add_enemigo(self): #AGREGA LOS ZOMBIES AL JUEGO
        
        #COMPROBAR EL TIEMPO:
        if self.contador_fps % FPS == 0: #Si es igual, sabemos que paso 1 segundo

            #Crear unicamente SI paso el tiempo de creacion:
            if self.tiempo_ronda % self.tiempo_spam_enemigo == 0: #CREA SI SON DIVISIBLES
                
                #TESTEAR - VELOCIDAD DE LOS ENEMIGOS
                                                                            #VELOCIDAD MINIMA  - VELOCIDAD MAXIMA
                enemigo = Enemigo(self.grupo_plataforma, self.grupo_portal, self.ronda_numero, 5 + self.ronda_numero)
                self.grupo_enemigo.add(enemigo)


    def chequear_colisiones(self): #CHEQUEA LAS COLISIONES DENTRO DEL JUEGO
        
        #group-collide(Grupo 1, Grupo 2, Desaparece GRUPO 1?, Desaparece GRUPO 2?)
        colision_dict = pygame.sprite.groupcollide(self.grupo_proyectil, self.grupo_enemigo, True, False) #Diccionario que guarda las colisiones        

        if colision_dict: #SI HAY COLISION: 

            for enemigos in colision_dict.values():
                for enemigo in enemigos:

                    #TESTEAR:

                    # 1) SE PODRIA AGREGAR OTRO TIPO DE ATAQUE - MAS FUERTE - CON OTRA TECLA
                    # 2) UNA POSIBILIDAD % DE ABATIR AL RIVAL EN EL MODO DAÑO                    
                    # 3.1) SACAR MENOS DAÑO CADA RONDA
                    # 3.2) ENEMIGO: SACAR EN CADA RONDA MAS DAÑO
                    # 4) CUANDO MUERE UN ENEMIGO: AGREGAR UN PORCENTAJE PARA QUE SALGAN LOS POTENCIADORES Y CADA RONDA IR RESTANDOLA
                    # 5) MODIFICAR LOS POTENCIADORES: A) UNO TE DA PUNTAJE (MAS POSIBILIDAD DE SALIR) B) UNO QUE DE VIDA (OTRA ANIMACION O COLOR) CON MENOS POSIBILIDAD DE SALIR (DENTRO DE LA POSIBILIDAD TOTAL)
                    # 6) MODO ATURDIR: AGREGAR A LA ROTACION DE LADO: UN PORCENTAJE PARA QUE CAMBIE DE ORIENTACION Y NO EL 100% DE LOS DISPAROS
                    # 7) MODO ATURDIR: EN BASE AL CASO DE USO: 6) DECRECER LA POSIBILIDAD DE CAMBIAR LA ORIENTACION AL DISPARARLE AL PASAR LAS RONDAS
                    # 8) MODO ATURDIR: REUTILIZAR CASO DE USO: 2) PARA EL MODO ATURDIR, QUE NO ATURDA AL PRIMER DISPARO, QUE DISMINUYA LA POSIBILIDAD CADA RONDA
                    # 9) PUNTAJE: QUE SEA DINAMICO EL PUNTAJE ENTRE UN RANGO DE PUNTOS Y NO ESTATICO
                    # 10) ENEMIGOS Y LOS POTENCIADORES: ¿MODIFICAR EL EFECTO? ¿AGREGARLE ALGO MAS? ¿POTENCIAR AL ENEMIGO? ¿OTRO?                 
                                        
                    #MODO JUEGO: #TRUE = MODO ATURDIR - FALSE = MODO DAÑO 
                                          
                    enemigo.sonido_daño.play()
                    enemigo.esta_abatido = self.modo_juego #ENEMIGO TUMBADO #SIN ESTO EL ZOMBIE SIGUE EN PIE - AL ESTAR ASOCIADO AL MODO DE JUEGO SE CAMBIA "AUTOMATICO"
                    enemigo.animacion_abatido = self.modo_juego #ANIMACION DE TUMBADO #SIN ESTO NO HAY ANIMACION - AL ESTAR ASOCIADO AL MODO DE JUEGO SE CAMBIA "AUTOMATICO"                                                                                 
                                                            
                    #RETROCEDE LOS ENEMIGOS DEPENDIENDO DONDE ESTE UBICADO EL JUGADOR:     
                                    
                    if self.jugador.velocidad.x < 0: #SI EL JUGADOR ESTA EN LA DERECHA:                                          
                        
                        if not self.modo_juego: #CONDICION MODO DAÑO

                            enemigo.posicion.x -= 20 #LO RETROCEDE PARA LA IZQUIERDA + CUANTO RETROCESO
                            enemigo.rect.bottomleft = enemigo.posicion

                            enemigo.vida -= 50 #CADA DISPARO LE SACA VIDA AL ENEMIGO - 3) SACAR MENOS DAÑO CADA RONDA  

                            if enemigo.vida <= 0: #SI SE QUEDA SIN VIDA:
                                    enemigo.sonido_eliminado.play()                                           
                                    enemigo.kill() #ELIMINA AL ZOMBIE
                                    self.score += 25 #SUMA PUNTAJE

                                    #Crea un potenciador cuando matamos un enemigo
                                    #5) Modificar la posibilidad de salida de los potenciadores
                                    ruby = Ruby(self.grupo_plataforma, self.grupo_portal)
                                    self.grupo_ruby.add(ruby)
                            
                        if enemigo.direccion == 1 and self.modo_juego:  #SI EL ZOMBIE VA PARA LA DERECHA: - (PARA EVITAR QUE ROTE EN CADA GOLPE) - MODO ATURDIR                           

                                enemigo.direccion = enemigo.direccion * -1 #CAMBIA LA ORIENTACION DE LA ANIMACION
                                enemigo.velocidad = enemigo.velocidad * -1 #CAMBIA LA ORIENTACION DE MOVIMIENTO (SI IBA A LA DERECHA, VA A LA IZQUIERDA, ETC)                                                  

                    else: #SI EL JUGADOR ESTA EN LA IZQUIERDA

                            if not self.modo_juego: #CONDICION MODO DAÑO
                                enemigo.posicion.x += 20 #LO RETROCEDE PARA LA IZQUIERDA
                                enemigo.rect.bottomleft =  enemigo.posicion

                                enemigo.vida -= 50 #CADA DISPARO LE SACA VIDA AL ENEMIGO - 3) SACAR MENOS DAÑO CADA RONDA  

                                if enemigo.vida <= 0: #SI SE QUEDA SIN VIDA:

                                    enemigo.sonido_eliminado.play()                                           
                                    enemigo.kill() #ELIMINA AL ZOMBIE
                                    self.score += 25 #SUMA PUNTAJE

                                    #Crea un potenciador cuando matamos un enemigo
                                    #5) Modificar la posibilidad de salida de los potenciadores
                                    ruby = Ruby(self.grupo_plataforma, self.grupo_portal)
                                    self.grupo_ruby.add(ruby)

                            if enemigo.direccion == -1 and self.modo_juego: #SI EL ZOMBIE VA PARA LA IZQUIERDA - PARA EVITAR QUE ROTE EN CADA GOLPE - MODO ATURDIR

                                enemigo.direccion = enemigo.direccion * -1 #CAMBIA LA ORIENTACION DE LA ANIMACION
                                enemigo.velocidad = enemigo.velocidad * -1 #CAMBIA LA ORIENTACION DE MOVIMIENTO (SI IBA A LA DERECHA, VA A LA IZQUIERDA, ETC)
                                
        #SI UN JUGADOR PISA EL ENEMIGO (MODO ABATIR) O CHOCO CON OTRO ENEMIGO:
        lista_colision = pygame.sprite.spritecollide(self.jugador, self.grupo_enemigo, False)

        if lista_colision: #RECORRE LA LISTA:
            for enemigo in lista_colision:
                
                if enemigo.esta_abatido == True: #Si el enemigo esta tumbado: - Por lo tanto, si el "MODO DAÑO" esta activado, esta se desactiva

                    enemigo.sonido_eliminado.play() #Sonido de eliminar
                    enemigo.kill() #Elimina el objeto
                    self.score += 25 #Agrega N puntos por eliminarlo

                    #Crea un potenciador cuando matamos un enemigo
                    ruby = Ruby(self.grupo_plataforma, self.grupo_portal)
                    self.grupo_ruby.add(ruby)

                else: #SI EL ENEMIGO NOS TOCA:

                    self.jugador.vida -= 20 #Nos resta N puntos de vida
                    self.jugador.sonido_daño.play() #Sonido de daño 
                    
                    #TAMBIEN SE PODRIA AGREGAR QUE EL PERSONAJE NO PUEDA RECIBIR DAÑO POR 2 SEGUNDOS, EN VEZ DE CORRERLO, COMO UNA "CAPA DE PROTECCION"
                    #EVITAR QUE EL JUGADOR SIGA RECIBIENDO DAÑO CONTINUO:
                    self.jugador.posicion.x -= 200 * enemigo.direccion #LO DESPLAZA AL JUGADOR A OTRA POSICION  - TESTEAR
                    self.jugador.rect.bottomleft = self.jugador.posicion
        
        #SI EL JUGADOR COLISIONA CON EL POTENCIADOR        
        if pygame.sprite.spritecollide(self.jugador, self.grupo_ruby, True): #True porque queremos que desaparezca cuando colisiona

            #if tipo = numero: entonces --> Haga algo
            
            self.agarrar_ruby_sonido.play() #Reproduce la musica cuando AGARRA el potenciador
            self.score += 100 #La puntuacion que aumenta
            self.jugador.vida += 10 #La vida que otorga al jugador

            #Si la vida del potenciador supera la inicial: #SE PUEDE QUITAR O MODIFICAR EN EL FUTURO
            if self.jugador.vida > self.jugador.VIDA_INICIAL:
                self.jugador.vida = self.jugador.VIDA_INICIAL #Le asigna la vida limite establecida

        #SI EL ENEMIGO COLISIONA CON EL POTENCIADOR 
        for enemigo in self.grupo_enemigo: #RECORRE TODOS LOS ENEMIGOS

            if enemigo.esta_abatido == False: #El enemigo NO puede estar aturdido para agarrar el BUFF

                if pygame.sprite.spritecollide(enemigo, self.grupo_ruby, True): #True porque queremos que desaparezca cuando colisiona
            
                    self.perdida_ruby_sonido.play() #Reproduce la musica cuando ROMPEN el potenciador
                    #AGREGA UN ENEMIGO AL JUEGO, SI LO AGARRAN ELLOS:                    
                    enemigo = Enemigo(self.grupo_plataforma, self.grupo_portal, self.ronda_numero, 5 + self.ronda_numero)
                    self.grupo_enemigo.add(enemigo)                 
              

    def chequear_ronda_terminada(self): #CHEQUEA SI SOBREVIVIO A UNA NOCHE
        
        if self.tiempo_ronda == 0:
           self.iniciar_nueva_ronda() 


    def chequear_juego_terminado(self): #CHEQUEA SI EL JUGADOR PERDIO EL JUEGO
        
        if self.jugador.vida <= 0: #SI EL JUGADOR MUERE:

            pygame.mixer.music.stop()
            self.contador_fps = 0 #Vuelvo el contador a 0 antes del reinicio para que la "P - Pausa" no se clickear
            self.pausar_juego("Game Over! Final Score:" + str(self.score), "Presiona 'Enter' para jugar otra vez")
            self.reiniciar_juego()


    def iniciar_nueva_ronda(self): #INICIA UNA NUEVA RONDA
        
        self.ronda_numero += 1 #INCREMENTA LAS RONDAS        

        #MODIFICACIONES DEL JUEGO QUE VAN A IR SUBIENDO O DISMINUYENDO RONDA TRAS RONDA:
        if self.ronda_numero < self.TIEMPO_SPAM_ENEMIGO:
            self.tiempo_spam_enemigo -= 1 #Tiempo de creacion de los enemigos disminuye
        
        #TESTEAR

        # AUMENTAR EL TIEMPO DE RAFAGA
        # RESTARLE VELOCIDAD AL JUGADOR
        # AUMENTARLE LA VIDA A LOS ENEMIGOS (SI ESTAMOS EN MODO DAÑO)                

        #RESET DE LOS VALORES DE LA RONDA.
        self.tiempo_ronda = self.TIEMPO_RONDA + self.ronda_numero #AUMENTA EL TIEMPO DE RONDAS
        self.grupo_enemigo.empty() #ELIMINA LOS ENEMIGOS
        self.grupo_ruby.empty() #ELIMINA LOS POTENCIADORES
        self.grupo_proyectil.empty() #ELIMINA LOS PROYECTILES
        self.jugador.reiniciar() #REINICIA AL JUGADOR

        self.pausar_juego("Has sobrevivido la noche!", "Presiona 'Enter' para continuar")
    

    def pausar_juego(self, texto_principal, texto_secundario): #PAUSA EL JUEGO - GIU

        #SE PODRIA AGREGAR OTRO TIPO DE PAUSA QUE SOLO SEA PARA LA INTRO DEL JUEGO
        #PARA QUE SE DIFERENCIA LA INTERFAZ DE PAUSA Y EL INICIO DEL JUEGO
        #SE PUEDE AGREGAR COMO PLANTILLA PARA OTRAS GUIS
        
        global running

        pygame.mixer.music.pause()

        #ESTABLECE COLORES EN LA PAUSA - EFECTOS:

        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (25, 200, 25)

        #TEXTO PRINCIPAL:

        texto_principal = self.titulo_fuente.render(texto_principal, True, GREEN) #Renderiza el texto
        texto_principal_rect = texto_principal.get_rect() #Guardo la posicion de la recta del texto, en el trazo.
        texto_principal_rect.center = (WIDTH // 2, HEIGHT // 2) #Posicion de la recta

        #TEXTO SECUNDARIO:

        texto_secundario = self.titulo_fuente.render(texto_secundario, True, WHITE) #Renderiza el texto
        texto_secundario_rect = texto_secundario.get_rect() #Guardo la posicion de la recta del texto, en el trazo.
        texto_secundario_rect.center = (WIDTH // 2, HEIGHT // 2 + 64) #Posicion de la recta

        #DIBUJOS DE PAUSA - HAY QUE AGREGARLOS PARA QUE APAREZCAN:
        display.fill(BLACK) #SOBRE-ESCRIBE LO QUE ESTABA EN EL DISPLAY
        display.blit(texto_principal, texto_principal_rect) #DIBUJO: PUNTAJE
        display.blit(texto_secundario, texto_secundario_rect) #DIBUJO: VIDA  
        
        pygame.display.update() #ACTUALIZA LA PANTALLA             

        #PAUSA EL JUEGO HASTA PULSAR ENTER - SALIR

        #CICLO DE VIDA DE LA PAUSA:

        en_pausa = True
        nuevo_juego = True

        while en_pausa: #Pausa = True

            for evento in pygame.event.get():

                #El jugador quiere terminar el juego:
                if evento.type == pygame.QUIT: #SALIR X
                    
                    en_pausa = False
                    running = False #Termina el ciclo del juego                                        
                    pygame.mixer.music.stop()
                    pygame.quit() #Cierra la pestaña 

                if evento.type == pygame.KEYDOWN:
                    #El evento KEYDOWN se produce cuando se presiona una tecla:

                    #EL USUARIO QUIERE INICIAR O REINICIAR EL JUEGO
                    if evento.key == pygame.K_RETURN: #ENTER
                        if self.contador_fps == 0:
                            en_pausa = False #Termina la pausa
                            nuevo_juego = False
                            pygame.mixer.music.unpause() #Vuelve la musica

                    #EL USUARIO QUIERE CONTINUAR EL JUEGO, LUEGO DE PAUSAR
                    if evento.key == pygame.K_p: #TECLA P

                        if self.contador_fps != 0: #Antes de iniciar el juego el contador espera en 0, por eso la P no puede clickearse, pero a partir que inicia, ya puede aplicarse

                            en_pausa = False #Termina la pausa
                            pygame.mixer.music.unpause() #Vuelve la musica                                           


    def reiniciar_juego(self): #REINICIA EL JUEGO
        
        #RESTABLECE LOS VALORES INICIALES

        self.score = 0
        self.ronda_numero = 1
        self.tiempo_ronda = self.TIEMPO_RONDA
        self.tiempo_spam_enemigo = self.TIEMPO_SPAM_ENEMIGO

        #Reiniciar el jugador:
        self.jugador.vida = self.jugador.VIDA_INICIAL
        self.jugador.reiniciar()

        #Vaciamos los GRUPOS - SPRITES
        self.grupo_enemigo.empty()
        self.grupo_ruby.empty()
        self.grupo_proyectil.empty()

        pygame.mixer.music.play(-1, 0.0) # (-1 = Bucle infinito, 0.0 = Comienza en:)
        pygame.mixer.music.set_volume(0.1) #VOLUMEN DESDE: 0.1 a 1.0

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
        self.rect.bottomleft = (x, y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

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

        colorProyectil = random.randint(0, 1) #COMO SON 2 TIPOS, EL AZAR SON 2 OPCIONES

        #0 = AZUL
        #1 = ROJO

        if colorProyectil == 0:        

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

        else:

            if jugador.velocidad.x > 0: #Significa que el movimiento es hacia la derecha -->
                
                self.image = pygame.transform.scale(pygame.image.load("images/player/slash1.png"),(32,32))

            else: #Significa que el movimiento es hacia la izquierda <--

                #Reutilizo la misma imagen, y la reverso con FLIP: (PRIMER BOOLEAN: "DAR VUELTA HORIZONTALMENTE", SEGUNDO BOOLEAN: "DAR VUELTA VERTICALMENTE")
                self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/player/slash1.png"), True, False), (32,32))
                self.velocidad = -1 * self.velocidad #Garantiza que el disparo tenga orientacion izquierda

            #RECORRIDO DE LA RECTA (rect):

            self.rect = self.image.get_rect() #OBTENGO LA DIRECCION DE PROYECTIL
            self.rect.center = (x,y) #SALDRA DESDE EL CENTRO DE LA POSICION QUE ESTE

            self.posicion_inicial_x = x #POSICION INICIAL DE LA BALA

            grupo_proyectil.add(self)#Lo agrego al grupo de las municiones

    def update(self):        
        
        self.rect.x += self.velocidad #Acumulo en el recorrido el movimiento de la bala

        #self.rect.x +=0 #Se puede usar para otro tipo de disparo (como si fuera una mina de aproximacion) disparo especial

        self.chequear_colision() #TESTEAR           

        #DESTRUCCION de la bala si supera el RANGO

        #ABS: Devuelve el valor absoluto del número dado = DISTANCIA = MODULO |abs|
        if abs(self.rect.x - self.posicion_inicial_x) > self.RANGO:

            self.kill() #destruye el objeto - en este caso la bala

    def chequear_colision(self): #SI EL PROYECTIL COLISIONA CON EL PORTAL: (CONTINUAR...) TESTEAR
        
        lista_colision = pygame.sprite.groupcollide(grupo_proyectil, grupo_portal, False, False) #Diccionario que guarda las colisiones        

        if lista_colision: #SI HAY COLISION: 

            for proyectiles in lista_colision.values():
                for proyectil in proyectiles:            
                 
                    if jugador.posicion.x < WIDTH / 2 and jugador.posicion.y > HEIGHT / 2: #JUGADOR: IZQUIERDA ABAJO                     
                        jugador.sonido_portal.play() #Activa el sonido del portal
                        self.velocidad = -1 * self.velocidad

                    if jugador.posicion.x > WIDTH / 2 and jugador.posicion.y > HEIGHT / 2: #JUGADOR: DERECHA ABAJO                       
                        jugador.sonido_portal.play() #Activa el sonido del portal
                        self.velocidad = -1 * self.velocidad 
                    
                    if jugador.posicion.x < WIDTH / 2 and jugador.posicion.y < HEIGHT / 2: #JUGADOR: IZQUIERDA ARRIBA                   
                        jugador.sonido_portal.play() #Activa el sonido del portal
                        self.velocidad = -1 * self.velocidad  

                    if jugador.posicion.x > WIDTH / 2 and jugador.posicion.y < HEIGHT / 2: #JUGADOR: DERECHA ARRIBA                     
                        jugador.sonido_portal.play() #Activa el sonido del portal
                        self.velocidad = -1 * self.velocidad       

############################################################################################    

class Enemigo(pygame.sprite.Sprite): #ENEMIGO

    def __init__(self, grupo_plataforma, grupo_portal, min_speed, max_speed): #Iniciar el enemigo
        
        super().__init__()

        #VARIABLES CONSTANTES DE LOS ENEMIGOS:
        self.ACELERACION_VERTICAL = 3 #GRAVEDAD
        self.TIEMPO_TUMBADO = 2 #TIEMPO PARA LEVANTARSE
        
        #AGREGO VIDA AL ENEMIGO TESTEAR (¿Esta bien el incremento? ¿Poco? ¿Mucho?)
        self.VIDA_INICIAL = 75 + (25 * juego.ronda_numero) #VIDA DEL ENEMIGO          

        #ANIMACION DE LOS FOTOGRAMAS - LISTAS VACIAS

        self.movimiento_derecho_sprites = [] #MOVIMIENTO DERECHO
        self.movimiento_izquierdo_sprites = [] #MOVIMIENTO IZQUIERDA

        self.muerte_derecha_sprites = [] #MUERTE DERECHA
        self.muerte_izquierda_sprites = [] #MUERZA IZQUIERDA

        self.aturdido_derecho_sprites = [] #STUNS - ATURDIR DERECHO
        self.aturdido_izquierdo_sprites = [] #STUNS - ATURDIR IZQUIERDO

        #QUE ENEMIGOS VAN A SALIR: (EN ESTE CASO HOMBRE - MUJER)
        #PERO SE PUEDE USAR PARA AGREGAR VARIAS CLASES DE ENEMIGOS
        #CON PROPIEDADES DIFERENTES - SKINS - HABILIDADES, ETC.

        genero = random.randint(0, 1) #COMO SON 2 TIPOS, EL AZAR SON 2 OPCIONES

        #0 = HOMBRE
        #1 = MUJER

        if genero == 0:

            #ANIMACION - CAMINANDO DERECHA: ANEXAR A LA LISTA DE ANIMACIONES
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (1).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (2).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (3).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (4).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (5).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (6).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (7).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (8).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (9).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.movimiento_derecho_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.movimiento_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION - MUERTE DERECHA
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.muerte_derecha_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.muerte_izquierda_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION STUNS - ATURDIMIENTOS

            #INVIERTE EL ORDEN DE LAS ANIMACIONES DE MUERTE PARA QUE "EMPIECE MUERTO Y TERMINE VIVO"
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.aturdido_derecho_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.aturdido_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

        else: #SI TOCA 1 = MUJER *************************************************************************************************************

            #ANIMACION - CAMINANDO DERECHA: ANEXAR A LA LISTA DE ANIMACIONES
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (1).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (2).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (3).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (4).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (5).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (6).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (7).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (8).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (9).png"),(64,64)))
            self.movimiento_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.movimiento_derecho_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.movimiento_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION - MUERTE DERECHA
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"),(64,64)))
            self.muerte_derecha_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.muerte_derecha_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.muerte_izquierda_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION STUNS - ATURDIMIENTOS

            #INVIERTE EL ORDEN DE LAS ANIMACIONES DE MUERTE PARA QUE "EMPIECE MUERTO Y TERMINE VIVO"
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"),(64,64)))
            self.aturdido_derecho_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS = INVIRTIENDO LAS IMAGENES DERECHAS
            for sprite in self.aturdido_derecho_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.aturdido_izquierdo_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #MOVIMIENTO DE LOS ENEMIGOS: (ALEATORIOS)
        self.direccion = random.choice([-1,1]) #SI SALE POR LA DERECHA O IZQUIERDA        

        #SE USARA COMO INDICE DE LA LISTA - INDEX
        self.indice_sprite = 0

        if self.direccion == -1:
            #CARGA LA IMAGEN DE PARTIDA
            self.image = self.movimiento_izquierdo_sprites[self.indice_sprite] 

        else:
            self.image = self.movimiento_derecho_sprites[self.indice_sprite]         

        #OBTENGO LA RECTA (get.rect): Es el recorrido del objeto - En este caso el ENEMIGO
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (random.randint(100, WIDTH - 100), - 100) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #GRUPOS SPRITES:
        self.grupo_plataforma = grupo_plataforma
        self.grupo_portal = grupo_portal

        #BANDERAS PARA LOS EVENTOS DISPARADORES (MUERTE Y ATURDIMIENTO)
        self.animacion_abatido = False
        self.animacion_levantarse = False        

        #CARGA DE SONIDOS
        self.sonido_daño = pygame.mixer.Sound("sounds/zombie_hit.wav") #SONIDO AL DAÑARSE
        self.sonido_eliminado = pygame.mixer.Sound("sounds/zombie_kick.wav") #SONIDO AL MORIR
        self.sonido_portal = pygame.mixer.Sound("sounds/portal_sound.wav") #SONIDO DEL PORTAL

        #VECTORES DE CINEMATICAS - AUXILIARES
                
        self.posicion = vector(self.rect.x,self.rect.y) #VECTOR DE POSICION

        #SE MULTIPLICA POR LA direccion PARA DAR LA DIRECCION CORRECTA (POSITIVA O NEGATIVA)
        self.velocidad = vector(self.direccion * random.randint(min_speed,max_speed),0) #VELOCIDAD DEL ENEMIGO       
        self.aceleracion = vector(0, self.ACELERACION_VERTICAL) #ACELERACION Y GRAVEDAD

        #VALORES INICIALES DEL ENEMIGO - INICIO - REINICIO
        self.esta_abatido = False #ESTA MUERTO = FALSO
        self.tiempo_ronda = 0 #TIEMPO DE RONDA
        self.contador_fps = 0 #CONTEO DE FOTOGRAMAS

        self.vida = self.VIDA_INICIAL #VIDA DEL ENEMIGO (TESTEAR)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        #grupo_principal.add(self)  


    def update(self): #Actualizar el enemigo
        
        self.mover()
        self.chequear_colisiones()
        self.chequear_animaciones()

        #Determina cuando el zombi debe levantarse despues de ser tumbado:

        if self.esta_abatido: #TUMBADO = TRUE

            self.contador_fps += 1

            if self.contador_fps % FPS == 0: #CONTEO DIVISIBLE FPS == 0 - SI

                self.tiempo_ronda += 1

                if self.tiempo_ronda == self.TIEMPO_TUMBADO: #SI SON IGUALES EL ENEMIGO SE LEVANTA

                    self.animacion_levantarse = True

                    #Cuando el Enemigo es tumbado, la imagen se mantiene igual
                    #Cuando se levanta tiene que comenzar en el indice cero de nuestro aumento:
                    self.indice_sprite = 0


    def mover(self): #Movimiento del enemigo       
        
            if not self.esta_abatido: #Mientras NO este muerto el Enemigo:

                #Condicion para que sea la animacion correcta:
                if self.direccion == -1:

                    self.animacion(self.movimiento_izquierdo_sprites, 0.5) #Caminando para la izquierda

                else:

                    self.animacion(self.movimiento_derecho_sprites, 0.5) #Caminando para la derecha

                #CALCULAR LOS VALORES DE LAS CINEMATICAS:      

                #NO SE NECESITA ACTUALIZAR EL VECTOR DE ACELERACION PORQUE NUNCA CAMBIA.
                
                #MATEMATICA VECTORIAL (5, 2) + (6, 1) = (11, 3)
                
                self.velocidad += self.aceleracion #ACTUALIZA EL VECTOR DE VELOCIDAD

                self.posicion += self.velocidad + 0.5 * self.aceleracion #ACTUALIZA EL VECTOR DE POSICION        

                #ACTUALIZAR LA RECTA (rect) BASADA EN LOS CALCULOS CINEMATICOS:
                
                #CONDICIONES PARA QUE EL ENEMIGO PASE DE UN LADO A OTRO DE LA PANTALLA        

                if self.posicion.x < 0: #Posicion ENEMIGO menor a 0

                    self.posicion.x = WIDTH

                elif self.posicion.x > WIDTH: #Posicion ENEMIGO mayor a la pantalla

                    self.posicion.x = 0

                #SE PUEDE CAMBIAR PARA QUE EL ENEMIGO NO PUEDA SALIR DE LA PANTALLA

                #DESPUES DE QUE SE ACTUALICEN TODOS LOS VECTORES CORREGIMOS LA POSICION:

                self.rect.bottomleft = self.posicion


    def chequear_colisiones(self): #Chequea las colisiones del enemigo con el entorno

        #spritecollide(Grupo a comprobar, Grupo A Colisionar, Desaparecer objeto al chocar?)
        colision_plataforma = pygame.sprite.spritecollide(self, self.grupo_plataforma, False, pygame.sprite.collide_mask) #COMPRUEBA COLISION

        #Tambien se puede usar para dañar al objeto colisionado
        if colision_plataforma: #SI LA LISTA >> NO << ESTA VACIA:
                
            #IGUALA LA POSICION AL OBJETO QUE CHOCA + 1: DE REBOTE AL CHOCAR.
            self.posicion.y = colision_plataforma[0].rect.top + 1
            self.velocidad.y = 0 #ASEGURA QUE SE DEJE DE MOVER
        
        #Chequea las colisiones con los portales:
        if pygame.sprite.spritecollide(self,self.grupo_portal, False, pygame.sprite.collide_mask):

            self.sonido_portal.play() #Activa el sonido del portal

            #Una vez que colisiona, determinar a que portal se movera:

            #IZQUIERDA Y DERECHA:

            #Si es mayor a la mitad HORIZONTAL, estas en el LADO DERECHO
            if self.posicion.x > WIDTH / 2: #Centro de la pantalla Horizontalmente
                self.posicion.x = 86 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas en el LADO IZQUIERDO
                self.posicion.x = WIDTH - 150 #150 Pixeles

            #ARRIBA Y ABAJO:

            #Si es mayor a la mitad VERTICAL, estas ARRIBA
            if self.posicion.y > HEIGHT / 2: #Centro de la pantalla Verticalmente
                self.posicion.y = 64 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas ABAJO
                self.posicion.y = HEIGHT - 132 #132 Pixeles

            self.rect.bottomleft = self.posicion #Guarda la posicion en la recta


    def chequear_animaciones(self): #Chequea las animaciones de muerte y ascenso
        
        #ANIMACION MUERTE - TUMBADO:
        if self.animacion_abatido:

            if self.direccion == 1: #DIRECCION DERECHA
                self.animacion(self.muerte_derecha_sprites, 0.95)

            else: #DIRECCION IZQUIERDA
                self.animacion(self.muerte_izquierda_sprites, 0.95)  

        #ANIMACION "RESURECCION" - LEVANTARSE:
        if self.animacion_levantarse: #LEVANTARSE = TRUE

            if self.direccion == 1: #DIRECCION DERECHA
                self.animacion(self.aturdido_derecho_sprites, 0.95)

            else: #DIRECCION IZQUIERDA
                 self.animacion(self.aturdido_izquierdo_sprites, 0.95)   


    def animacion(self, sprite_lista, speed): #Animaciones del enemigo
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.indice_sprite < len(sprite_lista) -1: #RESTA EN UNO PARA QUE COINCIDA CON INDICE
            self.indice_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.indice_sprite = 0 #PARA QUE VUELVA A EMPEZAR

            #TERMINAR LA ANIMACION DE TUMBADO:
            if self.animacion_abatido:
                self.indice_sprite = len(sprite_lista) - 1
                self.animacion_abatido = False #TERMINA EL BUCLE DE ANIMACION 

            #TERMINAR LA ANIMACION DE RESURECCION - LEVANTARSE
            if self.animacion_levantarse: #RESURECCION = TRUE                
                self.animacion_levantarse = False #TERMINA EL BUCLE DE ANIMACION
                self.esta_abatido = False #Para que no vuelva a TUMBARSE
                #Condicion para que sea la animacion correcta:

                #REINICIAR LAS VARIABLES DE SINCRONIZACION DE TIEMPO:
                self.contador_fps = 0 #RECUENTO DE FPS REINICIAR
                self.tiempo_ronda = 0 #REINICIAR                                               

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_lista[int(self.indice_sprite)]

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

    def __init__(self, grupo_plataforma, grupo_portal):
        
        super().__init__()

        #VARIABLES CONSTANTES:
        self.ACELERACION_VERTICAL = 3 #Gravedad
        self.HORIZONTAL_VELOCIDAD = 5 #Velocidad
        #TIPO = random.randint(0,N) SE PODRIA AGREGAR DIFERENTES TIPOS DE POTENCIADORES (DIF. IMAGENES) Y EN LA CLASE "JUEGO" DEPENDIENDO EL "TIPO" QUE SEA HAGA DIFERENTES COSAS

        #Animacion de los fotogramas
        self.ruby_sprites = []

        #ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"),(54,54)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"),(54,54)))

        #SE USARA COMO INDICE DE LA LISTA - INDEX
        self.indice_sprite = 0

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.ruby_sprites[self.indice_sprite] 

        #OBTENGO LA RECTA (get.rect):
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (WIDTH // 2 ,100) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #GRUPOS - SPRITES:
        self.grupo_plataforma = grupo_plataforma
        self.grupo_portal = grupo_portal

        #CARGA DE SONIDOS:
        self.sonido_portal= pygame.mixer.Sound("sounds/portal_sound.wav")

        #CINEMATICAS VECTORIALES:
        self.posicion = vector(self.rect.x, self.rect.y) #Posicion del trazo de la recta
        self.velocidad = vector(random.choice([-1 * self.HORIZONTAL_VELOCIDAD, self.HORIZONTAL_VELOCIDAD]), 0)
        self.aceleracion = vector(0, self.ACELERACION_VERTICAL)


    def update(self):
        
        self.animacion(self.ruby_sprites, 0.25)        
        self.mover()
        self.chequear_colisiones()


    def mover(self): #Movimiento del Ruby    

        #CALCULAR LOS VALORES DE LAS CINEMATICAS:      

        #NO SE NECESITA ACTUALIZAR EL VECTOR DE ACELERACION PORQUE NUNCA CAMBIA.
            
        #MATEMATICA VECTORIAL (5, 2) + (6, 1) = (11, 3)
            
        self.velocidad += self.aceleracion #ACTUALIZA EL VECTOR DE VELOCIDAD

        self.posicion += self.velocidad + 0.5 * self.aceleracion #ACTUALIZA EL VECTOR DE POSICION        

        #ACTUALIZAR LA RECTA (rect) BASADA EN LOS CALCULOS CINEMATICOS:
            
        #CONDICIONES PARA QUE EL RUBY PASE DE UN LADO A OTRO DE LA PANTALLA        

        if self.posicion.x < 0: #Posicion RUBY menor a 0

            self.posicion.x = WIDTH

        elif self.posicion.x > WIDTH: #Posicion RUBY mayor a la pantalla

            self.posicion.x = 0

        #SE PUEDE CAMBIAR PARA QUE EL RUBY NO PUEDA SALIR DE LA PANTALLA

        #DESPUES DE QUE SE ACTUALICEN TODOS LOS VECTORES CORREGIMOS LA POSICION:

        self.rect.bottomleft = self.posicion


    def chequear_colisiones(self): #Chequea las colisiones del Ruby con el entorno
        
        #spritecollide(Grupo a comprobar, Grupo A Colisionar, Desaparecer objeto al chocar?)
        colision_plataforma = pygame.sprite.spritecollide(self, self.grupo_plataforma, False, pygame.sprite.collide_mask) #COMPRUEBA COLISION

        #Tambien se puede usar para dañar al objeto colisionado
        if colision_plataforma: #SI LA LISTA >> NO << ESTA VACIA:
                
            #IGUALA LA POSICION AL OBJETO QUE CHOCA + 1: DE REBOTE AL CHOCAR.
            self.posicion.y = colision_plataforma[0].rect.top + 1
            self.velocidad.y = 0 #ASEGURA QUE SE DEJE DE MOVER
        
        #Chequea las colisiones con los portales:
        if pygame.sprite.spritecollide(self,self.grupo_portal, False, pygame.sprite.collide_mask):

            self.sonido_portal.play() #Activa el sonido del portal

            #Una vez que colisiona, determinar a que portal se movera:

            #IZQUIERDA Y DERECHA:

            #Si es mayor a la mitad HORIZONTAL, estas en el LADO DERECHO
            if self.posicion.x > WIDTH / 2: #Centro de la pantalla Horizontalmente
                self.posicion.x = 86 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas en el LADO IZQUIERDO
                self.posicion.x = WIDTH - 150 #150 Pixeles

            #ARRIBA Y ABAJO:

            #Si es mayor a la mitad VERTICAL, estas ARRIBA
            if self.posicion.y > HEIGHT / 2: #Centro de la pantalla Verticalmente
                self.posicion.y = 64 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas ABAJO
                self.posicion.y = HEIGHT - 132 #132 Pixeles

            self.rect.bottomleft = self.posicion #Guarda la posicion en la recta

    def animacion(self, sprite_list, speed):
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

    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], #21
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], #22
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  #23

            ]

#GENERAR LOS OBJETOS DEL MAPA DE MOSAICO

#RECORRER LAS 23 FILAS:

for i in range(len(mapa_mosaico)):

    #RECORRER LAS 40 COLUMNAS:
    for j in range(len(mapa_mosaico[i])):

    #CADA CONDICION MUESTRA LOS OBJETOS CORRESPONDIENTES:

    #SE LE ASIGNA LOS GRUPOS PARA CLASIFICAR CADA TIPO DE SPRITE U OBJETO

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

        #PORTALES:
        elif mapa_mosaico[i][j] == 7:
            Portal(j*32, i*32 + 35, "green", grupo_portal)
            #GRUPO PORTAL

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
juego = Juego(jugador, grupo_enemigo, grupo_plataforma, grupo_portal, grupo_proyectil, grupo_ruby)
juego.pausar_juego("Bienvenido", "Presiona 'Enter' para ingresar") #ESPERA EN LA INTERFACE DE PAUSA
pygame.mixer.music.play(-1, 0.0) # -1 INFINITO, INICIO DE MUSICA
pygame.mixer.music.set_volume(0.05) #VOLUMEN DESDE: 0.1 a 1.0 puede estirarse: 0.0001, 0.000009 etc

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
                if primer_disparo - jugador.ultimo_disparo > jugador.CADENCIA + (juego.ronda_numero * 25): 
                    #TESTEAR: SE HACE CADA VEZ MAS LENTO DISPARAR POR LA CADENCIA AUMENTADA

                    jugador.disparar() #DISPARAR
                    jugador.ultimo_disparo = primer_disparo #IMPORTANTE MODIFICAR EL VALOR

            #ELIMINAR FUNCION
            if evento.key == pygame.K_RETURN: #ENTER
                #CREACION DE LOS ENEMIGOS
                enemigo = Enemigo(grupo_plataforma, grupo_portal, 2, 7)  
                grupo_enemigo.add(enemigo) 

            #PAUSA
            if evento.key == pygame.K_p: #P
                #Pausa el juego                
                juego.pausar_juego("Juego en PAUSA!","Presiona 'P' para continuar")   

    #Dibujar (blit) el fondo en la pantalla: #SI SE DESACTIVA SE VEN LOS TRAZOS DE LAS ANIMACIONES    
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
    juego.update()
    juego.dibujar()    

    #Actualiza la pantalla y los frames:
    pygame.display.update() #Actualiza la pantalla
    clock.tick(FPS) #Cuadros por segundos

#### FIN CICLO DEL JUEGO ####

#Terminado el ciclo de vida del juego:
pygame.quit() #Cierra todos los procesos utilizados de la lib Pygame