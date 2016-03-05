import time

def app(environ, start_response):
     data = b"hello"
     start_response("200 OK", [
         ("Content-Type", "text/plain"),
         ("Content-Length", str(len(data)))
     ])
     # time.sleep(0.5)
     return iter([data])
