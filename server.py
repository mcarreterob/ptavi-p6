#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

IP = sys.argv[1]
PORT = sys.argv[2]
audio_file = sys.argv[3]


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        ip = self.client_address[0]
        PORT = self.client_address[1]
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().decode('utf-8')
            line_slices = line.split()
            if not line:
                break
            metodo = line_slices[0]
            if metodo == 'INVITE':
                self.wfile.write(b'SIP/2.0 100 Trying \r\n\r\n')
                self.wfile.write(b'SIP/2.0 180 Ring \r\n\r\n')
                self.wfile.write(b'SIP/2.0 200 OK \r\n\r\n')
            if metodo == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK \r\n\r\n')
            #print("El cliente nos manda " + line.decode('utf-8'))

            # Si no hay más líneas salimos del bucle infinito
            

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', int(PORT)), EchoHandler)
    print("Listening...")
    serv.serve_forever()
