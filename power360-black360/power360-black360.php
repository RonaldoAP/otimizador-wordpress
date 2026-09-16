<?php
/**
 * Plugin Name: Power 360 - Landing Black 360
 * Plugin URI:  https://powerppt.com.br/
 * Description: Landing page "Apresentacao" (Escola Black 360) como shortcode [black360_apresentacao], com botao proprio no editor (TinyMCE + Quicktags) e template de pagina.
 * Version:     1.0.0
 * Author:      Power 360
 * Text Domain: power360-black360
 *
 * Compativel com WordPress 4.2.2 (editor classico / TinyMCE 4) e PHP 5.2+.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'P360_B360_VERSION', '1.0.0' );
define( 'P360_B360_FILE', __FILE__ );
define( 'P360_B360_DIR', plugin_dir_path( __FILE__ ) );
define( 'P360_B360_URL', plugin_dir_url( __FILE__ ) );

require_once P360_B360_DIR . 'includes/data.php';
require_once P360_B360_DIR . 'includes/class-p360-assets.php';
require_once P360_B360_DIR . 'includes/class-p360-shortcode.php';
require_once P360_B360_DIR . 'includes/class-p360-editor.php';
require_once P360_B360_DIR . 'includes/class-p360-template.php';

/**
 * Inicializa o plugin.
 */
function p360_b360_init() {
	P360_B360_Assets::init();
	P360_B360_Shortcode::init();
	P360_B360_Editor::init();
	P360_B360_Template::init();

	load_plugin_textdomain( 'power360-black360', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}
add_action( 'plugins_loaded', 'p360_b360_init' );
