<?php
/**
 * Registro e carregamento condicional de CSS/JS do front-end.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class P360_B360_Assets {

	/**
	 * Marca se a landing ja foi renderizada nesta requisicao.
	 *
	 * @var bool
	 */
	protected static $rendered = false;

	/**
	 * Registra hooks.
	 */
	public static function init() {
		add_action( 'wp_enqueue_scripts', array( __CLASS__, 'register' ), 5 );
		add_action( 'wp_enqueue_scripts', array( __CLASS__, 'maybe_enqueue' ), 20 );
	}

	/**
	 * Registra (sem enfileirar) os handles.
	 */
	public static function register() {
		wp_register_style(
			'p360-black360',
			P360_B360_URL . 'assets/css/black360.css',
			array(),
			P360_B360_VERSION
		);

		wp_register_script(
			'p360-black360',
			P360_B360_URL . 'assets/js/black360.js',
			array(),
			P360_B360_VERSION,
			true
		);
	}

	/**
	 * Enfileira os assets quando a pagina atual usa o shortcode ou o template.
	 */
	public static function maybe_enqueue() {
		if ( self::is_landing() ) {
			self::enqueue();
		}
	}

	/**
	 * Enfileira de fato (tambem chamado pelo shortcode, para o caso de
	 * conteudos montados fora do loop principal).
	 */
	public static function enqueue() {
		wp_enqueue_style( 'p360-black360' );
		wp_enqueue_script( 'p360-black360' );
	}

	/**
	 * A pagina atual renderiza a landing?
	 *
	 * @return bool
	 */
	public static function is_landing() {
		if ( is_admin() ) {
			return false;
		}

		if ( is_page_template( 'templates/page-black360.php' ) ) {
			return true;
		}

		$post = get_post();

		if ( $post && has_shortcode( $post->post_content, 'black360_apresentacao' ) ) {
			return true;
		}

		return false;
	}

	/**
	 * Flag de "ja renderizado" (evita IDs duplicados se o shortcode aparecer
	 * duas vezes na mesma pagina).
	 *
	 * @param bool|null $set Define o valor quando informado.
	 * @return bool
	 */
	public static function rendered( $set = null ) {
		if ( null !== $set ) {
			self::$rendered = (bool) $set;
		}

		return self::$rendered;
	}
}
