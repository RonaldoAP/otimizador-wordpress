<?php
/**
 * Plugin Name: NTS Performance
 * Description: Otimizacoes de performance para o Terapeuta 360 preservando 100% do rastreamento. Mantem apenas o container GTM-N87JBK4 e nunca atrasa scripts de tracking.
 * Version:     1.0.0
 * Author:      NT Sinapse
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Unico container do Google Tag Manager permitido no HTML.
 * Qualquer outro gtm.js / gtag/js impresso na pagina e removido.
 */
if ( ! defined( 'NTS_GTM_ID' ) ) {
	define( 'NTS_GTM_ID', 'GTM-N87JBK4' );
}

/**
 * Dominios cujos scripts NUNCA podem ser adiados, deferidos ou removidos.
 * Tudo que for rastreamento entra aqui.
 */
function nts_tracking_hosts() {
	return apply_filters(
		'nts_tracking_hosts',
		array(
			'googletagmanager.com',
			'google-analytics.com',
			'analytics.google.com',
			'googleadservices.com',
			'googlesyndication.com',
			'doubleclick.net',
			'connect.facebook.net',
			'static.hotjar.com',
			'script.hotjar.com',
			'clarity.ms',
			'snap.licdn.com',
			'analytics.tiktok.com',
			'ct.pinterest.com',
		)
	);
}

function nts_is_tracking_url( $url ) {
	if ( ! $url ) {
		return false;
	}
	foreach ( nts_tracking_hosts() as $host ) {
		if ( false !== stripos( $url, $host ) ) {
			return true;
		}
	}
	return false;
}

function nts_is_optimizable_request() {
	if ( is_admin() || is_feed() || is_embed() || is_customize_preview() ) {
		return false;
	}
	if ( defined( 'DOING_AJAX' ) && DOING_AJAX ) {
		return false;
	}
	if ( defined( 'DOING_CRON' ) && DOING_CRON ) {
		return false;
	}
	if ( defined( 'REST_REQUEST' ) && REST_REQUEST ) {
		return false;
	}
	if ( isset( $_GET['elementor-preview'] ) || isset( $_GET['et_fb'] ) || isset( $_GET['nts_nopt'] ) ) {
		return false;
	}
	return true;
}

/* -------------------------------------------------------------------------
 * 1. Rastreamento: um unico container, carregado cedo e sem atraso
 * ---------------------------------------------------------------------- */

/**
 * Conexao antecipada com o GTM para o container carregar mais rapido.
 */
add_filter(
	'wp_resource_hints',
	function ( $hints, $relation ) {
		if ( 'preconnect' === $relation ) {
			$hints[] = 'https://www.googletagmanager.com';
			$hints[] = 'https://www.google-analytics.com';
		}
		return $hints;
	},
	10,
	2
);

/**
 * Desenfileira tags de analytics/ads impressas por plugins.
 * Todos esses IDs devem viver dentro do container GTM-N87JBK4, nao no HTML.
 */
add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! nts_is_optimizable_request() ) {
			return;
		}

		$duplicated = apply_filters(
			'nts_duplicate_tracking_handles',
			array(
				'google_gtagjs',                 // Site Kit / GA4 direto
				'googlesitekit-events-provider-woocommerce',
				'pys-js',                        // PixelYourSite
				'pys-public',
				'monsterinsights-frontend-script',
				'wp-analytify-frontend',
				'gtm4wp-scroll-tracking',
			)
		);

		foreach ( $duplicated as $handle ) {
			if ( wp_script_is( $handle, 'enqueued' ) || wp_script_is( $handle, 'registered' ) ) {
				wp_dequeue_script( $handle );
				wp_deregister_script( $handle );
			}
		}
	},
	9999
);

/* -------------------------------------------------------------------------
 * 2. Limpeza do <head> e de assets que nao sao usados
 * ---------------------------------------------------------------------- */

add_action(
	'init',
	function () {
		if ( ! nts_is_optimizable_request() ) {
			return;
		}

		// Emojis: ~15 KB de JS + CSS inutil em site pt-BR.
		remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
		remove_action( 'wp_print_styles', 'print_emoji_styles' );
		remove_action( 'admin_print_scripts', 'print_emoji_detection_script' );
		remove_action( 'admin_print_styles', 'print_emoji_styles' );
		remove_filter( 'the_content_feed', 'wp_staticize_emoji' );
		remove_filter( 'comment_text_rss', 'wp_staticize_emoji' );
		remove_filter( 'wp_mail', 'wp_staticize_emoji_for_email' );
		add_filter( 'emoji_svg_url', '__return_false' );
		add_filter(
			'tiny_mce_plugins',
			function ( $plugins ) {
				return is_array( $plugins ) ? array_diff( $plugins, array( 'wpemoji' ) ) : $plugins;
			}
		);

		// Metadados sem uso publico.
		remove_action( 'wp_head', 'rsd_link' );
		remove_action( 'wp_head', 'wlwmanifest_link' );
		remove_action( 'wp_head', 'wp_shortlink_wp_head' );
		remove_action( 'wp_head', 'wp_generator' );
		remove_action( 'wp_head', 'adjacent_posts_rel_link_wp_head' );

		// oEmbed: JS de discovery que nunca e usado em landing page.
		remove_action( 'wp_head', 'wp_oembed_add_discovery_links' );
		remove_action( 'wp_head', 'wp_oembed_add_host_js' );
		add_filter( 'embed_oembed_discover', '__return_false' );
	},
	20
);

