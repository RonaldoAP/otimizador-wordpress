<?php
/**
 * Template Name: Black 360 - Landing
 *
 * Template de pagina "limpo": renderiza apenas a landing, sem sidebar,
 * mantendo wp_head()/wp_footer() para que plugins e scripts continuem
 * funcionando normalmente.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

P360_B360_Assets::enqueue();

?><!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<title><?php wp_title( '|', true, 'right' ); ?></title>
	<?php wp_head(); ?>
</head>
<body <?php body_class( 'b360-page' ); ?>>

<?php
while ( have_posts() ) :
	the_post();

	$dados  = p360_b360_get_content();
	$secoes = array( 'hero', 'pilares', 'treinamentos', 'bonus', 'cta', 'marcas', 'adriel', 'footer' );

	include P360_B360_DIR . 'templates/black360-apresentacao.php';
endwhile;
?>

<?php wp_footer(); ?>
</body>
</html>
