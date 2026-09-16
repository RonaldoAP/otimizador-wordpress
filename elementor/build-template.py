#!/usr/bin/env python3
"""
Gera o template do Elementor da landing "Apresentacao" (Escola Black 360)
a partir do Figma node 203:4138.

A pagina e montada 100% com Containers flexbox e widgets nativos do Elementor
(heading, text-editor, image, button, image-carousel). Nao ha shortcode nem
widget de HTML.

Uso:

    python3 build-template.py --base-url https://seusite.com.br/wp-content/uploads/black360 \
        --out black360-apresentacao.json
"""

import argparse
import json
import random
import string

# ---------------------------------------------------------------------------
# Tokens do Figma
# ---------------------------------------------------------------------------

BG = "#111111"
BG_HERO = "#0D0B11"
BG_CARD = "#080808"
BG_FOOTER = "#0A0A0A"
NAVY = "#162B44"
OFF_WHITE = "#F2EDEB"
BLUE = "#488BD1"
BLUE_LIGHT = "#B0D0F0"
BORDER = "rgba(255,255,255,0.6)"
WHITE = "#FFFFFF"

FONT_TITLE = "Cutta"
FONT_TEXT = "Gotham"

CTA_LABEL = "QUERO ENTRAR NO GRUPO"
CTA_NOTE = "28 DE OUTUBRO - 20H - AO VIVO"


def uid():
    return "".join(random.choice(string.hexdigits.lower()[:16]) for _ in range(7))


# ---------------------------------------------------------------------------
# Helpers de estrutura
# ---------------------------------------------------------------------------


def container(settings=None, children=None, inner=True):
    return {
        "id": uid(),
        "elType": "container",
        "settings": settings or {},
        "elements": children or [],
        "isInner": inner,
    }


def widget(widget_type, settings):
    return {
        "id": uid(),
        "elType": "widget",
        "settings": settings,
        "elements": [],
        "widgetType": widget_type,
    }


def px(size, unit="px"):
    return {"unit": unit, "size": size, "sizes": []}


def dim(top, right, bottom, left, unit="px"):
    return {
        "unit": unit,
        "top": str(top),
        "right": str(right),
        "bottom": str(bottom),
        "left": str(left),
        "isLinked": False,
    }


def gap(column, row=None):
    row = column if row is None else row
    return {
        "column": str(column),
        "row": str(row),
        "isLinked": column == row,
        "unit": "px",
        "size": column,
    }


def typography(family, size, weight="400", line_height=1.3, letter_spacing=None, unit_lh="em"):
    out = {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": px(size),
        "typography_font_weight": weight,
        "typography_line_height": px(line_height, unit_lh),
    }
    if letter_spacing is not None:
        out["typography_letter_spacing"] = px(letter_spacing)
    return out


def gradient(color_a, color_b, angle, stop_a=15, stop_b=86):
    """Fundo em degrade, no formato do controle de background do Elementor."""
    return {
        "background_background": "gradient",
        "background_color": color_a,
        "background_color_stop": px(stop_a, "%"),
        "background_color_b": color_b,
        "background_color_b_stop": px(stop_b, "%"),
        "background_gradient_type": "linear",
        "background_gradient_angle": px(angle, "deg"),
    }


def border(width=1, color=BORDER):
    return {
        "border_border": "solid",
        "border_width": dim(width, width, width, width),
        "border_color": color,
    }


# ---------------------------------------------------------------------------
# Blocos reutilizaveis
# ---------------------------------------------------------------------------


def section(children, background=None, padding=(72, 0, 72, 0), boxed=1140, extra=None):
    """Container externo full-width (fundo sangrando) + container interno boxed."""
    outer = {
        "content_width": "full",
        "padding": dim(*padding),
        "flex_direction": "column",
        "flex_align_items": "center",
    }
    if background:
        outer.update(background)
    else:
        outer.update({"background_background": "classic", "background_color": BG})
    if extra:
        outer.update(extra)

    inner = container(
        {
            "content_width": "boxed",
            "boxed_width": px(boxed),
            "flex_direction": "column",
            "padding": dim(0, 20, 0, 20),
        },
        children,
    )

    return container(outer, [inner], inner=False)


def heading(text, size, color=WHITE, align="center", tag="h2", family=FONT_TITLE,
            weight="700", line_height=1.1, letter_spacing=None):
    settings = {
        "title": text,
        "header_size": tag,
        "align": align,
        "title_color": color,
    }
    settings.update(typography(family, size, weight, line_height, letter_spacing))
    return widget("heading", settings)


