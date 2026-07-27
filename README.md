# Otimização de performance — terapeuta360.ntsinapse.com.br

Regra que guiou tudo: **rastreamento nunca é atrasado, deferido ou removido.**
O único container permitido no HTML é `GTM-N87JBK4`.

## Instalação

Copie o arquivo para o servidor:

```
wp-content/mu-plugins/nts-performance.php
```

É um *must-use plugin*: ativa sozinho, não aparece na lista de plugins e não
pode ser desativado por engano. Se a pasta `mu-plugins` não existir, crie-a.

Para testar uma página sem as otimizações, adicione `?nts_nopt=1` na URL.

## O que o plugin faz

**Rastreamento**
- `preconnect` para `googletagmanager.com` e `google-analytics.com` — o container começa a carregar antes.
- Remove do HTML qualquer `gtm.js?id=` / `gtag/js?id=` que **não** seja `GTM-N87JBK4`, incluindo o snippet inline e o `<noscript>` de outros containers.
- Desenfileira tags de analytics duplicadas impressas por plugins (Site Kit, PixelYourSite, MonsterInsights, Analytify, GTM4WP).
- Nenhum script de domínio de tracking recebe `defer` ou delay. A lista de domínios protegidos está em `nts_tracking_hosts()`.

**JavaScript**
- `defer` nos scripts de tema/plugins — mas só nos que não têm inline `before`/`after`/`localize`, para não quebrar ordem de execução.
- jQuery e jQuery core ficam de fora do defer de propósito.
- `jquery-migrate` removido das dependências.
- Terceiros pesados que **não** são tracking (chat, mapas, reCAPTCHA, widgets de review, Elfsight, Zendesk…) só carregam na primeira interação, com fallback de 5s após o `load`. Lista editável em `nts_delayed_patterns()`.

**Peso da página**
- Emojis (JS + CSS) removidos.
- oEmbed discovery e `wp-embed.js` removidos.
- `wp-block-library`, `global-styles` e `classic-theme-styles` desenfileirados (tema não usa blocos — se usar, veja "Ajustes" abaixo).
- RSD, WLW manifest, shortlink, generator removidos do `<head>`.

**LCP / imagens**
- Primeira imagem do conteúdo: `fetchpriority="high"`, `loading="eager"`, `decoding="sync"`.
- Demais imagens: `loading="lazy"`, `decoding="async"`.

**TTFB**
- Heartbeat desregistrado no front-end (menos `admin-ajax.php`).
- XML-RPC e pingback desligados.

## O que NÃO dá para resolver por código — precisa ser feito no GTM

Isto é o ponto mais importante do seu print. Os IDs que aparecem lá:

```
AW-961…            gtag/js
G-N5GV3GVRK9       gtag/js
G-KNKELBJG55       gtag/js
482-603-6316       gtag/js
GTM-N87JBK4        gtm.js   ← o único que deve existir
```

Requisições `gtag/js?id=…` vindas de `googletagmanager.com` quase sempre são
**disparadas pelo próprio container GTM**, não impressas no HTML pelo WordPress.
Se for esse o caso, o plugin não as vê — elas nascem em runtime dentro do
`gtm.js`. O plugin cobre o cenário em que um plugin do WP imprime a tag; o
resto depende de uma limpeza no container:

1. Abra o GTM → container `GTM-N87JBK4` → **Tags**.
2. Procure tags do tipo *Google Tag* / *Google Analytics: GA4 Configuration* /
   *Google Ads Conversion*. Cada uma corresponde a um daqueles IDs.
3. Decida quais medições você realmente usa. Provavelmente há duas propriedades
   GA4 medindo a mesma coisa (`G-N5GV3GVRK9` e `G-KNKELBJG55`) — mantenha uma.
4. Pause/exclua as redundantes, publique uma nova versão do container.
5. Confira também **Google Site Kit** e qualquer plugin de pixel no WP-admin:
   se algum estiver com ID de GA4/Ads configurado, desligue a saída de tag dele
   (o plugin já desenfileira os handles mais comuns, mas desligar na origem é melhor).

Cada `gtag/js` a menos é uma requisição a terceiro removida do caminho crítico.

## Ajustes finos (via filtros, sem editar o arquivo)

```php
// Tema usa blocos Gutenberg no front-end:
add_filter( 'nts_remove_block_css', '__return_false' );

// Proteger outro domínio de tracking:
add_filter( 'nts_tracking_hosts', function ( $h ) { $h[] = 'meudominio.com'; return $h; } );

// Adiar outro terceiro pesado:
add_filter( 'nts_delayed_patterns', function ( $p ) { $p[] = 'algum-widget.com'; return $p; } );

// Não deferir um script problemático:
add_filter( 'nts_never_defer_handles', function ( $h ) { $h[] = 'meu-handle'; return $h; } );
```

## Itens de servidor que ainda valem muito (fora do escopo do plugin)

Estes exigem acesso ao painel de hospedagem e costumam valer mais pontos que
qualquer otimização de PHP:

- **Cache de página** (LiteSpeed Cache, WP Rocket ou cache do host). Sem isso o
  TTFB continua sendo PHP em toda visita.
- **Brotli/gzip** e `Cache-Control: max-age=31536000, immutable` para assets estáticos.
- **HTTP/2 ou HTTP/3** habilitado.
- **WebP/AVIF** nas imagens do tema e do conteúdo.
- **PHP 8.2+ com OPcache** ligado.
- **CDN** na frente do site.
- `font-display: swap` nas `@font-face` do tema, e `preload` da fonte usada no título acima da dobra.

## Verificação após instalar

1. `?nts_nopt=1` vs. URL normal — comparar o HTML.
2. GTM Preview mode: confirmar que `GTM-N87JBK4` dispara e que todas as tags
   que você quer manter continuam disparando.
3. Google Tag Assistant: conferir que os eventos de conversão ainda chegam.
4. Rodar o PageSpeed de novo em mobile.

## Limitação desta entrega

O ambiente onde este código foi escrito não tem acesso de rede ao site
(bloqueio de política: `CONNECT 403`), então **não foi possível** logar no
wp-admin, inspecionar o HTML real, ver quais plugins estão instalados nem rodar
o PageSpeed para medir antes/depois. As otimizações acima são as que se aplicam
com segurança a qualquer WordPress; a limpeza do container GTM e os itens de
servidor precisam ser feitos por quem tem acesso.
