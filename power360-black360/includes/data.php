<?php
/**
 * Conteudo da landing page.
 *
 * Todo o texto/estrutura vem daqui para que a edicao nao exija mexer no HTML.
 * Os filtros permitem sobrescrever o conteudo a partir do tema.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * URL de um asset de imagem do plugin.
 *
 * @param string $file Nome do arquivo dentro de assets/img/.
 * @return string
 */
function p360_b360_img( $file ) {
	return P360_B360_URL . 'assets/img/' . $file;
}

/**
 * Textos globais (hero, CTAs, footer).
 *
 * @return array
 */
function p360_b360_get_content() {
	$content = array(
		'cta_label' => 'QUERO ENTRAR NO GRUPO',
		'cta_url'   => '#inscricao',
		'cta_note'  => '28 DE OUTUBRO - 20H - AO VIVO',

		'brand_top'    => 'ESCOLA',
		'brand_strong' => 'BLACK',
		'brand_light'  => '360',

		'hero_title_1'    => 'Apresentações, IA, comunicação, networking e posicionamento.',
		'hero_title_2'    => 'Tudo em uma única escola',
		'hero_text_1'     => 'No dia 28 de setembro, o Adriel vai abrir a Escola Power 360 completa: 10 treinamentos,',
		'hero_text_2'     => 'acesso vitalício e uma condição especial só para alunos.',
		'hero_text_3'     => 'Quem estiver no grupo vai receber a oferta primeiro.',

		'pilares_title_1' => 'Apresentação é um dos pilares, mas para subir de nível',
		'pilares_title_2' => 'é preciso usar ela de forma 360 na sua carreira:',

		'recebe_title'   => 'Você recebe:',
		'recebe_text_1'  => 'Dez treinamentos. Acesso vitalício. Paga uma vez e é seu.',
		'recebe_text_2'  => 'Sem mensalidade, sem renovação, sem data para acabar.',

		'marcas_title_1' => 'A Black 360 é para ser',
		'marcas_title_2' => 'a melhor forma de ter a habilidade',
		'marcas_title_3' => 'que as',
		'marcas_title_4' => 'grandes marcas valorizam',

		'adriel_title' => 'Quem é o Adriel?',
		'adriel_text'  => 'Ele começou montando apresentação na empresa em que trabalhava como analista e hoje treina as maiores empresas do país. A minha missão é ajudar você a criar uma apresentação estratégica, inovadora, e muito acima da média, é fazer com que você impressione o seu público por onde passar, independente de qual seja sua área de atuação. Eu sou o fundador da PowerPPT, mas antes de chegar até aqui. Foram quase 12 anos de experiência profissional no mercado corporativo, atuei nas maiores empresas de comunicação do país (Editora Abril e TV Globo) e sempre me destaquei pelas habilidades de comunicação e apresentações inovadoras. Sou Formado em Marketing e Pós-graduado em Gestão de Projetos pela USP. Tenho experiências de estudo e trabalho nos Estados Unidos e Argentina.' . "\n\n" . 'Durante toda minha trajetória me aprofundei em Design, Storytelling e comunicação e coloquei todo esse conhecimento dentro de uma metodologia que já ajudou milhares de pessoas. E agora, eu quero compartilhar todo esse conhecimento com você.',

		'footer_text' => 'Todos direitos reservados',
	);

	return apply_filters( 'p360_b360_content', $content );
}

/**
 * Cards da secao de pilares (grid 2x2).
 *
 * @return array
 */
function p360_b360_get_pilares() {
	$pilares = array(
		'Fazer a apresentação é uma habilidade.',
		'Defender a sua ideia para seu chefe ou lider é outra.',
		'Conhecer as pessoas certas sem parecer que você quer tirar proveito é outra.',
		'E ser lembrado quando você não está na sala é outra.',
	);

	return apply_filters( 'p360_b360_pilares', $pilares );
}

/**
 * Treinamentos ("Voce recebe").
 *
 * Cada item: title, image, alt, badge, lead (negrito), text, variant (a|b).
 *
 * @return array
 */
