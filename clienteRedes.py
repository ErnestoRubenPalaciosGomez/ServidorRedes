#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket # importamos los modulos para trabajar con sockets
import sys #importamos los modulos para poder acceder a la linea de comandos 

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
		while True:
			#Con la distancia del objeto servidor (s) y el metodo , send enviamos el mensaje
			s.send(mensaje)
			respuesta = s.recv(1024)
			print respuesta
			mensaje = raw_input(">> ")
			s.send(mensaje)
			"""
			#Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
			mensaje = raw_input("Mensaje a enviar : ")
			#Con la distancia del objeto servidor (s) y el metodo , send enviamos el mensaje
			s.send(mensaje)
			#Obtenemos la contestacion del cliente con
			"""
			respuesta = s.recv(1024)
			#respuesta = s.recv(1024)
			#print respuesta

			print respuesta
			if respuesta == "n":
				break

			#Si por alguna razon el mensaje es close se cierra la conexion
			if mensaje == "close":
				break
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