/**
 * jQuery Migrate: so serve para compatibilidade com codigo antigo.
 */
add_action(
	'wp_default_scripts',
	function ( $scripts ) {
		if ( is_admin() || empty( $scripts->registered['jquery'] ) ) {
			return;
		}
		$scripts->registered['jquery']->deps = array_diff(
			$scripts->registered['jquery']->deps,
			array( 'jquery-migrate' )
		);
	}
);

/**
 * CSS do editor de blocos em tema que nao usa blocos.
 */
add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! nts_is_optimizable_request() || ! apply_filters( 'nts_remove_block_css', true ) ) {
			return;
		}
		wp_dequeue_style( 'wp-block-library' );
		wp_dequeue_style( 'wp-block-library-theme' );
		wp_dequeue_style( 'global-styles' );
		wp_dequeue_style( 'classic-theme-styles' );
	},
	100
);

/* -------------------------------------------------------------------------
 * 3. JavaScript: defer para o que e seguro, tracking sempre intocado
 * ---------------------------------------------------------------------- */

/**
 * Adiciona defer aos scripts do tema/plugins que nao tem inline dependente.
 * Scripts de tracking e handles criticos ficam de fora.
 */
add_filter(
	'script_loader_tag',
	function ( $tag, $handle, $src ) {
		if ( ! nts_is_optimizable_request() ) {
			return $tag;
		}

		// Regra numero um: rastreamento nunca e adiado.
		if ( nts_is_tracking_url( $src ) ) {
			return $tag;
		}

		$never_defer = apply_filters(
			'nts_never_defer_handles',
			array( 'jquery-core', 'jquery', 'jquery-migrate' )
		);
		if ( in_array( $handle, $never_defer, true ) ) {
			return $tag;
		}

		if ( false !== strpos( $tag, ' defer' ) || false !== strpos( $tag, ' async' ) ) {
			return $tag;
		}

		// Se o handle tem inline before/after ou wp_localize_script, defer quebra a ordem.
		$wp_scripts = wp_scripts();
		if ( isset( $wp_scripts->registered[ $handle ] ) ) {
			$item = $wp_scripts->registered[ $handle ];
			if ( ! empty( $item->extra['before'] ) || ! empty( $item->extra['after'] ) || ! empty( $item->extra['data'] ) ) {
				return $tag;
			}
		}

		return str_replace( ' src=', ' defer src=', $tag );
	},
	10,
	3
);

/**
 * Terceiros pesados que NAO sao tracking (chat, mapas, video, widgets):
 * carregam apenas na primeira interacao do usuario.
 */
function nts_delayed_patterns() {
	return apply_filters(
		'nts_delayed_patterns',
		array(
			'tawk.to',
			'crisp.chat',
			'wa.me',
			'widget.getbutton',
			'maps.googleapis.com',
			'recaptcha',
			'disqus.com',
			'addthis.com',
			'sharethis.com',
			'trustindex.io',
			'elfsight.com',
			'zendesk',
			'intercom',
		)
	);
}

/* -------------------------------------------------------------------------
 * 4. Imagens e iframes
 * ---------------------------------------------------------------------- */

/**
 * LCP: a primeira imagem do conteudo nao pode ser lazy e deve ter prioridade alta.
 */
add_filter(
	'wp_get_attachment_image_attributes',
	function ( $attr ) {
		static $first = true;
		if ( ! nts_is_optimizable_request() ) {
			return $attr;
		}
		if ( $first ) {
			$first          = false;
			$attr['loading']       = 'eager';
			$attr['fetchpriority'] = 'high';
			$attr['decoding']      = 'sync';
		} else {
			$attr['loading']  = isset( $attr['loading'] ) ? $attr['loading'] : 'lazy';
			$attr['decoding'] = 'async';
		}
		return $attr;
	},
	20
);

/* -------------------------------------------------------------------------
 * 5. Reducao de carga no servidor (TTFB)
 * ---------------------------------------------------------------------- */

// Heartbeat: de 15s para 120s no front-end (menos admin-ajax.php).
add_filter(
	'heartbeat_settings',
	function ( $settings ) {
		$settings['interval'] = 120;
		return $settings;
	}
);

