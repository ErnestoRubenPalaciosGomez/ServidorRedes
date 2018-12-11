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
	def run (self):
		while True:
			#Recibir datos del cliente
			datos = self.socket_cliente.recv(1024)
			datos = list(datos)
			if datos[0] == self.mandar_pokemon:
				self.socket_cliente.send("¿Te gustaria capturar a el pokemon " + POKEMONES_DISPONIBLES[random.randint(0,6)-1] + "?")

			#Si el mensaje recibido es la palabra close se cierra la aplicacion
			if datos == "close":
				break
			#si se reciben los datos nos muestra la IP y el mensaje recibido
			print  "el cliente "+ str(self.id) + " dice: " , datos
			#Devolvemos el mensaje al cliente
			

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











"""
#Funcion para iniciar las conexiones
def inicio():
	#instanciamos un objeto para trabajar con el socket
	socket_servidor = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	#Con el metodo bind indicamos que puerto debe de escuchar 
	socket_servidor.bind(("" , 9999))

	#Aceptamos conexciones entrantes con el metodo listen , y ademas aplicamos como parametro 
	#el numero de conexiones que podemos aceptar
	socket_servidor.listen(2)
	
	salida = False

	print ("esperando cliente ...")
	#Instanciamos un objeto sc (socket cliente) para recibir datos , al recibir datos este 
	#devolvera tambien un obejto que representa la tupla:IP , puerto
	socket_cliente , addr = socket_servidor.accept()
	print ("un cliente se ha conectado ... ")

	while not salida:
		#Recibimos el mensaje , con el metodo recv recibimos datos y como parametro la cantidad de bytes a escribir
		recibido = socket_cliente.recv(1024)

		#Si el mensaje recibido es la palabra close se cierra la aplicacion
		if recibido == "close":
			break

		#si se reciben los datos nos muestra la IP y el mensaje recibido
		print str(addr[0]) + " dice: " , recibido

		#Devolvemos el mensaje al cliente
		socket_cliente.send("mensaje recibido")
	print "Adios"

	socket_cliente.close()
	socket_servidor.close()

if __name__ == '__main__':
	inicio() """
 