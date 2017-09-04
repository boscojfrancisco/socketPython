#importamos modulo para trabajar con sockets.
import socket
import time
import os

#creamos un objeto del tipo socket y le decimos que vamos
#a utilizar flujo de datos (TPC).
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

value = True
while value:
      try:
            #serverHost = input("Ingrese la IP del servidor a conectar: >> ")
            serverPort = int(input("Ingrese el Puerto del servidor a conectar: >> "))
      
            #Establecemos conexion con el servidor, como parametro le pasamos la
            #ip de servidor y el puerto del mismo al cual nos vamos a conectar.
            clientSocket.connect(("localhost", serverPort))

            value = False
      except Exception:
            print("Vuelve a intentarlos, la conexion no se pudo realizar.")
      

      

#Creamos un bucle para retener la conexion.
seguir = True
while seguir:
      #Recibimos los datos que llegan al socket cliente por medio
      #del metodo recv, como tamaño de buffer le pasamos 1024 bytes.
      msjServer = clientSocket.recv(1024)

      print ("\n***************************************")
      print ("Server response >> ", msjServer.decode())
      #Instanciamos un flujo de entrada de datos, para que el
      #cliente pueda enviar datos.
      request = input("request >> ")
      #Enviamos el mensaje al servidor por medio del metodo sendto
      clientSocket.send(request.encode())

      if request == "close":
            clientSocket.close()
            seguir = False
            
#end while
print ("\n>> cerrando conexion...")
time.sleep(1)
print ("\n*********** LA CONEXION HA SIDO CERRADA EXITOSAMENTE ***********")

clientSocket.close()
