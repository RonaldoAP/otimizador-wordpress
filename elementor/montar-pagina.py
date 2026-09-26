#!/usr/bin/env python3
"""Monta o dump da pagina inteira a partir das secoes extraidas do Figma."""
import json, pathlib

AQUI = pathlib.Path(__file__).parent
BRANCO = [{"t": "solid", "cor": "#ffffff", "op": 1}]
OFF = [{"t": "solid", "cor": "#f2edeb", "op": 1}]
AZUL = [{"t": "solid", "cor": "#488bd1", "op": 1}]
BG = [{"t": "solid", "cor": "#111111", "op": 1}]
CARD = [{"t": "solid", "cor": "#080808", "op": 1}]
BORDA = {"paints": [{"t": "grad", "stops": [{"cor": "#ffffff", "a": 0.6, "pos": 0},
                                            {"cor": "#89bcf0", "a": 0.3, "pos": 1}]}], "peso": 1}
SOMBRA = [{"t": "DROP_SHADOW", "cor": "#000000", "a": 0.45, "r": 3.5, "off": {"x": 0, "y": 7}, "sp": 0}]


def flex(dir="VERTICAL", gap=20, pad=(0, 0, 0, 0), al="CENTER", ju="MIN",
         lg="FIXED", at="HUG", wrap=None):
    f = {"dir": dir, "gap": gap,
         "pad": {"top": pad[0], "right": pad[1], "bottom": pad[2], "left": pad[3]},
         "alinha": al, "justifica": ju, "larg": lg, "alt": at}
    if wrap:
        f["wrap"] = "WRAP"
    return f


def txt(nome, conteudo, fonte, tam, cor=BRANCO, lh=130, ls=0, alinha="CENTER", w=None):
    n = {"nome": nome, "tipo": "TEXT", "w": w, "h": None, "fundo": cor,
         "texto": {"conteudo": conteudo, "fonte": fonte, "tam": tam,
                   "lh": {"unit": "PERCENT", "value": lh},
                   "ls": {"unit": "PERCENT", "value": ls},
                   "alinha": alinha}}
    return n


def img(nome, w=None, h=None):
    return {"nome": "w/image · " + nome, "tipo": "IMG", "w": w, "h": h}


def cont(nome, filhos, w=None, h=None, fundo=None, borda=None, efeitos=None,
         raio=None, **kw):
    n = {"nome": nome, "tipo": "FRAME", "w": w, "h": h, "flex": flex(**kw),
         "filhos": filhos}
    if fundo:
        n["fundo"] = fundo
    if borda:
        n["borda"] = borda
    if efeitos:
        n["efeitos"] = efeitos
    if raio:
        n["raio"] = raio
    return n


def secao(nome, y, filhos, pad=(120, 0, 120, 0), gap=40, fundo=None,
          box=1140, sangra=(), **kw):
    """Secao full-bleed com um container boxed dentro.

    `filhos` entram no container boxed (conteudo centralizado); `sangra` entra
    direto na secao, de ponta a ponta — carrossel e faixa, que nao podem ser
    limitados pela coluna de conteudo.
    """
    dentro = []
    if filhos:
        dentro.append(cont("box/" + nome.split("/")[-1], filhos, w=box, gap=gap,
                           al="CENTER", lg="FIXED"))
    dentro.extend(sangra)
    s = cont(nome, dentro, w=1920, pad=pad, gap=gap, fundo=fundo or BG,
             al="CENTER", **kw)
    s["id"] = nome
    s["y"] = y
    return s


paginas = []

# ---------------------------------------------------------------- 1, 2 e 3
prontas = json.loads((AQUI / "a.json").read_text(encoding="utf-8"))
hero = prontas[0]
prova = prontas[1]
h1_problema = prontas[2]
paginas.append(hero)
paginas.append(prova)

