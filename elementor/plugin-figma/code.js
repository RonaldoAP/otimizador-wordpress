/* =========================================================================
 * Figma para Elementor — plugin do Figma
 *
 * Ajuste as constantes abaixo, rode o plugin e clique em "Baixar".
 * O arquivo .json vai para a sua pasta de downloads, pronto para importar em
 * WordPress → Modelos → Modelos salvos → Importar.
 * ========================================================================= */

// Deixe NODE_ID vazio ("") para converter o frame que estiver selecionado.
const NODE_ID = "291:2368";

// "fluido" = responsivo, seções empilham (recomendado)
// "exato"  = tudo em posição absoluta, idêntico em 1920, sem responsividade
const MODO = "fluido";

const BASE_URL = "https://adrielaraujo.com.br/wp-content/uploads/black360";
const LARGURA_CONTEUDO = 1140;
const TITULO = "LP VENDAS · Black 360";
const ARQUIVO = "lp-vendas-black360.json";

// Exportacao das imagens. O JSON referencia a mesma extensao escolhida aqui.
const EXPORTAR_IMAGENS = true;
const FORMATO_IMG = "PNG";
const ESCALA_IMG = 2;        // 2x para retina
const LARGURA_MAX = 1600;    // no mais largo que isso sai em 1x
const LADO_MAX_ARTE = 360;   // acima disso, arte vetorial nao colapsa em 1 imagem

/* --------------------------------------------------------------- estado */

figma.showUI(__html__, { width: 460, height: 420 });

const avisos = [];
const arquivos = new Set();
const paraExportar = [];  // { nome, no }
let nContainer = 0, nWidget = 0;

/* --------------------------------------------------------------- helpers */


const HEX16 = "0123456789abcdef";
function uid() {
  let s = "";
  for (let i = 0; i < 7; i++) s += HEX16[Math.floor(Math.random() * 16)];
  return s;
}
const num = (v) => typeof v === "number" && isFinite(v);
const r0 = (v) => (num(v) ? Math.round(v) : 0);
const r2 = (v) => (num(v) ? Math.round(v * 100) / 100 : 0);
const px = (size, unit) => ({ unit: unit || "px", size: size, sizes: [] });
const dim = (t, r, b, l) => ({
  unit: "px", top: String(r0(t)), right: String(r0(r)),
  bottom: String(r0(b)), left: String(r0(l)), isLinked: false,
});
function gapCtl(v) {
  const n = r0(v);
  return { column: String(n), row: String(n), isLinked: true, unit: "px", size: n };
}
const hex = (c) =>
  "#" + [c.r, c.g, c.b].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");
function rgba(c, alpha) {
  const a = alpha === undefined ? 1 : alpha;
  if (a >= 0.999) return hex(c);
  return "rgba(" + Math.round(c.r * 255) + "," + Math.round(c.g * 255) + "," +
         Math.round(c.b * 255) + "," + r2(a) + ")";
}

const DIRECAO = { VERTICAL: "column", HORIZONTAL: "row" };
const ALINHA = { MIN: "flex-start", CENTER: "center", MAX: "flex-end", BASELINE: "baseline" };
const JUSTIFICA = { MIN: "flex-start", CENTER: "center", MAX: "flex-end", SPACE_BETWEEN: "space-between" };
const WIDGETS = {
  heading: "heading", text: "text-editor", image: "image", button: "button",
  icon: "icon", carousel: "image-carousel", video: "video",
  divider: "divider", spacer: "spacer",
};
const VET = ["VECTOR", "BOOLEAN_OPERATION", "STAR", "LINE", "POLYGON"];

