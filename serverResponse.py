from threading import Thread #Importamos la clase
import re #Importamos la libreria regex necesaria para trabajar con expresiones regulares
import time
import sys
from os import curdir, sep

class serverResponse(Thread): #Heredamos comportamiento de la clase Thread

      bienvenida = "    A - BIENVENIDO, ESPERO REQUEST ****" 
      

      #Metodo constructor de la clase
      def __init__(self, connectionSocket, dataClient, myParent):
            #Instanciamos la clase padre.
            Thread.__init__(self)

            #Guardamos los parametros recibidos
            self.connectionSocket = connectionSocket
            self.serverHTTP = 'HTTP/1.1'
            self.dataClient = dataClient
            self.create_log
            self.while_run = True
            self.myParent = myParent
            self.method_list = ['GET', 'POST', 'HEAD', 'OPTION']
            self.version_http_supported = ['HTTP/1.0','HTTP/1.1']

            self.status_dic = {400 : 'ERROR 400 - Bad Request : Solicitud con sintaxis errónea', \
            404 : 'ERROR 404 -  Not Found: Recurso no encontrado', \
            200 : '200 - OK'}

            Thread.name = str("serverResponseThread")
            
      #end __init__

      def send(self, msg):
            self.connectionSocket.send(msg.encode('utf8'))

      #end send
            
      def recv(self):
            return self.connectionSocket.recv(1024).decode('utf8')
      
      #end recv

      #Crea un log.txt donde se guarda el historial de commandos solicitados
      def create_log(self):
            arch=open('log.txt','w')
            arch.close()
            
      #end create_log

      def get_nameClient(self):
            return self.connectionSocket.getbyaddr("127.0.0.1")
      
      #Agrega información al archivo log
      def add_log(self, comand, commit):
            fecha = time.strftime("%c") #Obtenemos la fecha y hora actual 
            arch=open('log.txt','a')
            arch.write(comand + " \t\t " + str(self.dataClient[0]) + ':' + str(self.dataClient[1]) + " \t " + commit + " \t " + fecha +"\n")
            arch.close()
            
      #end add_log
      
      def msj_bienvenida(self):
            self.send(self.bienvenida)
      
      #end msj_bienvebida

      def ask(self):
            self.send("Sigo aquí.")
      
      #end ask

      #Devuelve la ip del Cliente que esta atendiendo
      def getIpClient(self):
            return str(self.dataClient[0])
      
      #end getIpClient

      #Devuelve el puerto del Cliente que esta atendiendo
      def getPortClient(self):
            return str(self.dataClient[1])
      
      #end getPortClient
         
      def ip(self):
            self.send(str('Tu ip: ') + str(self.dataClient[0]))
      
      #end ip

      def puerto(self):
            self.connectionSocket.send(str('Tu puerto: ').encode()+str(self.dataClient[1]).encode())
      
      #end ip

      def ayuda(self):
            msj = """\n\nask -> Ver si sigo escuchando\nayuda -> Lista de request que entiendo.\n""" \
                  """ip -> Devuelvo tu ip\npuerto -> Devuelvo tu puerto por al cual me comunico\n""" \
                  """close -> Cierro la conexion.\n""" \
                  """HTTP Request -> [method] [resource] [version protocolo]\n"""
            self.connectionSocket.send(msj.encode())
      
      #end ask2

      def close(self):
            #remuevo esta conexion de la lista de conexiones activas
            #que se encuentra en el servidor que esta escuchando
            self.myParent.remove_conex(self)
            self.connectionSocket.close()
            self.while_run = False

      #end close

      def encabezado(self, p_code, p_content_type):
            head = ("\n\n%s %s \n" \
            "Date: %s\nContent-type: %s\n\n" \
            %(self.serverHTTP, self.status_dic[p_code],  time.strftime("%c"), p_content_type))
            return head
      #end encabezado

      def GET(self, p_request):
            resource = self.obtener_palabra(p_request, 1)
            version_server = self.obtener_palabra(p_request, 2)
            if resource == "/":
                  resource = "/index.html"

            try:

                  if resource.endswith(".html"):
                        mimetype = 'text/html'
                  if resource.endswith(".css"):
                        mimetype = 'text/css'

                  file = open(curdir + sep + resource)
                  body = file.read()
                  file.close()

                  head = self.encabezado(200, mimetype)
                  msj = str(head) + str(body) + "\n\n"
                  self.send(msj)

            except IOError:
                  head_err = self.encabezado(404, "text/html")
                  self.send_error_http(p_request, 404, head_err)

            #end if

      #end GET
      
      def contar_palabras(self, p_string):
            return len(p_string.split(' '))

      #end contar_palabras

      def obtener_palabra(self, p_string, p_nro_palabra):
            return p_string.strip().split(' ')[p_nro_palabra]

      #end primer_palabra

      def es_method_http(self, p_method):
            return (str(p_method) in self.method_list)

      #end es_mehod_http
      
      def send_error_http(self, p_request, p_code_error, p_head):
            msg = p_head + ("<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>%s</title>\n" \
                  "\t</head>\n\t<body>\n\t</body>\n</html>\n\n" %self.status_dic[p_code_error])

            self.connectionSocket.send(msg.encode('UTF-8'))
            self.add_log(p_request, ("Error: %s" % p_code_error))

      #end send-error

      def send_error(self, p_request, p_code_error):
            msg = self.status_dic[p_code_error]
            self.connectionSocket.send(msg.encode('utf8'))
            self.add_log(p_request, ("Error: %s" % p_code_error))

      #end send-error

      def run(self):
            
            while self.while_run:
                  
                  try:
                        
                        #Esperamos request del cliente, quita espacio con strip
                        request = self.recv().strip()

                        #Verificamos el nro de palabras en la solicitud
                        if self.contar_palabras(request) == 3 or self.contar_palabras(request) == 1:
                              #Obtenemos la primer palabra (o la unica) de la solicitud
                              method = self.obtener_palabra(request, 0)

                              #Verificamos que sea un atributo de la clase y que si es llamable
                              if hasattr(self, method) and callable(getattr(self, method)):

                                    #Si es una una pablabra y no es ningún metodo HTTP
                                    if self.contar_palabras(request) == 1 and (not self.es_method_http(method)):
                                          #Llamamos al metodo
                                          getattr(self, method)()
                                          self.add_log(method, "200 OK")

                                    #Si es un metodo HTTP y el nro de palabras de solicitud es 3
                                    elif self.es_method_http(method) and self.contar_palabras(request) == 3:
                                          version_HTTP = self.obtener_palabra(request, 2)

                                          #Si la version del protocolo enviado es valido
                                          if version_HTTP in self.version_http_supported:
                                                #Llamamos al metodo y pasamos la solicitud
                                                getattr(self, method)(request)
                                                self.add_log(method, "200 OK")
                                          else:
                                                self.send_error_http(request, 400, self.encabezado(400,"text/html"))

                                          #end if
                                    else:
                                          self.send_error(request, 400)

                              elif self.contar_palabras(request) == 1:

                                    self.send_error(request, 400)
                              else: 
                                    self.send_error_http(request, 400, self.encabezado(400,"text/html"))
                              #end if
                        else:
                              self.send_error(request, 400)

                        #end if

                  except Exception:
                        self.close()
                        
            #end while
      
      #end run
