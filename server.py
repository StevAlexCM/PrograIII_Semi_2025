from http.server import SimpleHTTPRequestHandler, HTTPServer
port=3000
class miServidor(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/":
            self.path="index.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        
print("Ejecutando el servidor en el puerto", port)
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()
            