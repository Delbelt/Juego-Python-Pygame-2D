import pygame, random

from pygame import image

#VECTOR 2D PARA LOS MOVIMIENTOS DE PLATAFORMA

vector = pygame.math.Vector2 #math.Vector2 = VECTOR de 2 DIMENSIONES

#INICIALIZAR PYGAME Y TODOS SUS MODULOS:
pygame.init()

#BALDOSAS DE 32 X 32: CALCULO PARA ASIGNAR LOS ESPACIOS EN EL MAPA MATRIZ:
#SUPERFICIE DE VISUALIZACION: (32 X 32: 1280/32 = 40 ancho, 736/32 = 23 alto)

WIDTH = 1280 # ANCHO
HEIGHT = 736 # ALTO

 #INICIA LA PANTALLA PARA SU VISUALIZACION CON LOS VALORES QUE ASIGNAMOS ARRIBA:

display_surface = pygame.display.set_mode((WIDTH, HEIGHT))# NOMBRE DE LA PANTALLA Y DIMENSIONES
pygame.display.set_caption("Zombie Knight") #TITULO DE LA PANTALLA

#ESTABLECE LOS FPS Y RELOJ:
FPS = 60
clock = pygame.time.Clock() #CREA EL OBJETO DEL TIEMPO PARA CONTROLARLO

#DEFINICION DE CLASES:

    # Sprite es una imagen bidimensional que forma parte de una escena gráfica.
    # Sprite es cierto tipo de objeto que interactúa. 
    # Rect es el recorrido del objeto

#CLASES:

############################################################################################

