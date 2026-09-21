"""Loopback-only preview; --without-script exercises the static fallback."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=4173)
parser.add_argument('--without-script', action='store_true')
args = parser.parse_args()


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if args.without_script and self.path.split('?')[0] == '/assets/preferences.js':
            self.send_response(200)
            self.send_header('Content-Type', 'text/javascript')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return
        super().do_GET()


directory = Path(__file__).resolve().parents[1] / 'dist'
server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(directory)))
print(f'Preview: http://127.0.0.1:{args.port}/', flush=True)
server.serve_forever()
