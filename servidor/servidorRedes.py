#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket #importamos el modulo de socket
from threading import Thread #importamos para los threads
import random

TIMEOUT = 5.0
HOST = "" #el host de donde vamos a poder recibir peticiones
PUERTO = 9999  #el puerto donde estaremos escuchando

POKEMONES_DISPONIBLES = ["Gengar" , "Yveltal" , "Blaziken" , "Alakazam" , "Bisharp" , "Charizard"]

mandar_pokemon = bytearray([10])
mandar_pokedex = bytearray([11])
autentificacion_correcta = bytearray([12])

intentos_agotados = bytearray([23])
info_pokemon = bytearray([24])
peticion_pokedex = bytearray([26])
info_pokedex = bytearray([28])

si = bytearray([30])
no = bytearray([31])
terminar_sesion = bytearray([32])

#error
opcion_desconocida = bytearray([42])
autentificacion_incorrecta = bytearray([43])
timeout = bytearray([44])

def getBytes(n):
	"""
		Funcion que nos regresa una lista con los 4 bytes que conforman el entero n
		Se convierte el entero n en una cadena de 32 bits y se dan los 4 bytes que lo forman 
	"""
	cadena = str(bin(n))[2:]
	
	while len(cadena) < 32	:
		cadena = "0"+cadena
	lista = []
	lista.append(int(cadena[:8] , 2))
	lista.append(int(cadena[8:16] , 2))
	lista.append(int(cadena[16:24] , 2))
	lista.append(int(cadena[24:32] , 2))
	return lista

def updatePokedex (usuario , pokemon):
	"""
		Funcion que cada vez que un usuario realiza una captura y el pokemon capturado no esta ya registrado
		entonces lo escribe en su pokedex
	"""
	archivo = open("baseDatos/" + str(usuario) , "r")
	linea = archivo.readline()
	pokedex = []
	pokemon = pokemon +"\n"
	while linea:
		pokedex.append(linea)
		linea = archivo.readline()
	archivo.close()
	archivo = open("baseDatos/" + str(usuario) , "a")
	if pokemon not in pokedex:
		archivo.write(pokemon)
	archivo.close()


#clase para cada uno de los hilos del servidor
class ServidorHilo(Thread):
	def __init__(self , socket_cliente, identificador):
		""" 
			Funcion que inicializa el hilo para entender al cliente que tiene como id el identificador
			y el socket_cliente es el socket por el cual se van aestar comunicando
		"""
		Thread.__init__(self) #inicializamos el padre

		self.socket_cliente = socket_cliente
		self.pokemon = random.randint(0,5)
		self.intentos_captura_cliente = random.randint(1,20)
		self.identificador = identificador



	def run (self):
		"""
			Funcion que corre el hilo para intercambiar mensajes con el cliente
		"""
		while True:
			#Recibir datos del cliente
			datos = self.socket_cliente.recv(1024)
			datos = list(datos)
			#self.socket_cliente.settimeout(TIMEOUT)
			if datos[0] == mandar_pokemon:
				self.socket_cliente.send(bytearray([20 , self.pokemon]))

			if datos[0] == info_pokemon:
				archivo = open("pokemonesDisponibles/" + POKEMONES_DISPONIBLES[self.pokemon] + ".png" , "rb")
				contenido = archivo.read(1024)
				while contenido:
					self.socket_cliente.send(contenido)
					contenido = archivo.read(1024)
				archivo.close()

			if datos[0] == si:
				capturado = random.randint(0,9)
				if capturado <= 3:
					archivo = open("pokemonesDisponibles/" + POKEMONES_DISPONIBLES[self.pokemon] + ".png" , "rb")
					contenido = archivo.read()
					mensaje = [22 , self.pokemon] + getBytes(len(contenido))
					self.socket_cliente.send(bytearray(mensaje))
					archivo.close()
					updatePokedex(self.identificador , POKEMONES_DISPONIBLES[self.pokemon])
				else:
					if self.intentos_captura_cliente <= 1:
						self.socket_cliente.send(intentos_agotados)
					else :
						self.socket_cliente.send(bytearray([21 , self.pokemon , self.intentos_captura_cliente]))
						self.intentos_captura_cliente =  self.intentos_captura_cliente-1

			if datos[0] == terminar_sesion:
				print "Terminando sesion con el cliente " , self.identificador
				self.socket_cliente.send(terminar_sesion)
				break;

			if datos[0] == no:
				self.socket_cliente.send(terminar_sesion)

			if datos[0] == opcion_desconocida:
				self.socket_cliente.send(opcion_desconocida)

			if datos[0] == mandar_pokedex:
				archivo = open ("baseDatos/" + str(self.identificador) , "rb")
				contenido = archivo.read()
				mensaje = [27 , self.identificador] + getBytes(len(contenido))
				self.socket_cliente.send(bytearray(mensaje))
				archivo.close()
			
			if datos[0] == info_pokedex:
				archivo = open ("baseDatos/" + str(self.identificador) , "rb")
				contenido = archivo.read(1024)
				while contenido:
					self.socket_cliente.send(contenido)
					contenido = archivo.read(1024)
				archivo.close()
			if datos[0] == timeout:
				break


	
			


def inicio():
	"""
		Funcion que inicia al servidor y cada que entre un cliente creara un hilo para atenderle 
	"""

	#instanciamos un objeto para trabajar con el socket
	socket_servidor = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

	#Con el metodo bind indicamos que puerto debe de escuchar 
	socket_servidor.bind((HOST , PUERTO))

	#Aceptamos conexciones entrantes con el metodo listen , y ademas aplicamos como parametro 
	#el numero de conexiones que podemos aceptar
	socket_servidor.listen(0)
	salir = False
	print ("esperando cliente ...")
	while not salir:
		#Instanciamos un objeto sc (socket cliente) para recibir datos , al recibir datos este 
		#devolvera tambien un obejto que representa la tupla:IP , puerto
		socket_cliente , addr = socket_servidor.accept()
		datos = socket_cliente.recv(1024)
		usr , pwd = datos.split(';')
		archivo = open("baseDatos/usuarios", "r")
		registrado = False
		linea = archivo.readline()
		identificador = 20
		while not registrado:
			if linea:
				identificador, usrb , pwdb = linea.split("\t")
				pwdb = pwdb[:len(pwdb)-1]
				identificador= int(identificador)
				if usrb == usr and pwdb == pwd:
					socket_cliente.send(autentificacion_correcta)
					registrado = True
			else:
				registrado = True
				socket_cliente.send(autentificacion_incorrecta)

			linea = archivo.readline()	
		archivo.close()
		hilo = ServidorHilo(socket_cliente , identificador) #creamos un hilo para atender a ese cliente
		hilo.start() # mandamos a correr el hilo 
		print "un cliente se ha conectado"

		

if __name__ == '__main__':
	inicio()