<?php
/**
 * Integracao com a API do editor do WordPress (editor classico / TinyMCE 4).
 *
 * - botao na barra do TinyMCE (mce_buttons + mce_external_plugins)
 * - botao Quicktag na aba "Texto"
 * - botao acima do editor (media_buttons)
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class P360_B360_Editor {

	/**
	 * Registra hooks do admin.
	 */
	public static function init() {
		add_action( 'admin_init', array( __CLASS__, 'register_tinymce' ) );
		add_action( 'admin_enqueue_scripts', array( __CLASS__, 'quicktags' ) );
		add_action( 'media_buttons', array( __CLASS__, 'media_button' ), 20 );
	}

	/**
	 * Adiciona o plugin/botao ao TinyMCE quando o usuario pode editar e o
	 * editor visual esta habilitado.
	 */
	public static function register_tinymce() {
		if ( ! current_user_can( 'edit_posts' ) && ! current_user_can( 'edit_pages' ) ) {
			return;
		}

		if ( 'true' !== get_user_option( 'rich_editing' ) ) {
			return;
		}

		add_filter( 'mce_external_plugins', array( __CLASS__, 'mce_external_plugins' ) );
		add_filter( 'mce_buttons', array( __CLASS__, 'mce_buttons' ) );
	}

	/**
	 * Registra o arquivo do plugin TinyMCE.
	 *
	 * @param array $plugins Plugins do TinyMCE.
	 * @return array
	 */
	public static function mce_external_plugins( $plugins ) {
		$plugins['p360black360'] = P360_B360_URL . 'assets/js/editor-plugin.js?ver=' . P360_B360_VERSION;

		return $plugins;
	}

	/**
	 * Adiciona o botao a primeira linha da barra de ferramentas.
	 *
	 * @param array $buttons Botoes.
	 * @return array
	 */
	public static function mce_buttons( $buttons ) {
		$buttons[] = 'p360black360';

		return $buttons;
	}

	/**
	 * Botao equivalente na aba "Texto" (Quicktags API).
	 *
	 * @param string $hook Hook atual do admin.
	 */
	public static function quicktags( $hook ) {
		if ( ! in_array( $hook, array( 'post.php', 'post-new.php' ), true ) ) {
			return;
		}

		if ( ! wp_script_is( 'quicktags' ) ) {
			return;
		}

		wp_enqueue_script(
			'p360-black360-quicktags',
			P360_B360_URL . 'assets/js/editor-quicktags.js',
			array( 'quicktags' ),
			P360_B360_VERSION,
			true
		);
	}

	/**
	 * Botao acima do editor, util quando o TinyMCE esta desativado.
	 *
	 * @param string $editor_id ID do editor.
	 */
	public static function media_button( $editor_id ) {
		if ( 'content' !== $editor_id ) {
			return;
		}

		printf(
			'<a href="#" class="button p360-b360-insert" data-editor="%s" data-shortcode="%s">%s</a>',
			esc_attr( $editor_id ),
			esc_attr( '[black360_apresentacao]' ),
			esc_html__( 'Inserir Black 360', 'power360-black360' )
		);
	}

}
