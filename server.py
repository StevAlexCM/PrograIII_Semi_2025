from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib import parse
port=3000
class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            self.path="index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
        
        
    def do_post(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        
        self.send_response(200)
        self.send_header()
        self.wfile.write
        print(datos)
        
        
print("Ejecutando el servidor en el puerto", port)
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()
    