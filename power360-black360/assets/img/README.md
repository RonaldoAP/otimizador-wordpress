# Assets de imagem

Os arquivos abaixo saem do Figma `Power 360` (node `203:4138`) e devem ser
exportados para esta pasta com **exatamente estes nomes**. O CSS e o PHP ja
apontam para eles.

Os caminhos `.../api/mcp/asset/6db011cb-8e12-43e0-9a12-c3be07dacc73/<id>` sao
temporarios (expiram em ~7 dias); prefira exportar direto do arquivo do Figma.

## Imagens (PNG)

| Arquivo | Origem no Figma | Tamanho no layout |
| --- | --- | --- |
| `capa-metodo-power.png` | `image` (203:4188) | 248 x 358 |
| `apresentacao-ia.png` | `APRESENTACAO 1` (203:4194) | 248 x 358 |
| `apresentacoes-express.png` | `APRESENTACAO 1` (220:6) | 248 x 358 |
| `mecanismos.png` | `d6b28dd0-...` (203:4206) | 248 x 358 |
| `bussola.png` | `BUSSOLA 2` (203:4212) | 248 x 359 |
| `networking.png` | `NETWORK 1` (220:8) | 248 x 358 |
| `posicionamento.png` | `Posicionamento` (203:4230), achatado | 248 x 358 |
| `comunica.png` | `COMUNICA 1` (220:10) | 248 x 358 |
| `alavanca.png` | `ALAVANCA 1` (220:12) | 255 x 341 |
| `adriel-retrato.png` | `FAC_0101 1` / `FAC_0108 1` (203:4559 / 203:4605) | recorte do Adriel |
| `adriel-bg.png` | `background image` (203:4552) | 1917 x 1070 |
| `hero-bg-magnific.png` | `magnific_crie-um-background...` (203:4572) | fundo do hero |
| `noise.png` | `NOISE` (203:4603) | textura, mix-blend overlay |
| `logo-avatar.png` | `magnific_remova-o-icone-central` (203:4589) | 58 x 58, circular |

## Vetores (SVG)

| Arquivo | Origem no Figma |
| --- | --- |
| `icon-sphere.svg` | `3D shapes/Sphere` (203:4149) |
| `glow-hero.svg` | `bg-hero-top` (203:4573) |
| `logo-power-footer.svg` | `svg logo` (203:4568) |

## Logos do carrossel (SVG)

`logo-hughes.svg`, `logo-sebrae.svg`, `logo-globo.svg`, `logo-cargill.svg`,
`logo-eletrobras.svg`, `logo-saint-gobain.svg`, `logo-novo-nordisk.svg`,
`logo-tedx.svg`, `logo-sbm-offshore.svg`, `logo-fs.svg`, `logo-rpc.svg`,
`logo-pfizer.svg`, `logo-suzano.svg`, `logo-banco-do-brasil.svg`,
`logo-senai.svg`, `logo-rede-bahia.svg`, `logo-equatorial.svg`,
`logo-bauducco.svg`, `logo-banco-bv.svg`, `logo-vivo.svg`, `logo-bayer.svg`,
`logo-taua.svg`, `logo-cni.svg`, `logo-copacol.svg`, `logo-accor.svg`,
`logo-sicoob.svg`, `logo-envista.svg`, `logo-orica.svg`

A lista e as larguras ficam em `includes/data.php`
(`p360_b360_get_logos()`) — para incluir/remover marcas, edite ali ou use o
filtro `p360_b360_logos`.
