/**
 * Power 360 - Landing Black 360 (front-end).
 *
 * Ajusta a duracao do marquee de logos conforme a largura real da faixa,
 * para que a velocidade fique constante independente da quantidade de logos.
 */
( function () {
	'use strict';

	var SPEED = 70; // pixels por segundo

	function setup( carousel ) {
		var track = carousel.querySelector( '.b360-carousel__track' );

		if ( ! track ) {
			return;
		}

		var distance = track.scrollWidth / 2;

		if ( ! distance ) {
			return;
		}

		var duration = Math.round( distance / SPEED );

		track.style.animationDuration = duration + 's';
		track.style.WebkitAnimationDuration = duration + 's';
	}

	function init() {
		var carousels = document.querySelectorAll( '[data-b360-carousel]' );

		for ( var i = 0; i < carousels.length; i++ ) {
			setup( carousels[ i ] );
		}
	}

	if ( 'loading' === document.readyState ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}

	window.addEventListener( 'resize', init );
}() );