# -------------------------------------------------- dobra 3 · o problema
FALAS = [
    ("Fico muito nervoso ao falar em reuniões importantes", "SEGUNDA · 12h14"),
    ("Será que meu chefe faz ideia do que eu realmente entrego?", "terça · 09h14"),
    ("Por que ele foi promovido e eu não?", "quarta · 18h40"),
    ("Estou há tanto tempo no mesmo cargo, quando vou ser promovido?", "quinta · 07h52"),
    ("E se me pedirem para apresentar isso amanhã, na frente da diretoria?", "quinta · 23h06"),
    ("Se eu fosse cortado amanhã, quem na empresa lembraria do meu nome?", "domingo · 21h33"),
    ("Eu uso IA, mas o resultado quase sempre é genérico.", "SEGUNDA · 11h13"),
]
cartas = [
    cont("col/fala", [
        txt("aspas", "”", "Gotham|Black", 55, AZUL, 100, 0, "LEFT"),
        txt("fala", f, "Gotham|Book", 19, BRANCO, 140, -2, "LEFT"),
        txt("hora", h, "Gotham|Light", 13, OFF, 120, 4, "LEFT"),
    ], w=252, h=357, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=16,
        gap=19, pad=(31, 31, 26, 31), al="MIN", lg="FIXED", at="FIXED")
    for f, h in FALAS
]
paginas.append(secao("sec/problema", 1959, [
    txt("w/heading · H1", h1_problema["texto"]["conteudo"], "Cutta|Bold", 54, BRANCO, 110, -8),
], gap=56, sangra=[cont("row/falas", cartas, w=1886, gap=20, al="CENTER", lg="FIXED")]))

# ---------------------------------------------------------------- dobra 4
paginas.append(dict(json.loads((AQUI / "dobra4.json").read_text(encoding="utf-8")),
                    id="dobra4", y=2735))

# ----------------------------------------------- dobra 5 · apresentações
APRESENTA = [
    "Você se apresenta quando entra numa reunião.",
    "Você se apresenta quando defende uma ideia.",
    "Você se apresenta quando conhece alguém.",
    "Você se apresenta quando publica alguma coisa relacionada ao seu trabalho",
    "Você se apresenta quando fala do seu trabalho.",
    "Você se apresenta quando tenta fechar um cliente ou um negócio.",
]
def tile(t, h):
    return cont("col/tile", [
        img("icone-apresentacao", 64, 64),
        txt("w/text", t, "Gotham|Medium", 14, BRANCO, 140, 0),
    ], w=296, h=h, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=12,
        gap=18, pad=(28, 20, 28, 20), al="CENTER", ju="CENTER", lg="FILL", at="FILL")

paginas.append(secao("sec/apresentacoes", 3880, [
    cont("box/apresentacoes", [
        txt("w/heading · H1",
            "As apresentações estão presentes em diversos formatos dentro do mundo profissional",
            "Cutta|Bold", 40, BRANCO, 115, -4),
        cont("col/grid", [
            cont("row/linha", [tile(APRESENTA[0], 180), tile(APRESENTA[1], 180), tile(APRESENTA[2], 180)],
                 w=928, gap=20, dir="HORIZONTAL", al="MIN", lg="FIXED"),
            cont("row/linha", [tile(APRESENTA[3], 200), tile(APRESENTA[4], 200), tile(APRESENTA[5], 200)],
                 w=928, gap=20, dir="HORIZONTAL", al="MIN", lg="FIXED"),
            cont("col/destaque", [
                txt("label", "QUANDO PRECISA MOSTRAR QUE ESTÁ PRONTO PARA UMA OPORTUNIDADE.",
                    "Gotham|Medium", 28, BRANCO, 140, 0),
            ], w=927, h=159, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=12,
                gap=18, pad=(28, 20, 28, 20), al="CENTER", ju="CENTER", lg="FIXED", at="FIXED"),
        ], w=930, gap=20, al="MIN", lg="HUG"),
        txt("w/text",
            "Por anos, a Escola POWER ensinou os profissionais a apresentar melhor as suas ideias. "
            "E a gente sempre soube que a apresentação vai muito além do slide.",
            "Gotham|Book", 18, OFF, 150, 0, w=930),
    ], w=1089, gap=36, pad=(56, 40, 56, 40), al="CENTER", ju="CENTER",
        fundo=[{"t": "grad", "stops": [{"cor": "#488bd1", "a": 0.2, "pos": 0},
                                       {"cor": "#111111", "a": 0, "pos": 1}]}],
        borda=BORDA, efeitos=SOMBRA, raio=16, lg="FIXED"),
]))