class Game():

    #pass = declaracion NULL de la implementacion

    def __init__(self, player, zombie_group, platform_group, portal_group, bullet_group, ruby_group): #INIT DEL JUEGO
        
        #VARIABLES CONSTANTES
        self.STARTING_ROUND_TIME = 30 #Duracion de cada ronda

        #VALORES DEL JUEGO:
        self.score = 0 #PUNTUACION INICIAL
        self.round_number = 1 #INICIO DE RONDA
        self.frame_count = 0 #CONTEO DE FOTOGRAMAS
        self.round_time = self.STARTING_ROUND_TIME #Duracion de la ronda

        #VALORES DE LAS FUENTE

        self.title_font = pygame.font.Font("fonts/Poultrygeist.ttf", 48) #FUENTE DEL TITULO
        self.HUD_font = pygame.font.Font("fonts/Pixel.ttf", 24) #FUENTE DE LA BARRA DE ESTADO

        #GRUPOS Y SPRITES:
        self.player = player
        self.zombie_group = zombie_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group        


    def update(self): #ACTUALIZAR JUEGO
        
        self.frame_count += 1 #CUENTA LOS FPS POR SEGUNDO

        if self.frame_count % FPS == 0: #CONDICION PARA IR RESTANDO TIEMPO A LA RONDA

            self.round_time -= 1
            self.frame_count = 0

        #CHEQUEAR LAS COLISIONES DEL JUEGO
        self.check_collisions()

    def draw(self): #HUD (Head-UP Display) = BARRA DE ESTADO
        
        #VALORES DE LOS COLORES:
        WHITE = (255, 255, 255)
        GREEN = (25, 200, 25)

        #TEXTOS DENTRO DEL JUEGO - HUD BARRAS DE ESTADO:

        # topleft = ARRIBA A PARTIR DE LA IZQUIERDA
        # topright = ARRIBA A PARTIR DE LA DERECHA
        # center = CENTRO

        score_text = self.HUD_font.render("Score: " + str(self.score), True, WHITE) #DONDE MUESTRA EL PUNTAJE
        score_rect = score_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        score_rect.topleft = (10, HEIGHT - 50) #POSICION DE LOS PUNTOS        

        health_text = self.HUD_font.render("Health: " + str(self.player.health), True, WHITE) #VIDA EN PANTALLA
        health_rect = health_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        health_rect.topleft = (10, HEIGHT - 25) #POSICION DE LA VIDA  

        title_text = self.title_font.render("Zombie Knight", True, GREEN)
        title_rect = title_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        title_rect.center = (WIDTH // 2, HEIGHT - 25) #POSICION TITULO DEL GIU

        round_text = self.HUD_font.render("Night: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        round_rect.topright = (WIDTH - 10, HEIGHT - 50) #RONDAS COMPLETADAS

        time_text = self.HUD_font.render("Sunrise In: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect() #OBTENGO LA POSICION DE LA RECTA
        time_rect.topright = (WIDTH - 10, HEIGHT - 25)

        #DIBUJOS DEL HUD - HAY QUE AGREGARLOS PARA QUE APAREZCAN:

        display_surface.blit(score_text, score_rect) #DIBUJO: PUNTAJE
        display_surface.blit(health_text, health_rect) #DIBUJO: VIDA
        display_surface.blit(title_text, title_rect) #DIBUJO: TITULO
        display_surface.blit(round_text, round_rect) #DIBUJO: RONDAS
        display_surface.blit(time_text, time_rect) #DIBUJO: TIEMPO

    def add_zombie(self): #AGREGA LOS ZOMBIES AL JUEGO
        pass

    def check_collisions(self): #CHEQUEA LAS COLISIONES DENTRO DEL JUEGO
        
        #group-collide(Grupo 1, Grupo 2, Desaparecer GRUPO 1?, DESAPARECER GRUPO 2?)
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)        

        if collision_dict: #SI HAY COLISION: 

            for zombies in collision_dict.values():
                for zombie in zombies:

                    #SE PODRIA AGREGAR OTRO TIPO DE ATAQUE O UNA POSIBILIDAD
                    #DE ABATIR AL RIVAL, QUEDA PENDIENTE A MODIFICAR
                    #TAMBIEN HAY QUE VER COMO HACER PARA QUE CADA NIVEL TENGA MAS VIDA EL ZOMBIE
                    #O SACAR MENOS DAÑO

                    #TAMBIEN SI SE TUMBA QUE HAYA UNA POSIBILIDAD QUE EL ENEMIGO
                    #CAMBIE LA ORIENTACION DE MARCHA

                    zombie.hit_sound.play()
                    zombie.is_dead = True #ENEMIGO TUMBADO #SIN ESTO EL ZOMBIE SIGUE EN PIE
                    zombie.animate_death = True #ANIMACION DE TUMBADO #SIN ESTO NO HAY ANIMACION                                                                                    
                                                            
                    #RETROCEDE LOS ENEMIGOS DEPENDIENDO DONDE ESTE UBICADO EL JUGADOR:                    

                    if self.player.velocity.x < 0: #SI EL JUGADOR ESTA EN LA DERECHA:                                          

                        zombie.position.x -= 10 #LO RETROCEDE PARA LA IZQUIERDA
                        zombie.rect.bottomleft = zombie.position
                        
                        if zombie.direction == 1:  #SI EL ZOMBIE VA PARA LA DERECHA: - PARA EVITAR QUE ROTE EN CADA GOLPE                           

                            zombie.direction = zombie.direction * -1 #CAMBIA LA ORIENTACION DE LA ANIMACION
                            zombie.velocity = zombie.velocity * -1 #CAMBIA LA ORIENTACION DE MOVIMIENTO (SI IBA A LA DERECHA, VA A LA IZQUIERDA, ETC)                                                  

                    else: #SI EL JUGADOR ESTA EN LA IZQUIERDA

                        zombie.position.x += 10 #LO RETROCEDE PARA LA IZQUIERDA
                        zombie.rect.bottomleft =  zombie.position

                        if zombie.direction == -1: #SI EL ZOMBIE VA PARA LA IZQUIERDA - PARA EVITAR QUE ROTE EN CADA GOLPE  

                            zombie.direction = zombie.direction * -1 #CAMBIA LA ORIENTACION DE LA ANIMACION
                            zombie.velocity = zombie.velocity * -1 #CAMBIA LA ORIENTACION DE MOVIMIENTO (SI IBA A LA DERECHA, VA A LA IZQUIERDA, ETC)                          
                                                         
                    #TESTEAR: FUNCIONA, PERO OPCION DESBLOQUEADA EN COMMIT 7.A

                    #zombie.health -= 50 #CADA DISPARO LE SACA VIDA AL ENEMIGO

                    #if zombie.health <= 0: #SI SE QUEDA SIN VIDA:
                        #zombie.kick_sound.play()                                           
                        #zombie.kill() #ELIMINA AL ZOMBIE
                        #self.score += 25           

        #SI UN JUGADOR PISO EL ENEMIGO O CHOCO CON OTRO ENEMIGO
        collision_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)

        if collision_list: #RECORRE LA LISTA:
            for zombie in collision_list:
                
                if zombie.is_dead == True: #Si el enemigo esta tumbado:

                    zombie.kick_sound.play() #Sonido de eliminar
                    zombie.kill() #Elimina el objeto
                    self.score += 25 #Agrega N puntos por eliminarlo                    

                #SI EL ENEMIGO NOS TOCA:                
                else:

                    self.player.health -= 20 #Nos resta N puntos de vida
                    self.player.hit_sound.play() #Sonido de daño 

                    #EVITAR QUE EL JUGADOR SIGA RECIBIENDO DAÑO CONTINUO:
                    self.player.position.x -= 200 * zombie.direction
                    self.player.rect.bottomleft = self.player.position


    def check_round_completation(self): #CHEQUEA SI SOBREVIVIO UNA NOCHE
        pass

    def check_game_over(self): #CHEQUEA SI EL JUGADOR PERDIO EL JUEGO
        pass

    def star_new_round(self): #INICIA UNA NUEVA RONDA
        pass
    
    def pause_game(self): #PAUSA EL JUEGO
        pass

    def reset_game(self): #REINICIA EL JUEGO
        pass

############################################################################################

class Tile(pygame.sprite.Sprite): #Clase que representa el MAPA MOSAICO de 32 x 32 px

    def __init__(self, x, y, image_int, main_group, sub_group=""): #DA INICIO A LA MATRIZ DEL MAPA DE MOSAICO
        super().__init__()

        #CARGAR LA IMAGEN CORRECTA Y AGREGARLA AL SUB-GRUPO CORRESPONDIENTE:

        #TIERRA:
        if image_int == 1:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (1).png"), (32,32))
       
        #PLATAFORMA:
        elif image_int == 2:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (2).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            sub_group.add(self)

        elif image_int == 3:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (3).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            sub_group.add(self)

        elif image_int == 4:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (4).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            sub_group.add(self)

        elif image_int == 5:

            #CARGA LA IMAGEN CORRESPONDIENTE + RE-ESCALA A 32 X 32 px:            
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/tile (5).png"), (32,32))
            #AGREGO AL  SUB-GRUPO CORRESPONDIENTE:
            sub_group.add(self)

        #SIN IMPORTAR QUE NUMERO DE IMAGEN SEA (image_int)
        #SE AGREGA AL GRUPO PRINCIPAL POR DEFECTO:

        main_group.add(self)

        #OBTIENE EL RESTO DE LA IMAGEN Y LA POSICION DENTRO DE LA MATRIZ:

        self.rect = self.image.get_rect() #OBTIENE LA COORDENADA DE LA RECTA
        self.rect.topleft = (x,y) #UBICA DESDE ARRIBA-IZQUIERDA EN LAS COORDENADAS: (x,y)

############################################################################################

class Player(pygame.sprite.Sprite): #JUGADOR

    def __init__(self, x, y, platform_group, portal_group, bullet_group):#Iniciar el jugador
        
        super().__init__()

        #CONSTANTES DEL JUGADOR:
        self.HORIZONTAL_ACCELERATION = 2 #VELOCIDAD DEL JUGADOR
        self.HORIZONTAL_FRICTION = 0.15 #FRICCION EN EL DESPLAZAMIENTO (RESBALON)
        self.VERTICAL_ACCELERATION = 0.8 #GRAVEDAD
        self.VERTICAL_JUMP_SPEED = 18 #QUE TAN ALTO SE PUEDE SALTAR
        self.STARTING_HEALTH = 100 #VIDA DEL PERSONAJE

        #ANIMACION DE LOS FOTOGRAMAS - LISTAS VACIAS:
        self.move_right_sprites = [] #MOVIMIENTO DERECHO
        self.move_left_sprites = [] #MOVIMIENTO IZQUIERDO

        self.idle_right_sprites = [] #INACTIVIDAD DERECHO 
        self.idle_left_sprites = [] #INACTIVIDAD IZQUIERDO

        self.jump_right_sprites = [] #SALTO DERECHO
        self.jump_left_sprites = [] #SALTO IZQUIERDO

        self.attack_right_sprites = [] #ATAQUE DERECHO
        self.attack_left_sprites = [] #ATAQUE IZQUIERDO

        #### ANIMACIONES ####

        #MOVIMIENTOS: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (1).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (2).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (3).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (4).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (5).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (6).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (7).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (8).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (9).png"), (64,64)))
        self.move_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/run/Run (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS
        for sprite in self.move_right_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #INACTIVO: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (2).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (3).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (4).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (5).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (6).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (7).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (8).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (9).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (10).png"), (64,64)))
        self.idle_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/idle/Idle (1).png"), (64,64)))

       #AÑADE LOS MOVIMIENTOS IZQUIERDOS
        for sprite in self.idle_right_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #SALTO: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (1).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (2).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (3).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (4).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (5).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (6).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (7).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (8).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (9).png"), (64,64)))
        self.jump_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/jump/Jump (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS
        for sprite in self.jump_right_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        #ATAQUE: ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS

        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (1).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (2).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (3).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (4).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (5).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (6).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (7).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (8).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (9).png"), (64,64)))
        self.attack_right_sprites.append(pygame.transform.scale(pygame.image.load("images/player/attack/Attack (10).png"), (64,64)))

        #AÑADE LOS MOVIMIENTOS IZQUIERDOS
        for sprite in self.attack_right_sprites:

            #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))


        #SE USARA COMO INDICE DE LA LISTA - VARIABLE AUTODIDACTA
        self.current_sprite = 0

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.idle_right_sprites[self.current_sprite] 

        #OBTENGO LA RECTA (get.rect): Es el recorrido del objeto - En este caso el jugador
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #GRUPOS SPRITES:
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group

        #BANDERAS PARA LOS EVENTOS DISPARADORES (DISPARAR Y SALTAR)
        self.animate_jump = False
        self.animate_fire = False

        #CARGA DE SONIDOS
        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav") #SONIDO AL SALTAR
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav") #SONIDO AL DISPARAR
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav") #SONIDO PORTAL
        self.hit_sound = pygame.mixer.Sound("sounds/player_hit.wav") #SONIDO AL DAÑARSE

        #VECTORES DE CINEMATICAS - AUXILIARES
                
        self.position = vector(x,y) #VECTOR DE POSICION
        self.velocity = vector(0,0) #VELOCIDAD INICIAL Y VELOCIDAD DE ARRESTRE (NO SE DESPLAZA SOLO)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION) #ACELERACION Y GRAVEDAD

        #VALORES INICIALES DEL JUGADOR - INICIO - REINICIO

        self.health = self.STARTING_HEALTH
        self.starting_x = x #POSICION COORDENADA X
        self.starting_y = y #POSICION COORDENADA Y

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        #main_group.add(self)  


    def update(self): #Actualizar el jugador

        #SE ELIGE SEPARAR LAS FUNCIONES PARA TENER UN MEJOR CONTROL DE CADA UNA:
        self.move() #MOVIMIENTO DEL JUGADOR
        self.check_colission() #CHEQUEA LAS COLISIONES
        self.check_animations() #CHEQUEA LAS ANIMACIONES (SI TIENE QUE DISPARAR EVENTO)
    
    def move(self): #Movimiento del jugador
        
        #VECTOR DE ACELERACION
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        #PRESION DE TECLAS: ESTABLECE EL COMPONENTE DE ACELERACION != DE CERO

        keys = pygame.key.get_pressed() #TECLAS = VERIFICA SI SE TOCO UNA TECLA

        if keys[pygame.K_LEFT]: #SE PULSO LA IZQUIERDA? SI:

            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.5) #AGREGO LA ANIMACION AL MOVIMIENTO

        elif keys[pygame.K_RIGHT]: #SE PULSO LA DERECHA? SI:

            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, 0.5) #AGREGO LA ANIMACION AL MOVIMIENTO

        else: #SI NO ESTOY TOCANDO NINGUNA TECLA ENTONCES: (REPOSO)

            if self.velocity.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animate(self.idle_right_sprites, 0.5) #MOVIMIENTO INACTIVO DERECHO

            else: #Entonces se estaba moviendo hacia la izquierda <--
                self.animate(self.idle_left_sprites, 0.5) #MOVIMIENTO INACTIVO IZQUIERDO

        #CALCULAR LOS VALORES DE LAS CINEMATICAS:        

        #CUANTO MAS RAPIDO NOS MOVEMOS MAS FRICCION RECIBIMOS:
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION #AÑADIMOS FRICCION
        
        #MATEMATICA VECTORIAL (5, 2) + (6, 1) = (11, 3)
        
        self.velocity += self.acceleration #ACTUALIZA EL VECTOR DE VELOCIDAD

        self.position += self.velocity + 0.5 * self.acceleration #ACTUALIZA EL VECTOR DE POSICION        

        #ACTUALIZAR LA RECTA (rect) BASADA EN LOS CALCULOS CINEMATICOS:
        
        #CONDICIONES PARA QUE EL JUGADOR PASE DE UN LADO A OTRO DE LA PANTALLA
        

        if self.position.x < 0: #Posicion Jugador menor a 0

            self.position.x = WIDTH

        elif self.position.x > WIDTH: #Posicion Jugador mayor a la pantalla

            self.position.x = 0

        #SE PUEDE CAMBIAR PARA QUE EL JUGADOR NO PUEDA SALIR DE LA PANTALLA

        #DESPUES DE QUE SE ACTUALICEN TODOS LOS VECTORES CORREGIMOS LA POSICION:

        self.rect.bottomleft = self.position


    def check_colission(self): #Chequea las colisiones del jugador con el entorno
        
        if self.velocity.y > 0:
            #spritecollide(Grupo a comprobar, Grupo A Colisionar, Desaparecer objeto al chocar?)
            collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False) #COMPRUEBA COLISION

            #Tambien se puede usar para dañar al objeto colisionado
            if collided_platforms: #SI LA LISTA >> NO << ESTA VACIA:
                
                #IGUALA LA POSICION AL OBJETO QUE CHOCA + 1: DE REBOTE AL CHOCAR.
                self.position.y = collided_platforms[0].rect.top + 1
                self.velocity.y = 0 #ASEGURA QUE SE DEJE DE MOVER

        #Chequea las colisiones cuando el jugador esta saltando:
        if self.velocity.y < 0:
            collided_platforms = pygame.sprite.spritecollide(self,self.platform_group, False)    

            if collided_platforms: #Si colisiona:
                self.velocity.y=0 #ASEGURA QUE SE DEJE DE MOVER
                
                # BUCLE - MOVIMIENTO INCREMENTAL DE LA POSICION DEL JUGADOR:
                # While: Mientras el jugador colisione con algun objeto de la plataforma:
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    
                    self.position.y += 1 #POSICION DEL JUGADOR + 1 PIXEL
                    self.rect.bottomleft = self.position #SALTA, COLISIONA, Y LUEGO CAE
        
        #Chequea las colisiones con los portales:
        if pygame.sprite.spritecollide(self,self.portal_group, False):

            self.portal_sound.play()#Activa el sonido del portal

            #Una vez que colisiona, determinar a que portal se movera:

            #IZQUIERDA Y DERECHA:

            #Si es mayor a la mitad HORIZONTAL, estas en el LADO DERECHO
            if self.position.x > WIDTH / 2: #Centro de la pantalla Horizontalmente
                self.position.x = 86 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas en el LADO IZQUIERDO
                self.position.x = WIDTH - 150 #150 Pixeles

            #ARRIBA Y ABAJO:

            #Si es mayor a la mitad VERTICAL, estas ARRIBA
            if self.position.y > HEIGHT / 2: #Centro de la pantalla Verticalmente
                self.position.y = 64 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas ABAJO
                self.position.y = HEIGHT - 132 #132 Pixeles

            self.rect.bottomleft = self.position #Guarda la posicion en la recta
            
    def check_animations(self): #Chequea las animaciones de salto y disparo
        
        #CHEQUEO DE SALTO:
        if self.animate_jump: #La animacion de SALTO esta activada? SI:

            if self.velocity.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animate(self.jump_right_sprites, 0.1) #MOVIMIENTO SALTO DERECHO

            else: #Significa que el movimiento era hacia la izquierda <--
                self.animate(self.jump_left_sprites, 0.1) #MOVIMIENTO SALTO IZQUIERDO

        #CHEQUEO DE DISPARO:
        if self.animate_fire: #La animacion de DISPARO esta activada? SI:

            if self.velocity.x > 0: #Significa que el movimiento era hacia la derecha -->
                self.animate(self.attack_right_sprites, 0.25) #MOVIMIENTO SALTO DERECHO

            else: #Significa que el movimiento era hacia la izquierda <--
                self.animate(self.attack_left_sprites, 0.25) #MOVIMIENTO SALTO IZQUIERDO

    def jump(self): #Salto del jugador
        
        #El jugador esta colisionando con algun objeto de la plataforma?
        if pygame.sprite.spritecollide(self, self.platform_group,False): #SI:
            
            self.jump_sound.play() #Reproduce el sonido del salto
            #Para saltar nuestra velocidad de salto VERTICAL tiene que ser negativa:
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            #Activo la animacion de salto:
            self.animate_jump = True

    def fire(self): #Disparo del jugador
        
        self.slash_sound.play() #Reproduce el sonido del disparo

        #Le paso a la clase: las coordenadas del jugador, el grupo y el jugador
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)
        self.animate_fire = True #Activa la bandera de disparo

    def reset(self): #Restablece la posicion del jugador
        
        self.position = vector(self.starting_x, self.starting_y) #GUARDO LA POSICION CON LOS VALORES INICIALES
        self.rect.bottomleft = self.position #LLEVO AL JUGADOR A LA POSICION INICIAL

    def animate(self, sprite_list, speed): #Animaciones del jugador

        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.current_sprite < len(sprite_list) -1: #RESTA EN UNO PARA QUE COINCIDA CON CURRENT
            self.current_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.current_sprite = 0 #PARA QUE VUELVA A EMPEZAR

            #COMPROBAR QUE TERMINO LA ANIMACION DE SALTO:
            if self.animate_jump: #SI ESTA ACTIVADO LA ANIMACION:
                self.animate_jump = False #LA DESACTIVA PORQUE O SINO TIENDE AL INFINITO

            #COMPROBAR QUE TERMINO LA ANIMACION DE DISPARO:
            if self.animate_fire: #SI ESTA ACTIVADO LA ANIMACION:
                self.animate_fire = False #LA DESACTIVA PORQUE O SINO TIENDE AL INFINITO                     

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_list[int(self.current_sprite)]