function papel(nome) {
  const m = /^(sec|box|row|col|w|bg|img|cls|hide)\/\s*([^\s·]*)/i.exec((nome || "").trim());
  return m ? { tipo: m[1].toLowerCase(), detalhe: (m[2] || "").toLowerCase() } : { tipo: null, detalhe: "" };
}
function soVetor(x) {
  if (VET.indexOf(x.type) >= 0) return true;
  if ((x.type === "GROUP" || x.type === "FRAME") && x.children && x.children.length)
    return x.children.every(soVetor);
  return false;
}
function ehImagem(x) {
  return "fills" in x && Array.isArray(x.fills) &&
         x.fills.some((f) => f.type === "IMAGE" && f.visible !== false);
}
function ehArteVetorial(x) {
  // Logo com microtexto dentro (o do Sebrae, por exemplo) tem texto e por isso
  // não colapsa pela regra normal — e sairia como uma imagem por path.
  // Se há vetor e nenhum texto de corpo legível, é arte: vira uma imagem só.
  if (!("children" in x) || !x.children.length) return false;
  // Só vale para arte pequena — logo, ícone, selo. Uma grade de logos inteira
  // não pode virar uma imagem só, senão o carrossel perde os slides.
  const larg = (x.absoluteBoundingBox && x.absoluteBoundingBox.width) || x.width || 0;
  const alt = (x.absoluteBoundingBox && x.absoluteBoundingBox.height) || x.height || 0;
  if (larg > LADO_MAX_ARTE || alt > LADO_MAX_ARTE) return false;
  if (papel(x.name).detalhe === "carousel") return false;
  let vetor = false, textoDeVerdade = false;
  (function anda(n) {
    for (const c of n.children || []) {
      if (VET.indexOf(c.type) >= 0) vetor = true;
      if (c.type === "TEXT" && (typeof c.fontSize !== "number" || c.fontSize >= 12))
        textoDeVerdade = true;
      if ("children" in c) anda(c);
    }
  })(x);
  return vetor && !textoDeVerdade;
}

function temTexto(x) {
  if (x.type === "TEXT") return true;
  if (!("children" in x)) return false;
  return x.children.some(temTexto);
}
function ehAbsoluto(x) {
  const p = x.parent;
  const paiAuto = p && "layoutMode" in p && p.layoutMode !== "NONE";
  return !paiAuto || x.layoutPositioning === "ABSOLUTE";
}

/* ------------------------------------------------------------- estilos */

function corDoPaint(p) {
  if (!p || p.visible === false) return null;
  if (p.type === "SOLID") return rgba(p.color, p.opacity);
  return null;
}
function fundo(x) {
  const s = {};
  if (!("fills" in x) || !Array.isArray(x.fills)) return s;
  const vis = x.fills.filter((f) => f.visible !== false);
  const grad = vis.find((f) => f.type && f.type.indexOf("GRADIENT") === 0);
  const solido = vis.find((f) => f.type === "SOLID");
  const imagem = vis.find((f) => f.type === "IMAGE");

  if (grad) {
    const st = grad.gradientStops || [];
    if (st.length >= 2) {
      const a = st[0], b = st[st.length - 1];
      s.background_background = "gradient";
      s.background_color = rgba(a.color, a.color.a);
      s.background_color_stop = px(Math.round(a.position * 100), "%");
      s.background_color_b = rgba(b.color, b.color.a);
      s.background_color_b_stop = px(Math.round(b.position * 100), "%");
      s.background_gradient_type = "linear";
      s.background_gradient_angle = px(180, "deg");
    }
  } else if (solido) {
    s.background_background = "classic";
    s.background_color = corDoPaint(solido);
  } else if (imagem) {
    s.background_background = "classic";
    s.background_image = { url: BASE_URL + "/" + nomeArquivo(x.name, x), id: "" };
    s.background_size = imagem.scaleMode === "FIT" ? "contain" : "cover";
    s.background_position = "center center";
    s.background_repeat = "no-repeat";
  }
  return s;
}
function borda(x) {
  const s = {};
  if (!("strokes" in x) || !Array.isArray(x.strokes) || !x.strokes.length) return s;
  const vis = x.strokes.filter((k) => k.visible !== false);
  if (!vis.length) return s;
  const peso = num(x.strokeWeight) ? Math.max(1, Math.round(x.strokeWeight)) : 1;
  s.border_border = "solid";
  s.border_width = { unit: "px", top: String(peso), right: String(peso),
                     bottom: String(peso), left: String(peso), isLinked: true };
  const p = vis[0];
  if (p.type === "SOLID") {
    s.border_color = corDoPaint(p);
  } else {
    const st = p.gradientStops || [];
    if (st.length) s.border_color = rgba(st[0].color, st[0].color.a);
    avisos.push("Borda em gradiente em '" + x.name + "' virou cor sólida — aplicar a classe .b360-borda.");
  }
  return s;
}
function raio(x) {
  const s = {};
  if ("cornerRadius" in x && num(x.cornerRadius) && x.cornerRadius > 0) {
    const r = Math.round(x.cornerRadius);
    s.border_radius = { unit: "px", top: String(r), right: String(r),
                        bottom: String(r), left: String(r), isLinked: true };
  }
  return s;
}
function sombra(x) {
  const s = {};
  if (!("effects" in x) || !Array.isArray(x.effects)) return s;
  for (const e of x.effects) {
    if (e.visible === false) continue;
    if (e.type === "DROP_SHADOW" || e.type === "INNER_SHADOW") {
      s.box_shadow_box_shadow_type = "yes";
      s.box_shadow_box_shadow = {
        horizontal: r0(e.offset && e.offset.x),
        vertical: r0(e.offset && e.offset.y),
        blur: r0(e.radius),
        spread: r0(e.spread),
        color: rgba(e.color, e.color && e.color.a),
      };
      s.box_shadow_box_shadow_position = e.type === "INNER_SHADOW" ? "inset" : " ";
      break;
    }
  }
  for (const e of x.effects) {
    if (e.visible === false) continue;
    if (e.type === "LAYER_BLUR" || e.type === "BACKGROUND_BLUR") {
      avisos.push("Blur de camada em '" + x.name + "' precisa de CSS (.b360-vidro).");
      break;
    }
  }
  return s;
}
function opacidade(x) {
  return num(x.opacity) && x.opacity < 0.999 ? { _element_opacity: px(r2(x.opacity), "") } : {};
}

