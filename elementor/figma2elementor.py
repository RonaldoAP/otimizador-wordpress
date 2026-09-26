#!/usr/bin/env python3
"""
Converte um dump da arvore do Figma em template importavel do Elementor.

O dump vem do MCP do Figma (script de leitura em `dump-figma.js`), no formato:

    {"id","nome","tipo","w","h","flex":{...},"fundo":[...],"borda":{...},
     "raio","efeitos":[...],"texto":{...},"filhos":[...]}

A traducao e direta porque container do Elementor e flexbox e auto layout do
Figma tambem e:

    Figma                     Elementor
    ------------------------- -----------------------------
    layoutMode VERTICAL       flex_direction: column
    layoutMode HORIZONTAL     flex_direction: row
    itemSpacing               flex_gap
    padding*                  padding
    counterAxisAlignItems     flex_align_items
    primaryAxisAlignItems     flex_justify_content
    layoutSizing FIXED        width: <px>
    layoutSizing HUG          width: fit-content
    layoutSizing FILL         flex_grow: 1

O papel de cada no vem do prefixo do nome da camada (ver README):
`sec/`, `box/`, `row/`, `col/` viram container; `w/<widget>` vira widget nativo.

Uso:

    python3 figma2elementor.py dump.json --out secao.json \\
        --base-url https://adrielaraujo.com.br/wp-content/uploads/black360
"""

import argparse
import json
import random
import re
import string
import unicodedata
import sys

# ---------------------------------------------------------------------------
# Mapas de traducao
# ---------------------------------------------------------------------------

DIRECAO = {"VERTICAL": "column", "HORIZONTAL": "row"}

# counterAxisAlignItems -> align-items
ALINHA = {"MIN": "flex-start", "CENTER": "center", "MAX": "flex-end",
          "BASELINE": "baseline", "STRETCH": "stretch"}

# primaryAxisAlignItems -> justify-content
JUSTIFICA = {"MIN": "flex-start", "CENTER": "center", "MAX": "flex-end",
             "SPACE_BETWEEN": "space-between"}

# prefixo da camada -> widget nativo
WIDGETS = {
    "heading": "heading",
    "text": "text-editor",
    "image": "image",
    "button": "button",
    "icon": "icon",
    "carousel": "image-carousel",
    "video": "video",
    "divider": "divider",
    "spacer": "spacer",
}

# nomes que, em texto, indicam titulo em vez de paragrafo
TITULOS = re.compile(r"^(h[1-6]|w/heading|titulo|título)\b", re.I)

TAG_POR_TAMANHO = [(48, "h1"), (36, "h2"), (28, "h3"), (22, "h4"), (0, "h5")]


def uid():
    return "".join(random.choice(string.hexdigits.lower()[:16]) for _ in range(7))


def tem_texto(n):
    """True se o no ou qualquer descendente carrega texto."""
    if n.get("texto"):
        return True
    return any(tem_texto(f) for f in (n.get("filhos") or []))


def papel(nome):
    """Retorna (tipo, detalhe) a partir do nome da camada."""
    limpo = (nome or "").strip()
    m = re.match(r"^(sec|box|row|col|w|bg|img|cls|hide)/\s*([^\s·]*)", limpo, re.I)
    if not m:
        return (None, limpo)
    return (m.group(1).lower(), m.group(2).lower())


# ---------------------------------------------------------------------------
# Helpers de valor
# ---------------------------------------------------------------------------

def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dim(pad):
    v = lambda k: int(round(pad.get(k) or 0))
    return {"unit": "px", "top": str(v("top")), "right": str(v("right")),
            "bottom": str(v("bottom")), "left": str(v("left")), "isLinked": False}


def gap(valor):
    v = int(round(valor or 0))
    return {"column": str(v), "row": str(v), "isLinked": True, "unit": "px", "size": v}


def cor(paint):
    """Um paint do dump -> string de cor CSS."""
    if not paint:
        return None
    if paint["t"] == "solid":
        op = paint.get("op", 1)
        if op >= 0.999:
            return paint["cor"]
        r = int(paint["cor"][1:3], 16)
        g = int(paint["cor"][3:5], 16)
        b = int(paint["cor"][5:7], 16)
        return "rgba(%d,%d,%d,%s)" % (r, g, b, round(op, 2))
    return None


def linha_de_gradiente(paint):
    """Paint de gradiente -> dict de background do Elementor (2 paradas)."""
    stops = paint.get("stops") or []
    if len(stops) < 2:
        return {}
    a, b = stops[0], stops[-1]
    return {
        "background_background": "gradient",
        "background_color": a["cor"],
        "background_color_stop": px(int(a["pos"] * 100), "%"),
        "background_color_b": b["cor"],
        "background_color_b_stop": px(int(b["pos"] * 100), "%"),
        "background_gradient_type": "linear",
        "background_gradient_angle": px(180, "deg"),
    }