############################################################################################

class Bullet(pygame.sprite.Sprite): #PROYECTIL DISPARADO POR EL JUGADOR

    def __init__(self, x, y, bullet_group, player):

        super().__init__()

        #VARIABLES CONSTANTES DE LA MUNICION
        self.VELOCITY = 20 #VELOCIDAD NO AFECTADA POR LA GRAVEDAD
        self.RANGE = 500 #RANGO <= LUEGO SE DESTRUYE
        
        #ANIMACION DEL PROYECTIL:

        #CONDICIONES PARA ASEGURAR QUE LA ANIMACION SEA LA CORRECTA + CARGA DE LA MISMA

        if player.velocity.x > 0: #Significa que el movimiento es hacia la derecha -->
            
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"),(32,32))

        else: #Significa que el movimiento es hacia la izquierda <--

            #Reutilizo la misma imagen, y la reverso con FLIP: (PRIMER BOOLEAN: "DAR VUELTA HORIZONTALMENTE", SEGUNDO BOOLEAN: "DAR VUELTA VERTICALMENTE")
            self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/player/slash.png"), True, False), (32,32))
            self.VELOCITY = -1 * self.VELOCITY #Garantiza que el disparo tenga orientacion izquierda

        #RECORRIDO DE LA RECTA (rect):

        self.rect = self.image.get_rect() #OBTENGO LA DIRECCION DE PROYECTIL
        self.rect.center = (x,y) #SALDRA DESDE EL CENTRO DE LA POSICION QUE ESTE

        self.starting_x = x #POSICION INICIAL DE LA BALA

        bullet_group.add(self)#Lo agrego al grupo de las municioones

    def update(self):
        
        self.rect.x += self.VELOCITY #Acumulo en el recorrido el movimiento de la bala

        #DESTRUCCION de la bala si supera el RANGO

        #ABS: Devuelve el valor absoluto del número dado = DISTANCIA = MODULO |abs|
        if abs(self.rect.x - self.starting_x) > self.RANGE:

            self.kill() #destruye el objeto - en este caso la bala 
    