add_action(
	'init',
	function () {
		if ( is_admin() ) {
			return;
		}
		wp_deregister_script( 'heartbeat' );
	},
	1
);

// XML-RPC / pingback: vetor de carga sem uso no site.
add_filter( 'xmlrpc_enabled', '__return_false' );
add_filter(
	'wp_headers',
	function ( $headers ) {
		unset( $headers['X-Pingback'] );
		return $headers;
	}
);

/* -------------------------------------------------------------------------
 * 6. Filtro de saida: um unico GTM + delay dos terceiros nao-tracking
 * ---------------------------------------------------------------------- */

/**
 * Remove qualquer script do googletagmanager cujo id nao seja NTS_GTM_ID.
 * Cobre gtm.js?id=GTM-XXXX e gtag/js?id=G-XXXX / AW-XXXX / DC-XXXX.
 */
function nts_strip_extra_tracking( $html ) {
	$allowed = NTS_GTM_ID;

	// <script src="...googletagmanager.com/(gtm|gtag)/js?id=XXX">
	$html = preg_replace_callback(
		'#<script\b[^>]*\bsrc=["\'][^"\']*googletagmanager\.com/(?:gtm\.js|gtag/js)\?[^"\']*id=([^"\'&]+)[^"\']*["\'][^>]*>\s*</script>#is',
		function ( $m ) use ( $allowed ) {
			return ( $m[1] === $allowed ) ? $m[0] : '';
		},
		$html
	);

	// Snippet inline do GTM de outros containers.
	$html = preg_replace_callback(
		'#<script\b[^>]*>(?:(?!</script>).)*?GTM-[A-Z0-9]+(?:(?!</script>).)*?</script>#is',
		function ( $m ) use ( $allowed ) {
			return ( false !== strpos( $m[0], $allowed ) ) ? $m[0] : '';
		},
		$html
	);

	// <noscript> de outros containers.
	$html = preg_replace_callback(
		'#<noscript>\s*<iframe[^>]*googletagmanager\.com/ns\.html\?id=([^"\'&]+)[^>]*>\s*</iframe>\s*</noscript>#is',
		function ( $m ) use ( $allowed ) {
			return ( $m[1] === $allowed ) ? $m[0] : '';
		},
		$html
	);

	return $html;
}

/**
 * Converte scripts de terceiros nao-tracking em carregamento sob interacao.
 */
function nts_delay_third_party( $html ) {
	$patterns = nts_delayed_patterns();
	if ( empty( $patterns ) ) {
		return $html;
	}

	$found = false;

	$html = preg_replace_callback(
		'#<script\b([^>]*\bsrc=["\']([^"\']+)["\'][^>]*)>\s*</script>#i',
		function ( $m ) use ( $patterns, &$found ) {
			$src = $m[2];

			if ( nts_is_tracking_url( $src ) ) {
				return $m[0];
			}

			foreach ( $patterns as $needle ) {
				if ( false !== stripos( $src, $needle ) ) {
					$found = true;
					$attrs = preg_replace( '#\bsrc=#i', 'data-nts-src=', $m[1] );
					$attrs = preg_replace( '#\btype=["\'][^"\']*["\']#i', '', $attrs );
					return '<script type="text/nts-delayed"' . $attrs . '></script>';
				}
			}

			return $m[0];
		},
		$html
	);

	if ( ! $found ) {
		return $html;
	}

	$loader = <<<'JS'
<script id="nts-delay-loader">
(function(){
  var done=false;
  var events=['mousemove','touchstart','keydown','scroll','wheel','click'];
  function run(){
    if(done){return;} done=true;
    events.forEach(function(e){window.removeEventListener(e,run,{passive:true});});
    document.querySelectorAll('script[type="text/nts-delayed"]').forEach(function(old){
      var s=document.createElement('script');
      for(var i=0;i<old.attributes.length;i++){
        var a=old.attributes[i];
        if(a.name==='type'){continue;}
        s.setAttribute(a.name==='data-nts-src'?'src':a.name,a.value);
      }
      old.parentNode.replaceChild(s,old);
    });
  }
  events.forEach(function(e){window.addEventListener(e,run,{passive:true});});
  // Rede de seguranca: se ninguem interagir, carrega depois do load.
  window.addEventListener('load',function(){setTimeout(run,5000);});
})();
</script>
JS;

	return str_replace( '</body>', $loader . '</body>', $html );
}

/**
 * Buffer da pagina inteira.
 */
add_action(
	'template_redirect',
	function () {
		if ( ! nts_is_optimizable_request() ) {
			return;
		}

		ob_start(
			function ( $html ) {
				if ( '' === trim( $html ) || false === stripos( $html, '</html>' ) ) {
					return $html;
				}
				$html = nts_strip_extra_tracking( $html );
				$html = nts_delay_third_party( $html );
				return $html;
			}
		);
	},
	1
);
