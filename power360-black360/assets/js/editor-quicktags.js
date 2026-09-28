/**
 * Botao na aba "Texto" (Quicktags API) e no botao acima do editor.
 */
( function () {
	'use strict';

	if ( 'undefined' !== typeof QTags ) {
		QTags.addButton(
			'p360_black360',
			'Black 360',
			'[black360_apresentacao]',
			'',
			'',
			'Inserir a landing page Black 360',
			200
		);
	}

	function insert( event ) {
		var target = event.target;

		if ( ! target || ! target.className || target.className.indexOf( 'p360-b360-insert' ) === -1 ) {
			return;
		}

		event.preventDefault();

		var shortcode = target.getAttribute( 'data-shortcode' ) || '[black360_apresentacao]';
		var editorId = target.getAttribute( 'data-editor' ) || 'content';

		if ( 'undefined' !== typeof window.send_to_editor ) {
			window.send_to_editor( shortcode );
			return;
		}

		var textarea = document.getElementById( editorId );

		if ( textarea ) {
			textarea.value += shortcode;
		}
	}

	document.addEventListener( 'click', insert );
}() );