############################################################################################    

class Zombie(pygame.sprite.Sprite): #ENEMIGO

    def __init__(self, platform_group, portal_group, min_speed, max_speed):#Iniciar el enemigo
        
        super().__init__()

        #VARIABLES CONSTANTES DE LOS ENEMIGOS:
        self.VERTICAL_ACCELERATION = 3 #GRAVEDAD
        self.RISE_TIME = 2
        
        #AGREGO VIDA AL ZOMBIE (TESTEAR)
        self.STARTING_HEALTH = 100 #VIDA DEL ENEMIGO    

        #ANIMACION DE LOS FOTOGRAMAS - LISTAS VACIAS

        self.walk_right_sprites = [] #MOVIMIENTO DERECHO
        self.walk_left_sprites = [] #MOVIMIENTO IZQUIERDA

        self.die_right_sprites = [] #MUERTE DERECHA
        self.die_left_sprites = [] #MUERZA IZQUIERDA

        self.rise_right_sprites = [] #STUNS - ATURDIR DERECHO
        self.rise_left_sprites = [] #STUNS - ATURDIR IZQUIERDO

        #QUE ENEMIGOS VAN A SALIR: (EN ESTE CASO HOMBRE - MUJER)
        #PERO SE PUEDE USAR PARA AGREGAR VARIAS CLASES DE ENEMIGOS
        #CON PROPIEDADES DIFERENTES - SKINS - HABILIDADES, ETC.

        genero = random.randint(0,1) #COMO SON 2 TIPOS, EL AZAR SON 2 OPCIONES

        #0 = HOMBRE
        #1 = MUJER

        if genero == 0:

            #ANIMACION - CAMINANDO DERECHA: ANEXAR A LA LISTA DE ANIMACIONES
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (1).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (2).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (3).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (4).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (5).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (6).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (7).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (8).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (9).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/walk/Walk (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.walk_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION - MUERTE DERECHA
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.die_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION STUNS - ATURDIMIENTOS

            #INVIERTE EL ORDEN DE LAS ANIMACIONES DE MUERTE PARA QUE "EMPIECE MUERTO Y TERMINE VIVO"
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (10).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (9).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (8).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (7).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (6).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (5).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (4).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (3).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (2).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/boy/dead/Dead (1).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.rise_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        else:

            #ANIMACION - CAMINANDO DERECHA: ANEXAR A LA LISTA DE ANIMACIONES
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (1).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (2).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (3).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (4).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (5).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (6).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (7).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (8).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (9).png"),(64,64)))
            self.walk_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/walk/Walk (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.walk_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION - MUERTE DERECHA
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"),(64,64)))
            self.die_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.die_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            #ANIMACION STUNS - ATURDIMIENTOS

            #INVIERTE EL ORDEN DE LAS ANIMACIONES DE MUERTE PARA QUE "EMPIECE MUERTO Y TERMINE VIVO"
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (10).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (9).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (8).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (7).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (6).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (5).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (4).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (3).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (2).png"),(64,64)))
            self.rise_right_sprites.append(pygame.transform.scale(pygame.image.load("images/zombie/girl/dead/Dead (1).png"),(64,64)))

            #AÑADE LOS MOVIMIENTOS IZQUIERDOS
            for sprite in self.rise_right_sprites:
                #FLIP = INVERTIR(IMAGEN A VOLTEAR, HORIZONTAL, VERTICAL)
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        
        #MOVIMIENTO DE LOS ENEMIGOS: (ALEATORIOS)
        self.direction = random.choice([-1,1]) #SI SALE POR LA DERECHA O IZQUIERDA        

        #SE USARA COMO INDICE DE LA LISTA - VARIABLE AUTODIDACTA
        self.current_sprite = 0

        if self.direction == -1:
            #CARGA LA IMAGEN DE PARTIDA
            self.image = self.walk_left_sprites[self.current_sprite] 
        else:
            self.image = self.walk_right_sprites[self.current_sprite]         

        #OBTENGO LA RECTA (get.rect): Es el recorrido del objeto - En este caso el ENEMIGO
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (random.randint(100, WIDTH - 100), - 100) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #GRUPOS SPRITES:
        self.platform_group = platform_group
        self.portal_group = portal_group

        #BANDERAS PARA LOS EVENTOS DISPARADORES (MUERTE Y ATURDIMIENTO)
        self.animate_death = False
        self.animate_rise = False        

        #CARGA DE SONIDOS
        self.hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav") #SONIDO AL DAÑARSE
        self.kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav") #SONIDO AL MORIR
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav") #SONIDO DEL PORTAL

        #VECTORES DE CINEMATICAS - AUXILIARES
                
        self.position = vector(self.rect.x,self.rect.y) #VECTOR DE POSICION

        #SE MULTIPLICA POR LA DIRECTION PARA DAR LA DIRECCION CORRECTA (POSITIVA O NEGATIVA)
        self.velocity = vector(self.direction * random.randint(min_speed,max_speed),0) #VELOCIDAD DEL ENEMIGO       
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION) #ACELERACION Y GRAVEDAD

        #VALORES INICIALES DEL ENEMIGO - INICIO - REINICIO

        self.is_dead = False #ESTA MUERTO = FALSO
        self.round_time = 0 #TIEMPO DE RONDA
        self.frame_count = 0 #CONTEO DE FOTOGRAMAS

        self.health = self.STARTING_HEALTH #VIDA DEL ENEMIGO (TESTEAR)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        #main_group.add(self)  

    def update(self): #Actualizar el enemigo
        
        self.move()
        self.check_colissions()
        self.check_animations()

        #Determina cuando el zombi debe levantarse despues de ser tumbado:

        if self.is_dead: #TUMBADO = TRUE
            self.frame_count += 1
            if self.frame_count % FPS == 0: #CONTEO DIVISIBLE FPS == 0 - SI
                self.round_time += 1
                if self.round_time == self.RISE_TIME: #SI SON IGUALES EL ENEMIGO SE LEVANTA
                    self.animate_rise = True

                    #Cuando el Enemigo es tumbado, la imagen se mantiene igual
                    #Cuando se levanta tiene que comenzar en el indice cero de nuestro aumento:
                    self.current_sprite = 0
    
    def move(self): #Movimiento del enemigo       
        
            if not self.is_dead: #Mientras no este muerto el Enemigo:

                #Condicion para que sea la animacion correcta:
                if self.direction == -1:
                    self.animate(self.walk_left_sprites, 0.5) #Caminando para la izquierda

                else:
                    self.animate(self.walk_right_sprites, 0.5) #Caminando para la derecha

                #CALCULAR LOS VALORES DE LAS CINEMATICAS:      

                #NO SE NECESITA ACTUALIZAR EL VECTOR DE ACELERACION PORQUE NUNCA CAMBIA.
                
                #MATEMATICA VECTORIAL (5, 2) + (6, 1) = (11, 3)
                
                self.velocity += self.acceleration #ACTUALIZA EL VECTOR DE VELOCIDAD

                self.position += self.velocity + 0.5 * self.acceleration #ACTUALIZA EL VECTOR DE POSICION        

                #ACTUALIZAR LA RECTA (rect) BASADA EN LOS CALCULOS CINEMATICOS:
                
                #CONDICIONES PARA QUE EL ENEMIGO PASE DE UN LADO A OTRO DE LA PANTALLA        

                if self.position.x < 0: #Posicion Jugador menor a 0

                    self.position.x = WIDTH

                elif self.position.x > WIDTH: #Posicion Jugador mayor a la pantalla

                    self.position.x = 0

                #SE PUEDE CAMBIAR PARA QUE EL ENEMIGO NO PUEDA SALIR DE LA PANTALLA

                #DESPUES DE QUE SE ACTUALICEN TODOS LOS VECTORES CORREGIMOS LA POSICION:

                self.rect.bottomleft = self.position
    

    def check_colissions(self): #Chequea las colisiones del enemigo con el entorno

        #spritecollide(Grupo a comprobar, Grupo A Colisionar, Desaparecer objeto al chocar?)
        collided_platforms = pygame.sprite.spritecollide(self, self.platform_group, False) #COMPRUEBA COLISION

        #Tambien se puede usar para dañar al objeto colisionado
        if collided_platforms: #SI LA LISTA >> NO << ESTA VACIA:
                
            #IGUALA LA POSICION AL OBJETO QUE CHOCA + 1: DE REBOTE AL CHOCAR.
            self.position.y = collided_platforms[0].rect.top + 1
            self.velocity.y = 0 #ASEGURA QUE SE DEJE DE MOVER
        
        #Chequea las colisiones con los portales:
        if pygame.sprite.spritecollide(self,self.portal_group, False):

            self.portal_sound.play() #Activa el sonido del portal

            #Una vez que colisiona, determinar a que portal se movera:

            #IZQUIERDA Y DERECHA:

            #Si es mayor a la mitad HORIZONTAL, estas en el LADO DERECHO
            if self.position.x > WIDTH / 2: #Centro de la pantalla Horizontalmente
                self.position.x = 86 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas en el LADO IZQUIERDO
                self.position.x = WIDTH - 150 #150 Pixeles

            #ARRIBA Y ABAJO:

            #Si es mayor a la mitad VERTICAL, estas ARRIBA
            if self.position.y > HEIGHT / 2: #Centro de la pantalla Verticalmente
                self.position.y = 64 #Lleva al jugador a esta posicion
            
            else: #Por contrario estas ABAJO
                self.position.y = HEIGHT - 132 #132 Pixeles

            self.rect.bottomleft = self.position #Guarda la posicion en la recta

    def check_animations(self): #Chequea las animaciones de muerte y ascenso
        
        #ANIMACION MUERTE - TUMBADO:
        if self.animate_death:

            if self.direction == 1: #DIRECCION DERECHA
                self.animate(self.die_right_sprites, .095)

            else: #DIRECCION IZQUIERDA
                self.animate(self.die_left_sprites, 0.95)  

        #ANIMACION "RESURECCION" - LEVANTARSE:
        if self.animate_rise: #LEVANTARSE = TRUE

            if self.direction == 1: #DIRECCION DERECHA
                self.animate(self.rise_right_sprites, 0.95)

            else: #DIRECCION IZQUIERDA
                 self.animate(self.rise_left_sprites, 0.95)   


    def animate(self, sprite_list, speed): #Animaciones del enemigo
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.current_sprite < len(sprite_list) -1: #RESTA EN UNO PARA QUE COINCIDA CON CURRENT
            self.current_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.current_sprite = 0 #PARA QUE VUELVA A EMPEZAR

            #TERMINAR LA ANIMACION DE TUMBADO:
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False #TERMINA EL BUCLE DE ANIMACION 

            #TERMINAR LA ANIMACION DE RESURECCION - LEVANTARSE
            if self.animate_rise: #RESURECCION = TRUE                
                self.animate_rise = False #TERMINA EL BUCLE DE ANIMACION
                self.is_dead = False #Para que no vuelva a TUMBARSE
                #Condicion para que sea la animacion correcta:

                #REINICIAR LAS VARIABLES DE SINCRONIZACION DE TIEMPO:
                self.frame_count = 0 #RECUENTO DE FPS REINICIAR
                self.round_time = 0 #REINICIAR                                               

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_list[int(self.current_sprite)]

############################################################################################

class RubyMaker(pygame.sprite.Sprite): #Animacion de Ruby

    def __init__(self, x, y, main_group):
        
        super().__init__()

        #ANIMACION DE LOS FRAMES DEL RUBY
        self.ruby_sprites = []

        #ANIMACION GIRATORIA:

        #ANEXAR A LA LISTA LAS ANIMACIONES Y RE-DIMENSIONARLAS
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"),(64,64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"),(64,64)))
        
        #SE USARA COMO INDICE DE LA LISTA - VARIABLE AUTODIDACTA
        self.current_sprite = 0

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.ruby_sprites[self.current_sprite] 

        #OBTENGO LA RECTA (get.rect):
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        main_group.add(self)        

    def update(self):

        self.animate(self.ruby_sprites, 0.25)
        # .25 O 0.25 = 1/4 ---> TOMARA 4 BUCLES PARA MOVERSE HACIA EL SIGUIENTE FOTOGRAMA

    def animate(self, sprite_list, speed): #Animacion del Ruby
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.current_sprite < len(sprite_list) -1: #RESTA EN UNO PARA QUE COINCIDA CON CURRENT
            self.current_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.current_sprite = 0 #PARA QUE VUELVA A EMPEZAR

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_list[int(self.current_sprite)]

