#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket # importamos los modulos para trabajar con sockets
import sys #importamos los modulos para poder acceder a la linea de comandos 

POKEMONES_DISPONIBLES = ["Gengar" , "Yveltal" , "Blaziken" , "Alakazam" , "Bisharp" , "Charizard"]
pedir_pokemon =  bytearray([10])
#recibir_pokemon = 20
recibir_pokemon = bytearray([20])
si = bytearray([30])
no = bytearray([31])
intentos_agotados = bytearray(23)
opcion_desconocida = bytearray([42])
numero_intentos_captura_agotados = bytearray([23])
terminar_sesion = bytearray([32])
def obtener_indice (respuesta):
	for i in range(0,50):
		if bytearray([i]) == respuesta:
			return i
	

def inicio(ip_servidor,puerto):

	#Creamos un objeto de tipo socket para el servidor
	s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	try:
		#Nos conectamos al al servidor con el metodo connect. Tiene dos parametros
		#El primero es la IP del servidor y el segundo es el puerto de conexion 
		s.connect((ip_servidor , int(puerto)))
	except:
		print "Protocol Error 41 \n No se pudo conectar con el servidor"
	else:
		#Creamos un bucle para retener la conexion
		
		#mensaje para poder establecer la conexion
		mensaje = bytearray([10])
		s.send(mensaje)

		while True:
			#Con la distancia del objeto servidor (s) y el metodo , send enviamos el mensaje
			respuesta = s.recv(1024)
			respuesta = list(respuesta)
			print(respuesta)
			if respuesta[0] == recibir_pokemon:
				print("¿Te gustaria capturar a el pokemon " + POKEMONES_DISPONIBLES[obtener_indice(respuesta[1])] + "?")
				mensaje = raw_input(">> ")
				if mensaje == "si":
					s.send(si)

				if mensaje == "no":
					s.send(no)
				

			if respuesta[0] == intentos_agotados:
				s.send(terminar_sesion)

			if respuesta[0] == terminar_sesion:
				print "Terminando sesion"
				s.send(terminar_sesion)
				break;
		
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
