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

## Antes de usar: as 10 capas

O único passo manual. O download das imagens direto do Figma está bloqueado
pela política de rede do ambiente, então exporte você mesmo:

1. No Figma, selecione o frame `imagem` (nó `291-2901`).
2. Selecione as 10 capas dentro dele e exporte em **JPG 2x**.
3. Suba para `wp-content/uploads/black360/`.
4. No bloco, ajuste a lista `FOTOS` (logo no começo do `<script>`) com os
   nomes dos arquivos. A ordem é a mesma do Figma, da esquerda para a direita.

Enquanto um arquivo não existir, aquela capa aparece como um retângulo
tracejado com o nome do módulo — dá para publicar sem quebrar o layout.

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