############################################################################################

class Ruby(pygame.sprite.Sprite): #Ruby: Da puntos y aumenta la salud del jugador

    def __init__(self):
        pass

    def update(self):
        pass

    def move(self): #Movimiento del Ruby
        pass

    def check_colissions(self): #Chequea las colisiones del Ruby con el entorno
        pass
 
############################################################################################

class Portal(pygame.sprite.Sprite): #Portal de teletransportacion

    def __init__(self,x,y, color, portal_group):  
        
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

        #SE USARA COMO INDICE DE LA LISTA - VARIABLE AUTODIDACTA
        self.current_sprite = random.randint(0,len(self.portal_sprites)-1) #INDEX RANDOM

        #CARGA LA IMAGEN DE PARTIDA
        self.image = self.portal_sprites[self.current_sprite] #EMPIEZA SIEMPRE DIFERENTE

        #OBTENGO LA RECTA (get.rect):
        self.rect = self.image.get_rect() #POSICION DE LA RECTA
        self.rect.bottomleft = (x,y) #A PARTIR DE: ABAJO A LA IZQUIERDA = (x,y)

        #AGREGO AL GRUPO PRINCIPAL PARA QUE SE MUESTRE EL DIBUJO:
        portal_group.add(self) 

    def update(self):

        self.animate(self.portal_sprites, .2)

    def animate(self, sprite_list, speed):
        #sprite_list[]: Lista que contiene las animaciones correspondientes
        #speed: Velocidad de la animacion

        if self.current_sprite < len(sprite_list) -1: #RESTA EN UNO PARA QUE COINCIDA CON CURRENT
            self.current_sprite += speed #AGREGO A LA VARIABLE LA VELOCIDAD

        else:
            self.current_sprite = 0 #PARA QUE VUELVA A EMPEZAR

        #ASEGURA DE QUE ESTAMOS CAMBIANDO NUESTRO VALOR ACTUAL DE SPRITE:

        #ESTABLECE LA IMAGEN CON LA VARIABLE + EL SPEED DE LAS CONDICIONES:
        self.image = sprite_list[int(self.current_sprite)]

