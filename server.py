import sys
import argparse
import logging
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

log = logging.getLogger()


class Server(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log.debug(format, *args)

    def log_error(self, format, *args):
        log.error(format, *args)

    def _health(self):
        log.debug('health check')
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Health: ok\n"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    def _other(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = f"{self.command} request at path: {self.path}"
        log.info(message)

        # Write content as utf-8 data
        self.wfile.write(bytes(message + "\n", "utf8"))

        # Read body (if any)
        if self.command in ['POST', 'PUT']:
            content_len_str = self.headers.get('Content-Length')
            if content_len_str:
                content_len = int(content_len_str)
                if content_len:
                    body = self.rfile.read(content_len)
                    self.rfile.close()
                    log.info("Body:")
                    log.info(body)

        return True

    def do_GET(self):
        if self.path == "/health":
            return self._health()
        return self._other()

    def do_POST(self):
        return self._other()
    
    def do_PUT(self):
        return self._other()

def run(port=8000):
    log.info('Serving at port %s', port)
    server_address = ('', port)
    httpd = ThreadingHTTPServer(server_address, Server)
    httpd.serve_forever()


def parse_command_line(argv):
    """Parse command line arguments.
    :param argv: arguments on the command line, includes caller file name as first argument.
    """
    formatter_class = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--loglevel", dest="loglevel",
                        help="Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_argument("-p", "--port", dest="port",
                        type=int, default=8000,
                        help="Set listening port")

    arguments = parser.parse_args(argv[1:])

    if arguments.loglevel:
        numeric_level = getattr(logging, arguments.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        log.setLevel(numeric_level)
        log.debug('Setting log level to %s', arguments.loglevel.upper())

    return arguments


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    args = parse_command_line(sys.argv)
    run(port=args.port)
