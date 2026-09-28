#!/usr/bin/env python3
"""
Renderiza um template do Elementor como HTML, para conferir o layout sem subir
no WordPress.

Reproduz a estrutura que o Elementor gera de verdade:

    <div class="e-con e-flex e-con-full">        largura total
        ...filhos...
    </div>

    <div class="e-con e-flex e-con-boxed">       boxed
        <div class="e-con-inner">                max-width + margin auto
            ...filhos...
        </div>
    </div>

Os controles de flex (direção, gap, alinhamento) o Elementor aplica no
`.e-con-inner` quando é boxed, e no `.e-con` quando é full — e é isso que esta
saída faz também.

Não é o Elementor: é uma aproximação fiel o bastante para pegar erro de
largura, empilhamento, espaçamento e tipografia antes de importar.

Uso:

    python3 preview.py template.json --out preview.html --largura 1920
"""

import argparse
import html
import json


def v(ctl, padrao=None):
    """Extrai o valor de um controle {unit, size} do Elementor."""
    if not isinstance(ctl, dict):
        return padrao
    size = ctl.get("size")
    if size in (None, ""):
        return padrao
    unit = ctl.get("unit", "px")
    if unit == "custom":
        return str(size)
    return "%s%s" % (size, "" if unit == "" else unit)


def dims(ctl):
    if not isinstance(ctl, dict):
        return None
    u = ctl.get("unit", "px")
    return " ".join("%s%s" % (ctl.get(k, "0") or "0", u)
                    for k in ("top", "right", "bottom", "left"))


def fundo_css(s):
    out = []
    tipo = s.get("background_background")
    if tipo == "gradient":
        a = s.get("background_color", "#000")
        b = s.get("background_color_b", "#000")
        pa = v(s.get("background_color_stop"), "0%")
        pb = v(s.get("background_color_b_stop"), "100%")
        ang = v(s.get("background_gradient_angle"), "180deg")
        out.append("background-image:linear-gradient(%s,%s %s,%s %s)" % (ang, a, pa, b, pb))
    elif tipo == "classic":
        if s.get("background_color"):
            out.append("background-color:%s" % s["background_color"])
        img = s.get("background_image") or {}
        if img.get("url"):
            out.append("background-image:url('%s')" % img["url"])
            out.append("background-size:%s" % s.get("background_size", "cover"))
            out.append("background-position:%s" % s.get("background_position", "center center"))
            out.append("background-repeat:%s" % s.get("background_repeat", "no-repeat"))
    return out


def caixa_css(s):
    out = fundo_css(s)
    if s.get("border_border") and s.get("border_border") != "none":
        larg = dims(s.get("border_width")) or "1px"
        out.append("border-style:%s" % s["border_border"])
        out.append("border-width:%s" % larg)
        out.append("border-color:%s" % s.get("border_color", "#000"))
    r = dims(s.get("border_radius"))
    if r:
        out.append("border-radius:%s" % r)
    if s.get("box_shadow_box_shadow_type") == "yes":
        sh = s.get("box_shadow_box_shadow") or {}
        inset = "inset " if (s.get("box_shadow_box_shadow_position") or "").strip() == "inset" else ""
        out.append("box-shadow:%s%spx %spx %spx %spx %s" % (
            inset, sh.get("horizontal", 0), sh.get("vertical", 0),
            sh.get("blur", 0), sh.get("spread", 0), sh.get("color", "#000")))
    op = v(s.get("_element_opacity"))
    if op:
        out.append("opacity:%s" % op)
    return out


def posicao_css(s):
    out = []
    if s.get("_position") == "absolute":
        out.append("position:absolute")
        x = v(s.get("_offset_x"), "0px")
        y = v(s.get("_offset_y"), "0px")
        out.append("left:%s" % x if s.get("_offset_orientation_h") != "end" else "right:%s" % x)
        out.append("top:%s" % y if s.get("_offset_orientation_v") != "end" else "bottom:%s" % y)
        if s.get("_element_width") == "initial":
            w = v(s.get("_element_custom_width"))
            if w:
                out.append("width:%s" % w)
    return out


def flex_css(s):
    out = ["display:flex"]
    out.append("flex-direction:%s" % s.get("flex_direction", "column"))
    g = s.get("flex_gap") or {}
    if g:
        out.append("gap:%spx %spx" % (g.get("row", 0), g.get("column", 0)))
    if s.get("flex_align_items"):
        out.append("align-items:%s" % s["flex_align_items"])
    if s.get("flex_justify_content"):
        out.append("justify-content:%s" % s["flex_justify_content"])
    if s.get("flex_wrap"):
        out.append("flex-wrap:%s" % s["flex_wrap"])
    return out


def tipografia_css(s):
    out = []
    fam = s.get("typography_font_family")
    if fam:
        out.append("font-family:'%s',system-ui,sans-serif" % fam)
    t = v(s.get("typography_font_size"))
    if t:
        out.append("font-size:%s" % t)
    if s.get("typography_font_weight"):
        out.append("font-weight:%s" % s["typography_font_weight"])
    lh = v(s.get("typography_line_height"))
    if lh:
        out.append("line-height:%s" % lh)
    ls = v(s.get("typography_letter_spacing"))
    if ls:
        out.append("letter-spacing:%s" % ls)
    if s.get("typography_text_transform"):
        out.append("text-transform:%s" % s["typography_text_transform"])
    return out


