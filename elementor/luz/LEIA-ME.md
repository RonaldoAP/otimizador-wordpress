# Luz de fundo para containers

Reprodução do nó `291-2571` do Figma (Power 360): aquela mancha de luz
azul-clara nascendo no topo do container e morrendo no preto.

Arquivos:

- `luz-fundo.css` — o CSS. É só isto que vai para o site.
- `demo.html` — abra no navegador para ver as variações lado a lado.

## Usando com uma classe (recomendado)

Serve para qualquer número de seções, e você muda tudo num lugar só.

1. **Elementor → Configurações → CSS personalizado** (ou o CSS do tema filho):
   cole o conteúdo de `luz-fundo.css`.
2. No container, **Avançado → CSS classes**: `b360-luz b360-luz--topo`
3. Ainda em **Avançado**:
   - **Posição** → `Relativo`
   - **Overflow** → `Oculto` ← sem isto a luz vaza e cria barra de rolagem lateral
4. O container precisa de um fundo escuro, senão não há o que iluminar.

### Variações

| Classe | O que faz |
|---|---|
| `b360-luz--topo` | como no Figma, luz nascendo na borda de cima |
| `b360-luz--centro` | halo no meio do container |
| `b360-luz--canto` | luz entrando pelo canto superior esquerdo |
| `b360-luz--dupla` | soma um segundo foco no canto oposto |
| `b360-luz--suave` / `--forte` | menos / mais intensidade |
| `b360-luz--azul` `--gelo` `--verde` `--roxo` | cor da luz |
| `b360-luz--pulsa` | respiro lento de 9s (opcional) |

Combine à vontade: `b360-luz b360-luz--topo b360-luz--dupla b360-luz--suave`.

## Usando só num container (aba CSS personalizado do próprio widget)

Se preferir não mexer no CSS global, cole isto no **CSS personalizado do
container** — aí `selector` já aponta para ele:

```css
selector {
  position: relative;
  overflow: hidden;
  isolation: isolate;
}

selector::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 4%;
  width: 125%;
  height: 185%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 0;
  background: radial-gradient(ellipse 50% 50% at 50% 50%,
    #dce7f5            0%,
    rgba(143,182,228,.70) 14%,
    rgba(143,182,228,.40) 26%,
    rgba(143,182,228,.20) 40%,
    rgba(143,182,228,.09) 56%,
    rgba(143,182,228,.03) 74%,
    transparent          100%);
}

selector > .e-con-inner { position: relative; z-index: 1; }
```

## Sobre o código que você mandou

A ideia é a mesma, mas troquei `filter: blur(180px)` num círculo sólido por um
`radial-gradient` elíptico. O resultado na tela é praticamente o mesmo e evita
três problemas do `blur`:

- **Custo.** Um `blur(180px)` obriga o navegador a criar uma camada de
  composição e a borrar uma superfície enorme a cada repintura. Com uma ou
  duas seções passa; com seis, o scroll no celular começa a engasgar. O
  gradiente é desenhado direto, sem camada extra.
- **Corte nas bordas.** O `blur` amostra pixels de fora do elemento, então a
  luz costuma ficar com a borda “cortada” contra o limite do container. O
  gradiente já nasce com o degradê pronto.
- **Barra de rolagem.** Um círculo de 600px posicionado em `right: 0` estoura
  a largura da página se o container não tiver `overflow: hidden` — é a causa
  mais comum de rolagem lateral no celular.

Dois detalhes do seu trecho que valem corrigir de qualquer jeito, se você
mantiver a versão com `blur`: o `left: inherit` junto com `right: 0` no
`::after` é contraditório (o `left` herdado ganha e o `right` é ignorado em
elemento de largura fixa), e o container precisa de `position: relative`,
senão o `::before` se ancora no ancestral posicionado mais próximo e a luz
aparece na seção errada.

O ajuste fino fica todo nas variáveis do topo do arquivo: `--luz-cor`,
`--luz-nucleo`, `--luz-forca`, `--luz-l`, `--luz-a`, `--luz-x`, `--luz-y`.