/* -------------------------------------------------------- posicionamento */

function posicaoAbsoluta(x) {
  const b = x.absoluteBoundingBox;
  const pb = x.parent && x.parent.absoluteBoundingBox;
  if (!b || !pb) return {};
  return {
    _position: "absolute",
    _offset_orientation_h: "start",
    _offset_x: px(r0(b.x - pb.x)),
    _offset_orientation_v: "start",
    _offset_y: px(r0(b.y - pb.y)),
    _element_width: "initial",
    _element_custom_width: px(r0(b.width)),
  };
}

function flexDoNo(x, ehRaiz) {
  const s = { container_type: "flex" };
  const p = papel(x.name);
  const auto = "layoutMode" in x && x.layoutMode !== "NONE";

  if (auto) {
    s.flex_direction = DIRECAO[x.layoutMode] || "column";
    s.flex_gap = gapCtl(x.itemSpacing);
    s.padding = dim(x.paddingTop, x.paddingRight, x.paddingBottom, x.paddingLeft);
    s.flex_align_items = ALINHA[x.counterAxisAlignItems] || "flex-start";
    s.flex_justify_content = JUSTIFICA[x.primaryAxisAlignItems] || "flex-start";
    if (x.layoutWrap === "WRAP") s.flex_wrap = "wrap";
  } else {
    s.flex_direction = "column";
  }

  // largura: o prefixo manda; sem prefixo, manda o sizing do auto layout
  if (p.tipo === "sec" || ehRaiz) {
    s.content_width = "full";
  } else if (p.tipo === "box") {
    s.content_width = "boxed";
    s.boxed_width = px(r0(x.width) || LARGURA_CONTEUDO);
  } else if (auto && x.layoutSizingHorizontal === "FILL") {
    s._flex_size = "grow";
  } else if (auto && x.layoutSizingHorizontal === "HUG") {
    s.width = { unit: "custom", size: "fit-content", sizes: [] };
  } else if (r0(x.width)) {
    s.width = px(r0(x.width));
  }

  // altura travada so em caixa sem texto: texto quebra diferente no navegador
  const alturaFixa = !auto || x.layoutSizingVertical === "FIXED";
  if (alturaFixa && r0(x.height) && !temTexto(x)) s.min_height = px(r0(x.height));

  return s;
}

/* ------------------------------------------------------------- widgets */

// Nomes que o Figma gera sozinho e não dizem nada sobre o conteúdo.
// "capa", "slide", "logo" NÃO entram aqui: são nomes de verdade no projeto.
const GENERICOS = /^(image|imagem|rectangle|ellipse|frame|group|vector|mask group|img|union|subtract|component)\b/i;
// "w/" leva junto a palavra do widget: "w/image · logo-globo" -> "logo-globo",
// "w/image" -> "". Os outros prefixos levam só o prefixo: "sec/marcas" -> "marcas".
const PREFIXO_W = /^w\/(heading|text|image|button|icon|carousel|video|divider|spacer)?\s*[·:\-]?\s*/i;
const PREFIXO = /^(sec|box|row|col|bg|img|cls|hide)\/\s*[·:\-]?\s*/i;

