# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from random import randint
import os.path
import math

class punto:
	def __init__(self, x, y):
			self.x = x
			self.y = y
	
ANCHO_VENTANA = 600
ALTO_VENTANA = 400

ANCHO_RAQUETA = 10
ALTO_RAQUETA = 60
	
ANCHO_BOLA = ALTO_BOLA = 10

VELOCIDADE_RAQUETA = 5

y_raqueta_esquerda = y_raqueta_dereita = (ALTO_VENTANA - ALTO_RAQUETA) / 2
	
x_raqueta_esquerda = 0
x_raqueta_dereita = ANCHO_VENTANA - ANCHO_RAQUETA
	
punto_bola = punto((ANCHO_VENTANA-ANCHO_BOLA)/2,(ALTO_VENTANA-ALTO_BOLA)/2)

VELOCIDADE_BOLA_TOTAL = 7

VELOCIDADE_BOLA_Y = 2

def calc_vel_x():
	return VELOCIDADE_BOLA_TOTAL * (math.sin(math.radians(90 - math.degrees(math.asin(VELOCIDADE_BOLA_Y/float(VELOCIDADE_BOLA_TOTAL))))))

VELOCIDADE_BOLA_X = calc_vel_x()

puntuacion_esquerda = puntuacion_dereita = 0

if randint(0,1) == 1:
	VELOCIDADE_BOLA_X = -VELOCIDADE_BOLA_X
	
VELOCIDADE_MAX_BOLA_Y = 5

if randint(0,1) == 1:
	VELOCIDADE_BOLA_Y = -VELOCIDADE_BOLA_Y

ancho_cadrados_centrales = 2
separacion_cadrados_centrales = 5

TICKS_SEGUNDO = 60

pausa_ticks = 1000 // TICKS_SEGUNDO

#INICIAR PYGAME

pygame.init()

ventana = pygame.display.set_mode([ANCHO_VENTANA, ALTO_VENTANA],0,32)
pygame.display.set_caption("Python_Pong")

sonidos = False

if os.path.exists("sounds/pong_bep.ogg") and os.path.exists("sounds/pong_plop.ogg"):
	sonido_bep = pygame.mixer.Sound("sounds/pong_bep.ogg")
	sonido_plop = pygame.mixer.Sound("sounds/pong_plop.ogg")
	sonido_bep.set_volume(0.1)
	sonido_plop.set_volume(0.1)
	sonidos = True

#FUNCIÓN PARA CALCULAR DIRECCIÓN DA BOLA DESPOIS DE UN CHOQUE:

def calcular_direccion(bola_y,y_raqueta_esq,vel_bola_y):
	VEL_Y = VELOCIDADE_BOLA_Y
	choque_altura = (bola_y+ANCHO_BOLA) - y_raqueta_esq
	VEL_Y = (((choque_altura * 100)/ALTO_RAQUETA) * 0.1) - VELOCIDADE_MAX_BOLA_Y
	VEL_Y = max(-VELOCIDADE_MAX_BOLA_Y, VEL_Y)
	VEL_Y = min(VELOCIDADE_MAX_BOLA_Y, VEL_Y)
	return VEL_Y

#BUCLE DE XOGO

pausa_bola = 30

ON = True

