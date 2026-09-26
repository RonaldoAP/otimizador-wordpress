<?php
/**
 * Markup da landing "Apresentacao" (Escola Black 360).
 *
 * Variaveis disponiveis:
 *
 * @var array $dados  Textos globais.
 * @var array $secoes Secoes habilitadas.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! isset( $dados ) ) {
	$dados = p360_b360_get_content();
}

if ( ! isset( $secoes ) || ! is_array( $secoes ) ) {
	$secoes = array( 'hero', 'pilares', 'treinamentos', 'bonus', 'cta', 'marcas', 'adriel', 'footer' );
}

$b360_cta = '<div class="b360-cta">'
	. '<a class="b360-btn" href="' . esc_url( $dados['cta_url'] ) . '">'
	. '<span class="b360-btn__label">' . esc_html( $dados['cta_label'] ) . '</span>'
	. '</a>'
	. '<p class="b360-cta__note">' . esc_html( $dados['cta_note'] ) . '</p>'
	. '</div>';
?>
<div class="b360">

	<?php if ( in_array( 'hero', $secoes, true ) ) : ?>
	<section class="b360-section b360-hero">
		<div class="b360-hero__box">
			<div class="b360-hero__bg" aria-hidden="true">
				<span class="b360-hero__bg-photo"></span>
				<span class="b360-hero__bg-glow"></span>
				<span class="b360-hero__bg-noise"></span>
			</div>

			<div class="b360-container">
				<div class="b360-topbar">
					<div class="b360-brand">
						<span class="b360-brand__avatar"></span>
						<span class="b360-brand__text">
							<span class="b360-brand__line b360-brand__line--top"><?php echo esc_html( $dados['brand_top'] ); ?></span>
							<span class="b360-brand__line b360-brand__line--main">
								<span class="b360-brand__black"><?php echo esc_html( $dados['brand_strong'] ); ?></span>
								<span class="b360-brand__360"><?php echo esc_html( $dados['brand_light'] ); ?></span>
							</span>
						</span>
					</div>

					<a class="b360-btn b360-topbar__btn" href="<?php echo esc_url( $dados['cta_url'] ); ?>">
						<span class="b360-btn__label"><?php echo esc_html( $dados['cta_label'] ); ?></span>
					</a>
				</div>

				<div class="b360-hero__content">
					<h1 class="b360-hero__title">
						<span><?php echo esc_html( $dados['hero_title_1'] ); ?></span>
						<span class="b360-grad"><?php echo esc_html( $dados['hero_title_2'] ); ?></span>
					</h1>

					<p class="b360-hero__text">
						<?php echo esc_html( $dados['hero_text_1'] ); ?>
						<strong class="b360-grad"><?php echo esc_html( $dados['hero_text_2'] ); ?></strong>
						<?php echo esc_html( $dados['hero_text_3'] ); ?>
					</p>

					<?php echo $b360_cta; // phpcs:ignore WordPress.Security.EscapeOutput ?>
				</div>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'pilares', $secoes, true ) ) : ?>
	<section class="b360-section b360-pilares">
		<div class="b360-container b360-container--930">
			<h2 class="b360-title b360-title--40">
				<span><?php echo esc_html( $dados['pilares_title_1'] ); ?></span>
				<span class="b360-grad"><?php echo esc_html( $dados['pilares_title_2'] ); ?></span>
			</h2>

			<div class="b360-grid">
				<?php foreach ( p360_b360_get_pilares() as $b360_pilar ) : ?>
					<div class="b360-pilar">
						<div class="b360-pilar__icon">
							<img src="<?php echo esc_url( p360_b360_img( 'icon-sphere.svg' ) ); ?>" width="32" height="32" alt="" />
						</div>
						<p class="b360-pilar__text"><?php echo esc_html( $b360_pilar ); ?></p>
					</div>
				<?php endforeach; ?>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'treinamentos', $secoes, true ) || in_array( 'bonus', $secoes, true ) ) : ?>
	<section class="b360-section b360-recebe">
		<div class="b360-container b360-container--782">

			<?php if ( in_array( 'treinamentos', $secoes, true ) ) : ?>
				<header class="b360-recebe__header">
					<h2 class="b360-title b360-title--54"><?php echo esc_html( $dados['recebe_title'] ); ?></h2>
					<p class="b360-recebe__lead">
						<strong class="b360-grad"><?php echo esc_html( $dados['recebe_text_1'] ); ?></strong>
						<?php echo esc_html( $dados['recebe_text_2'] ); ?>
					</p>
				</header>

				<div class="b360-cards">
					<?php foreach ( p360_b360_get_treinamentos() as $b360_item ) : ?>
						<article class="b360-card b360-card--<?php echo esc_attr( $b360_item['variant'] ); ?>">
							<div class="b360-card__inner">
								<div class="b360-card__media">
									<img src="<?php echo esc_url( p360_b360_img( $b360_item['image'] ) ); ?>"
										width="248" height="358"
										alt="<?php echo esc_attr( $b360_item['alt'] ); ?>" />
								</div>

								<div class="b360-card__body">
									<?php if ( '' !== $b360_item['badge'] ) : ?>
										<span class="b360-badge"><?php echo esc_html( $b360_item['badge'] ); ?></span>
									<?php endif; ?>

									<h3 class="b360-card__title"><?php echo esc_html( $b360_item['title'] ); ?></h3>

									<div class="b360-card__text">
										<?php if ( '' !== $b360_item['lead'] ) : ?>
											<p><strong><?php echo esc_html( $b360_item['lead'] ); ?></strong></p>
										<?php endif; ?>
										<p><?php echo esc_html( $b360_item['text'] ); ?></p>
									</div>
								</div>
							</div>
						</article>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>

			<?php
			if ( in_array( 'bonus', $secoes, true ) ) :
				$b360_bonus = p360_b360_get_bonus();
				?>
				<article class="b360-card b360-card--b b360-card--bonus">
					<div class="b360-card__inner">
						<div class="b360-card__media">
							<img src="<?php echo esc_url( p360_b360_img( $b360_bonus['image'] ) ); ?>"
								width="255" height="341"
								alt="<?php echo esc_attr( $b360_bonus['alt'] ); ?>" />
						</div>

						<div class="b360-card__veil" aria-hidden="true"></div>

						<div class="b360-card__body">
							<h3 class="b360-card__title"><?php echo esc_html( $b360_bonus['title'] ); ?></h3>
							<div class="b360-card__text">
								<p><strong><?php echo esc_html( $b360_bonus['lead'] ); ?></strong></p>
								<p><?php echo esc_html( $b360_bonus['text'] ); ?></p>
							</div>
						</div>
					</div>
				</article>
			<?php endif; ?>

		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'cta', $secoes, true ) ) : ?>
	<section class="b360-section b360-cta-section">
		<div class="b360-container">
			<?php echo $b360_cta; // phpcs:ignore WordPress.Security.EscapeOutput ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'marcas', $secoes, true ) ) : ?>
	<section class="b360-section b360-marcas">
		<div class="b360-container b360-container--734">
			<h2 class="b360-title b360-title--40">
				<span><?php echo esc_html( $dados['marcas_title_1'] ); ?></span>
				<span class="b360-grad"><?php echo esc_html( $dados['marcas_title_2'] ); ?></span>
				<span><?php echo esc_html( $dados['marcas_title_3'] ); ?></span>
				<span class="b360-grad"><?php echo esc_html( $dados['marcas_title_4'] ); ?></span>
			</h2>
		</div>

		<div class="b360-carousel" data-b360-carousel>
			<div class="b360-carousel__track">
				<?php
				$b360_logos = p360_b360_get_logos();

				// Duas passagens para o loop infinito do marquee.
				for ( $b360_pass = 0; $b360_pass < 2; $b360_pass++ ) :
					foreach ( $b360_logos as $b360_logo ) :
						?>
						<div class="b360-carousel__item" style="width:<?php echo (int) $b360_logo['w']; ?>px">
							<img src="<?php echo esc_url( p360_b360_img( $b360_logo['file'] ) ); ?>"
								alt="<?php echo 0 === $b360_pass ? esc_attr( $b360_logo['alt'] ) : ''; ?>"
								<?php echo 0 === $b360_pass ? '' : 'aria-hidden="true"'; ?> />
						</div>
						<?php
					endforeach;
				endfor;
				?>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'adriel', $secoes, true ) ) : ?>
	<section class="b360-section b360-adriel">
		<div class="b360-adriel__bg" aria-hidden="true"></div>

		<div class="b360-container b360-container--1140">
			<div class="b360-adriel__box">
				<div class="b360-adriel__content">
					<h2 class="b360-adriel__title"><?php echo esc_html( $dados['adriel_title'] ); ?></h2>
					<div class="b360-adriel__text">
						<?php
						foreach ( preg_split( '/\n\s*\n/', $dados['adriel_text'] ) as $b360_p ) {
							echo '<p>' . esc_html( trim( $b360_p ) ) . '</p>';
						}
						?>
					</div>
				</div>

				<div class="b360-adriel__media">
					<img src="<?php echo esc_url( p360_b360_img( 'adriel-retrato.png' ) ); ?>"
						alt="<?php esc_attr_e( 'Adriel Araújo', 'power360-black360' ); ?>" />
				</div>
			</div>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( in_array( 'footer', $secoes, true ) ) : ?>
	<footer class="b360-footer">
		<div class="b360-container b360-container--1140">
			<div class="b360-footer__row">
				<img class="b360-footer__logo"
					src="<?php echo esc_url( p360_b360_img( 'logo-power-footer.svg' ) ); ?>"
					width="128" height="21"
					alt="<?php esc_attr_e( 'Power', 'power360-black360' ); ?>" />
				<p class="b360-footer__text"><?php echo esc_html( $dados['footer_text'] ); ?></p>
			</div>
		</div>
	</footer>
	<?php endif; ?>

</div>
