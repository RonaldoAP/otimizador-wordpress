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

Já estão em `capas/`, endireitadas. O Figma guarda cada pôster **já inclinado**;
extraí e desfiz o cisalhamento, para que o ângulo venha do CSS e você possa
trocar uma capa por outra reta sem que fique torta. Resultado: pôster de
176 x 300 px.

### Dois arquivos, escolha um

**`faixas-black360-embutido.html`** — as capas vão dentro do próprio bloco, em
data URI. Cole e acabou: não depende de caminho, de pasta nem de upload.
São 125 KB no total. É a opção sem o que dar errado.

**`faixas-black360.html`** — as capas vêm por URL. O bloco **descobre a pasta
sozinho**: testa `wp-content/uploads/black360/` e depois as pastas ano/mês dos
últimos 14 meses, que é onde a Biblioteca de mídia guarda os arquivos. Esse
teste acontece uma vez só, com a primeira capa; as outras nove já vão direto.

Se quiser cravar o caminho e pular a procura, preencha `BASE` no começo do
`<script>`: abra uma capa na Biblioteca de mídia, copie a URL do arquivo e
apague o nome do arquivo do fim. Fica algo como
`https://adrielaraujo.com.br/wp-content/uploads/2026/09/`.

Se nenhuma pasta responder, as capas ficam como retângulos tracejados com o
nome do módulo, e o console do navegador (F12) diz qual arquivo faltou.

> Atenção ao subir pela Biblioteca de mídia: o WordPress sanitiza nomes de
> arquivo. Se algum vier com sufixo (`capa-bussola-1.webp`) por já existir
> outro igual, a descoberta automática não acha — nesse caso ajuste o nome na
> lista `FOTOS` ou use a versão embutida.

### Resolução

176 x 300 px é o tamanho nativo que o Figma entrega por esta via — ele não faz
upscale no export. Serve bem em tela comum e fica um pouco macio em retina.
Para a versão final, exporte as mesmas 10 do Figma em **2x** (frame `imagem`,
nó `291-2901`), substitua os arquivos em `capas/` mantendo os nomes e rode
`python3 embutir.py` para regerar a versão embutida.

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
