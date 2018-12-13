#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket #importamos el modulo de socket
from threading import Thread #importamos para los threads
import random


HOST = "" #el host de donde vamos a poder recibir peticiones
PUERTO = 9999  #el puerto donde estaremos escuchando

POKEMONES_DISPONIBLES = ["Gengar" , "Yveltal" , "Blaziken" , "Alakazam" , "Bisharp" , "Charizard"]

mandar_pokemon = bytearray([10])
si = bytearray([30])
no = bytearray([31])
intentos_agotados = bytearray([23])

opcion_desconocida = bytearray([42])
terminar_sesion = bytearray([32])
capturado = bytearray([32])
info_pokemon = bytearray([24])
opcion_desconocida = bytearray([42])
autentificacion_correcta = bytearray([25])
autentificacion_incorrecta = bytearray([43])


def getBytes(n):
	cadena = str(bin(n))[2:]
	
	while len(cadena) < 32	:
		cadena = "0"+cadena
	print cadena 
	lista = []
	lista.append(int(cadena[:8] , 2))
	lista.append(int(cadena[8:16] , 2))
	lista.append(int(cadena[16:24] , 2))
	lista.append(int(cadena[24:32] , 2))
	print lista
	return lista

def updatePokedex (usuario , pokemon):
	archivo = open("baseDatos/" + usuario , "r")
	linea = archivo.readline()
	pokedex = []
	pokemon = pokemon +"\n"
	while linea:
		pokedex.append(linea)
		linea = archivo.readline()
	archivo.close()
	archivo = open("baseDatos/" + usuario , "w")
	if pokemon not in pokedex:
		archivo.write(pokemon)
	archivo.close()


#clase para cada uno de los hilos del servidor
class ServidorHilo(Thread):
	def __init__(self , socket_cliente , usr):
		Thread.__init__(self) #inicializamos el padre

		self.socket_cliente = socket_cliente
		self.usr = usr
		self.pokemon = random.randint(0,5)
		self.intentos_captura_cliente = random.randint(1,20)




	def run (self):
		while True:
			#Recibir datos del cliente
			datos = self.socket_cliente.recv(1024)
			datos = list(datos)
			if datos[0] == mandar_pokemon:
				self.socket_cliente.send(bytearray([20 , self.pokemon]))

			if datos[0] == opcion_desconocida:
				self.socket_cliente("Protocol Error 42 : 42 Opcion desconocida ")

			if datos[0] == info_pokemon:
				archivo = open("pokemonesDisponibles/" + POKEMONES_DISPONIBLES[self.pokemon] + ".png" , "rb")
				contenido = archivo.read(1024)
				while contenido:
					self.socket_cliente.send(contenido)
					contenido = archivo.read(1024)
				archivo.close()
				self.socket_cliente.send(contenido)

			if datos[0] == si:
				capturado = random.randint(0,9)
				if capturado <= 3:
					archivo = open("pokemonesDisponibles/" + POKEMONES_DISPONIBLES[self.pokemon] + ".png" , "rb")
					contenido = archivo.read()
					mensaje = [22 , self.pokemon] + getBytes(len(contenido))
					self.socket_cliente.send(bytearray(mensaje))
					archivo.close()
					updatePokedex(self.usr , POKEMONES_DISPONIBLES[self.pokemon])
					

				else:
					if self.intentos_captura_cliente <= 1:
						self.socket_cliente.send(intentos_agotados)
					else :
						self.socket_cliente.send(bytearray([21 , self.pokemon , self.intentos_captura_cliente]))
						self.intentos_captura_cliente =  self.intentos_captura_cliente-1

			if datos[0] == terminar_sesion:
				print "Terminando sesion con el cliente " + self.usr 
				self.socket_cliente.send(terminar_sesion)
				break;

			if datos[0] == no:
				self.socket_cliente.send(terminar_sesion)

			if datos[0] == opcion_desconocida:

				self.socket_cliente.send(terminar_sesion)

	
			

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
		datos = socket_cliente.recv(1024)
		usr , pwd = datos.split(';')
		archivo = open("baseDatos/usuarios", "r")
		registrado = False
		linea = archivo.readline()
		while not registrado:
			if linea:
				usrb , pwdb = linea.split("\t")
				pwdb = pwdb[:len(pwdb)-1]
				if usrb == usr and pwdb == pwd:
					socket_cliente.send(autentificacion_correcta)
					print ("un cliente se ha conectado el cliente " + usr)

					registrado = True
			else:
				registrado = True
				socket_cliente.send(autentificacion_incorrecta)

			linea = archivo.readline()	
		archivo.close()
		hilo = ServidorHilo(socket_cliente , usr) #creamos un hilo para atender a ese cliente
		hilo.start() # mandamos a correr el hilo 

		

if __name__ == '__main__':
	inicio()