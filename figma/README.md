# LP VENDAS — página de venda da BLACK 360 (Figma)

Página construída direto no Figma, no arquivo
[Power 360](https://www.figma.com/design/IaGTZRWjKUszVD4lAmlAQl/Power-360),
página **LP VENDAS** (`node-id=243-6`), no frame `LP VENDAS` — ao lado da
`LP CAPTURA` (`node-id=243-7`), que serviu de referência de identidade.

Conteúdo vindo da copy `BLACK 360 ADRIEL ETAPA 1 PARA ALUNOS.docx`.

## Estrutura (1920 px, auto-layout vertical)

| Seção | Origem |
| --- | --- |
| DOBRA 1 · HERO | hero da LP CAPTURA clonada, textos novos |
| DOBRA 2 · PROVA SOCIAL | nova — 3 cards com placeholder de foto |
| DOBRA 3 · O PROBLEMA | nova — 5 cards de fala |
| DOBRA 4 · O MECANISMO | nova — 3 manchetes (placeholder) + bloco de texto |
| DOBRA 5 · A SOLUÇÃO | nova + carrossel de logos e grid das 4 habilidades reaproveitados |
| DOBRA 7 · O QUE ESTÁ DENTRO | 9 cards de treinamento e card de bônus reaproveitados + card novo "Arsenal Magnético" |
| DOBRA 8 · A OFERTA | nova — stack de valores, preço, CTA, garantia, prints |
| DOBRA 9 · QUEM SOU EU | seção do Adriel reaproveitada + 3 números |
| DOBRA 10 · FAQ E CTA FINAL | nova — 11 perguntas, CTA e contatos |
| footer | reaproveitado |

## Tokens (lidos da LP CAPTURA)

| Token | Valor |
| --- | --- |
| Fundo | `#111111` · card `#080808` |
| Off white | `#F2EDEB` |
| Azul | `#488BD1` · claro `#B0D0F0` |
| Navy | `#162B44` |
| Borda dos cards | gradiente `rgba(255,255,255,.6)` → `rgba(137,188,240,.3)`, 1 px |
| Sombra dos cards | `0 7px 3.5px rgba(0,0,0,.45)` |
| Sombra interna do botão | `inset 0 3.49px 17.4px rgba(98,153,209,.9)` |

## Fontes — pendência

Cutta e Gotham são licenciadas e ficam instaladas localmente, então não
existem no ambiente onde a página foi montada. Os textos **novos** saíram em
Montserrat (stand-in geométrico do Gotham), seguindo esta convenção:

| Montserrat | Deve virar |
| --- | --- |
| Bold / SemiBold | Cutta (Bold / Medium) |
| Regular / Light | Gotham (Book / Light) |

Os textos **reaproveitados** da LP CAPTURA já estão nas fontes certas.

Para trocar, com Cutta e Gotham ativas na sua máquina, rode o script abaixo
(Figma → Plugins → Development → console, ou via MCP):

```js
const MAPA = {
  "Bold":      {family: "Cutta",  style: "Bold"},
  "SemiBold":  {family: "Cutta",  style: "Medium"},
  "Regular":   {family: "Gotham", style: "Book"},
  "Light":     {family: "Gotham", style: "Light"}
};

const frame = await figma.getNodeByIdAsync("246:2"); // LP VENDAS
for (const destino of Object.values(MAPA)) await figma.loadFontAsync(destino);

let trocados = 0;
for (const t of frame.findAllWithCriteria({types: ["TEXT"]})) {
  const f = t.fontName;
  if (typeof f === "symbol" || f.family !== "Montserrat") continue;
  const destino = MAPA[f.style];
  if (!destino) continue;
  await figma.loadFontAsync(f);
  t.fontName = destino;
  trocados++;
}
return {trocados};
```

Se algum texto ficar com fonte mista, o `getStyledTextSegments(['fontName'])`
resolve por segmento — mas aqui todos os textos novos foram criados com uma
fonte só.

## Placeholders a preencher

- Dobra 2: fotos dos palcos (Thiago Nigro — autorização pendente, Ícaro de
  Carvalho, Minotauro).
- Dobra 4: prints e links das 3 manchetes.
- Dobra 7: capa do Arsenal Magnético.
- Dobra 8: 6 prints de resultado (3 de carreira, depois 3 de apresentação).

## A conferir na copy

- Logos da dobra 5: manter só as empresas que foram in-company de fato.
- Preço: o documento traz `R$X 1297,00` e `R$ [8.055,90]` entre marcadores —
  a página usa R$ 1.297,00, 12x R$ 142,16 e total R$ 8.055,90.
- Prazo: o hero da LP CAPTURA falava em 28 de outubro; o FAQ da copy nova
  fala em 15/12. A página de venda segue 15/12.