# ------------------------------------------------------ dobra 5 · empresas
LOGOS = ["globo", "suzano", "pfizer", "novo-nordisk", "bauducco", "bayer", "sicoob", "sebrae"]
paginas.append(secao("sec/empresas", 4914, [
    txt("w/heading", "Mais de 60 das maiores empresas do Brasil atendidas",
        "Montserrat|Bold", 32, BRANCO, 120, -4, w=830),
], pad=(0, 0, 0, 0), gap=36, sangra=[
    cont("w/carousel", [img("logo-" + m, 160, 75) for m in LOGOS],
         w=1920, gap=85, dir="HORIZONTAL", al="CENTER", ju="CENTER", lg="FIXED")]))

# ------------------------------------------------------- agora é 360
HAB = [
    ("01", "Fazer a apresentação", "mensagem, storytelling e design"),
    ("02", "Defender a ideia ao vivo", "segurança na hora de falar"),
    ("03", "Conhecer as pessoas certas", "networking sem parecer interesseiro"),
    ("04", "Ser lembrado sem estar na sala", "posicionamento e reputação"),
]
cards360 = [
    cont("col/habilidade", [
        txt("num", n, "Gotham|Bold", 15, AZUL, 130, 8, "LEFT"),
        txt("H1", t, "Gotham|Medium", 21, BRANCO, 125, -2, "LEFT"),
        txt("H2", s, "Gotham|Light", 15, OFF, 140, 0, "LEFT"),
    ], w=420, fundo=[{"t": "solid", "cor": "#111111", "op": 0.3}], borda=BORDA,
        efeitos=[{"t": "DROP_SHADOW", "cor": "#000000", "a": 0.55, "r": 27,
                  "off": {"x": 0, "y": 12}, "sp": 0}],
        raio=17, gap=20, pad=(25, 30, 25, 30), al="MIN", lg="FIXED")
    for n, t, s in HAB
]
paginas.append(secao("sec/agora-e-360", 5234, [
    cont("col/texto", [
        txt("w/text", "Por isso, a Escola POWER agora é 360.", "Gotham|Bold", 24, AZUL, 115, -4),
        txt("w/heading",
            "Apresentação é um pilar fundamental e para subir de nível é preciso usar ela de forma 360 na carreira.",
            "Cutta|Bold", 40, BRANCO, 110, -8),
        txt("w/text",
            "Foram essas habilidades que tiraram o Adriel de júnior, levaram ele a executivo e depois a "
            "palestrar e aplicar treinamentos no Brasil inteiro. Nenhuma delas estava no currículo dele.",
            "Gotham|Book", 18, OFF, 150, 0),
    ], w=931, gap=24, al="CENTER", lg="FIXED"),
    cont("row/orbita", [
        cont("col/lado", [cards360[0], cards360[2]], w=440, gap=200, al="MIN", lg="FIXED"),
        img("esfera-360", 259, 259),
        cont("col/lado", [cards360[1], cards360[3]], w=440, gap=200, al="MIN", lg="FIXED"),
    ], w=1300, gap=40, dir="HORIZONTAL", al="CENTER", ju="CENTER", lg="FIXED"),
], gap=64))