def rich_text(html, size=16, color=OFF_WHITE, align="left", family=FONT_TEXT,
              weight="400", line_height=1.3):
    """Widget Editor de Texto: o conteudo continua editavel no painel."""
    settings = {
        "editor": html,
        "text_color": color,
        "align": align,
    }
    settings.update(typography(family, size, weight, line_height))
    return widget("text-editor", settings)


def image(url, width=None, alt="", align="center", blur=None):
    settings = {
        "image": {"url": url, "id": "", "alt": alt, "source": "library"},
        "image_size": "full",
        "align": align,
    }
    if width:
        settings["width"] = px(width)
    if blur:
        settings["css_filters_css_filter"] = "custom"
        settings["css_filters_blur"] = px(blur)
    return widget("image", settings)


def cta_button(url, label=CTA_LABEL):
    """Botao nativo dentro de um container com o degrade do layout."""
    btn = widget(
        "button",
        {
            "text": label,
            "link": {"url": url, "is_external": "", "nofollow": ""},
            "align": "center",
            "size": "md",
            "button_text_color": WHITE,
            "background_color": "rgba(0,0,0,0)",
            "border_border": "solid",
            "border_width": dim(1, 1, 1, 1),
            "border_color": BORDER,
            "text_padding": dim(8, 16, 8, 16),
            "button_box_shadow_box_shadow_type": "yes",
            "button_box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 3,
                "blur": 17,
                "spread": 0,
                "color": "rgba(98,153,209,0.9)",
            },
            "button_box_shadow_box_shadow_position": "inset",
            **typography(FONT_TITLE, 18, "500", 1.2),
        },
    )

    wrapper = {
        "content_width": "full",
        "width": px(351),
        "min_height": px(62),
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_justify_content": "center",
        "padding": dim(0, 0, 0, 0),
    }
    wrapper.update(gradient(BLUE, BG, 187))

    return container(wrapper, [btn])


def cta_block(url):
    return container(
        {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "center",
            "flex_gap": gap(15),
            "padding": dim(0, 0, 0, 0),
        },
        [
            cta_button(url),
            heading(CTA_NOTE, 12.7, WHITE, "center", "div", FONT_TITLE, "700", 1.3),
        ],
    )


# ---------------------------------------------------------------------------
# Secoes
# ---------------------------------------------------------------------------


def build_hero(img, url):
    brand = container(
        {
            "content_width": "full",
            "width": px(50, "%"),
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_gap": gap(12),
            "padding": dim(0, 0, 0, 0),
        },
        [
            image(img("logo-avatar.png"), 58, "Escola Black 360", "left"),
            rich_text(
                '<p style="margin:0;letter-spacing:-0.05em;">ESCOLA</p>'
                '<p style="margin:0;font-size:22px;letter-spacing:-0.06em;">'
                '<span style="font-weight:200;">BLACK</span> '
                '<span style="font-weight:400;">360</span></p>',
                16.3,
                OFF_WHITE,
                "left",
                FONT_TITLE,
                "700",
                1.1,
            ),
        ],
    )

    topbar_settings = {
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_justify_content": "space-between",
        "min_height": px(86),
        "padding": dim(12, 12, 12, 20),
        "background_background": "classic",
        "background_color": "rgba(0,0,0,0.2)",
    }
    topbar_settings.update(border(1, "rgba(228,232,243,0.4)"))
    topbar = container(topbar_settings, [brand, cta_button(url)])

    content = container(
        {
            "content_width": "full",
            "width": px(690),
            "flex_direction": "column",
            "flex_align_items": "flex-start",
            "flex_gap": gap(32),
            "padding": dim(200, 0, 120, 0),
        },
        [
            heading(
                "Apresentações, IA, comunicação, networking e posicionamento.",
                50, WHITE, "left", "h1", FONT_TITLE, "700", 1.1, -4,
            ),
            heading(
                "Tudo em uma única escola",
                50, BLUE_LIGHT, "left", "h1", FONT_TITLE, "700", 1.1, -4,
            ),
            rich_text(
                "<p>No dia 28 de setembro, o Adriel vai abrir a Escola Power 360 "
                "completa: 10 treinamentos, "
                '<strong style="color:#B0D0F0;">acesso vitalício e uma condição '
                "especial só para alunos.</strong> Quem estiver no grupo vai "
                "receber a oferta primeiro.</p>",
                24, WHITE, "left", FONT_TEXT, "300", 1.3,
            ),
            cta_block(url),
        ],
    )

    hero_bg = {
        "background_background": "classic",
        "background_color": BG_HERO,
        "background_image": {"url": img("adriel-retrato.png"), "id": "", "source": "library"},
        "background_position": "bottom right",
        "background_repeat": "no-repeat",
        "background_size": "contain",
        "border_radius": dim(24, 24, 24, 24),
    }

    return section(
        [topbar, content],
        background=hero_bg,
        padding=(0, 0, 0, 0),
        boxed=1140,
        extra={"min_height": px(1040)},
    )