def render(no, prof=0):
    s = no.get("settings") or {}
    ident = "  " * prof

    if no["elType"] == "container":
        boxed = s.get("content_width") == "boxed"

        externo = ["box-sizing:border-box", "position:relative"]
        externo += caixa_css(s)
        externo += posicao_css(s)
        p = dims(s.get("padding"))
        if p:
            externo.append("padding:%s" % p)
        mh = v(s.get("min_height"))
        if mh:
            externo.append("min-height:%s" % mh)

        if s.get("_flex_size") == "grow":
            externo.append("flex-grow:1")
        w = v(s.get("width"))
        if w and not boxed:
            externo.append("width:%s" % w)
        elif not boxed and s.get("_flex_size") != "grow" and "width" not in s:
            externo.append("width:100%")

        filhos = "\n".join(render(c, prof + 2) for c in no.get("elements", []))

        if boxed:
            largura = v(s.get("boxed_width"), "1140px")
            interno = flex_css(s) + ["box-sizing:border-box",
                                     "width:100%", "max-width:%s" % largura,
                                     "margin-left:auto", "margin-right:auto"]
            externo.append("width:100%")
            return (
                '%s<div class="e-con e-con-boxed" style="%s">\n'
                '%s  <div class="e-con-inner" style="%s">\n%s\n%s  </div>\n%s</div>'
                % (ident, ";".join(externo), ident, ";".join(interno), filhos, ident, ident)
            )

        externo = flex_css(s) + externo
        return '%s<div class="e-con" style="%s">\n%s\n%s</div>' % (
            ident, ";".join(externo), filhos, ident)

    # ---- widgets ----
    wt = no.get("widgetType")
    base = ["box-sizing:border-box"] + posicao_css(s)
    if s.get("_flex_size") == "grow":
        base.append("flex-grow:1")

    if wt == "heading":
        css = base + tipografia_css(s) + ["margin:0"]
        if s.get("title_color"):
            css.append("color:%s" % s["title_color"])
        if s.get("align"):
            css.append("text-align:%s" % s["align"])
        tag = s.get("header_size", "h2")
        return '%s<div class="e-widget" style="%s"><%s style="font:inherit;color:inherit;margin:0">%s</%s></div>' % (
            ident, ";".join(css), tag, html.escape(s.get("title", "")), tag)

    if wt == "text-editor":
        css = base + tipografia_css(s)
        if s.get("text_color"):
            css.append("color:%s" % s["text_color"])
        if s.get("align"):
            css.append("text-align:%s" % s["align"])
        corpo = s.get("editor", "")
        return '%s<div class="e-widget e-texto" style="%s">%s</div>' % (
            ident, ";".join(css), corpo)

    if wt == "image":
        img = s.get("image") or {}
        w = v(s.get("width"))
        css = base + (["width:%s" % w] if w else [])
        if s.get("align") == "center":
            css.append("text-align:center")
        return ('%s<div class="e-widget" style="%s">'
                '<img src="%s" alt="" style="max-width:100%%;height:auto;display:block" '
                'onerror="this.replaceWith(Object.assign(document.createElement(\'div\'),'
                '{className:\'falta\',textContent:this.src.split(\'/\').pop()}))"></div>'
                % (ident, ";".join(css), img.get("url", "")))

    if wt == "button":
        css = base + tipografia_css(s) + caixa_css(s) + [
            "display:inline-flex", "align-items:center", "justify-content:center",
            "padding:14px 28px", "color:%s" % s.get("button_text_color", "#fff"),
            "text-decoration:none"]
        return '%s<div class="e-widget"><span style="%s">%s</span></div>' % (
            ident, ";".join(css), html.escape(s.get("text", "")))

    if wt == "image-carousel":
        slides = s.get("carousel") or []
        por = int(s.get("slides_to_show", 3) or 3)
        esp = v(s.get("image_spacing_custom"), "20px")
        itens = "".join(
            '<div class="slide" style="flex:0 0 calc((100%% - %s * %d) / %d)">'
            '<img src="%s" alt="" style="width:100%%;display:block" '
            'onerror="this.replaceWith(Object.assign(document.createElement(\'div\'),'
            '{className:\'falta\',textContent:this.src.split(\'/\').pop()}))"></div>'
            % (esp, por - 1, por, sl.get("url", "")) for sl in slides)
        return ('%s<div class="e-widget carrossel" style="%s">'
                '<div class="trilho" style="display:flex;gap:%s;overflow:hidden">%s</div>'
                '<div class="rotulo">carrossel · %d slides · %d por tela</div></div>'
                % (ident, ";".join(base + ["width:100%"]), esp, itens, len(slides), por))

    return '%s<div class="e-widget desconhecido">[%s]</div>' % (ident, wt)


PAGINA = """<!doctype html>
<html lang="pt-BR"><meta charset="utf-8">
<title>%s</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; background: #111; color: #fff;
         font-family: system-ui, -apple-system, sans-serif; }
  .e-texto p { margin: 0 0 1em; }
  .e-texto p:last-child { margin-bottom: 0; }
  .falta {
    min-height: 120px; display: flex; align-items: center; justify-content: center;
    padding: 12px; text-align: center; font-size: 11px; color: #7fb1e8;
    background: #17181c; border: 1px dashed rgba(72,139,209,.5); border-radius: 8px;
    word-break: break-all;
  }
  .carrossel .rotulo {
    font-size: 11px; color: #7fb1e8; text-align: center; padding-top: 8px;
    letter-spacing: .08em; text-transform: uppercase;
  }
</style>
%s
</html>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("template")
    p.add_argument("--out", default="preview.html")
    p.add_argument("--largura", type=int, default=1920)
    args = p.parse_args()

    with open(args.template, encoding="utf-8") as fh:
        t = json.load(fh)

    corpo = "\n".join(render(s) for s in t.get("content", []))
    saida = PAGINA % (html.escape(t.get("title", "preview")),
                      '<div style="width:%dpx">\n%s\n</div>' % (args.largura, corpo))

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(saida)
    print("%s -> %s  (%d px de largura)" % (args.template, args.out, args.largura))


if __name__ == "__main__":
    main()