############################################################################################

#ALMACENAMIENTO DE LOS GRUPOS DE SPRITE
#(DONDE VAN TODOS LOS OBJETOS)

main_tile_group = pygame.sprite.Group() #GRUPO PRINCIPAL DE SPRITES
platform_group = pygame.sprite.Group() #GRUPO DE LOS OBJETOS DENTRO DE LA PLATAFORMA
player_group = pygame.sprite.Group() #GRUPO JUGADOR
bullet_group = pygame.sprite.Group() #GRUPO DE LAS RAFAGAS
zombie_group = pygame.sprite.Group() #GRUPO ENEMIGO
portal_group = pygame.sprite.Group() #GRUPO DEL PORTAL DE TELETRANSPORTACION
ruby_group = pygame.sprite.Group() #GRUPO DE POTENCIADORES - BUFFERS

# MAPA DE MOSAICO: MAPA DEL JUEGO, EN SIMPLES PALABRAS O MATRIZ DEL MAPA

# 0 -> NO REPRESENTA NINGUN AZULEJO (TILE)
# 1 -> TIERRA
# 2-5 -> PLATAFORMAS
# 6 -> RUBI MAKER - POTENCIADOR
# 7-8 -> PORTALES 7 = VERDE ---- 8 = VIOLETA
#9 -> JUGADOR