function p360_b360_get_treinamentos() {
	$treinamentos = array(
		array(
			'title'   => 'Método POWER',
			'image'   => 'capa-metodo-power.png',
			'alt'     => 'Capa do treinamento Método POWER',
			'badge'   => '',
			'lead'    => 'Formação completa em apresentações, desde o planejamento do conteúdo, narrativas de storytelling, ao design e à entrega.',
			'text'    => 'A metodologia principal da Power, aprovada pelo MEC e totalmente regravada este ano.',
			'variant' => 'a',
		),
		array(
			'title'   => 'IA Apresentações 2.0',
			'image'   => 'apresentacao-ia.png',
			'alt'     => 'Capa do treinamento IA Apresentações 2.0',
			'badge'   => '',
			'lead'    => 'Aprenda a usar IA para criar apresentações mais rápido sem cair no resultado genérico.',
			'text'    => 'Como usar as melhores ferramentas de IA para criar estrutura do conteúdo com storytelling, insumos para apresentação, imagens para criação visual, e até mesmo apresentações inteiras, mas com método para manter qualidade, personalidade e controle do resultado final.',
			'variant' => 'a',
		),
		array(
			'title'   => 'Apresentações Express',
			'image'   => 'apresentacoes-express.png',
			'alt'     => 'Capa do treinamento Apresentações Express',
			'badge'   => '',
			'lead'    => 'Para quando você precisa criar uma boa apresentação em pouco tempo.',
			'text'    => 'Um processo para sair do zero e chegar a uma apresentação pronta em cerca de uma hora.',
			'variant' => 'a',
		),
		array(
			'title'   => 'Mecanismos de uma Apresentação de Sucesso',
			'image'   => 'mecanismos.png',
			'alt'     => 'Capa do treinamento Mecanismos de uma Apresentação de Sucesso',
			'badge'   => '',
			'lead'    => '',
			'text'    => 'A caixa-preta das Palestras aberta: por que alguns pitch’s do Shark Tank fecham parcerias, o que faz o Steve Jobs prender a atenção de uma plateia inteira por horas, como foram montadas as apresentações do Thiago Nigro e do Ícaro de Carvalho. Você enxerga o mecanismo que se repete, reconhece e começa a aplicar nas suas apresentações.',
			'variant' => 'a',
		),
		array(
			'title'   => 'Bússola da Criatividade',
			'image'   => 'bussola.png',
			'alt'     => 'Capa do treinamento Bússola da Criatividade',
			'badge'   => '',
			'lead'    => '',
			'text'    => 'Para a hora em que você encara a tela em branco e pensa "eu não sou criativo". Ao contrário do que muita gente pensa, a criatividade pode sim ser desenvolvida através de um método.',
			'variant' => 'a',
		),
		array(
			'title'   => 'Networking',
			'image'   => 'networking.png',
			'alt'     => 'Capa do treinamento Networking',
			'badge'   => 'NOVO',
			'lead'    => 'Aprenda a construir relações profissionais que geram acesso e oportunidades.',
			'text'    => 'Como se aproximar das pessoas certas, manter contato e criar uma rede de forma natural, sem ser interesseiro.',
			'variant' => 'b',
		),
		array(
			'title'   => 'Branding Pessoal e Posicionamento',
			'image'   => 'posicionamento.png',
			'alt'     => 'Capa do treinamento Branding Pessoal e Posicionamento',
			'badge'   => 'NOVO',
			'lead'    => 'Saia de “mais um bom profissional” para alguém com uma posição clara no seu trabalho.',
			'text'    => 'Um treinamento para definir seu posicionamento, fortalecer sua reputação e aumentar o valor percebido do seu trabalho.',
			'variant' => 'b',
		),
		array(
			'title'   => 'Comunicação de Poder',
			'image'   => 'comunica.png',
			'alt'     => 'Capa do treinamento Comunicação de Poder',
			'badge'   => 'NOVO',
			'lead'    => 'Não basta ter uma boa apresentação se você não consegue sustentar a mensagem ao falar.',
			'text'    => 'Oratória, comunicação verbal e não verbal para apresentar ideias com mais clareza e segurança, responder a perguntas difíceis, lidar com imprevistos e manter o controle da apresentação mesmo quando algo não sai como o planejado.',
			'variant' => 'b',
		),
		array(
			'title'   => 'Novo treinamento',
			'image'   => 'capa-metodo-power.png',
			'alt'     => 'Capa do novo treinamento',
			'badge'   => 'NOVO',
			'lead'    => 'Como transformar esse conhecimento em conteúdo para as redes sociais, que gera visibilidade e oportunidade profissional.',
			'text'    => 'Como eu faço hoje com a Power.',
			'variant' => 'b',
		),
	);

	return apply_filters( 'p360_b360_treinamentos', $treinamentos );
}

