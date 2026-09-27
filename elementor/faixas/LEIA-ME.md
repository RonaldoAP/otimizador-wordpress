# Faixas BLACK 360 · fotos em ângulo

Reprodução em HTML/CSS/JS do nó `387-7235` do Figma (Power 360), pronta para
colar num **widget HTML do Elementor**. Sem jQuery, sem plugin, sem biblioteca.

Arquivo: `faixas-black360.html`

## O que ele faz

- **Duas faixas atrás**, em carrossel infinito de verdade: a escura (preta,
  inclinada +5°) anda para a esquerda, a clara (branca, inclinada −5°) anda
  para a direita. Elas se cruzam por trás das capas, como no Figma.
- **Capas no ângulo do Figma** (`skewY(-9deg)`), sobrepostas em leque.
- **Hover**: a capa sobe no `translateY` e ganha sombra + contorno azul.
- **No celular**: mesma coisa. Como as capas não cabem na tela, a fileira
  também vira carrossel infinito, com as pontas em degradê; o toque levanta a
  capa (e pausa a fileira). Tocar de novo abaixa.

A animação é feita com `requestAnimationFrame`, não com `@keyframes`: ela
mede o conteúdo, duplica o necessário e reinicia exatamente no tamanho de uma
cópia, então a emenda nunca aparece — e para sozinha quando a seção sai da
tela ou a aba fica em segundo plano.

## As 10 capas

Já estão em `capas/` (e no `capas-black360.zip` na raiz do repositório),
endireitadas e prontas: o Figma guarda cada pôster já inclinado, então
extraí e desfiz o cisalhamento, para que o ângulo venha do CSS e você possa
trocar uma capa por outra reta sem que fique torta.

Suba a pasta para `wp-content/uploads/black360/` e pronto — os nomes na lista
`FOTOS` já batem.

**Resolução:** 176 x 300 px. É o tamanho nativo que o Figma entrega por esta
via e serve bem em tela comum, mas fica um pouco macio em tela retina. Para a
versão final, exporte as mesmas 10 do Figma em **2x** (frame `imagem`, nó
`291-2901`) e substitua os arquivos mantendo os nomes.

Enquanto um arquivo faltar, aquela capa aparece como retângulo tracejado com o
nome do módulo — dá para publicar sem quebrar o layout.

## Ajustes rápidos

Tudo que costuma precisar de ajuste está no topo:

| Onde | O quê |
|---|---|
| `--carta-l` / `--carta-a` | tamanho da capa |
| `--carta-sobrepoe` | quanto uma capa entra na outra |
| `--angulo` | inclinação das capas |
| `--sobe` | quanto a capa sobe no hover |
| `--azul` / `--navy` | cores do "360" e da faixa clara |
| `data-velocidade` (no HTML) | px por segundo de cada faixa; sinal negativo inverte o sentido |
| `MOVER_FOTOS` | `"auto"` (padrão), `true` ou `false` |

`MOVER_FOTOS = "auto"` deixa a fileira **parada e centralizada** quando as 10
capas cabem na tela — que é o comportamento do Figma no desktop — e só liga o
carrossel quando não cabem.

## Fontes

As faixas usam `Cutta`/`Gotham` com `Archivo` e a fonte do sistema como
reserva. Se o Cutta ainda não estiver em *Elementor → Configurações → Fontes
personalizadas*, a faixa cai na fonte reserva e fica um pouco diferente do
Figma — o layout não quebra.

## Pré-visualizar sem o WordPress

Abra `faixas-black360.html` direto no navegador: o bloco se vira sozinho.
