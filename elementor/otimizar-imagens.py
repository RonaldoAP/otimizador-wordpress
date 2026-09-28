#!/usr/bin/env python3
"""
Prepara imagens para a web: redimensiona, recomprime e renomeia.

Gera duas pastas: webp/ (o que vai para o site) e jpg/ (reserva, para o caso
de algum plugin antigo não aceitar WebP). Os nomes saem em minúsculo com
hífen, que é o que o WordPress espera na URL, e os metadados (EXIF, GPS) são
descartados.

Uso:

    python3 otimizar-imagens.py entrada/ --saida out --max 1600
    python3 otimizar-imagens.py entrada/ --prefixo depoimento   # numera
"""

import argparse
import glob
import os
import re
import unicodedata

from PIL import Image, ImageOps

EXTENSOES = ("*.png", "*.jpg", "*.jpeg", "*.JPG", "*.JPEG", "*.PNG", "*.webp")


def numero(caminho):
    m = re.search(r"(\d+)", os.path.basename(caminho))
    return int(m.group(1)) if m else 0


def apelido(caminho):
    """Nome de arquivo seguro para URL, a partir do nome original."""
    base = os.path.splitext(os.path.basename(caminho))[0]
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "imagem"


def tem_texto(im):
    """
    Print de tela ou foto?

    Print tem muito pixel de contraste alto contra fundo liso; foto tem o
    tom variando devagar. Como texto sofre muito mais com compressão, o que
    cair aqui recebe qualidade maior.
    """
    p = im.convert("L").resize((160, 160))
    viz = p.tobytes()
    bordas = 0
    for y in range(160):
        for x in range(1, 160):
            if abs(viz[y * 160 + x] - viz[y * 160 + x - 1]) > 60:
                bordas += 1
    return bordas / (160 * 159) > 0.035


def main():
    p = argparse.ArgumentParser()
    p.add_argument("entrada")
    p.add_argument("--saida", default="out")
    p.add_argument("--prefixo", help="numera os arquivos com este prefixo, em vez de usar o nome original")
    p.add_argument("--max", type=int, default=0, help="maior lado em px (0 = não redimensiona)")
    p.add_argument("--qualidade", type=int, default=82)
    p.add_argument("--qualidade-texto", type=int, default=90,
                   help="qualidade para prints de tela, onde o texto precisa continuar nítido")
    args = p.parse_args()

    arquivos = []
    for e in EXTENSOES:
        arquivos += glob.glob(os.path.join(args.entrada, e))
    arquivos = sorted(set(arquivos), key=numero if args.prefixo else str.lower)
    if not arquivos:
        raise SystemExit("nenhuma imagem em %s" % args.entrada)

    os.makedirs(os.path.join(args.saida, "webp"), exist_ok=True)
    os.makedirs(os.path.join(args.saida, "jpg"), exist_ok=True)

    tot_o = tot_w = tot_j = 0
    for f in arquivos:
        base = ("%s-%02d" % (args.prefixo, numero(f))) if args.prefixo else apelido(f)
        o = os.path.getsize(f)

        im = ImageOps.exif_transpose(Image.open(f))   # respeita a rotação da câmera
        antes = im.size
        if args.max and max(im.size) > args.max:
            im.thumbnail((args.max, args.max), Image.LANCZOS)

        q = args.qualidade_texto if tem_texto(im) else args.qualidade
        rgb = im.convert("RGB") if im.mode not in ("RGB", "RGBA") else im

        cw = os.path.join(args.saida, "webp", base + ".webp")
        rgb.save(cw, "WEBP", quality=q, method=6)
        w = os.path.getsize(cw)

        cj = os.path.join(args.saida, "jpg", base + ".jpg")
        rgb.convert("RGB").save(cj, "JPEG", quality=max(q - 4, 70), optimize=True, progressive=True)
        j = os.path.getsize(cj)

        tot_o, tot_w, tot_j = tot_o + o, tot_w + w, tot_j + j
        print("%-26s %sx%s -> %sx%s  q%d  %7.1f KB -> webp %6.1f KB (-%2.0f%%)  jpg %6.1f KB"
              % (base, antes[0], antes[1], im.size[0], im.size[1], q,
                 o / 1024, w / 1024, 100 - 100 * w / o, j / 1024))

    print("\nTOTAL  %.2f MB -> webp %.2f MB (-%.0f%%) | jpg %.2f MB (-%.0f%%)"
          % (tot_o / 1048576, tot_w / 1048576, 100 - 100 * tot_w / tot_o,
             tot_j / 1048576, 100 - 100 * tot_j / tot_o))


if __name__ == "__main__":
    main()