# ---------------------------------------------------------------- dobra 7
TREINOS = [
    ("Método POWER PRO", "capa-pro",
     "Formação completa em apresentações, desde o planejamento do conteúdo, narrativas de storytelling, ao design e à entrega. A metodologia principal da Power, aprovada pelo MEC e totalmente regravada este ano.", None),
    ("IA Apresentações 2.0", "ia-apresentacoes",
     "Aprenda a usar IA para criar apresentações mais rápido sem cair no resultado genérico. Como usar as melhores ferramentas de IA para criar estrutura do conteúdo com storytelling, insumos para apresentação, imagens para criação visual, e até mesmo apresentações inteiras, mas com método para manter qualidade, personalidade e controle do resultado final.", None),
    ("Apresentações Express", "apresentacoes-express",
     "Para quando você precisa criar uma boa apresentação em pouco tempo. Um processo para sair do zero e chegar a uma apresentação pronta em cerca de uma hora.", None),
    ("Arsenal Magnético", "arsenal-magnetico",
     "Mais de 30 templates editáveis para acelerar a criação dos seus slides. Modelos usados pela própria Power em projetos profissionais, prontos para você adaptar ao seu conteúdo.", None),
    ("Mecanismos de uma Apresentação de Sucesso", "mecanismos",
     "A caixa-preta das Palestras aberta: por que alguns pitch’s do Shark Tank fecham parcerias, o que faz o Steve Jobs prender a atenção de uma plateia inteira por horas, como foram montadas as apresentações do Thiago Nigro e do Ícaro de Carvalho. Você enxerga o mecanismo que se repete, reconhece e começa a aplicar nas suas apresentações.", None),
    ("Bússola da Criatividade", "bussola",
     "Para a hora em que você encara a tela em branco e pensa \"eu não sou criativo\". Ao contrário do que muita gente pensa, a criatividade pode sim ser desenvolvida através de um método.", None),
    ("Networking", "networking",
     "Aprenda a construir relações profissionais que geram acesso e oportunidades. Como se aproximar das pessoas certas, manter contato e criar uma rede de forma natural, sem ser interesseiro.", "NOVO"),
    ("Branding Pessoal e Posicionamento", "branding",
     "Saia de “mais um bom profissional” para alguém com uma posição clara no seu trabalho. Um treinamento para definir seu posicionamento, fortalecer sua reputação e aumentar o valor percebido do seu trabalho.", "NOVO"),
    ("Comunicação de Poder", "comunicacao-de-poder",
     "Não basta ter uma boa apresentação se você não consegue sustentar a mensagem ao falar. Oratória, comunicação verbal e não verbal para apresentar ideias com mais clareza e segurança, responder a perguntas difíceis, lidar com imprevistos e manter o controle da apresentação mesmo quando algo não sai como o planejado.", "NOVO"),
    ("Guia da Rede Social Lucrativa", "rede-social",
     "Como transformar o seu conhecimento em conteúdo para as redes sociais, que gera visibilidade e oportunidade profissional. Como eu faço hoje com a Power.", "NOVO"),
    ("Como ganhar dinheiro com apresentações", "alavanca",
     "Três caminhos para transformar tudo isso em dinheiro no bolso: ser promovido, vender palestra ou vender a criação de apresentações para fora (o serviço pelo qual o Adriel cobrava cerca de R$ 10 mil por apresentação). Esse bônus não vai ser vendido depois, em lugar nenhum.", "BÔNUS"),
]
def card_treino(titulo, capa, corpo, selo):
    col = []
    if selo:
        col.append(cont("col/selo", [txt("selo", selo, "Gotham|Bold", 16, BRANCO, 120, 4, "LEFT")],
                        w=80, fundo=AZUL, raio=6, gap=0, pad=(6, 12, 6, 12),
                        al="CENTER", ju="CENTER", lg="HUG"))
    col.append(txt("w/heading", titulo, "Cutta|Bold", 32, BRANCO, 115, -4, "LEFT", w=411))
    col.append(txt("w/text", corpo, "Gotham|Book", 16, OFF, 150, 0, "LEFT", w=411))
    return cont("row/card-treino", [
        img("capa-" + capa, 248, 358),
        cont("col/texto", col, w=411, gap=16, al="MIN", lg="FIXED"),
    ], w=782, h=428, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=12,
        gap=44, dir="HORIZONTAL", al="CENTER", ju="MIN", pad=(35, 35, 35, 35), lg="FIXED")

paginas.append(secao("sec/o-que-esta-dentro", 6394, [
    cont("col/cabecalho", [
        txt("linha de apoio", "O QUE ESTÁ DENTRO DA BLACK 360", "Gotham|Light", 13, AZUL, 120, 10),
        txt("w/heading", "A Escola POWER inteira. 10 treinamentos. Acesso vitalício.",
            "Cutta|Bold", 40, BRANCO, 115, -4),
        txt("w/text", "Paga uma vez e é seu. Sem mensalidade, sem renovação, sem data para acabar.",
            "Gotham|Book", 18, OFF, 150, 0),
    ], w=930, gap=18, al="CENTER", lg="FIXED"),
    cont("col/treinamentos", [card_treino(*t) for t in TREINOS],
         w=782, gap=18, al="CENTER", lg="FIXED"),
], gap=48))