def tipografia(t, fonte_titulo, fonte_texto):
    """Bloco `texto` do dump -> controles de tipografia do Elementor."""
    fam, _, estilo = (t.get("fonte") or "").partition("|")
    if fam in ("", "MISTA"):
        # texto com mais de uma fonte no Figma: cai na fonte de corpo do projeto
        fam, estilo = fonte_texto, ""
    tam = t.get("tam")
    if tam == "mista" or tam is None:
        tam = 16

    peso = "400"
    e = (estilo or "").lower().replace(" ", "")
    for chave, valor in (("thin", "100"), ("extralight", "200"), ("light", "300"),
                         ("book", "400"), ("regular", "400"), ("medium", "500"),
                         ("semibold", "600"), ("extrabold", "800"), ("black", "900"),
                         ("bold", "700")):
        if chave in e:
            peso = valor
            break

    out = {
        "typography_typography": "custom",
        "typography_font_family": fam or fonte_texto,
        "typography_font_size": px(int(round(tam))),
        "typography_font_weight": peso,
    }

    lh = t.get("lh") or {}
    if lh.get("unit") == "PERCENT":
        out["typography_line_height"] = px(round(lh["value"] / 100.0, 2), "em")
    elif lh.get("unit") == "PIXELS":
        out["typography_line_height"] = px(round(lh["value"], 1))

    ls = t.get("ls") or {}
    if ls.get("unit") == "PERCENT" and abs(ls.get("value", 0)) > 0.01:
        out["typography_letter_spacing"] = px(round(tam * ls["value"] / 100.0, 2))
    elif ls.get("unit") == "PIXELS" and abs(ls.get("value", 0)) > 0.01:
        out["typography_letter_spacing"] = px(round(ls["value"], 2))

    if t.get("caixa") == "UPPER":
        out["typography_text_transform"] = "uppercase"

    return out


def efeitos_para_sombra(efeitos):
    """Primeiro DROP_SHADOW/INNER_SHADOW -> controle box_shadow do Elementor."""
    for e in efeitos or []:
        if e["t"] not in ("DROP_SHADOW", "INNER_SHADOW"):
            continue
        c = e.get("cor") or "#000000"
        a = e.get("a")
        a = 1 if a is None else a
        r = int(c[1:3], 16)
        g = int(c[3:5], 16)
        b = int(c[5:7], 16)
        off = e.get("off") or {"x": 0, "y": 0}
        return {
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": int(round(off.get("x", 0))),
                "vertical": int(round(off.get("y", 0))),
                "blur": int(round(e.get("r") or 0)),
                "spread": int(round(e.get("sp") or 0)),
                "color": "rgba(%d,%d,%d,%s)" % (r, g, b, round(a, 2)),
            },
            "box_shadow_box_shadow_position": "inset" if e["t"] == "INNER_SHADOW" else " ",
        }
    return {}


# ---------------------------------------------------------------------------
# Conversao
# ---------------------------------------------------------------------------

