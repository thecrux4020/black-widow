from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer


class RootedHTTPServer(HTTPServer):
    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path


class Http_server:
	def __init__(self, port, directory):
		self.port = port
		self.dir = directory

	def start(self, ServerClass=RootedHTTPServer):
	    server_address = ('', self.port)

	    httpd = ServerClass(self.dir, server_address, SimpleHTTPRequestHandler)
	    sa = httpd.socket.getsockname()
	    print "Serving HTTP on", sa[0], "port", sa[1], "..."
	    httpd.serve_forever()