# ---------------------------------------------------------------- dobra 8
STACK = [
    ("01 · Método POWER", "R$ 597,00"), ("02 · IA Apresentações 2.0 + Oficina", "R$ 427,00"),
    ("03 · Apresentações Express", "R$ 49,90"), ("04 · Arsenal Magnético", "R$ 397,00"),
    ("05 · Mecanismos", "R$ 3.000,00"), ("06 · Bússola da Criatividade", "R$ 197,00"),
    ("07 · Networking", "R$ 897,00"), ("08 · Branding e Posicionamento", "R$ 997,00"),
    ("09 · Comunicação de Poder", "R$ 797,00"), ("10 · Guia da Rede Social Lucrativa", "R$ 697,00"),
    ("Bônus · Ganhar dinheiro com apresentações", "INCALCULÁVEL"),
]
linhas = [cont("row/linha", [
    txt("item", a, "Gotham|Light", 12, OFF, 130, 0, "LEFT"),
    txt("valor", b, "Gotham|Book", 12, OFF, 130, 0, "RIGHT"),
], w=700, gap=12, dir="HORIZONTAL", al="CENTER", ju="SPACE_BETWEEN", pad=(7, 0, 7, 0), lg="FILL")
    for a, b in STACK]
linhas.append(cont("row/total", [
    txt("label", "Total:", "Gotham|Bold", 24, OFF, 130, 0, "LEFT"),
    txt("valor", "R$ 8.055,90", "Gotham|Bold", 32, BRANCO, 130, 0, "RIGHT"),
], w=700, gap=12, dir="HORIZONTAL", al="CENTER", ju="SPACE_BETWEEN", pad=(20, 0, 0, 0), lg="FILL"))

paginas.append(secao("sec/oferta", 11794, [
    txt("w/heading", "Se você fosse comprar treinamento por treinamento, pagaria mais de R$ 5 mil.",
        "Cutta|Bold", 40, BRANCO, 115, -4, w=930),
    cont("col/stack", linhas, w=773, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=12,
         gap=0, pad=(36, 40, 36, 40), al="CENTER", lg="FIXED"),
    cont("col/preco", [
        txt("w/text",
            "Menos de R$ 120 por treinamento. E é seu para sempre. Escolas de carreira por assinatura "
            "cobram mais de R$ 2.700 por ano, e quando a assinatura acaba, o acesso acaba junto. "
            "Aqui você paga uma vez e tem acesso para sempre. Na BLACK 360, a escola POWER inteira sai por 12x de:",
            "Gotham|Book", 18, OFF, 150, 0),
        txt("valor", "R$ 142,16", "Cutta|Bold", 76, BRANCO, 100, -5),
        txt("parcelado", "ou R$ 1.297,00 à vista", "Gotham|Book", 15, OFF, 130, 0),
    ], w=773, gap=10, pad=(44, 48, 44, 48), fundo=CARD, borda=BORDA, raio=12,
        efeitos=[{"t": "DROP_SHADOW", "cor": "#488bd1", "a": 0.35, "r": 80,
                  "off": {"x": 0, "y": 0}, "sp": 0}], al="CENTER", lg="FIXED"),
    cont("w/button", [
        txt("rotulo", "QUERO ACESSO VITALÍCIO À ESCOLA POWER", "Cutta|Medium", 18, BRANCO, 120, 0),
    ], w=613, h=62, fundo=[{"t": "grad", "stops": [{"cor": "#488bd1", "a": 1, "pos": 0},
                                                   {"cor": "#111111", "a": 1, "pos": 1}]}],
        borda=BORDA, efeitos=[{"t": "INNER_SHADOW", "cor": "#6299d1", "a": 0.9, "r": 17.4,
                               "off": {"x": 0, "y": 3.5}, "sp": 0}],
        gap=8, dir="HORIZONTAL", al="CENTER", ju="CENTER", lg="FIXED", at="FIXED"),
    cont("row/garantia", [
        img("selo-30-dias", 250, 250),
        cont("col/texto", [
            txt("w/heading", "30 DIAS DE GARANTIA", "Cutta|Bold", 32, BRANCO, 115, -4, "LEFT"),
            txt("w/text",
                "Entre, assista e aplique na sua próxima reunião ou apresentação. Se em até 30 dias você "
                "sentir que a Escola POWER não é para você, é só falar com a gente e devolvemos 100% do "
                "valor pago. 30 dias é o tempo de testar de verdade, no seu trabalho, e não uma semana "
                "correndo contra o relógio.",
                "Gotham|Book", 18, OFF, 150, 0, "LEFT"),
        ], w=401, gap=16, al="MIN", lg="FIXED"),
    ], w=686, gap=35, dir="HORIZONTAL", al="CENTER", ju="MIN", lg="FIXED"),
], gap=56))

