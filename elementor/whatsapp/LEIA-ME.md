# Botão flutuante do WhatsApp

Arquivo: `botao-whatsapp.html`

Cole o bloco inteiro num **widget HTML do Elementor**. Pode ser no rodapé ou
em qualquer ponto da página — ele usa `position: fixed` e vai sozinho para o
canto inferior direito da tela, acompanhando a rolagem.

Para aparecer em todas as páginas de uma vez, o melhor lugar é o **rodapé do
tema** (Elementor → Modelos → Construtor de temas → Rodapé). Num widget solto
dentro de uma página ele só existe naquela página.

## O que ele faz

Ao clicar, abre o WhatsApp **já com a mensagem escrita** na caixa de texto,
pronta para a pessoa só apertar enviar:

> Quero mais informações da Black

No celular abre o aplicativo; no computador, o WhatsApp Web. É o link oficial
`wa.me`, que funciona sem cadastro nem API.

- Ícone verde no canto inferior direito, com uma onda pulsando por trás.
- No computador, um balão "Fale com a gente" aparece ao passar o mouse.
- No celular o balão some (não existe hover) e o botão fica um pouco menor.
- Respeita a faixa de gestos do iPhone (`safe-area-inset`).
- Não sai na impressão da página.
- `z-index` bem alto, para ficar acima de pop-up e barra de cookie.

## Trocar número ou mensagem

No começo do `<script>`:

```js
var NUMERO = "5511922264029";                       // só dígitos, com o 55
var MENSAGEM = "Quero mais informações da Black";
var ATRASO = 900;                                   // ms até o botão surgir
```

A mensagem vai em texto normal — o código cuida de codificar acento e espaço
para a URL. O número é **só dígitos**: código do país (55), DDD e o número,
sem `+`, espaço, parênteses ou hífen. O atual é o +55 11 92226-4029.

## Aparência

No CSS, no topo da regra `.b360-zap`:

| Variável | O quê |
|---|---|
| `--zap-verde` | cor do botão |
| `--zap-tamanho` | diâmetro do círculo |
| `--zap-margem` | distância das bordas da tela |

Para trocar o texto do balão, edite direto no HTML, em `.b360-zap-balao`.
Para tirar o balão, apague aquela linha. Para tirar a onda pulsando, apague a
regra `.b360-zap-icone::before`.

## Se o botão ficar escondido atrás de algo

Alguns temas e plugins usam `z-index` altíssimo. O botão já está em
2147483000; se ainda assim algo cobrir, o problema é o outro elemento estar
num contexto de empilhamento por cima — nesse caso mova o bloco para o rodapé
do tema, que fica no fim do `body`.
