#!/usr/bin/env python3
"""
Gera uma versão do bloco com as capas embutidas em data URI.

Assim não existe passo de upload: o arquivo que você cola no Elementor já
carrega consigo as imagens. Rode de novo depois de trocar qualquer capa
dentro de capas/.

    python3 embutir.py
"""

import base64
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(AQUI, "faixas-black360.html")
SAIDA = os.path.join(AQUI, "faixas-black360-embutido.html")
CAPAS = os.path.join(AQUI, "capas")

TIPOS = {".webp": "image/webp", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
         ".png": "image/png", ".avif": "image/avif"}


def data_uri(nome):
    caminho = os.path.join(CAPAS, nome)
    if not os.path.exists(caminho):
        return None
    tipo = TIPOS.get(os.path.splitext(nome)[1].lower())
    if not tipo:
        return None
    with open(caminho, "rb") as fh:
        return "data:%s;base64,%s" % (tipo, base64.b64encode(fh.read()).decode("ascii"))


def main():
    with open(ENTRADA, encoding="utf-8") as fh:
        html = fh.read()

    faltando, total = [], 0

    def troca(m):
        nonlocal total
        nome = m.group(1)
        uri = data_uri(nome)
        if not uri:
            faltando.append(nome)
            return m.group(0)
        total += 1
        return 'img: "%s"' % uri

    html = re.sub(r'img:\s*"(capa-[^"]+)"', troca, html)

    # a busca por pasta deixa de fazer sentido: as capas já estão aqui dentro
    html = html.replace(
        'var BASE = "";',
        'var BASE = "";   // não é usado nesta versão: as capas estão embutidas\n'
        '                 // abaixo, em data URI. Nada para subir no servidor.')

    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write(html)

    print("%s  (%d capas embutidas, %.0f KB)"
          % (os.path.basename(SAIDA), total, os.path.getsize(SAIDA) / 1024))
    if faltando:
        print("não encontradas em capas/: " + ", ".join(faltando), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