PILARES = [
    "Fazer a apresentação é uma habilidade.",
    "Defender a sua ideia para seu chefe ou lider é outra.",
    "Conhecer as pessoas certas sem parecer que você quer tirar proveito é outra.",
    "E ser lembrado quando você não está na sala é outra.",
]


def build_pilares(img):
    cards = []
    for texto in PILARES:
        icon_settings = {
            "content_width": "full",
            "width": px(64),
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_justify_content": "center",
            "flex_shrink": "0",
            "padding": dim(16, 16, 16, 16),
        }
        icon_settings.update(gradient(BLUE, "rgba(17,17,17,0)", 216))

        card_settings = {
            "content_width": "full",
            "width": px(49, "%"),
            "min_height": px(112),
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_gap": gap(24),
            "padding": dim(24, 48, 24, 32),
        }
        card_settings.update(border())
        card_settings.update(gradient("rgba(72,139,209,0.2)", "rgba(17,17,17,0)", 190))

        cards.append(
            container(
                card_settings,
                [
                    container(icon_settings, [image(img("icon-sphere.svg"), 32, "")]),
                    rich_text(
                        "<p>%s</p>" % texto,
                        20, OFF_WHITE, "left", FONT_TEXT, "400", 1.2,
                    ),
                ],
            )
        )

    grid = container(
        {
            "content_width": "full",
            "flex_direction": "row",
            "flex_wrap": "wrap",
            "flex_gap": gap(10),
            "padding": dim(0, 0, 0, 0),
        },
        cards,
    )

    return section(
        [
            heading(
                "Apresentação é um dos pilares, mas para subir de nível",
                40, WHITE, "center", "h2", FONT_TITLE, "700", 1.1, -3.2,
            ),
            heading(
                "é preciso usar ela de forma 360 na sua carreira:",
                40, BLUE_LIGHT, "center", "h2", FONT_TITLE, "700", 1.1, -3.2,
            ),
            grid,
        ],
        boxed=930,
        extra={"flex_gap": gap(58)},
    )


