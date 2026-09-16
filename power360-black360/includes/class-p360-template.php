<?php
/**
 * Disponibiliza um template de pagina ("Black 360 - Landing") mesmo estando
 * dentro de um plugin.
 *
 * Em WordPress 4.2.2 o filtro `theme_page_templates` ainda nao existe
 * (chegou na 4.4), entao a lista e injetada via `page_attributes_meta_box`
 * e o arquivo e resolvido no `template_include`.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

class P360_B360_Template {

	/**
	 * Valor guardado em _wp_page_template.
	 */
	const SLUG = 'templates/page-black360.php';

	/**
	 * Registra hooks.
	 */
	public static function init() {
		add_filter( 'theme_page_templates', array( __CLASS__, 'add_template' ) );
		add_filter( 'template_include', array( __CLASS__, 'load_template' ) );
		add_action( 'add_meta_boxes_page', array( __CLASS__, 'legacy_metabox' ) );
	}

	/**
	 * Adiciona o template a lista do editor (WP 4.4+).
	 *
	 * @param array $templates Templates do tema.
	 * @return array
	 */
	public static function add_template( $templates ) {
		$templates[ self::SLUG ] = __( 'Black 360 - Landing', 'power360-black360' );

		return $templates;
	}

	/**
	 * Injeta a opcao no seletor de template em instalacoes antigas (4.2.x),
	 * onde `theme_page_templates` nao e aplicado.
	 */
	public static function legacy_metabox() {
		global $wp_version;

		if ( version_compare( $wp_version, '4.4', '>=' ) ) {
			return;
		}

		add_action( 'admin_footer-post.php', array( __CLASS__, 'legacy_metabox_script' ) );
		add_action( 'admin_footer-post-new.php', array( __CLASS__, 'legacy_metabox_script' ) );
	}

	/**
	 * Script que acrescenta a <option> ao seletor de templates.
	 */
	public static function legacy_metabox_script() {
		$post = get_post();

		if ( ! $post ) {
			return;
		}

		$current = get_post_meta( $post->ID, '_wp_page_template', true );
		?>
		<script type="text/javascript">
		( function () {
			var select = document.getElementById( 'page_template' );
			if ( ! select ) { return; }
			var option = document.createElement( 'option' );
			option.value = <?php echo wp_json_encode( self::SLUG ); ?>;
			option.text = 'Black 360 - Landing';
			if ( <?php echo wp_json_encode( (string) $current ); ?> === option.value ) {
				option.selected = true;
			}
			select.appendChild( option );
		}() );
		</script>
		<?php
	}

	/**
	 * Resolve o arquivo do template a partir do plugin.
	 *
	 * @param string $template Caminho escolhido pelo WordPress.
	 * @return string
	 */
	public static function load_template( $template ) {
		if ( ! is_singular() ) {
			return $template;
		}

		$post = get_post();

		if ( ! $post ) {
			return $template;
		}

		if ( self::SLUG !== get_post_meta( $post->ID, '_wp_page_template', true ) ) {
			return $template;
		}

		$file = P360_B360_DIR . self::SLUG;

		return file_exists( $file ) ? $file : $template;
	}
}
