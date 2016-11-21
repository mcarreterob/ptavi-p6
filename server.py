#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


try:
    IP = sys.argv[1]
    PORT = sys.argv[2]
    audio_file = sys.argv[3]
except IndexError:
    print('Usage: python server.py IP port audio_file')

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #ip = self.client_address[0]
        #PORT = self.client_address[1]
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line = line.decode('utf-8')
            print("El cliente nos manda " + line)
            line_slices = line.split()
            
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            metodo = line_slices[0]
            if metodo == 'INVITE':
                self.wfile.write(b'SIP/2.0 100 Trying\r\n\r\n')
                self.wfile.write(b'SIP/2.0 180 Ring\r\n\r\n')
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
            elif metodo == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
            elif metodo == 'ACK':
                aEjecutar = 'mp32rtp -i ' + IP + ' -p 23032 < ' + audio_file
                print ('Vamos a ejecutar', aEjecutar)
                os.system(aEjecutar)
                print('Finished transfer')
            elif metodo != 'INVITE' or metodo != 'BYE' or metodo != 'ACK':
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
            else:
                self.wfile.write(b'SIP/2.0 400 Bad Request')


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    if os.path.exists(audio_file):
        serv = socketserver.UDPServer((IP, int(PORT)), EchoHandler)
        print("Listening...")
        serv.serve_forever()
    else:
        sys.exit('Audio file not found')