while ON:

	#tempo_0 = pygame.time.get_ticks()
	reloj = pygame.time.Clock()
	
	#DEBUXAR:
	
	ventana.fill((0,0,0))
	
	imagen_raqueta_esq = pygame.Rect(x_raqueta_esquerda,y_raqueta_esquerda,ANCHO_RAQUETA,ALTO_RAQUETA)
	pygame.draw.rect(ventana, (255,255,255), imagen_raqueta_esq)
		
	imagen_raqueta_der = pygame.Rect(x_raqueta_dereita,y_raqueta_dereita,ANCHO_RAQUETA,ALTO_RAQUETA)
	pygame.draw.rect(ventana, (255,255,255), imagen_raqueta_der)
	
	
	for i in range(1, ALTO_VENTANA, separacion_cadrados_centrales):
		pygame.draw.rect(ventana, (255,255,255), pygame.Rect((ANCHO_VENTANA-ancho_cadrados_centrales)/2,i,ancho_cadrados_centrales,ancho_cadrados_centrales))
	
	font = pygame.font.SysFont("System",40)
	puntuacion1 = font.render(str(puntuacion_esquerda),1,(255,255,255))
	ventana.blit(puntuacion1,((ANCHO_VENTANA/2)-puntuacion1.get_width()*2,ALTO_VENTANA/20))
	
	puntuacion2 = font.render(str(puntuacion_dereita),1,(255,255,255))
	ventana.blit(puntuacion2,((ANCHO_VENTANA/2)+puntuacion1.get_width(),ALTO_VENTANA/20))
		
	imagen_bola = pygame.Rect(punto_bola.x,punto_bola.y,ANCHO_BOLA,ALTO_BOLA)
	pygame.draw.rect(ventana, (255,255,255), imagen_bola)
	pygame.draw.rect(ventana, (255,255,255), imagen_bola)
	
	#--
	
	if pausa_bola > 0:
		pausa_bola -= 1

	#MOVEMENTO DA RAQUETA ESQUERDA:
	
	tecla_pulsada = pygame.key.get_pressed()
	if tecla_pulsada[K_UP]:
		y_raqueta_esquerda -= VELOCIDADE_RAQUETA
	if tecla_pulsada[K_DOWN]:
		y_raqueta_esquerda += VELOCIDADE_RAQUETA
		
	y_raqueta_esquerda = max(0,y_raqueta_esquerda)
	y_raqueta_esquerda = min(ALTO_VENTANA-ALTO_RAQUETA,y_raqueta_esquerda)
		
	#MOVEMENTO DA BOLA:
	
	if pausa_bola == 0:
		punto_bola = punto(punto_bola.x+VELOCIDADE_BOLA_X, punto_bola.y+VELOCIDADE_BOLA_Y)
		
	punto_bola = punto(punto_bola.x,max(-ALTO_BOLA,punto_bola.y))
	punto_bola = punto(punto_bola.x,min(ALTO_VENTANA-ALTO_BOLA,punto_bola.y))
	
	if punto_bola.x+ANCHO_BOLA*2 < 0 or punto_bola.x > ANCHO_VENTANA+ANCHO_BOLA:
		if sonidos:
			sonido_plop.play()
		if punto_bola.x+ANCHO_BOLA*2 < 0:
			puntuacion_dereita += 1
		if punto_bola.x > ANCHO_VENTANA+ANCHO_BOLA:
			puntuacion_esquerda += 1
		pausa_bola = 20
		punto_bola = punto((ANCHO_VENTANA-ANCHO_BOLA)/2,(ALTO_VENTANA-ALTO_BOLA)/2)
		if randint(0,1) == 1:
			VELOCIDADE_BOLA_X = -VELOCIDADE_BOLA_X
		VELOCIDADE_BOLA_Y = 2
		if randint(0,1) == 1:
			VELOCIDADE_BOLA_Y = -VELOCIDADE_BOLA_Y
		VELOCIDADE_BOLA_X = calc_vel_x()
	
			
	#MOVEMENTO DA RAQUETA DEREITA:
	
	VELOCIDADE_RAQUETA_DEREITA = 4
	
	if y_raqueta_dereita < punto_bola.y and punto_bola.x >= ANCHO_VENTANA/2 and VELOCIDADE_BOLA_X > 0:
		y_raqueta_dereita += VELOCIDADE_RAQUETA_DEREITA
	elif y_raqueta_dereita > punto_bola.y and punto_bola.x >= ANCHO_VENTANA/2 and VELOCIDADE_BOLA_X > 0:
		y_raqueta_dereita -= VELOCIDADE_RAQUETA_DEREITA
	else:
		y_raqueta_dereita
	
	y_raqueta_dereita = max(0,y_raqueta_dereita)
	y_raqueta_dereita = min(ALTO_VENTANA-ALTO_RAQUETA,y_raqueta_dereita)
	
	#COLISIÓNS:
	
		#PAREDES:
	
	if punto_bola.y <= 0 and VELOCIDADE_BOLA_Y < 0:
		VELOCIDADE_BOLA_Y = -VELOCIDADE_BOLA_Y
		if sonidos:
			pygame.mixer.stop()
			sonido_bep.play()
			
	if punto_bola.y >= ALTO_VENTANA - ANCHO_BOLA and VELOCIDADE_BOLA_Y > 0:
		VELOCIDADE_BOLA_Y = -VELOCIDADE_BOLA_Y
		if sonidos:
			pygame.mixer.stop()
			sonido_bep.play()
	
		#RAQUETA ESQUERDA:
	
	if (punto_bola.x > 0 and punto_bola.x <= ANCHO_RAQUETA) and (y_raqueta_esquerda <= (punto_bola.y+ANCHO_BOLA) and (y_raqueta_esquerda+ALTO_RAQUETA) >= punto_bola.y) and VELOCIDADE_BOLA_X < 0:
		VELOCIDADE_BOLA_X = -VELOCIDADE_BOLA_X
		VELOCIDADE_BOLA_Y = calcular_direccion(punto_bola.y,y_raqueta_esquerda,VELOCIDADE_BOLA_Y)
		VELOCIDADE_BOLA_X = calc_vel_x()
		if sonidos:
			pygame.mixer.stop()
			sonido_bep.play()
		
		#RAQUETA DEREITA:
		
	if (punto_bola.x < ANCHO_VENTANA-ANCHO_BOLA and punto_bola.x >= ANCHO_VENTANA-(ANCHO_BOLA+ANCHO_RAQUETA)) and (y_raqueta_dereita <= (punto_bola.y+ANCHO_BOLA) and (y_raqueta_dereita+ALTO_RAQUETA) >= punto_bola.y) and VELOCIDADE_BOLA_X > 0:
		VELOCIDADE_BOLA_X = -VELOCIDADE_BOLA_X
		if sonidos:
			pygame.mixer.stop()
			sonido_bep.play()
			
	for eventos in pygame.event.get():
		if eventos.type == pygame.QUIT:
			pygame.display.quit()
			ON = False
	
	pygame.display.update()
	
	#tempo_frame = pygame.time.get_ticks() - tempo_0
	#pygame.time.wait(max(0,pausa_ticks - tempo_frame))
	reloj.tick(TICKS_SEGUNDO)