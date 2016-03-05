import pprint

def app(environ, start_response):
     data = pprint.pformat(environ).encode("utf-8")
     start_response("200 OK", [
         ("Content-Type", "text/plain"),
         ("Content-Length", str(len(data)))
     ])

     return iter([data])