TREINAMENTOS = [
    {
        "title": "Método POWER",
        "image": "capa-metodo-power.png",
        "badge": "",
        "variant": "a",
        "html": "<p><strong>Formação completa em apresentações, desde o planejamento "
                "do conteúdo, narrativas de storytelling, ao design e à entrega.</strong></p>"
                "<p>A metodologia principal da Power, aprovada pelo MEC e totalmente "
                "regravada este ano.</p>",
    },
    {
        "title": "IA Apresentações 2.0",
        "image": "apresentacao-ia.png",
        "badge": "",
        "variant": "a",
        "html": "<p><strong>Aprenda a usar IA para criar apresentações mais rápido sem "
                "cair no resultado genérico.</strong></p>"
                "<p>Como usar as melhores ferramentas de IA para criar estrutura do "
                "conteúdo com storytelling, insumos para apresentação, imagens para "
                "criação visual, e até mesmo apresentações inteiras, mas com método "
                "para manter qualidade, personalidade e controle do resultado final.</p>",
    },
    {
        "title": "Apresentações Express",
        "image": "apresentacoes-express.png",
        "badge": "",
        "variant": "a",
        "html": "<p><strong>Para quando você precisa criar uma boa apresentação em "
                "pouco tempo.</strong></p>"
                "<p>Um processo para sair do zero e chegar a uma apresentação pronta "
                "em cerca de uma hora.</p>",
    },
    {
        "title": "Mecanismos de uma Apresentação de Sucesso",
        "image": "mecanismos.png",
        "badge": "",
        "variant": "a",
        "html": "<p>A caixa-preta das Palestras aberta: por que alguns pitch’s do Shark "
                "Tank fecham parcerias, o que faz o Steve Jobs prender a atenção de uma "
                "plateia inteira por horas, como foram montadas as apresentações do "
                "Thiago Nigro e do Ícaro de Carvalho. Você enxerga o mecanismo que se "
                "repete, reconhece e começa a aplicar nas suas apresentações.</p>",
    },
    {
        "title": "Bússola da Criatividade",
        "image": "bussola.png",
        "badge": "",
        "variant": "a",
        "html": "<p>Para a hora em que você encara a tela em branco e pensa \"eu não sou "
                "criativo\". Ao contrário do que muita gente pensa, a criatividade pode "
                "sim ser desenvolvida através de um método.</p>",
    },
    {
        "title": "Networking",
        "image": "networking.png",
        "badge": "NOVO",
        "variant": "b",
        "html": "<p><strong>Aprenda a construir relações profissionais que geram acesso "
                "e oportunidades.</strong></p>"
                "<p>Como se aproximar das pessoas certas, manter contato e criar uma "
                "rede de forma natural, sem ser interesseiro.</p>",
    },
    {
        "title": "Branding Pessoal e Posicionamento",
        "image": "posicionamento.png",
        "badge": "NOVO",
        "variant": "b",
        "html": "<p><strong>Saia de “mais um bom profissional” para alguém com uma "
                "posição clara no seu trabalho.</strong></p>"
                "<p>Um treinamento para definir seu posicionamento, fortalecer sua "
                "reputação e aumentar o valor percebido do seu trabalho.</p>",
    },
    {
        "title": "Comunicação de Poder",
        "image": "comunica.png",
        "badge": "NOVO",
        "variant": "b",
        "html": "<p><strong>Não basta ter uma boa apresentação se você não consegue "
                "sustentar a mensagem ao falar.</strong></p>"
                "<p>Oratória, comunicação verbal e não verbal para apresentar ideias "
                "com mais clareza e segurança, responder a perguntas difíceis, lidar "
                "com imprevistos e manter o controle da apresentação mesmo quando algo "
                "não sai como o planejado.</p>",
    },
    {
        "title": "Novo treinamento",
        "image": "capa-metodo-power.png",
        "badge": "NOVO",
        "variant": "b",
        "html": "<p><strong>Como transformar esse conhecimento em conteúdo para as "
                "redes sociais, que gera visibilidade e oportunidade profissional."
                "</strong></p><p>Como eu faço hoje com a Power.</p>",
    },
]


def build_card(img, item, blur=None):
    body_children = []

    if item["badge"]:
        badge_settings = {
            "content_width": "full",
            "width": px(65),
            "min_height": px(25),
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_justify_content": "center",
            "padding": dim(0, 12, 0, 12),
        }
        badge_settings.update(border(1, BLUE_LIGHT))
        badge_settings.update(gradient(BLUE, "rgba(17,17,17,0)", 195))
        body_children.append(
            container(
                badge_settings,
                [heading(item["badge"], 16, OFF_WHITE, "center", "div", FONT_TEXT, "400", 1.3)],
            )
        )

    body_children.append(
        heading(item["title"], 32, BLUE_LIGHT, "left", "h3", FONT_TITLE, "700", 1.3)
    )
    body_children.append(rich_text(item["html"], 16, OFF_WHITE, "left", FONT_TEXT, "400", 1.3))

    body = container(
        {
            "content_width": "full",
            "flex_direction": "column",
            "flex_align_items": "flex-start",
            "flex_gap": gap(12),
            "flex_grow": "1",
            "padding": dim(0, 0, 0, 0),
        },
        body_children,
    )

    media_settings = {
        "content_width": "full",
        "width": px(248),
        "flex_shrink": "0",
        "padding": dim(0, 0, 0, 0),
    }
    media_settings.update(border())
    media = container(
        media_settings,
        [image(img(item["image"]), 248, item["title"], "center", blur)],
    )

    inner_settings = {
        "content_width": "full",
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": gap(32),
        "padding": dim(22, 22, 22, 22),
        "box_shadow_box_shadow_type": "yes",
        "box_shadow_box_shadow": {
            "horizontal": 0,
            "vertical": 7,
            "blur": 4,
            "spread": 0,
            "color": "rgba(0,0,0,0.45)",
        },
    }
    inner_settings.update(border())
    if item["variant"] == "a":
        inner_settings.update(gradient("rgba(72,139,209,0.2)", "rgba(17,17,17,0)", 201))
    else:
        inner_settings.update(gradient("rgba(17,17,17,0)", "rgba(72,139,209,0.6)", 201))

    if blur:
        inner_settings["background_overlay_background"] = "classic"
        inner_settings["background_overlay_color"] = "rgba(0,0,0,0.6)"

    inner = container(inner_settings, [media, body])

    outer_settings = {
        "content_width": "full",
        "flex_direction": "column",
        "padding": dim(11, 10, 11, 10),
        "background_background": "classic",
        "background_color": BG_CARD,
    }
    outer_settings.update(border())

    return container(outer_settings, [inner])