# ------------------------------------------------------- depoimentos
paginas.append(secao("sec/depoimentos", 14518, [
    txt("w/heading", "Resultados reais de quem já é aluno", "Cutta|Bold", 40, BRANCO, 115, -4, w=930),
], gap=40, sangra=[
    cont("w/carousel", [img("depoimento-%02d" % i, 324, 318) for i in range(1, 25)],
         w=1886, gap=20, dir="HORIZONTAL", al="CENTER", ju="MIN", lg="FIXED")]))

# ---------------------------------------------------------------- dobra 9
paginas.append(dict(json.loads((AQUI / "dobra9.json").read_text(encoding="utf-8")),
                    id="dobra9", y=15808))

# ------------------------------------------------------------------- FAQ
PERGUNTAS = [
    "Até quando vale a condição da BLACK 360?",
    "Já sou aluno da Black do ano passado. Vale a pena entrar?",
    "Não vou conseguir fazer 10 treinamentos.",
    "Não tenho tempo.",
    "Networking e posicionamento não são só puxar saco com nome bonito?",
    "Serve para a minha área?",
    "Preciso saber usar PowerPoint?",
    "Como recebo o acesso?",
    "Por quanto tempo tenho acesso?",
    "E se eu não gostar?",
    "Quais as formas de pagamento?",
]
linhas_faq = [cont("row/pergunta", [
    txt("pergunta", p, "Gotham|Medium", 18, BRANCO, 135, -2, "LEFT"),
    img("icone-mais", 26, 26),
], w=900, gap=28, dir="HORIZONTAL", al="CENTER", ju="SPACE_BETWEEN", pad=(26, 0, 26, 0), lg="FILL")
    for p in PERGUNTAS]

paginas.append(secao("sec/faq", 16962, [
    cont("col/cabecalho", [
        txt("linha de apoio", "PERGUNTAS FREQUENTES", "Gotham|Light", 13, AZUL, 120, 12),
        txt("w/heading", "Ainda ficou alguma dúvida?", "Cutta|Bold", 40, BRANCO, 115, -4),
    ], w=1040, gap=16, al="CENTER", lg="FIXED"),
    cont("col/acordeao", linhas_faq, w=966, fundo=CARD, borda=BORDA, efeitos=SOMBRA, raio=14,
         gap=0, pad=(6, 36, 6, 36), al="CENTER", lg="FIXED"),
    cont("w/button", [
        txt("rotulo", "QUERO ACESSO VITALÍCIO À ESCOLA POWER", "Cutta|Medium", 18, BRANCO, 120, 0),
    ], w=527, h=62, fundo=[{"t": "grad", "stops": [{"cor": "#488bd1", "a": 1, "pos": 0},
                                                   {"cor": "#111111", "a": 1, "pos": 1}]}],
        borda=BORDA, gap=8, dir="HORIZONTAL", al="CENTER", ju="CENTER", lg="FIXED", at="FIXED"),
], gap=44))

# ---------------------------------------------------------------- rodapé
paginas.append(secao("sec/footer", 18566, [
    cont("row/footer", [
        img("logo-power", 128, 21),
        txt("w/text", "Todos direitos reservados", "Gotham|Light", 14, BRANCO, 110, -8),
        cont("col/contatos", [
            txt("w/text", "Contatos oficiais da POWER", "Gotham|Bold", 14, BRANCO, 110, -8, "LEFT"),
            txt("w/text", "(11) 98651-8961\n(11) 99962-4029\n(11) 91421-4029",
                "Gotham|Light", 14, BRANCO, 155, -8, "LEFT"),
        ], w=175, gap=10, al="MIN", lg="HUG"),
    ], w=1140, gap=60, dir="HORIZONTAL", al="CENTER", ju="SPACE_BETWEEN", lg="FIXED"),
], pad=(64, 391, 64, 391), gap=0, fundo=[{"t": "solid", "cor": "#0a0a0a", "op": 1}]))

(AQUI / "pagina.json").write_text(json.dumps(paginas, ensure_ascii=False), encoding="utf-8")
print("seções:", len(paginas))
for s in sorted(paginas, key=lambda x: x.get("y", 0)):
    print("  %6d  %s" % (s.get("y", 0), s.get("nome")))
