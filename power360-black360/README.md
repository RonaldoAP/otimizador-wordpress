# Power 360 — Landing Black 360 (plugin WordPress)

Implementação da página **"Apresentação"** do Figma
[Power 360 · node `203-4138`](https://www.figma.com/design/IaGTZRWjKUszVD4lAmlAQl/Power-360?node-id=203-4138)
como plugin WordPress compatível com **WordPress 4.2.2** (editor clássico /
TinyMCE 4) e **PHP 5.2+**.

## Como é compatível com a API do editor

A página não é HTML colado no editor: ela é registrada nas APIs oficiais do
editor, então o conteúdo do post guarda apenas um shortcode.

| API do WordPress | Onde | O que faz |
| --- | --- | --- |
| Shortcode API (`add_shortcode`) | `includes/class-p360-shortcode.php` | Registra `[black360_apresentacao]` |
| `mce_external_plugins` + `mce_buttons` | `includes/class-p360-editor.php` + `assets/js/editor-plugin.js` | Botão **Black 360** na barra do editor visual e item no menu *Inserir* |
| Quicktags API (`QTags.addButton`) | `assets/js/editor-quicktags.js` | Botão equivalente na aba **Texto** |
| `media_buttons` | `includes/class-p360-editor.php` | Botão **Inserir Black 360** acima do editor |
| Page template | `includes/class-p360-template.php` + `templates/page-black360.php` | Template de página "Black 360 - Landing" (sem sidebar) |

> Em WP 4.2.2 o filtro `theme_page_templates` ainda não existe (chegou na 4.4),
> por isso a opção é injetada no seletor de templates via `admin_footer-post.php`
> e o arquivo é resolvido no `template_include`.

## Instalação

1. Copie a pasta `power360-black360/` para `wp-content/plugins/`.
2. Exporte as imagens do Figma para `assets/img/` — a lista com os nomes
   exatos está em [`assets/img/README.md`](assets/img/README.md).
3. Ative o plugin em **Plugins → Plugins instalados**.

## Uso

**Opção A — shortcode (recomendada).** Crie uma página e clique no botão
*Black 360* no editor, ou digite:

```
[black360_apresentacao]
```

Atributos opcionais:

| Atributo | Padrão | Descrição |
| --- | --- | --- |
| `cta_url` | `#inscricao` | Destino de todos os botões |
| `cta_label` | `QUERO ENTRAR NO GRUPO` | Texto dos botões |
| `cta_note` | `28 DE OUTUBRO - 20H - AO VIVO` | Linha abaixo do botão |
| `secoes` | todas | Seções a exibir, separadas por vírgula: `hero,pilares,treinamentos,bonus,cta,marcas,adriel,footer` |

Exemplo:

```
[black360_apresentacao cta_url="https://chat.whatsapp.com/xxxx" secoes="hero,pilares,treinamentos,cta"]
```

**Opção B — template de página.** Em **Atributos da página → Modelo**,
escolha **Black 360 - Landing**. Nesse caso o tema não envolve a landing
(header/footer próprios), útil quando a página deve ocupar a tela inteira.

O CSS e o JS só são carregados nas páginas que realmente usam a landing
(`has_shortcode()` / template).

## Estrutura e conteúdo

Todo o texto fica em `includes/data.php`, em arrays, com filtros para
sobrescrever a partir do tema sem tocar no plugin:

```php
add_filter( 'p360_b360_content', function ( $c ) {
	$c['cta_url'] = 'https://chat.whatsapp.com/xxxx';
	return $c;
} );

add_filter( 'p360_b360_treinamentos', 'meu_tema_treinamentos' );
add_filter( 'p360_b360_logos', 'meu_tema_logos' );
add_filter( 'p360_b360_template', 'meu_tema_template_black360' );
```

```
power360-black360/
├── power360-black360.php        # cabeçalho do plugin + bootstrap
├── includes/
│   ├── data.php                 # todo o conteúdo (textos, cards, logos)
│   ├── class-p360-assets.php    # registro/carregamento condicional de CSS e JS
│   ├── class-p360-shortcode.php # Shortcode API
│   ├── class-p360-editor.php    # TinyMCE + Quicktags + media_buttons
│   └── class-p360-template.php  # template de página
├── templates/
│   ├── black360-apresentacao.php # markup da landing (todos os contêineres)
│   └── page-black360.php         # template de página
└── assets/
    ├── css/black360.css
    ├── js/black360.js            # marquee do carrossel de marcas
    ├── js/editor-plugin.js       # botão do TinyMCE
    ├── js/editor-quicktags.js    # botão da aba Texto
    └── img/                      # exportar do Figma (ver README de lá)
```

## Fidelidade ao layout

Tokens e medidas vêm do Figma e ficam em custom properties no topo do CSS:

| Token | Valor |
| --- | --- |
| Fundo | `#111` / seção hero `#0d0b11` / card `#080808` |
| Navy | `#162b44` |
| Off White | `#f2edeb` |
| Azul | `#488bd1` · claro `#b0d0f0` |
| Bordas | `rgba(255,255,255,.6)` |

Contêineres seguem as larguras do design: hero `1880px` (raio 24px), barra
superior e seção do Adriel `1140px`, pilares `930px`, cards `782px`, título
das marcas `734px`. O card de treinamento reproduz a moldura dupla do Figma
(externa `#080808` com padding `11px 10px`, interna `0.788px` com sombra
`0 7px 3.5px rgba(0,0,0,.45)`) e a imagem de `248×358`. Os cinco primeiros
cards usam o gradiente azul no topo (`--b360-grad-card-a`) e os quatro últimos
o gradiente invertido (`--b360-grad-card-b`), como no layout.

As fontes do design (Cutta, Gotham, Herokid) são licenciadas e não
acompanham o plugin. O CSS as declara primeiro na pilha e cai para
Montserrat/Helvetica; se o tema já carregar as fontes reais, elas são usadas
automaticamente.

O layout é responsivo (breakpoints em 1180px, 960px e 720px): os cards
empilham imagem sobre texto, o grid de pilares vira uma coluna e a barra
superior vira bloco.

---

> **Nota:** a entrega principal do projeto passou a ser o template do Elementor
> em [`../elementor/`](../elementor/README.md), montado com Containers e widgets
> nativos. Este plugin (shortcode) fica mantido como alternativa para sites sem
> Elementor.
