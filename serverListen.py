# Author Francisco Aguirre DNI: 36705359
# Modified Francisco Bosco
# UNNE - Catedra Redes de Datos
# Lic. En Sistemas de Informacion
# Corrientes Argentina 

import socket
import time
import threading
from threading import Thread
from serverResponse import serverResponse

#Clase serverListen que hereda de Theread 
class serverListen(Thread):
      
      #Metodo constructor de la clase
      def __init__(self, mySocket):
            #Instanciamos la clase padre que es de tipo hilo
            Thread.__init__(self)
            #Guardo el Socket que se instancio en el Main
            self.mySocket = mySocket
            #Le asigno un nombre al este hilo
            Thread.name = str("serverListenThread") 
            #Diccionario key -> valor, opciones de menu. 
            self.dic_menu = {'1':'status','2':'conex_activas', '3':'close'}
            #Lista donde se van a almacenar todos los serverResponse activas.
            self.listServerResponse = list()
      
      #end __init__

      #Eliminar serverReponse de la lista de conexiones activas, guardadas por el 
      #servidor que esta escuchando (serverListen)
      def remove_conex(self, p_serverResponse):
            self.listServerResponse.remove(p_serverResponse)

      #end remove_conex

      #Metodo menu 
      def menu(self):
            print("\n*********** Menu de Opciones del Servidor **************\n\n\t1) - Status\n\t2) - Conexiones activas\n")
            opcion = input("Ingresar opcion >> ")

            #Verificamos si la ocion ingresada existe y es llamable en esta clase, por medio del diccionario
            #dic_menu obtenemos el valor de la opciona ingresada
            #Con Hasattr verificar el valor de la key pasa el cliente, si existe ese atributo en la clase
            #callable verificamos si es llamable, si es metodo
            #getattr llamamos a ese metodo
            if hasattr(self, self.dic_menu[opcion]) and callable(getattr(self,self.dic_menu[opcion])):
                  print("\n")
                  #obtenemos el valor y llamamos al metodo corrspondiente
                  getattr(self,self.dic_menu[opcion])()
            else:
                  print("lo siento no entiendo error: 500")

            #end if
                  
      #end menu

      #Obtenemos información a cerca del socket actualmente activo.
      def status(self):
            print('Escuchando >> '+ str(self.mySocket.getsockname()))
            print("\n\n")
            
      #end status

      #vemos las conexiones activas que tiene el servidor
      def conex_activas(self):

            #Recorremos la lista listServerResponse para mostrar todos los clientes activos
            if len(self.listServerResponse) > 0:
                  for x in self.listServerResponse:
                        print('Thread name: '+ x.getName() + ' - IP Client: ' + x.getIpClient() + ' - Port Client: ' + x.getPortClient() )
            else:
                  print("No hay conexiones activas")

            #end if
                  
      #end conex_activas
                  
      def close(self):
            self.status = False
            #self.mySocket.close()
      #end close

      #Metodo run que ce un nuevo hilo 
      def run(self):
            
            while self.status:
                  
                  #Cuando aparece un cliente se realiza la conexion y se captura los datos del cliente.
                  #El meto accep de mySocket devuelve la IP y el puerto
                  self.connectionSocket, self.dataClient = self.mySocket.accept()
                  print('Este es el Socket del cliente'+str(self.dataClient) + "\n\n" )

                  #Se instancia un objeto cliente que iniciara en un nuevo hilo
                  serverReponse = serverResponse(self.connectionSocket, self.dataClient, self)

                  #Esperamos unos dos segundos antes de dar confirmar conexion
                  time.sleep(2)

                  #confirmamos conexion y damos la bienvenida
                  #Este metodo se encuentra en la clase serverResponse
                  serverReponse.msj_bienvenida()
        
                  #Iniciamos el hilo serverResponse(objeto) que va a atender al cliente que se conecto
                  serverReponse.start()

                  self.listServerResponse.append(serverReponse)

            #end while
                  
      #end run
                  
#end class

while True:
      
      try:
            #creamos un objeto del tipo socket y le decimos que vamos a utilizar flujo de
            #datos (TPC), y la familia de protocolos va a ser AF_INET (IPv4)
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            #Permitimos que la IP pueda ser reutilizada.
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            #Solicitamos un puerto que deseemos escuchar.
            portServer = int(input("Ingrese el puerto a escuchar: "))

            #Le indicamos al Sistema Operativo que vamos a atender conexiones por este puerto.
            serverSocket.bind(("192.168.200.60",portServer))

            #Se establece la conexion y se empieza a escuchar en el puerto correspondiente, como parametro,
            #el nro de conexiones en espera de manera simultanea.
            serverSocket.listen(1)

            #Creamos el servidor principal que escuchara el puerto y delegara a los serverResponse
            #la llegada de nuevos clientes.
            servList = serverListen(serverSocket)

            #Iniciamos el hilo principal que estara escuchando el puerto
            #Llama al metodo run, start es un metodo de Thread.
            #Y ahi comienza el segundo plano del hilo 
            servList.start()

            #Pequeño menu de administración del servidor principal, (serverListen)
            while servList.status:
                  servList.menu()

            #end while

            break
      except ValueError:
            print("Valor del puerto invalido, intentelo nuevamente!\n")

      #end Try
      
print('Conexion Cerrada')
