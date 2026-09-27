# Plugin "Figma para Elementor"

Converte um frame do Figma em template importável do Elementor, lendo a árvore
ao vivo. Sem cópia manual no meio do caminho.

## Instalar (uma vez só)

Precisa do **Figma desktop** — no navegador não dá para rodar plugin em
desenvolvimento.

1. Menu **Plugins → Development → New plugin…**
2. Escolha **"Figma design"** e o template **"Empty"**
3. Dê um nome (ex.: `Figma para Elementor`) e escolha uma pasta para salvar

O Figma cria uma pasta com `manifest.json`, `code.js` e às vezes `ui.html`.
**É esperado.** Agora substitua o conteúdo dessa pasta pelos três arquivos
daqui — `manifest.json`, `code.js` e `ui.html` — sobrescrevendo os que o Figma
gerou.

## Usar

1. Abra `code.js` num editor e ajuste as constantes do topo:

   | Constante | O que é |
   | --- | --- |
   | `NODE_ID` | o frame a converter. Deixe `""` para usar o que estiver selecionado |
   | `MODO` | `"fluido"` (responsivo) ou `"exato"` (posição absoluta, igual em 1920) |
   | `BASE_URL` | onde as imagens vão ficar no WordPress |
   | `LARGURA_CONTEUDO` | largura da coluna boxed (padrão 1140) |

2. No Figma: **Plugins → Development → Figma para Elementor**
3. A janela mostra o resumo (seções, containers, widgets) e os avisos
4. Clique em **Baixar `.json`**
5. Espere a barra de progresso das imagens e clique em **Baixar imagens** —
   sai um `.zip` com todos os arquivos
6. Descompacte o zip em `wp-content/uploads/black360/` (ou onde o `BASE_URL`
   apontar), e importe o `.json` em WordPress → **Modelos → Modelos salvos →
   Importar**

A ordem importa: **suba as imagens antes de importar o template.** O JSON
referencia as imagens por URL; se elas não estiverem lá, a página abre vazia e
parece quebrada mesmo com o layout correto.

### Exportação das imagens

| Constante | Padrão | O que faz |
| --- | --- | --- |
| `EXPORTAR_IMAGENS` | `true` | desligue para gerar só o JSON |
| `FORMATO_IMG` | `"PNG"` | o JSON usa a mesma extensão |
| `ESCALA_IMG` | `2` | 2x para retina |
| `LARGURA_MAX` | `1600` | nó mais largo que isso sai em 1x |
| `LADO_MAX_ARTE` | `360` | acima disso, arte vetorial não vira imagem única |

Os nomes saem das camadas do Figma, com o prefixo da convenção removido:
`w/image · logo-globo` vira `logo-globo.png`. Camada com nome genérico
(`Rectangle 12`) herda o nome de um filho ou do container mais próximo. Cada
arquivo exportado é exatamente o que o JSON referencia — sem imagem órfã nem
referência quebrada.

Logo com microtexto dentro (o do Sebrae) sai como **um** arquivo, não um por
path — é o que `LADO_MAX_ARTE` controla.

Alterou o Figma? Rode o plugin de novo. Ele sempre lê o estado atual.

## Onde achar o NODE_ID

Está na URL do frame:

```
https://figma.com/design/<arquivo>/<nome>?node-id=291-2368
                                                   └──┬──┘
                                        NODE_ID = "291:2368"   (troque - por :)
```

## O que o plugin não consegue

Dois recursos não existem no painel do Elementor e saem como aviso, para serem
resolvidos pelo `bordas-gradiente.css`:

- **borda em gradiente** → vira cor sólida; aplique a classe `.b360-borda`
- **blur de camada / fundo** → aplique `.b360-vidro`

E o **Carrossel de imagens** do Elementor só aceita imagem: carrossel cujos
slides tenham texto sai como linha, e o aviso diz quais.
