"""Local-only server. Run directly or use start-local.cmd."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import webbrowser

ROOT = Path(__file__).resolve().parent

class LocalHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

def main():
    parser = argparse.ArgumentParser(description='Run Vietnam Atlas locally')
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    page = ROOT / 'dist' / 'index.html'
    if not page.is_file():
        raise SystemExit('Missing dist/index.html. Run python build.py first.')
    handler = partial(LocalHandler, directory=str(page.parent))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError:
        raise SystemExit(f'Port {args.port} is busy. Try: python serve.py --port {args.port + 1}')
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'Vietnam Atlas is running locally: {url}', flush=True)
    print('Keep this window open. Press Ctrl+C to stop.', flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
