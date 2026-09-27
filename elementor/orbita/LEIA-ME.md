# Órbita BLACK 360

Nó `394-7236` do Figma em HTML/CSS/JS, para colar num **widget HTML do
Elementor**. Sem biblioteca.

Arquivo: `orbita-black360.html` (23 KB, com a esfera embutida)

## O que tem dentro

- **Os dois anéis girando.** O externo é pontilhado e gira em 90s; o interno é
  contínuo, com o brilho concentrado de um lado, e gira em 34s no sentido
  contrário — é esse brilho assimétrico que faz a rotação ser percebida (um
  círculo uniforme girando não se mexe aos olhos). Dois pontos de luz
  acompanham o anel interno.
- **Os quatro boxes nos lugares do Figma.** As posições e larguras saíram
  medidas do arquivo, em porcentagem de um palco de 1124 x 734, então a
  composição inteira escala junto com a largura da tela sem sair do lugar.
- **A luz de fundo.** As duas elipses `luz de fundo` do Figma, na posição e no
  tamanho de lá, mais um véu largo por baixo que é o que dá o ar de ambiente
  iluminado.
- **A esfera do meio** vem embutida em data URI: não depende de upload.

O giro pausa sozinho quando a seção sai da tela ou a aba vai para segundo
plano, e não acontece para quem pediu menos animação no sistema
(`prefers-reduced-motion`).

## A imagem do container de trás

É a única coisa que falta. No começo do `<script>`:

```js
var TRASEIRA = "";   // ponha aqui a URL da imagem
```

Suba a imagem, copie a URL do arquivo na Biblioteca de mídia e cole entre as
aspas. Enquanto estiver vazio, esse container nem é criado — nada quebra.

Ela é posicionada centralizada, com 118% do tamanho do palco e `contain`. Se
precisar de outro enquadramento, mexa em `.b360-traseira` no CSS.

## Ajustes

| Onde | O quê |
|---|---|
| `--giro-fora` / `--giro-dentro` | tempo de uma volta de cada anel |
| `--azul` | cor dos números |
| `.b360-luz-a` `.b360-luz-b` `.b360-luz-c` | as três camadas de luz |
| `style="--x / --y / --w"` em cada `.b360-cartao` | posição e largura do box |

Para inverter o sentido de um anel, troque `animation-direction: reverse` em
`.b360-gira--dentro`.

## No celular

Abaixo de 900px a órbita não comporta os boxes em volta. O palco vira quadrado,
a cena inteira (luzes, anéis e esfera) é ampliada junto — para as proporções do
Figma não se perderem — e os quatro boxes viram uma lista embaixo.

## Fontes

Usa `Cutta`/`Gotham` com `Archivo` e a fonte do sistema como reserva. Sem o
Cutta registrado em *Elementor → Fontes personalizadas*, os títulos ficam um
pouco mais largos que no Figma; o layout não quebra.