def build_treinamentos(img):
    children = [
        heading("Você recebe:", 54, WHITE, "center", "h2", FONT_TITLE, "700", 1.1, -4.3),
        rich_text(
            '<p><strong style="color:#B0D0F0;">Dez treinamentos. Acesso vitalício. '
            "Paga uma vez e é seu.</strong> Sem mensalidade, sem renovação, sem data "
            "para acabar.</p>",
            24, WHITE, "center", FONT_TEXT, "300", 1.3,
        ),
    ]

    for item in TREINAMENTOS:
        children.append(build_card(img, item))

    children.append(
        build_card(
            img,
            {
                "title": "+ Bônus surpresa",
                "image": "alavanca.png",
                "badge": "",
                "variant": "b",
                "html": "<p><strong>Tem um bônus que não vai ser vendido depois, em "
                        "lugar nenhum. Ele é sobre transformar tudo isso em dinheiro no "
                        "seu bolso.</strong></p>"
                        "<p>O que é exatamente, eu vou contar ao vivo no dia 28.</p>",
            },
            blur=8,
        )
    )

    return section(children, boxed=782, extra={"flex_gap": gap(18)})


LOGOS = [
    "logo-hughes.svg", "logo-sebrae.svg", "logo-globo.svg", "logo-cargill.svg",
    "logo-eletrobras.svg", "logo-saint-gobain.svg", "logo-novo-nordisk.svg",
    "logo-tedx.svg", "logo-sbm-offshore.svg", "logo-fs.svg", "logo-rpc.svg",
    "logo-pfizer.svg", "logo-suzano.svg", "logo-banco-do-brasil.svg",
    "logo-senai.svg", "logo-rede-bahia.svg", "logo-equatorial.svg",
    "logo-bauducco.svg", "logo-banco-bv.svg", "logo-vivo.svg", "logo-bayer.svg",
    "logo-taua.svg", "logo-cni.svg", "logo-copacol.svg", "logo-accor.svg",
    "logo-sicoob.svg", "logo-envista.svg", "logo-orica.svg",
]


def build_marcas(img, url):
    carousel = widget(
        "image-carousel",
        {
            "carousel": [{"id": "", "url": img(name)} for name in LOGOS],
            "slides_to_show": "5",
            "slides_to_show_tablet": "3",
            "slides_to_show_mobile": "2",
            "slides_to_scroll": "1",
            "image_size": "full",
            "navigation": "none",
            "autoplay": "yes",
            "autoplay_speed": 2500,
            "infinite": "yes",
            "speed": 600,
            "pause_on_hover": "yes",
            "image_spacing": "custom",
            "image_spacing_custom": px(52),
        },
    )

    return section(
        [
            cta_block(url),
            rich_text(
                "<p>A Black 360 é para ser "
                '<span style="color:#B0D0F0;">a melhor forma de ter a habilidade</span>'
                ' que as <span style="color:#B0D0F0;">grandes marcas valorizam</span></p>',
                40, WHITE, "center", FONT_TITLE, "700", 1.1,
            ),
            carousel,
        ],
        boxed=1140,
        extra={"flex_gap": gap(48)},
    )


ADRIEL_HTML = (
    "<p>Ele começou montando apresentação na empresa em que trabalhava como analista "
    "e hoje treina as maiores empresas do país. A minha missão é ajudar você a criar "
    "uma apresentação estratégica, inovadora, e muito acima da média, é fazer com que "
    "você impressione o seu público por onde passar, independente de qual seja sua "
    "área de atuação. Eu sou o fundador da PowerPPT, mas antes de chegar até aqui. "
    "Foram quase 12 anos de experiência profissional no mercado corporativo, atuei nas "
    "maiores empresas de comunicação do país (Editora Abril e TV Globo) e sempre me "
    "destaquei pelas habilidades de comunicação e apresentações inovadoras. Sou "
    "Formado em Marketing e Pós-graduado em Gestão de Projetos pela USP. Tenho "
    "experiências de estudo e trabalho nos Estados Unidos e Argentina.</p>"
    "<p>Durante toda minha trajetória me aprofundei em Design, Storytelling e "
    "comunicação e coloquei todo esse conhecimento dentro de uma metodologia que já "
    "ajudou milhares de pessoas. E agora, eu quero compartilhar todo esse conhecimento "
    "com você.</p>"
)


