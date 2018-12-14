#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket # importamos los modulos para trabajar con sockets
import sys #importamos los modulos para poder acceder a la linea de comandos

TIMEOUT = 5.0
POKEMONES_DISPONIBLES = ["Gengar" , "Yveltal" , "Blaziken" , "Alakazam" , "Bisharp" , "Charizard"]

pedir_pokemon =  bytearray([10])
pedir_pokedex = bytearray([11])


recibir_pokemon = bytearray([20])
no_capturado = bytearray([21])
pokemon_capturado = bytearray([22])
intentos_agotados = bytearray([23])
info_pokemon = bytearray([24])
autentificacion_correcta = bytearray([25])
recibir_pokedex  = bytearray([27])
info_pokedex = bytearray([28])

si = bytearray([30])
no = bytearray([31])
terminar_sesion = bytearray([32])


opcion_desconocida = bytearray([42])
autentificacion_incorrecta = bytearray([43])
timeout = bytearray([44])


def obtenerNum(respuesta):
	"""
		Nos dice que entero corresponde <respuesta>
	"""
	for i in range(0,255):
		if bytearray([i]) == respuesta:
			return i
	
def getNum(lista_bytes):
	"""
		Dada una lista de bytes se quitan los primeros 2 que son mensajes del servidor
		y de los 4 restantes nos dan el numero en decimal que forman
	"""
	lista = lista_bytes[2:]
	resultado = ""
	for x in lista:
		y = obtenerNum(x)
		y = str(bin(y))[2:]
		while len(y) < 8:
			y = "0" + y
		resultado = resultado + y
	return int(resultado , 2)

def enviaRespuesta(socket):
	"""
		Funcion que manda al servidor la respuesta de si y no
		Se ocupa cuando el mensaje del servidor es 20 o 21
	"""
	mensaje = raw_input(">> ")
	if mensaje == "s":
		socket.send(si)

	if mensaje == "n":
		socket.send(no)

def enviaUsuarioPass(socket):
	"""
		Funcion que envia el usuario y contraseña con los que nos queremos conectar al servidor por medio
		del socket
	"""
	usuario = raw_input("Usuario: ")
	contra = raw_input("Contraseña: ")
	usuario_sesion = usuario
	socket.send(usuario + ";" + contra) 

def menu(socket):
	"""
		menu de inicio que nos da las acciones que se pueden hacer una vez que ya se estrablecio conexion
		con el servidor y manda esa opcion al servidor 
	"""
	print "Que quieres hacer:\n"
	print "1 .- Revisar tu pokedex\n"
	print "2 .- Pedir un pokemon"
	mensaje = raw_input(">> ")
	if mensaje == "1":
		socket.send(pedir_pokedex)
	else :
		if mensaje == "2":
			socket.send(pedir_pokemon)
		else:
			socket.send(opcion_desconocida)

def inicio(ip_servidor,puerto):
	"""
		Funcion principal que inicial al cliente con 
		<ip_servidor> : la ip del servidor al cual nos vamos a conectar
		<puerto> : el puerto por el cual se va a establecer la comunicacion
	"""

	#Creamos un objeto de tipo socket para el servidor
	s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	try:
		#Nos conectamos al al servidor con el metodo connect. Tiene dos parametros
		#El primero es la IP del servidor y el segundo es el puerto de conexion 
		s.connect((ip_servidor , int(puerto)))
	except:
		print "Protocol Error 41 \nNo se pudo conectar con el servidor"
	else:
		#Creamos un bucle para retener la conexion
		
		#mensaje para poder establecer la conexion
		#s.send(pedir_pokemon)
		enviaUsuarioPass(s)
		#iteracion = 0
		try : 
			while True:
				#Con la distancia del objeto servidor (s) y el metodo , send enviamos el mensaje
				respuesta = s.recv(1024)
				respuesta = list(respuesta)
				#s.settimeout(TIMEOUT)
				if respuesta[0] == autentificacion_correcta:
					menu(s)

				if respuesta[0] == autentificacion_incorrecta:
					print("Error 43 \nUsuario o contraseña invalidas")
					s.send(terminar_sesion)
				if respuesta[0] == recibir_pokemon:
					print("¿Te gustaria capturar a el pokemon " + POKEMONES_DISPONIBLES[obtenerNum(respuesta[1])] + "?[s/n]")
					enviaRespuesta(s)
						
				if respuesta[0] ==  no_capturado:
					print("¿Intentar capturar de nuevo? Quedan " + str(obtenerNum(respuesta[2]))+ " intentos [s/n]")
					enviaRespuesta(s)

				if respuesta[0] == intentos_agotados:
					s.send(terminar_sesion)

				if respuesta[0] == pokemon_capturado:
					s.send(info_pokemon)
					dato = getNum(respuesta)
					archivo = open("pokemonesCapturados/" + POKEMONES_DISPONIBLES[obtenerNum(respuesta[1])] + ".png" , "wb")
					print "Obteniendo el pokemon ..."
					while dato > 0:
						respuesta = s.recv(1024)
						archivo.write(respuesta)
						dato -=1024
					archivo.close()
					print "pokemon guardado con exito"
					s.send(terminar_sesion)
					
				if respuesta[0] == terminar_sesion:
					print "Terminando sesion"
					s.send(terminar_sesion)
					break;

				if respuesta[0] == opcion_desconocida:
					print "Opcion desconocida"
					s.send(terminar_sesion)
					break;
				if respuesta[0] == recibir_pokedex:
					s.send(info_pokedex)
					dato = getNum(respuesta)
					print "Obteniendo la pokedex ..."
					archivo = open("pokedex/" + str(obtenerNum(respuesta[1]))  + ".pokedex" , "wb")
					while dato > 0:
						contenido = s.recv(1024)
						archivo.write(contenido)
						dato -=1024
					archivo.close()
					print "pokedex guardada con exito"
					s.send(terminar_sesion)
				
				if respuesta[0] == timeout:
					print "Protocol Error 44 tiempo excedido"
					break	
		except:
			s.send(timeout)		
		
		#Imprimimos adios cuando se cierre la conexion
		print "Adios"
		#Cerramos la instancia de servidor
		s.close()

if __name__ == '__main__':
	if len(sys.argv) == 3:
		_ , ip_servidor , puerto = sys.argv
		inicio (ip_servidor , puerto)

	else:
		print "Error en los parametros"