class Conversor:
    def __init__(self, base_url, fonte_titulo, fonte_texto, largura_conteudo):
        self.base_url = base_url.rstrip("/")
        self.fonte_titulo = fonte_titulo
        self.fonte_texto = fonte_texto
        self.largura_conteudo = largura_conteudo
        self.avisos = []
        self.arquivos = set()
        self.contagem = {"container": 0, "widget": 0}

    # -- estilo comum a containers ----------------------------------------
    def estilo_caixa(self, n):
        s = {}
        fundos = n.get("fundo") or []
        solidos = [f for f in fundos if f["t"] == "solid"]
        grads = [f for f in fundos if f["t"] == "grad"]
        if grads:
            s.update(linha_de_gradiente(grads[0]))
        elif solidos:
            s["background_background"] = "classic"
            s["background_color"] = cor(solidos[0])

        if n.get("raio"):
            r = int(round(n["raio"]))
            s["border_radius"] = {"unit": "px", "top": str(r), "right": str(r),
                                  "bottom": str(r), "left": str(r), "isLinked": True}

        b = n.get("borda")
        if b:
            peso = b.get("peso")
            peso = 1 if peso in (None, "mixed") else int(round(peso))
            s["border_border"] = "solid"
            s["border_width"] = {"unit": "px", "top": str(peso), "right": str(peso),
                                 "bottom": str(peso), "left": str(peso), "isLinked": True}
            paints = b.get("paints") or []
            if paints and paints[0]["t"] == "solid":
                s["border_color"] = cor(paints[0])
            elif paints:
                # Elementor nao aceita gradiente em borda: cai na cor inicial
                stops = paints[0].get("stops") or []
                if stops:
                    s["border_color"] = stops[0]["cor"]
                self.avisos.append(
                    "Borda em gradiente em '%s' virou cor solida — refazer com CSS." % n["nome"])

        s.update(efeitos_para_sombra(n.get("efeitos")))

        if any(e["t"] in ("LAYER_BLUR", "BACKGROUND_BLUR") for e in (n.get("efeitos") or [])):
            self.avisos.append("Blur de camada em '%s' precisa de CSS." % n["nome"])

        return s

    # -- flex --------------------------------------------------------------
    def estilo_flex(self, n, raiz=False):
        f = n.get("flex")
        s = {}
        if not f:
            return s
        s["flex_direction"] = DIRECAO.get(f["dir"], "column")
        s["flex_gap"] = gap(f.get("gap"))
        s["padding"] = dim(f.get("pad") or {})
        s["flex_align_items"] = ALINHA.get(f.get("alinha"), "flex-start")
        s["flex_justify_content"] = JUSTIFICA.get(f.get("justifica"), "flex-start")
        if f.get("wrap") == "WRAP":
            s["flex_wrap"] = "wrap"

        s["container_type"] = "flex"

        # Largura: `content_width`/`boxed_width` so existem no container de topo.
        # Em container aninhado o controle e `width`, e um filho que estica usa
        # `_flex_size: grow` — largura 100% dentro de uma linha quebra o flex.
        larg = f.get("larg")
        if raiz:
            s["content_width"] = "full"
        elif larg == "FILL":
            s["_flex_size"] = "grow"
        elif larg == "HUG":
            s["width"] = {"unit": "custom", "size": "fit-content", "sizes": []}
        elif larg == "FIXED" and n.get("w"):
            s["width"] = px(int(n["w"]))

        # Altura fixa do Figma NAO vira min-height quando ha texto dentro: o
        # navegador quebra linha diferente e a altura travada gera buraco ou
        # transbordo. So caixas sem texto (imagem, espacador) levam altura.
        if f.get("alt") == "FIXED" and n.get("h") and not tem_texto(n):
            s["min_height"] = px(int(n["h"]))
        return s

    # -- widgets -----------------------------------------------------------
    def widget_texto(self, n, forcar=None):
        t = n["texto"]
        conteudo = t["conteudo"]
        tam = t.get("tam")
        tam = 16 if tam in (None, "mista") else tam

        ehtitulo = forcar == "heading" or (forcar is None and TITULOS.match(n["nome"] or ""))
        if forcar is None and not ehtitulo:
            ehtitulo = len(conteudo) < 90 and tam >= 24

        tipografia_ = tipografia(t, self.fonte_titulo, self.fonte_texto)
        alinha = (t.get("alinha") or "LEFT").lower()
        cor_texto = cor((n.get("fundo") or [{}])[0]) or "#FFFFFF"

        if t.get("fonte") == "MISTA":
            self.avisos.append(
                "Texto '%s' tem mais de uma fonte no Figma — o template usa uma so." % conteudo[:40])

        if ehtitulo:
            tag = next(t_ for lim, t_ in TAG_POR_TAMANHO if tam >= lim)
            s = {"title": conteudo, "header_size": tag, "align": alinha, "title_color": cor_texto}
            s.update(tipografia_)
            return {"id": uid(), "elType": "widget", "widgetType": "heading",
                    "settings": s, "elements": []}

        s = {"editor": "<p>%s</p>" % conteudo.replace("\n", "<br>"),
             "align": alinha, "text_color": cor_texto}
        s.update(tipografia_)
        return {"id": uid(), "elType": "widget", "widgetType": "text-editor",
                "settings": s, "elements": []}

    def widget_imagem(self, n):
        bruto = re.sub(r"^(w/image|img/)\s*", "", n["nome"] or "", flags=re.I).strip()
        if not bruto:
            # o nome util costuma estar no no de dentro que carrega o preenchimento
            for f in n.get("filhos") or []:
                if any(p["t"] == "img" for p in (f.get("fundo") or [])):
                    bruto = f["nome"]
                    break
        nome = unicodedata.normalize("NFKD", bruto).encode("ascii", "ignore").decode()
        nome = re.sub(r"[^\w.\-]+", "-", nome).strip("-.").lower() or "imagem"
        if nome.rpartition(".")[2] not in ("webp", "png", "jpg", "jpeg", "svg", "gif", "avif"):
            nome = nome.replace(".", "-") + ".webp"
        base, _, ext = nome.rpartition(".")
        n_ = 2
        while nome in self.arquivos:
            nome = "%s-%d.%s" % (base, n_, ext)
            n_ += 1
        self.arquivos.add(nome)
        s = {
            "image": {"url": "%s/%s" % (self.base_url, nome), "id": "", "alt": "", "source": "library"},
            "image_size": "full",
            "align": "center",
        }
        if n.get("w"):
            s["width"] = px(int(n["w"]))
        return {"id": uid(), "elType": "widget", "widgetType": "image",
                "settings": s, "elements": []}

    def widget_botao(self, n):
        rotulo = ""
        for f in n.get("filhos") or []:
            if f.get("texto"):
                rotulo = f["texto"]["conteudo"]
                break
        s = {"text": rotulo or "CLIQUE AQUI", "align": "center", "size": "md",
             "link": {"url": "#", "is_external": "", "nofollow": ""}}
        s.update({k: v for k, v in self.estilo_caixa(n).items()
                  if k.startswith(("border", "background"))})
        return {"id": uid(), "elType": "widget", "widgetType": "button",
                "settings": s, "elements": []}

    # -- no ----------------------------------------------------------------
    def converte(self, n, raiz=False):
        tipo, detalhe = papel(n.get("nome"))

        # widget explicito
        if tipo == "w":
            wt = WIDGETS.get(detalhe)
            if wt == "image":
                self.contagem["widget"] += 1
                return self.widget_imagem(n)
            if wt == "button":
                self.contagem["widget"] += 1
                return self.widget_botao(n)
            if wt in ("heading", "text-editor") and n.get("texto"):
                self.contagem["widget"] += 1
                return self.widget_texto(n, "heading" if wt == "heading" else "text")
            if wt and not n.get("filhos"):
                self.contagem["widget"] += 1
                self.avisos.append("Widget '%s' em '%s' entrou vazio — preencher no painel."
                                   % (wt, n["nome"]))
                return {"id": uid(), "elType": "widget", "widgetType": wt,
                        "settings": {}, "elements": []}

        # decorativo: vira fundo do pai, nao entra como no
        if tipo == "bg":
            self.avisos.append("'%s' e decorativo: aplicar como fundo do container pai."
                               % n["nome"])
            return None

        # texto solto
        if n.get("texto"):
            self.contagem["widget"] += 1
            return self.widget_texto(n)

        # imagem solta (retangulo com preenchimento de imagem)
        if any(f["t"] == "img" for f in (n.get("fundo") or [])) and not n.get("filhos"):
            self.contagem["widget"] += 1
            return self.widget_imagem(n)

        # container
        filhos = []
        for f in n.get("filhos") or []:
            c = self.converte(f)
            if c:
                filhos.append(c)

        if not filhos:
            return None

        if not n.get("flex"):
            self.avisos.append(
                "'%s' nao tem auto layout no Figma — virou coluna simples, posicao perdida."
                % n["nome"])

        s = {}
        s.update(self.estilo_flex(n, raiz=raiz))
        s.update(self.estilo_caixa(n))
        if not n.get("flex"):
            s.setdefault("flex_direction", "column")

        self.contagem["container"] += 1
        return {"id": uid(), "elType": "container", "settings": s,
                "elements": filhos, "isInner": not raiz}


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("dump", help="JSON exportado do Figma")
    p.add_argument("--out", default="secao.json")
    p.add_argument("--base-url",
                   default="https://adrielaraujo.com.br/wp-content/uploads/black360")
    p.add_argument("--fonte-titulo", default="Cutta")
    p.add_argument("--fonte-texto", default="Gotham")
    p.add_argument("--largura-conteudo", type=int, default=1140)
    p.add_argument("--titulo", default="LP VENDAS · Black 360")
    p.add_argument("--seed", type=int, default=360)
    args = p.parse_args()

    random.seed(args.seed)

    with open(args.dump, encoding="utf-8") as fh:
        arvore = json.load(fh)

    conv = Conversor(args.base_url, args.fonte_titulo, args.fonte_texto,
                     args.largura_conteudo)

    # uma lista no dump = pagina inteira, uma secao por item, na ordem vertical
    if isinstance(arvore, list):
        secoes = sorted(arvore, key=lambda s: s.get("y", 0))
        conteudo = [c for c in (conv.converte(s, raiz=True) for s in secoes) if c]
        if not conteudo:
            sys.exit("Nada para converter.")
        template = {
            "content": conteudo,
            "page_settings": [],
            "version": "0.4",
            "title": args.titulo,
            "type": "page",
        }
    else:
        raiz = conv.converte(arvore, raiz=True)
        if not raiz:
            sys.exit("Nada para converter.")
        template = {
            "content": [raiz],
            "page_settings": [],
            "version": "0.4",
            "title": arvore.get("nome", "Secao"),
            "type": "section",
        }

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(template, fh, ensure_ascii=False, indent=2)

    print("%s -> %s" % (args.dump, args.out))
    print("  containers: %d   widgets: %d" % (conv.contagem["container"],
                                              conv.contagem["widget"]))
    if conv.avisos:
        print("  avisos:")
        for a in dict.fromkeys(conv.avisos):
            print("    - " + a)


if __name__ == "__main__":
    main()