function nomeUtil(x) {
  // O nome da camada costuma ser generico ("w/image", "Rectangle 12"). Nesse
  // caso procura um nome de verdade: primeiro nos filhos, depois nos pais.
  const limpo = (n) =>
    (n || "").replace(PREFIXO_W, "").replace(PREFIXO, "").replace(/^[·:\-]\s*/, "").trim();
  let n = limpo(x.name);
  if (n && !GENERICOS.test(n)) return n;

  if ("children" in x) {
    const fila = x.children.slice();
    while (fila.length) {
      const c = fila.shift();
      const cn = limpo(c.name);
      if (cn && !GENERICOS.test(cn)) return cn;
      if ("children" in c) fila.push.apply(fila, c.children);
    }
  }
  let p = x.parent, salto = 0;
  while (p && salto < 3) {
    const pn = limpo(p.name);
    if (pn && !GENERICOS.test(pn)) return pn;
    p = p.parent; salto++;
  }
  return n || "imagem";
}

function nomeArquivo(bruto, no) {
  const ext = "." + FORMATO_IMG.toLowerCase();
  let n = no ? nomeUtil(no) : (bruto || "imagem");
  n = n.normalize("NFD").replace(/[̀-ͯ]/g, "");
  n = n.replace(/\.[a-z0-9]{2,4}$/i, "");
  n = n.replace(/[^\w\-]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase() || "imagem";
  let final = n + ext, i = 2;
  while (arquivos.has(final)) { final = n + "-" + i + ext; i++; }
  arquivos.add(final);
  if (no && EXPORTAR_IMAGENS) paraExportar.push({ nome: final, no: no });
  return final;
}

function widgetImagem(x) {
  nWidget++;
  const s = {
    image: { url: BASE_URL + "/" + nomeArquivo(x.name, x), id: "", alt: "", source: "library" },
    image_size: "full",
    align: "center",
  };
  if (r0(x.width)) s.width = px(r0(x.width));
  const extra = MODO === "exato" || ehAbsoluto(x) ? posicaoAbsoluta(x) : {};
  return { id: uid(), elType: "widget", widgetType: "image",
           settings: Object.assign(s, extra, opacidade(x)), elements: [] };
}

function tipografia(x) {
  const s = {};
  const f = x.fontName;
  const fam = typeof f === "symbol" ? null : f.family;
  const estilo = typeof f === "symbol" ? "" : (f.style || "").toLowerCase().replace(/\s+/g, "");
  if (typeof f === "symbol")
    avisos.push("Texto '" + x.characters.slice(0, 40) + "' tem mais de uma fonte — o template usa uma só.");

  const tam = num(x.fontSize) ? Math.round(x.fontSize) : 16;
  let peso = "400";
  const mapa = [["thin", "100"], ["extralight", "200"], ["light", "300"], ["book", "400"],
                ["regular", "400"], ["medium", "500"], ["semibold", "600"],
                ["extrabold", "800"], ["black", "900"], ["bold", "700"]];
  for (const [k, v] of mapa) if (estilo.indexOf(k) >= 0) { peso = v; break; }

  s.typography_typography = "custom";
  if (fam) s.typography_font_family = fam;
  s.typography_font_size = px(tam);
  s.typography_font_weight = peso;

  const lh = x.lineHeight;
  if (lh && lh.unit === "PERCENT") s.typography_line_height = px(r2(lh.value / 100), "em");
  else if (lh && lh.unit === "PIXELS") s.typography_line_height = px(r0(lh.value));

  const ls = x.letterSpacing;
  if (ls && num(ls.value) && Math.abs(ls.value) > 0.01) {
    s.typography_letter_spacing = ls.unit === "PERCENT" ? px(r2(tam * ls.value / 100)) : px(r2(ls.value));
  }
  if (x.textCase === "UPPER") s.typography_text_transform = "uppercase";
  return s;
}

function widgetTexto(x, forcar) {
  nWidget++;
  const conteudo = x.characters;
  const tam = num(x.fontSize) ? x.fontSize : 16;
  const nome = (x.name || "").trim();
  let ehTitulo = forcar === "heading" ||
    (forcar === undefined && (/^(h[1-6]|w\/heading|t[ií]tulo)\b/i.test(nome) ||
                              (conteudo.length < 90 && tam >= 24)));

  const fills = ("fills" in x && Array.isArray(x.fills)) ? x.fills.filter((f) => f.visible !== false) : [];
  let corTexto = "#FFFFFF";
  if (fills.length) {
    if (fills[0].type === "SOLID") corTexto = corDoPaint(fills[0]);
    else if (fills[0].gradientStops && fills[0].gradientStops.length)
      corTexto = rgba(fills[0].gradientStops[0].color, fills[0].gradientStops[0].color.a);
  }
  const alinha = (x.textAlignHorizontal || "LEFT").toLowerCase();
  const extra = MODO === "exato" || ehAbsoluto(x) ? posicaoAbsoluta(x) : {};

  if (ehTitulo) {
    const tag = tam >= 48 ? "h1" : tam >= 36 ? "h2" : tam >= 28 ? "h3" : tam >= 22 ? "h4" : "h5";
    const s = Object.assign({ title: conteudo, header_size: tag, align: alinha, title_color: corTexto },
                            tipografia(x), extra, opacidade(x));
    return { id: uid(), elType: "widget", widgetType: "heading", settings: s, elements: [] };
  }
  const s = Object.assign({ editor: "<p>" + conteudo.replace(/\n/g, "<br>") + "</p>",
                            align: alinha, text_color: corTexto },
                          tipografia(x), extra, opacidade(x));
  return { id: uid(), elType: "widget", widgetType: "text-editor", settings: s, elements: [] };
}

function widgetBotao(x) {
  nWidget++;
  let rotulo = "";
  const t = x.findAll ? x.findAll((n) => n.type === "TEXT")[0] : null;
  if (t) rotulo = t.characters;
  const s = Object.assign(
    { text: rotulo || "CLIQUE AQUI", align: "center", size: "md",
      link: { url: "#", is_external: "", nofollow: "" } },
    fundo(x), borda(x), raio(x), sombra(x),
    MODO === "exato" || ehAbsoluto(x) ? posicaoAbsoluta(x) : {}
  );
  if (t) Object.assign(s, tipografia(t), { button_text_color: "#FFFFFF" });
  return { id: uid(), elType: "widget", widgetType: "button", settings: s, elements: [] };
}

function widgetCarrossel(x) {
  nWidget++;
  const slides = [], larguras = [];
  (function junta(n) {
    if (n.children && n.children.length && !soVetor(n)) { n.children.forEach(junta); return; }
    if (n.type === "TEXT") return;
    slides.push(BASE_URL + "/" + nomeArquivo(n.name, n));
    if (r0(n.width)) larguras.push(n.width);
  })(x);

  if (!slides.length) avisos.push("Carrossel '" + x.name + "' entrou sem slides.");
  const media = larguras.length ? larguras.reduce((a, b) => a + b, 0) / larguras.length : 300;
  const porTela = Math.max(1, Math.min(slides.length || 1, Math.floor(LARGURA_CONTEUDO / Math.max(media, 1))));
  const espaco = r0(("itemSpacing" in x && num(x.itemSpacing)) ? x.itemSpacing : 20);

  const s = {
    carousel: slides.map((u) => ({ id: "", url: u })),
    image_size: "full",
    slides_to_show: String(porTela),
    slides_to_scroll: "1",
    navigation: "arrows",
    autoplay: "yes", autoplay_speed: 3000, infinite: "yes",
    pause_on_hover: "yes", speed: 600,
    image_spacing: "custom", image_spacing_custom: px(espaco),
  };
  return { id: uid(), elType: "widget", widgetType: "image-carousel", settings: s, elements: [] };
}

/* ------------------------------------------------------------ conversao */

function converte(x, ehRaiz) {
  if (x.visible === false) return null;
  const p = papel(x.name);

  if (p.tipo === "bg") {
    avisos.push("'" + x.name + "' é decorativo: virou fundo do container pai.");
    return null;
  }
  if (p.tipo === "w") {
    const wt = WIDGETS[p.detalhe];
    if (wt === "image") return widgetImagem(x);
    if (wt === "button") return widgetBotao(x);
    if (wt === "image-carousel") {
      if (temTexto(x)) {
        avisos.push("'" + x.name + "' tem texto nos slides: o Carrossel nativo só aceita imagem. " +
                    "Saiu como linha — esse caso pede Loop Carousel (Elementor Pro).");
      } else {
        return widgetCarrossel(x);
      }
    }
    if ((wt === "heading" || wt === "text-editor") && x.type === "TEXT")
      return widgetTexto(x, wt === "heading" ? "heading" : "text");
  }

  if (x.type === "TEXT") return widgetTexto(x);
  if (soVetor(x) || ehArteVetorial(x) || (ehImagem(x) && !temTexto(x))) return widgetImagem(x);

  const filhos = [];
  if ("children" in x) {
    for (const f of x.children) {
      const c = converte(f, false);
      if (c) filhos.push(c);
    }
  }
  if (!filhos.length) return null;

  nContainer++;
  const s = Object.assign(
    flexDoNo(x, ehRaiz), fundo(x), borda(x), raio(x), sombra(x), opacidade(x)
  );
  // no modo exato, ou quando o Figma posiciona em absoluto, a posicao vai junto
  if (!ehRaiz && (MODO === "exato" || ehAbsoluto(x))) {
    Object.assign(s, posicaoAbsoluta(x));
    delete s._flex_size;
  }
  return { id: uid(), elType: "container", settings: s, elements: filhos, isInner: !ehRaiz };
}


/* ---------------------------------------------------------------- saída */

async function rodar() {
  let raiz;
  if (NODE_ID) {
    const alvo = await figma.getNodeByIdAsync(NODE_ID);
    if (!alvo) throw new Error("Nó " + NODE_ID + " não encontrado neste arquivo.");
    let pagina = alvo;
    while (pagina && pagina.type !== "PAGE") pagina = pagina.parent;
    if (pagina && pagina.id !== figma.currentPage.id) await figma.setCurrentPageAsync(pagina);
    raiz = await figma.getNodeByIdAsync(NODE_ID);
  } else {
    raiz = figma.currentPage.selection[0];
    if (!raiz) throw new Error("Selecione um frame, ou preencha NODE_ID no topo do código.");
  }
  if (!("children" in raiz)) throw new Error("'" + raiz.name + "' não tem filhos para converter.");

  let conteudo;
  if (MODO === "exato") {
    const palco = converte(raiz, true);
    palco.settings.min_height = px(r0(raiz.height));
    palco.settings.content_width = "full";
    conteudo = [palco];
  } else {
    const filhos = raiz.children
      .filter((c) => c.visible !== false)
      .slice()
      .sort((a, b) => a.absoluteBoundingBox.y - b.absoluteBoundingBox.y);
    conteudo = [];
    for (const f of filhos) {
      const c = converte(f, true);
      if (!c) continue;
      for (const k of ["_position", "_offset_x", "_offset_y", "_offset_orientation_h",
                       "_offset_orientation_v", "_element_width", "_element_custom_width",
                       "_flex_size"]) delete c.settings[k];
      c.settings.content_width = c.settings.content_width || "full";
      conteudo.push(c);
    }
  }

  const template = { content: conteudo, page_settings: [], version: "0.4",
                     title: TITULO, type: "page" };
  const texto = JSON.stringify(template);

  figma.ui.postMessage({
    tipo: "pronto",
    ok: true,
    json: texto,
    arquivo: ARQUIVO,
    resumo: { modo: MODO, secoes: conteudo.length, containers: nContainer,
              widgets: nWidget, imagens: arquivos.size, tamanhoJSON: texto.length },
    avisos: Array.from(new Set(avisos)),
    totalImagens: EXPORTAR_IMAGENS ? paraExportar.length : 0,
  });

  if (EXPORTAR_IMAGENS && paraExportar.length) await exportarImagens();
}

/* ------------------------------------------------------- exportar imagens */

async function exportarImagens() {
  // Um nó pode aparecer duas vezes com nomes diferentes (imagem e fundo);
  // exporta uma vez por nome, que é o que o JSON referencia.
  let feitas = 0, erros = 0;

  for (const item of paraExportar) {
    const no = item.no;
    try {
      if (!no || typeof no.exportAsync !== "function") { erros++; continue; }

      // nó muito largo não precisa de 2x: dobraria o peso sem ganho visível
      const largura = (no.absoluteBoundingBox && no.absoluteBoundingBox.width) || no.width || 0;
      const escala = largura > LARGURA_MAX ? 1 : ESCALA_IMG;

      const bytes = await no.exportAsync({
        format: FORMATO_IMG,
        constraint: { type: "SCALE", value: escala },
      });

      figma.ui.postMessage({
        tipo: "imagem",
        nome: item.nome,
        bytes: Array.from(bytes),
        feitas: ++feitas,
        total: paraExportar.length,
      });
    } catch (e) {
      erros++;
      avisos.push("Não consegui exportar '" + item.nome + "': " + ((e && e.message) || e));
    }
  }

  figma.ui.postMessage({
    tipo: "imagens-fim",
    feitas: feitas,
    erros: erros,
    avisos: Array.from(new Set(avisos)),
  });
}

rodar().catch((e) => {
  figma.ui.postMessage({ ok: false, erro: String((e && e.message) || e) });
});
