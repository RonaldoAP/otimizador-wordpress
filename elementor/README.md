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

**1. Suba as imagens.** Os 41 arquivos otimizados estão em
[`assets/`](assets/) — envie todos para `wp-content/uploads/black360/`
(ou para a Biblioteca de mídia, reconectando depois; ver passo 5).

Otimização aplicada: 13,3 MB de PNG viraram **688 KB**.

| Tipo | Tratamento |
| --- | --- |
| Capas dos treinamentos | 745×1076 → 496×716 (2x do exibido), WebP q82 |
| Foto do Adriel | 1290×1464 → 860×976, WebP |
| Fundos (hero e perfil) | recomprimidos em WebP, largura original |
| Logo Black 360 | 606×174 → 400×115, WebP |
| 28 logos do carrossel + ícone | SVG rasterizado em PNG 150 px de altura, cinza + alfa |

Os logos viraram PNG de propósito: o WordPress bloqueia upload de SVG por
padrão, e rasterizar evita depender de um plugin para isso. Os SVGs originais
continuam disponíveis no Figma se um dia fizer falta.

**2. Confira a URL das imagens.** O arquivo versionado já aponta para
`https://adrielaraujo.com.br/wp-content/uploads/black360`. Para gerar com outro
domínio ou já com o link do CTA, rode:

```bash
python3 build-template.py \
  --base-url https://adrielaraujo.com.br/wp-content/uploads/black360 \
  --cta-url https://chat.whatsapp.com/xxxx \
  --out black360-apresentacao.json
```

**3. Importe.** Painel → **Modelos → Modelos salvos → Importar modelos** →
envie o `.json`.

> O import só existe na biblioteca **local**. Se a tela mostrar abas (Nuvem /
> Site), selecione a local antes — na aba da nuvem o Elementor responde
> *"This source does not support import"*. Algumas versões também só aceitam
> `.zip` no upload; gere um com
> `zip black360-apresentacao.zip black360-apresentacao.json`.

> Os botões estão com o link provisório `#inscricao`. Troque pelos três botões
> no editor do Elementor, ou por um find-and-replace no JSON antes de importar.

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
