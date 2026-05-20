#!/usr/bin/env python3
"""
serve.py — Servidor HTTP local com CORS headers para testar web export do Godot.

SharedArrayBuffer requer Cross-Origin-Opener-Policy e Cross-Origin-Embedder-Policy.
http.server padrão do Python não envia esses headers — este script adiciona.

Uso:
    cd export/web
    python3 /Users/renatojaf/jogo-natalia/serve.py
    # Acessar: http://localhost:8000

    # Porta customizada:
    python3 serve.py 9000
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler, test
import sys


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    test(CORSRequestHandler, HTTPServer, port=port)
