<?php
/**
 * Shortcode [black360_apresentacao].
 *
 * Usa a Shortcode API do WordPress, o que torna a landing compativel com o
 * editor classico (o conteudo do post guarda apenas o shortcode).
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class P360_B360_Shortcode {

	/**
	 * Registra o shortcode.
	 */
	public static function init() {
		add_shortcode( 'black360_apresentacao', array( __CLASS__, 'render' ) );
	}

	/**
	 * Renderiza a landing.
	 *
	 * @param array  $atts    Atributos do shortcode.
	 * @param string $content Conteudo interno (nao usado).
	 * @return string
	 */
	public static function render( $atts, $content = '' ) {
		$atts = shortcode_atts(
			array(
				'cta_url'   => '',
				'cta_label' => '',
				'cta_note'  => '',
				'secoes'    => 'hero,pilares,treinamentos,bonus,cta,marcas,adriel,footer',
			),
			$atts,
			'black360_apresentacao'
		);

		$dados = p360_b360_get_content();

		if ( '' !== $atts['cta_url'] ) {
			$dados['cta_url'] = $atts['cta_url'];
		}
		if ( '' !== $atts['cta_label'] ) {
			$dados['cta_label'] = $atts['cta_label'];
		}
		if ( '' !== $atts['cta_note'] ) {
			$dados['cta_note'] = $atts['cta_note'];
		}

		$secoes = array_filter( array_map( 'trim', explode( ',', $atts['secoes'] ) ) );

		P360_B360_Assets::enqueue();

		$template = apply_filters(
			'p360_b360_template',
			P360_B360_DIR . 'templates/black360-apresentacao.php'
		);

		if ( ! file_exists( $template ) ) {
			return '';
		}

		ob_start();
		include $template;
		$html = ob_get_clean();

		P360_B360_Assets::rendered( true );

		return $html;
	}
}
