#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket #importamos el modulo de socket
from threading import Thread #importamos para los threads
import random


HOST = "" #el host de donde vamos a poder recibir peticiones
PUERTO = 9999  #el puerto donde estaremos escuchando

POKEMONES_DISPONIBLES = ["Gengar" , "Yveltal" , "Blaziken" , "Alakazam" , "Bisharp" , "Charizard"]

#clase para cada uno de los hilos del servidor
class ServidorHilo(Thread):
	def __init__(self , socket_cliente , id):
		Thread.__init__(self) #inicializamos el padre

		self.socket_cliente = socket_cliente
		self.id = id
		self.mandar_pokemon = bytearray([10])
		self.si = bytearray([30])
		self.no = bytearray([31])
		self.intentos_agotados = bytearray([23])
		self.intentos_captura_cliente = random.randint(1,100)
		self.opcion_desconocida = bytearray([42])
		self.pokemon = random.randint(0,5)
		self.numero_intentos_captura_agotados = bytearray([23])
		self.terminar_sesion = bytearray([32])
		
	def capturaPokemon():
		self.estado_anterior = 3
		capturado = random.randint(0,10)
		if capturado <= 3:
			#mandar la imagen del pokemon
			self.socket_cliente.send("mande la foto")
		else:
			if self.intentos_captura_cliente <= 1:
				self.socket_cliente.send(self.intentos_agotados)
			else :
				self.socket_cliente.send(bytearray([21 , self.pokemon , self.intentos_captura_cliente]))
				self.intentos_captura_cliente -=1



	def run (self):
		while True:
			#Recibir datos del cliente
			datos = self.socket_cliente.recv(1024)
			datos = list(datos)
			print (datos)
			if datos[0] == self.mandar_pokemon:
				print self.pokemon
				self.socket_cliente.send(bytearray([20 , self.pokemon]))

			if datos[0] == self.opcion_desconocida:
				self.socket_cliente("Protocol Error 42 : 42 Opcion desconocida ")

			if datos[0] == self.si:
				self.capturaPokemon()

			if datos[0] == self.terminar_sesion:
				print "Terminando sesion con el cliente" , self.id 
				self.socket_cliente.send(self.terminar_sesion)
				break;

			if datos[0] == self.no:
				# print "Terminando sesion con el cliente" , self.id 
				self.socket_cliente.send(self.terminar_sesion)


			"""
			#Opcion para capturar al pokemon
			if datos[0] == "s":
				intentos = random.randint(1,10)
				self.socket_cliente.send("numero de intentos: " + str(intentos))
			#Se cierra sesion cuando el cliente no quiere capturar el pokemon
			elif datos[0] == "n":
				self.socket_cliente.send("Terminando sesion")

			#Si el mensaje recibido es la palabra close se cierra la aplicacion
			if datos == "close":
				break
			#si se reciben los datos nos muestra la IP y el mensaje recibido
			print  "el cliente "+ str(self.id) + " dice: " , datos
			#Devolvemos el mensaje al cliente"""

	
			

#Funcion para iniciar las conexiones
def inicio():
	#instanciamos un objeto para trabajar con el socket
	socket_servidor = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	#Con el metodo bind indicamos que puerto debe de escuchar 
	socket_servidor.bind((HOST , PUERTO))

	#Aceptamos conexciones entrantes con el metodo listen , y ademas aplicamos como parametro 
	#el numero de conexiones que podemos aceptar
	socket_servidor.listen(0)

	salir = False

	print ("esperando cliente ...")
	id = 1
	while not salir:
		#Instanciamos un objeto sc (socket cliente) para recibir datos , al recibir datos este 
		#devolvera tambien un obejto que representa la tupla:IP , puerto
		socket_cliente , addr = socket_servidor.accept()
		
		hilo = ServidorHilo(socket_cliente , id) #creamos un hilo para atender a ese cliente
		hilo.start() # mandamos a correr el hilo 
		print ("un cliente se ha conectado el cliente " + str(id))
		id += 1

if __name__ == '__main__':
	inicio()