#23 BALDOSAS (FILAS) - 40 BALDOSAS (FILAS) COLUMNAS

#MATRIZ DEL MAPA (MAPA DE MOSAICO): EN DONDE LOS NUMEROS YA DEFINIDOS ARRIBA SERAN ASIGADOS EN CADA POSICION
#CADA POSICION DE LA MATRIZ REPRESENTA UN AZULEJO EN EL MAPA

tile_map = [

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

    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4], #1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #5
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #6
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #10

    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0], #1
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], #2
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  #3

            ]

#GENERAR LOS OBJETOS DEL MAPA DE MOSAICO

#RECORRER LAS 23 FILAS:

for i in range(len(tile_map)):

    #RECORRER LAS 40 COLUMNAS:
    for j in range(len(tile_map[i])):

    #CADA CONDICION MUESTRA LOS OBJETOS CORRESPONDIENTES:

        #TIERRA:        
        if tile_map[i][j] == 1:

            Tile(j*32, i*32, 1, main_tile_group)
            #COMO NO ES PARTE DE LA PLATAFORMA, VA AL GRUPO PRINCIPAL

        #PLATAFORMA:               
        elif tile_map[i][j] == 2:
            Tile(j*32, i*32, 2, main_tile_group, platform_group)
            #GRUPO PLATAFORMA

        elif tile_map[i][j] == 3:
            Tile(j*32, i*32, 3, main_tile_group, platform_group)
            #GRUPO PLATAFORMA

        elif tile_map[i][j] == 4:
            Tile(j*32, i*32, 4, main_tile_group, platform_group)
            #GRUPO PLATAFORMA
            
        elif tile_map[i][j] == 5:
            Tile(j*32, i*32, 5, main_tile_group, platform_group)
            #GRUPO PLATAFORMA    
        
        #RUBY MAKER:
        elif tile_map[i][j] == 6:
            RubyMaker(j*32, i*32, main_tile_group)
            #COMO NO ES PARTE DE LA PLATAFORMA, VA AL GRUPO PRINCIPAL         

        #PORTALES:
        elif tile_map[i][j] == 7:
            Portal(j*32, i*32 + 35, "green", portal_group)
            #GRUPO PORTAL

        elif tile_map[i][j] == 8:
            Portal(j*32, i*32 + 35, "purple", portal_group) 
            #GRUPO PORTAL
        
        #JUGADOR:
        elif tile_map[i][j] == 9:

            #(32 - 25 = POSICION IZQUIERDA) ---- (32 + 35 = POSICION ARRIBA O ABAJO)    
            player = Player(j*32 - 25, i*32 + 32, platform_group, portal_group, bullet_group) 
            player_group.add(player)
            #GRUPO JUGADOR