def build_adriel(img):
    texto = container(
        {
            "content_width": "full",
            "flex_direction": "column",
            "flex_gap": gap(32),
            "flex_grow": "1",
            "padding": dim(98, 41, 98, 51),
        },
        [
            heading("Quem é o Adriel?", 40, NAVY, "left", "h2", FONT_TITLE, "700", 1.1, -3.2),
            rich_text(ADRIEL_HTML, 16, NAVY, "left", FONT_TEXT, "400", 1.3),
        ],
    )

    foto = container(
        {
            "content_width": "full",
            "width": px(430),
            "flex_shrink": "0",
            "padding": dim(0, 0, 0, 0),
            "background_background": "classic",
            "background_color": NAVY,
            "margin": dim(56, 40, 56, 0),
        },
        [image(img("adriel-retrato.png"), None, "Adriel Araújo", "center")],
    )

    box = container(
        {
            "content_width": "full",
            "flex_direction": "row",
            "flex_align_items": "stretch",
            "min_height": px(600),
            "padding": dim(0, 0, 0, 0),
            "background_background": "classic",
            "background_color": WHITE,
            "box_shadow_box_shadow_type": "yes",
            "box_shadow_box_shadow": {
                "horizontal": 0,
                "vertical": 4,
                "blur": 23,
                "spread": 9,
                "color": "rgba(0,0,0,0.55)",
            },
        },
        [texto, foto],
    )

    fundo = {
        "background_background": "classic",
        "background_color": BG,
        "background_image": {"url": img("adriel-bg.png"), "id": "", "source": "library"},
        "background_position": "center center",
        "background_size": "cover",
        "background_overlay_background": "gradient",
        "background_overlay_color": BG,
        "background_overlay_color_stop": px(38, "%"),
        "background_overlay_color_b": "rgba(17,17,17,0)",
        "background_overlay_color_b_stop": px(100, "%"),
        "background_overlay_gradient_type": "linear",
        "background_overlay_gradient_angle": px(180, "deg"),
    }

    return section([box], background=fundo, padding=(95, 0, 120, 0), boxed=1140)


def build_footer(img):
    row = container(
        {
            "content_width": "full",
            "flex_direction": "row",
            "flex_align_items": "center",
            "flex_justify_content": "space-between",
            "padding": dim(0, 0, 0, 0),
        },
        [
            image(img("logo-power-footer.svg"), 128, "Power", "left"),
            rich_text(
                "<p>Todos direitos reservados</p>",
                14, WHITE, "right", FONT_TEXT, "300", 1.1,
            ),
        ],
    )

    return section(
        [row],
        background={"background_background": "classic", "background_color": BG_FOOTER},
        padding=(64, 0, 64, 0),
        boxed=1140,
    )


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------


def build(base_url, cta_url):
    def img(name):
        return "%s/%s" % (base_url.rstrip("/"), name)

    content = [
        build_hero(img, cta_url),
        build_pilares(img),
        build_treinamentos(img),
        build_marcas(img, cta_url),
        build_adriel(img),
        build_footer(img),
    ]

    return {
        "content": content,
        "page_settings": {
            "background_background": "classic",
            "background_color": BG,
            "hide_title": "yes",
        },
        "version": "0.4",
        "title": "Black 360 - Apresentação",
        "type": "page",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base-url",
        default="https://SEUDOMINIO.com.br/wp-content/uploads/black360",
        help="URL da pasta onde as imagens exportadas do Figma foram enviadas.",
    )
    parser.add_argument(
        "--cta-url",
        default="#inscricao",
        help="Destino dos botoes de CTA.",
    )
    parser.add_argument("--out", default="black360-apresentacao.json")
    parser.add_argument("--seed", type=int, default=360, help="Semente dos IDs (saida estavel).")
    args = parser.parse_args()

    random.seed(args.seed)

    data = build(args.base_url, args.cta_url)

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent="\t")
        fh.write("\n")

    widgets = json.dumps(data).count('"elType": "widget"')
    print("%s gerado (%d widgets nativos)" % (args.out, widgets))


if __name__ == "__main__":
    main()