/**
 * Card de bonus (imagem borrada / conteudo velado).
 *
 * @return array
 */
function p360_b360_get_bonus() {
	$bonus = array(
		'title' => '+ Bônus surpresa',
		'image' => 'alavanca.png',
		'alt'   => 'Bônus surpresa',
		'lead'  => 'Tem um bônus que não vai ser vendido depois, em lugar nenhum. Ele é sobre transformar tudo isso em dinheiro no seu bolso.',
		'text'  => 'O que é exatamente, eu vou contar ao vivo no dia 28.',
	);

	return apply_filters( 'p360_b360_bonus', $bonus );
}

/**
 * Logos do carrossel de marcas.
 *
 * @return array
 */
function p360_b360_get_logos() {
	$logos = array(
		array( 'file' => 'logo-hughes.svg', 'alt' => 'Hughes', 'w' => 220 ),
		array( 'file' => 'logo-sebrae.svg', 'alt' => 'Sebrae', 'w' => 126 ),
		array( 'file' => 'logo-globo.svg', 'alt' => 'Globo', 'w' => 74 ),
		array( 'file' => 'logo-cargill.svg', 'alt' => 'Cargill', 'w' => 166 ),
		array( 'file' => 'logo-eletrobras.svg', 'alt' => 'Eletrobras', 'w' => 220 ),
		array( 'file' => 'logo-saint-gobain.svg', 'alt' => 'Saint-Gobain', 'w' => 119 ),
		array( 'file' => 'logo-novo-nordisk.svg', 'alt' => 'Novo Nordisk', 'w' => 101 ),
		array( 'file' => 'logo-tedx.svg', 'alt' => 'TEDx', 'w' => 198 ),
		array( 'file' => 'logo-sbm-offshore.svg', 'alt' => 'SBM Offshore', 'w' => 139 ),
		array( 'file' => 'logo-fs.svg', 'alt' => 'FS', 'w' => 146 ),
		array( 'file' => 'logo-rpc.svg', 'alt' => 'RPC', 'w' => 156 ),
		array( 'file' => 'logo-pfizer.svg', 'alt' => 'Pfizer', 'w' => 181 ),
		array( 'file' => 'logo-suzano.svg', 'alt' => 'Suzano', 'w' => 220 ),
		array( 'file' => 'logo-banco-do-brasil.svg', 'alt' => 'Banco do Brasil', 'w' => 220 ),
		array( 'file' => 'logo-senai.svg', 'alt' => 'Senai', 'w' => 220 ),
		array( 'file' => 'logo-rede-bahia.svg', 'alt' => 'Rede Bahia', 'w' => 220 ),
		array( 'file' => 'logo-equatorial.svg', 'alt' => 'Equatorial', 'w' => 220 ),
		array( 'file' => 'logo-bauducco.svg', 'alt' => 'Bauducco', 'w' => 214 ),
		array( 'file' => 'logo-banco-bv.svg', 'alt' => 'Banco BV', 'w' => 107 ),
		array( 'file' => 'logo-vivo.svg', 'alt' => 'Vivo', 'w' => 220 ),
		array( 'file' => 'logo-bayer.svg', 'alt' => 'Bayer', 'w' => 74 ),
		array( 'file' => 'logo-taua.svg', 'alt' => 'Tauá', 'w' => 149 ),
		array( 'file' => 'logo-cni.svg', 'alt' => 'CNI', 'w' => 220 ),
		array( 'file' => 'logo-copacol.svg', 'alt' => 'Copacol', 'w' => 220 ),
		array( 'file' => 'logo-accor.svg', 'alt' => 'Accor', 'w' => 212 ),
		array( 'file' => 'logo-sicoob.svg', 'alt' => 'Sicoob', 'w' => 220 ),
		array( 'file' => 'logo-envista.svg', 'alt' => 'Envista', 'w' => 220 ),
		array( 'file' => 'logo-orica.svg', 'alt' => 'Orica', 'w' => 220 ),
	);

	return apply_filters( 'p360_b360_logos', $logos );
}
