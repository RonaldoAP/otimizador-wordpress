# Landing Black 360 — template do Elementor

Página **"Apresentação"** do Figma
([node `203-4138`](https://www.figma.com/design/IaGTZRWjKUszVD4lAmlAQl/Power-360?node-id=203-4138))
montada **100% com Containers flexbox e widgets nativos do Elementor**.

Sem shortcode, sem widget de HTML, sem código do tema: tudo é editável pelo
painel do Elementor.

| Arquivo | O que é |
| --- | --- |
| `black360-apresentacao.json` | Template pronto para importar |
| `build-template.py` | Gerador do JSON (permite regerar com outra URL de imagens ou outro CTA) |

## O que tem dentro

6 seções de topo, 77 containers e 63 widgets nativos:

| Widget | Qtd. | Onde |
| --- | --- | --- |
| `heading` | 22 | títulos, badges "NOVO", data do CTA |
| `text-editor` | 20 | parágrafos e títulos com palavras coloridas |
| `image` | 17 | capas dos treinamentos, ícones, logo, foto |
| `button` | 3 | CTAs "QUERO ENTRAR NO GRUPO" |
| `image-carousel` | 1 | carrossel das 28 marcas |

Seções: hero (topbar + headline + CTA), pilares (grid 2×2), "Você recebe"
(9 treinamentos + bônus), CTA + marcas, "Quem é o Adriel?" e rodapé.

## Como importar

**1. Suba as imagens.** Exporte do Figma para a Biblioteca de mídia (ou para
`wp-content/uploads/black360/`) usando os nomes listados em
[`../power360-black360/assets/img/README.md`](../power360-black360/assets/img/README.md).

**2. Gere o JSON com a URL do seu site.** O arquivo versionado aponta para
`https://SEUDOMINIO.com.br/wp-content/uploads/black360`. Troque por um
find-and-replace no JSON ou rode:

```bash
python3 build-template.py \
  --base-url https://seusite.com.br/wp-content/uploads/black360 \
  --cta-url https://chat.whatsapp.com/xxxx \
  --out black360-apresentacao.json
```

**3. Importe.** Painel → **Modelos → Modelos salvos → Importar modelos** →
envie o `.json`.

**4. Aplique.** Crie a página, abra com **Editar com Elementor**, clique no
ícone de pasta (Adicionar modelo) → aba **Meus modelos** → **Inserir**.

**5. Reconecte as imagens (recomendado).** As imagens entram por URL. Para que
fiquem na Biblioteca de mídia e gerem os tamanhos responsivos, clique em cada
widget de imagem e reselecione o arquivo — ou importe com um plugin que puxe
imagens externas para a biblioteca.

## Fontes

O template pede **Cutta** (títulos) e **Gotham** (textos), que são licenciadas
e não podem ser distribuídas aqui. Sem elas o Elementor cai na fonte do tema.
Suba as duas em **Elementor → Fontes personalizadas** com exatamente esses
nomes e o template passa a usá-las sozinho.

## Ajustes que valem fazer depois de importar

- **Cores e tipografia globais:** o template usa valores fixos, tirados do
  Figma (`#111`, `#0D0B11`, `#080808`, `#162B44`, `#F2EDEB`, `#488BD1`,
  `#B0D0F0`). Se quiser herdar dos Globais do Kit, troque nos widgets.
- **Responsivo:** as larguras vêm do desktop do Figma (o layout mobile não
  estava no node). Os containers são flex, então quebram sozinhos, mas vale
  passar nos breakpoints de tablet/celular ajustando tamanhos de fonte e a
  direção dos cards.

## Regerando o template

`build-template.py` monta o JSON a partir dos tokens e do conteúdo no topo do
arquivo — editar texto, card ou logo ali e rodar de novo é mais seguro do que
mexer no JSON à mão. Os IDs dos elementos são estáveis (semente fixa), então
duas gerações seguidas produzem o mesmo arquivo.
