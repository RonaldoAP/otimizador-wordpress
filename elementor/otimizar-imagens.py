#!/usr/bin/env python3
"""
Recomprime prints/PNGs para a web sem mexer nas dimensões.

Gera duas pastas: webp/ (o que vai para o site) e png/ (reserva em paleta de
256 cores, para o caso de algum plugin antigo não aceitar WebP). Os nomes saem
em minúsculo com hífen, que é o que o WordPress espera na URL.

Uso:
    python3 otimizar-imagens.py entrada/ --saida out --prefixo depoimento
"""

import argparse
import glob
import os
import re

from PIL import Image


def numero(caminho):
    m = re.search(r"(\d+)", os.path.basename(caminho))
    return int(m.group(1)) if m else 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("entrada")
    p.add_argument("--saida", default="out")
    p.add_argument("--prefixo", default="imagem")
    p.add_argument("--qualidade", type=int, default=85)
    args = p.parse_args()

    arquivos = sorted(glob.glob(os.path.join(args.entrada, "*.png"))
                      + glob.glob(os.path.join(args.entrada, "*.jpg")), key=numero)
    if not arquivos:
        raise SystemExit("nenhuma imagem em %s" % args.entrada)

    os.makedirs(os.path.join(args.saida, "webp"), exist_ok=True)
    os.makedirs(os.path.join(args.saida, "png"), exist_ok=True)

    tot_o = tot_w = tot_p = 0
    for f in arquivos:
        base = "%s-%02d" % (args.prefixo, numero(f))
        im = Image.open(f)
        o = os.path.getsize(f)

        cw = os.path.join(args.saida, "webp", base + ".webp")
        im.save(cw, "WEBP", quality=args.qualidade, method=6)
        w = os.path.getsize(cw)

        # Em print de texto a paleta de 256 cores é visualmente idêntica ao
        # original e corta bem mais que o `optimize` sozinho.
        cp = os.path.join(args.saida, "png", base + ".png")
        (im.convert("RGB")
           .quantize(colors=256, method=Image.MAXCOVERAGE, dither=Image.NONE)
           .save(cp, optimize=True))
        p_ = os.path.getsize(cp)

        tot_o, tot_w, tot_p = tot_o + o, tot_w + w, tot_p + p_
        print("%-18s %dx%d  %6.1f KB -> webp %5.1f KB (-%2.0f%%)  png %5.1f KB (-%2.0f%%)"
              % (base, im.size[0], im.size[1], o / 1024,
                 w / 1024, 100 - 100 * w / o, p_ / 1024, 100 - 100 * p_ / o))

    print("\nTOTAL  %.2f MB -> webp %.2f MB (-%.0f%%) | png %.2f MB (-%.0f%%)"
          % (tot_o / 1048576, tot_w / 1048576, 100 - 100 * tot_w / tot_o,
             tot_p / 1048576, 100 - 100 * tot_p / tot_o))


if __name__ == "__main__":
    main()