#FONDO DE PANTALLA - CARGA LA IMAGEN:
background_image = pygame.transform.scale(pygame.image.load("images/background.png"),(WIDTH,HEIGHT))
#pygame.transform.scale CAMBIA LA ESCALA DE LA IMAGEN(IMAGEN,(ANCHO, ALTO))
#pygame.image.load CARGA LA IMAGEN

#Superficie para rellenar con la imagen cargada:
backgroud_rect = background_image.get_rect() #RECTA (Rect) DEL SPRITE (0,0)
backgroud_rect.topleft = (0,0) #POSICIONA DESDE ARRIBA-IZQUIERDA LA RECTA (Rect) DEL SPRITE

#CREACION DEL JUEGO

game = Game(player, zombie_group, platform_group, portal_group, bullet_group, ruby_group)

#BUCLE PRINCIPAL DEL JUEGO (CICLO DE VIDA DEL JUEGO):

running = True #VARIABLE BANDERA PARA DETERMINAR SI SE ESTA EJECUTANDO EL CICLO

while running: #Mientras se este corriendo el juego:

    for event in pygame.event.get(): #Captura los eventos dentro del juego

        if event.type == pygame.QUIT: #Cuando el evento es igual a X (SALIR)
            running = False #Termina el ciclo del juego

        if event.type == pygame.KEYDOWN:
            #El evento KEYDOWN se produce cuando se presiona una tecla:

            if event.key == pygame.K_SPACE: #BARRA ESPACIADORA
                player.jump() #SALTAR

            if event.key == pygame.K_x: #TECLA X
                player.fire()#DISPARAR

            if event.key == pygame.K_RETURN: #ENTER
                #CREACION DE LOS ENEMIGOS
                zombie = Zombie(platform_group, portal_group, 2, 7)  
                zombie_group.add(zombie)              

    #Dibujar (blit) el fondo en la pantalla:    
    display_surface.blit(background_image, backgroud_rect) #Superposicion (Fondo, Fondo recta)

    #DIBUJAR AZULEJOS - TILES - GRAFICOS - OBJETOS - ESTRUCTURAS - PLATAFORMA - ETC    
    main_tile_group.draw(display_surface)

    #ACTUALIZAR AZULEJOS - TILES - GRAFICOS - OBJETOS - ESTRUCTURAS - PLATAFORMA - ETC  
    main_tile_group.update()

    #ACTUALIZAR Y DIBUJAR LOS GRUPOS DE SPRITES

    portal_group.update()
    portal_group.draw(display_surface)

    player_group.update()
    player_group.draw(display_surface)

    bullet_group.update()
    bullet_group.draw(display_surface)

    zombie_group.update()
    zombie_group.draw(display_surface)

    #ACTUALIZACION Y DIBUJO DEL JUEGO:
    game.update()
    game.draw()    

    #Actualiza la pantalla y los frames:

    pygame.display.update() #Actualiza la pantalla
    clock.tick(FPS) #Cuadros por segundos

#Terminado el ciclo de vida del juego:

pygame.quit() #Cierra todos los procesos utilizados de la lib Pygame
