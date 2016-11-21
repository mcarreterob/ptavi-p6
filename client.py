#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = 'localhost'
#PORT = 6001

try:
    metodo = sys.argv[1]
    datos = sys.argv[2]
    datos_split = sys.argv[2].split('@')
    ip = datos_split[1].split(':')[0]
    PORT = sys.argv[2].split(':')[1]
except IndexError:
    sys.exit('Usage: python3 client.py method receiver@IP:SIPport')

# Contenido que vamos a enviar
LINE = metodo + ' sip:' + datos.split(':')[0] + ' SIP/2.0\r\n'
print(ip)

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((ip, int(PORT)))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))

response = data.decode('utf-8')
slices =  response.split()
if slices[1] == '100' and slices[4] == '180' and slices[7] == '200':
    method = 'ACK'
    AutoLINE = method + ' sip:' + datos.split(':')[0] + ' SIP/2.0\r\n\r\n'
    print('Enviando: ' + AutoLINE)
    my_socket.send(bytes(AutoLINE, 'utf-8') + b'\r\n\r\n')

print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
