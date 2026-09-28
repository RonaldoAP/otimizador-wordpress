/*
 * Leitor da arvore do Figma para o conversor `figma2elementor.py`.
 *
 * Roda no contexto do plugin do Figma (MCP `use_figma`, ou Plugins →
 * Development → console). Troque NODE_ID pelo no da seçao e copie o JSON
 * devolvido para um arquivo.
 *
 *     node.id do Figma:  https://figma.com/design/<fileKey>/<nome>?node-id=291-2372
 *                        -> NODE_ID = "291:2372"
 *
 * O formato de saida e o que o conversor espera: layout flexbox, estilos de
 * caixa, tipografia e conteudo de texto, preservando a hierarquia.
 */

const NODE_ID = "291:2372";

const alvo = await figma.getNodeByIdAsync(NODE_ID);
let pagina = alvo;
while (pagina && pagina.type !== "PAGE") pagina = pagina.parent;
await figma.setCurrentPageAsync(pagina);
const raiz = await figma.getNodeByIdAsync(NODE_ID);

const hex = (c) =>
  "#" + [c.r, c.g, c.b].map((v) => Math.round(v * 255).toString(16).padStart(2, "0")).join("");

function paint(p) {
  if (!p || p.visible === false) return null;
  if (p.type === "SOLID") {
    return { t: "solid", cor: hex(p.color), op: p.opacity === undefined ? 1 : Number(p.opacity.toFixed(2)) };
  }
  if (p.type && p.type.indexOf("GRADIENT") === 0) {
    return {
      t: "grad",
      tipo: p.type,
      stops: (p.gradientStops || []).map((s) => ({
        cor: hex(s.color),
        a: Number((s.color.a === undefined ? 1 : s.color.a).toFixed(2)),
        pos: Number(s.position.toFixed(2)),
      })),
    };
  }
  if (p.type === "IMAGE") return { t: "img", modo: p.scaleMode };
  return { t: p.type };
}

function padding(x) {
  return { top: x.paddingTop, right: x.paddingRight, bottom: x.paddingBottom, left: x.paddingLeft };
}

function no(x) {
  const b = x.absoluteBoundingBox;
  const o = {
    id: x.id,
    nome: x.name,
    tipo: x.type,
    w: b ? Math.round(b.width) : null,
    h: b ? Math.round(b.height) : null,
  };

  if ("layoutMode" in x && x.layoutMode !== "NONE") {
    o.flex = {
      dir: x.layoutMode,
      gap: x.itemSpacing,
      wrap: x.layoutWrap,
      pad: padding(x),
      alinha: x.counterAxisAlignItems,
      justifica: x.primaryAxisAlignItems,
      larg: x.layoutSizingHorizontal,
      alt: x.layoutSizingVertical,
    };
  } else if ("layoutMode" in x) {
    o.absoluto = true;
    if (x.parent && x.parent.absoluteBoundingBox && b) {
      o.pos = {
        x: Math.round(b.x - x.parent.absoluteBoundingBox.x),
        y: Math.round(b.y - x.parent.absoluteBoundingBox.y),
      };
    }
  }

  if ("fills" in x && Array.isArray(x.fills)) {
    const f = x.fills.map(paint).filter(Boolean);
    if (f.length) o.fundo = f;
  }
  if ("strokes" in x && Array.isArray(x.strokes) && x.strokes.length) {
    o.borda = { paints: x.strokes.map(paint).filter(Boolean), peso: x.strokeWeight };
  }
  if ("cornerRadius" in x && x.cornerRadius && x.cornerRadius !== figma.mixed) {
    o.raio = x.cornerRadius;
  }
  if ("effects" in x && Array.isArray(x.effects) && x.effects.length) {
    o.efeitos = x.effects
      .filter((e) => e.visible !== false)
      .map((e) => ({
        t: e.type,
        cor: e.color ? hex(e.color) : null,
        a: e.color && e.color.a !== undefined ? Number(e.color.a.toFixed(2)) : null,
        r: e.radius,
        off: e.offset ? { x: e.offset.x, y: e.offset.y } : null,
        sp: e.spread,
      }));
  }

  if (x.type === "TEXT") {
    const f = x.fontName;
    o.texto = {
      conteudo: x.characters,
      fonte: typeof f === "symbol" ? "MISTA" : f.family + "|" + f.style,
      tam: x.fontSize === figma.mixed ? "mista" : x.fontSize,
      lh: x.lineHeight,
      ls: x.letterSpacing,
      caixa: x.textCase,
      alinha: x.textAlignHorizontal,
      autoResize: x.textAutoResize,
    };
  }

  if ("children" in x && x.children.length) o.filhos = x.children.map(no);
  return o;
}

return no(raiz);
