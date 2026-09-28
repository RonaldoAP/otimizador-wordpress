/**
 * Plugin do TinyMCE: botao que insere o shortcode da landing Black 360.
 *
 * Registrado via filtro mce_external_plugins (API do editor do WordPress).
 */
( function () {
	'use strict';

	if ( 'undefined' === typeof tinymce ) {
		return;
	}

	tinymce.PluginManager.add( 'p360black360', function ( editor ) {
		editor.addButton( 'p360black360', {
			text: 'Black 360',
			icon: false,
			tooltip: 'Inserir a landing page Black 360',
			onclick: function () {
				editor.insertContent( '[black360_apresentacao]' );
			}
		} );

		editor.addMenuItem( 'p360black360', {
			text: 'Landing Black 360',
			context: 'insert',
			onclick: function () {
				editor.insertContent( '[black360_apresentacao]' );
			}
		} );
	} );
}() );
