from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse
from urllib.parse import urlparse, parse_qs
import json
import os
from crud_usuario import crud_usuario
import crud_alumno
import crud_docente  

port = 3000


crudAlumno = crud_alumno.crud_alumno()
crudDocente = crud_docente.crud_docente()

class miServidor(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        url_parseada = urlparse(self.path)
        path = url_parseada.path
        parametros = parse_qs(url_parseada.query)
        
        print(f"Solicitud GET: {self.path}")
        
        # Mapeo de rutas a archivos
        rutas = {
            '/': 'login.html',
            '/login': 'login.html',
            '/sistema': 'index.html'
        }
        
        # Si es una ruta conocida, servir el archivo correspondiente
        if path in rutas:
            self.path = rutas[path]
            print(f"Sirviendo archivo: {self.path}")
            return SimpleHTTPRequestHandler.do_GET(self)
        
        # Endpoint para alumnos (del CRUD original)
        if self.path == "/alumnos":
            alumnos = crudAlumno.consultar("")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(alumnos).encode('utf-8'))
            return
        
        # Endpoint para docentes (NUEVO)
        if self.path.startswith("/docentes"):
            url_parseada = urlparse(self.path)
            parametros = parse_qs(url_parseada.query)
            buscar = parametros.get('buscar', [''])[0]
            
            docentes = crudDocente.consultar(buscar)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(docentes).encode('utf-8'))
            return
        
  
        elif path == "/vistas":
            form_name = parametros.get('form', [''])[0]
            if form_name:
                self.path = f'modulos/{form_name}.html'
                print(f"Cargando vista: {self.path}")
                return SimpleHTTPRequestHandler.do_GET(self)
            else:
                self.send_error(404, "Parámetro 'form' no especificado")
                return
        
   
        elif os.path.exists(self.path[1:]) and os.path.isfile(self.path[1:]):
            return SimpleHTTPRequestHandler.do_GET(self)
        
    
        elif os.path.exists(self.path[1:]) and self.path != '/':
            return SimpleHTTPRequestHandler.do_GET(self)
        
        else:
            
            print(f"Archivo no encontrado: {self.path}, sirviendo login.html")
            self.path = 'login.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        
        print(f"Solicitud POST: {self.path}")
        print(f"Datos recibidos: {datos}")
        
        try:
            datos = json.loads(datos)
        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            self.send_error(400, "JSON inválido")
            return
        
      
        if self.path == "/login":
            self.procesar_login(datos)
            
      
        elif self.path == "/usuarios":
            self.procesar_usuarios(datos)
            
   
        elif self.path == "/alumnos":
            resp = {"msg": crudAlumno.administrar(datos)}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            
    
        elif self.path == "/docentes":
            resp = {"msg": crudDocente.administrar(datos)}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            
        else:
            self.send_response(404)
            self.end_headers()

    def procesar_login(self, datos):
        usuario = datos.get('usuario', '')
        clave = datos.get('clave', '')
        
        print(f"Intentando login para usuario: {usuario}")
        
        
        usuario_valido = crud_usuario.login(usuario, clave)
        
        if usuario_valido:
            resp = {
                "msg": "ok", 
                "usuario": {
                    "id": usuario_valido['idUsuario'],
                    "nombre": usuario_valido['nombre'],
                    "usuario": usuario_valido['usuario']
                }
            }
        else:
            resp = {"msg": "error", "error": "Usuario o contraseña incorrectos"}
            
        self.enviar_respuesta(resp)

    def procesar_usuarios(self, datos):
        accion = datos.get('accion', '')
        respuesta = {"msg": "error", "error": "Acción no válida"}
        
        if accion == "nuevo":
            resultado = crud_usuario.crear_usuario(datos)
            respuesta = {"msg": resultado}
            
        elif accion == "modificar":
            resultado = crud_usuario.actualizar_usuario(datos)
            respuesta = {"msg": resultado}
            
        elif accion == "eliminar":
            id_usuario = datos.get('idUsuario')
            if id_usuario:
                resultado = crud_usuario.eliminar_usuario(id_usuario)
                respuesta = {"msg": resultado}
                
        elif accion == "consultar":
            if datos.get('idUsuario'):
                usuario = crud_usuario.obtener_usuario_por_id(datos['idUsuario'])
                respuesta = {"msg": "ok", "usuario": usuario}
            else:
                usuarios = crud_usuario.obtener_todos_usuarios()
                respuesta = {"msg": "ok", "usuarios": usuarios}
        
        self.enviar_respuesta(respuesta)

    def enviar_respuesta(self, datos):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(datos).encode("utf-8"))

    def list_directory(self, path):
        # Prevenir listado de directorios
        self.send_error(404, "No permission to list directory")

print("=" * 50)
print("Servidor académico iniciando...")
print("Puerto:", port)
print("URL: http://localhost:3000")
print("=" * 50)

try:
    server = HTTPServer(("localhost", port), miServidor)
    print("Servidor iniciado correctamente!")
    print("CRUDs activos: Usuarios, Alumnos y Docentes")
    server.serve_forever()
except Exception as e:
    print(f"Error al iniciar el servidor: {e}")