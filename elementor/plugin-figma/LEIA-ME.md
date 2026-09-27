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
4. Clique em **Baixar** — o `.json` vai para a pasta de downloads
5. WordPress → **Modelos → Modelos salvos → Importar**

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
