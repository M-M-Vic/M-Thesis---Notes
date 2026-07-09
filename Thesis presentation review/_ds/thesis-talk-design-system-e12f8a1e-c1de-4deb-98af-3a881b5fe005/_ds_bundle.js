/* @ds-bundle: {"format":4,"namespace":"ThesisTalkDesignSystem_e12f8a","components":[{"name":"Chip","sourcePath":"components/content/Chip.jsx"},{"name":"Figure","sourcePath":"components/content/Figure.jsx"},{"name":"ModelBadge","sourcePath":"components/content/ModelBadge.jsx"},{"name":"StatCallout","sourcePath":"components/content/StatCallout.jsx"},{"name":"BirthDeathChain","sourcePath":"components/math/BirthDeathChain.jsx"},{"name":"Equation","sourcePath":"components/math/Equation.jsx"},{"name":"FlowDiagram","sourcePath":"components/math/FlowDiagram.jsx"},{"name":"QueueDiagram","sourcePath":"components/math/QueueDiagram.jsx"},{"name":"TheoremBox","sourcePath":"components/math/TheoremBox.jsx"}],"sourceHashes":{"components/content/Chip.jsx":"eca0521d89f5","components/content/Figure.jsx":"8705ce148bdc","components/content/ModelBadge.jsx":"1e2f01212fad","components/content/StatCallout.jsx":"af7f43157eaa","components/math/BirthDeathChain.jsx":"d44bf677601d","components/math/Equation.jsx":"00860fcd4d47","components/math/FlowDiagram.jsx":"8908dac567de","components/math/QueueDiagram.jsx":"437bc7536c2f","components/math/TheoremBox.jsx":"22abec88fc7e"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ThesisTalkDesignSystem_e12f8a = window.ThesisTalkDesignSystem_e12f8a || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/content/Chip.jsx
try { (() => {
/**
 * Chip — a compact inline tag for a parameter, keyword or filter. The
 * "param" tone sets content in mono (for rates and symbols); other tones
 * tint with a class/mechanism hue.
 */
function Chip({
  children,
  tone = 'neutral',
  // 'neutral' | 'param' | 'class1' | 'class2' | 'jockey' | 'abandon'
  className = '',
  style = {}
}) {
  const tones = {
    neutral: {
      fg: 'var(--ink-700)',
      bg: 'var(--surface-sunken)',
      mono: false
    },
    param: {
      fg: 'var(--ink-900)',
      bg: 'var(--surface-sunken)',
      mono: true
    },
    class1: {
      fg: 'var(--terracotta-600)',
      bg: 'var(--terracotta-50)',
      mono: false
    },
    class2: {
      fg: 'var(--pine-600)',
      bg: 'var(--pine-50)',
      mono: false
    },
    jockey: {
      fg: 'var(--ochre-600)',
      bg: 'var(--ochre-50)',
      mono: false
    },
    abandon: {
      fg: 'var(--plum-600)',
      bg: 'var(--plum-50)',
      mono: false
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", {
    className: className,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      padding: '3px 10px',
      borderRadius: 'var(--radius-pill)',
      background: t.bg,
      color: t.fg,
      fontFamily: t.mono ? 'var(--font-mono)' : 'var(--font-sans)',
      fontSize: 'var(--fs-caption)',
      fontWeight: t.mono ? 'var(--fw-regular)' : 'var(--fw-medium)',
      lineHeight: 1.35,
      whiteSpace: 'nowrap',
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Chip.jsx", error: String((e && e.message) || e) }); }

// components/content/Figure.jsx
try { (() => {
/**
 * Figure — an image (typically a matplotlib result plot) with a numbered
 * caption and an optional source line. Frames research figures consistently
 * on results slides.
 */
function Figure({
  src,
  alt = '',
  number = null,
  caption = null,
  source = null,
  frame = true,
  className = '',
  style = {}
}) {
  return /*#__PURE__*/React.createElement("figure", {
    className: className,
    style: {
      margin: 0,
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-3)',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'transparent',
      border: frame ? '1px solid var(--border-subtle)' : 'none',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'none',
      padding: frame ? 'var(--space-4)' : 0,
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: alt,
    style: {
      display: 'block',
      width: '100%',
      height: 'auto',
      borderRadius: 'var(--radius-xs)'
    }
  })), (caption || number) && /*#__PURE__*/React.createElement("figcaption", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-caption)',
      color: 'var(--text-body)',
      lineHeight: 'var(--lh-normal)'
    }
  }, number != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 'var(--fw-semibold)',
      color: 'var(--text-heading)'
    }
  }, "Fig.\xA0", number, ".\xA0"), caption, source && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'block',
      marginTop: 'var(--space-1)',
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)'
    }
  }, source)));
}
Object.assign(__ds_scope, { Figure });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/Figure.jsx", error: String((e && e.message) || e) }); }

// components/content/ModelBadge.jsx
try { (() => {
/**
 * ModelBadge — the labelled tag for a model variant (A, B, B₂, C₂, Bᴴ, Cᴴ, X)
 * coloured by solution status. Use inline in prose, in overview tables, or as
 * a slide kicker. `name` accepts unicode sub/superscripts directly.
 */
function ModelBadge({
  name = 'A',
  status = 'neutral',
  // 'solved' | 'open' | 'neutral'
  mechanism = null,
  // optional short mechanism label
  active = false,
  size = 'md',
  // 'sm' | 'md'
  className = '',
  style = {}
}) {
  const palette = {
    solved: {
      fg: 'var(--pine-600)',
      bg: 'var(--pine-50)',
      dot: 'var(--status-solved)'
    },
    open: {
      fg: 'var(--terracotta-600)',
      bg: 'var(--terracotta-50)',
      dot: 'var(--status-open)'
    },
    neutral: {
      fg: 'var(--ink-700)',
      bg: 'var(--surface-sunken)',
      dot: 'var(--ink-300)'
    }
  }[status] || {};
  const pad = size === 'sm' ? '3px 9px' : '5px 12px';
  const fs = size === 'sm' ? 'var(--fs-label)' : 'var(--fs-caption)';
  return /*#__PURE__*/React.createElement("span", {
    className: className,
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 'var(--space-2)',
      padding: pad,
      borderRadius: 'var(--radius-sm)',
      background: palette.bg,
      color: palette.fg,
      border: active ? '1.5px solid currentColor' : '1px solid transparent',
      boxShadow: active ? 'var(--shadow-sm)' : 'none',
      fontFamily: 'var(--font-mono)',
      fontSize: fs,
      fontWeight: 'var(--fw-medium)',
      lineHeight: 1,
      whiteSpace: 'nowrap',
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: '50%',
      background: palette.dot,
      flex: 'none'
    }
  }), /*#__PURE__*/React.createElement("span", null, "Model\xA0", name), mechanism && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-label)',
      color: 'var(--text-muted)',
      fontWeight: 'var(--fw-regular)'
    }
  }, "\xB7 ", mechanism));
}
Object.assign(__ds_scope, { ModelBadge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/ModelBadge.jsx", error: String((e && e.message) || e) }); }

// components/content/StatCallout.jsx
try { (() => {
/**
 * StatCallout — a single headline metric with a label and optional trend.
 * Used on results slides to surface a number (mean queue length, loss
 * fraction, waiting-time ratio) with an at-a-glance change vs. baseline.
 */
function StatCallout({
  value,
  label,
  unit = null,
  trend = null,
  // 'down' | 'up' | 'flat' | null
  note = null,
  // small context line, e.g. "vs. Model A"
  accent = 'var(--accent)',
  align = 'left',
  className = '',
  style = {}
}) {
  const arrow = trend === 'down' ? '↓' : trend === 'up' ? '↑' : trend === 'flat' ? '→' : null;
  const trendColor = trend === 'down' ? 'var(--pine-600)' : trend === 'up' ? 'var(--terracotta-600)' : 'var(--text-muted)';
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 'var(--space-1)',
      textAlign: align,
      alignItems: align === 'center' ? 'center' : 'flex-start',
      paddingLeft: 'var(--space-4)',
      borderLeft: `3px solid ${accent}`,
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--fw-semibold)',
      fontSize: 'var(--fs-label)',
      letterSpacing: 'var(--ls-label)',
      textTransform: 'uppercase',
      color: 'var(--text-muted)'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 'var(--space-2)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontWeight: 'var(--fw-medium)',
      fontSize: 'var(--fs-display)',
      lineHeight: 1,
      color: 'var(--text-heading)',
      fontVariantNumeric: 'tabular-nums'
    }
  }, value), unit && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: 'var(--fs-lead)',
      color: 'var(--text-muted)'
    }
  }, unit), arrow && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-heading)',
      color: trendColor,
      fontWeight: 'var(--fw-semibold)'
    }
  }, arrow)), note && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-caption)',
      color: 'var(--text-muted)'
    }
  }, note));
}
Object.assign(__ds_scope, { StatCallout });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/content/StatCallout.jsx", error: String((e && e.message) || e) }); }

// components/math/BirthDeathChain.jsx
try { (() => {
/**
 * BirthDeathChain — a one-dimensional birth–death transition chain, the
 * canonical picture of an M/M/1-type queue. States 0,1,2,… sit in a row;
 * arrivals bow over the top (constant λ), departures bow under the bottom.
 *
 * mode="mm1":  departures are the constant μ.
 * mode="mm1m": departures grow with the number in system — μ, μ+θ, μ+2θ, …
 *              (the M/M/1+M impatience chain).
 *
 * Faithful to the balance relation shown alongside it:
 *   λ π_n = (μ + nθ) π_{n+1}.
 */
function BirthDeathChain({
  mode = 'mm1',
  lambda = 'λ',
  mu = 'μ',
  theta = 'θ',
  count = 4,
  // explicit numbered states 0..count-1, then a "⋯" node
  width = 640,
  className = '',
  style = {}
}) {
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const idUp = `bd-up-${uid}`,
    idDn = `bd-dn-${uid}`;
  const ink = 'var(--ink-900)';
  const mut = 'var(--ink-500)';
  const up = 'var(--pine-600)';
  const dn = 'var(--terracotta-600)';
  const labels = [];
  for (let i = 0; i < count; i++) labels.push(String(i));
  labels.push('⋯');
  const nGaps = labels.length - 1;

  // geometry
  const r = 21;
  const gap = 118;
  const padX = 34;
  const cy = 72;
  const H = 152;
  const W = padX * 2 + (labels.length - 1) * gap + r * 2;
  const cx = i => padX + r + i * gap;
  const downLabel = i => {
    // departure from state i+1 -> i
    if (mode !== 'mm1m') return mu;
    if (i === 0) return mu;
    return `${mu}+${i > 1 ? i : ''}${theta}`;
  };
  const arcs = [];
  for (let i = 0; i < nGaps; i++) {
    const x1 = cx(i),
      x2 = cx(i + 1);
    const mid = (x1 + x2) / 2;
    // forward (arrival) — bows up, points right
    const fs = x1 + r - 2,
      fe = x2 - r + 2;
    arcs.push(/*#__PURE__*/React.createElement("g", {
      key: `f${i}`
    }, /*#__PURE__*/React.createElement("path", {
      d: `M ${fs},${cy - 9} Q ${mid},${cy - 50} ${fe},${cy - 9}`,
      fill: "none",
      stroke: up,
      strokeWidth: "1.7",
      markerEnd: `url(#${idUp})`
    }), /*#__PURE__*/React.createElement("text", {
      x: mid,
      y: cy - 52,
      fill: up,
      fontSize: "15",
      textAnchor: "middle",
      style: {
        fontFamily: 'var(--font-mono)'
      }
    }, lambda)));
    // backward (departure) — bows down, points left
    const bs = x2 - r + 2,
      be = x1 + r - 2;
    arcs.push(/*#__PURE__*/React.createElement("g", {
      key: `b${i}`
    }, /*#__PURE__*/React.createElement("path", {
      d: `M ${bs},${cy + 9} Q ${mid},${cy + 50} ${be},${cy + 9}`,
      fill: "none",
      stroke: dn,
      strokeWidth: "1.7",
      markerEnd: `url(#${idDn})`
    }), /*#__PURE__*/React.createElement("text", {
      x: mid,
      y: cy + 63,
      fill: dn,
      fontSize: "15",
      textAnchor: "middle",
      style: {
        fontFamily: 'var(--font-mono)'
      }
    }, downLabel(i))));
  }
  return /*#__PURE__*/React.createElement("svg", {
    className: className,
    viewBox: `0 0 ${W} ${H}`,
    width: width,
    style: {
      maxWidth: '100%',
      height: 'auto',
      overflow: 'visible',
      ...style
    },
    role: "img",
    "aria-label": "Birth-death transition chain"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("marker", {
    id: idUp,
    markerUnits: "userSpaceOnUse",
    markerWidth: "11",
    markerHeight: "11",
    refX: "8.4",
    refY: "5",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L9,5 L0,9 Z",
    fill: up
  })), /*#__PURE__*/React.createElement("marker", {
    id: idDn,
    markerUnits: "userSpaceOnUse",
    markerWidth: "11",
    markerHeight: "11",
    refX: "8.4",
    refY: "5",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L9,5 L0,9 Z",
    fill: dn
  }))), arcs, labels.map((lab, i) => {
    const isDots = lab === '⋯';
    return /*#__PURE__*/React.createElement("g", {
      key: `n${i}`
    }, !isDots && /*#__PURE__*/React.createElement("circle", {
      cx: cx(i),
      cy: cy,
      r: r,
      fill: "var(--surface-card)",
      stroke: ink,
      strokeWidth: "1.7"
    }), /*#__PURE__*/React.createElement("text", {
      x: cx(i),
      y: cy + (isDots ? 2 : 1),
      fill: ink,
      fontSize: isDots ? 24 : 18,
      textAnchor: "middle",
      dominantBaseline: "middle",
      style: {
        fontFamily: isDots ? 'inherit' : 'var(--font-mono)',
        fontWeight: isDots ? 400 : 500
      }
    }, lab));
  }));
}
Object.assign(__ds_scope, { BirthDeathChain });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/math/BirthDeathChain.jsx", error: String((e && e.message) || e) }); }

// components/math/Equation.jsx
try { (() => {
/**
 * Equation — a KaTeX-rendered mathematical expression.
 *
 * Requires KaTeX to be present on the page (window.katex). Load it once
 * per document from the CDN:
 *   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
 *   <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
 * If KaTeX is missing the raw TeX is shown in a mono fallback, so the
 * component never throws.
 */
function Equation({
  tex = '',
  display = true,
  number = null,
  align = 'center',
  size = 'md',
  className = '',
  style = {}
}) {
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (!ref.current) return;
    const k = typeof window !== 'undefined' ? window.katex : null;
    if (k) {
      try {
        k.render(tex, ref.current, {
          displayMode: display,
          throwOnError: false,
          errorColor: 'var(--accent-strong)'
        });
        return;
      } catch (e) {/* fall through to raw */}
    }
    ref.current.textContent = tex;
  }, [tex, display]);
  const fontSize = {
    sm: '0.85em',
    md: '1em',
    lg: '1.35em'
  }[size] || '1em';
  const justify = align === 'left' ? 'flex-start' : align === 'right' ? 'flex-end' : 'center';
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      display: 'flex',
      alignItems: 'baseline',
      justifyContent: justify,
      gap: 'var(--space-6)',
      width: display ? '100%' : 'auto',
      color: 'var(--text-heading)',
      fontSize,
      ...style
    }
  }, /*#__PURE__*/React.createElement("span", {
    ref: ref,
    style: {
      fontFamily: 'var(--font-mono)',
      fontSize: window && window.katex ? undefined : '0.9em',
      color: 'inherit'
    }
  }), number != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontSize: 'var(--fs-caption)',
      color: 'var(--text-muted)',
      whiteSpace: 'nowrap'
    }
  }, "(", number, ")"));
}
Object.assign(__ds_scope, { Equation });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/math/Equation.jsx", error: String((e && e.message) || e) }); }

// components/math/FlowDiagram.jsx
try { (() => {
/**
 * FlowDiagram — the thesis's state-transition diagrams, faithful to the TikZ
 * sources (figures/model_c-diagram.tikz for S, figures/
 * diagram_jockeying_and_abandonments.tikz for S̃).
 *
 * space="S":      axes n₁ (→) × n₂ (↑); sample states (0,0), (n₁,0),
 *                 (n₁,n₂), (0,n₂) with their local rates, plus the idle arcs.
 * space="Stilde": axes n₂ (→) × n (↑) with the dotted diagonal n = n₂;
 *                 sample states (0,0), (0,n), (n₂,n), (n,n) and idle arcs.
 *
 * Mechanism arrows appear only when toggled: jockeying is ochre dashed,
 * abandonment plum dotted; arrivals/service are solid ink. Labels default to
 * the length-proportional rates (γ₁n₁ …); override for head-of-line variants.
 */
function FlowDiagram({
  space = 'S',
  gamma1 = false,
  gamma2 = false,
  theta1 = false,
  theta2 = false,
  gamma1Label = null,
  gamma2Label = null,
  theta1Label = null,
  theta2Label = null,
  width = 560,
  className = '',
  style = {}
}) {
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const idAh = `fd-ah-${uid}`,
    idJk = `fd-ah-jk-${uid}`,
    idAb = `fd-ah-ab-${uid}`;
  const ink = 'var(--ink-900)';
  const mut = 'var(--ink-500)';
  const jk = 'var(--mech-jockey)';
  const ab = 'var(--mech-abandon)';
  const g1L = gamma1Label || (space === 'S' ? 'γ₁n₁' : 'γ₁(n−n₂)');
  const g2L = gamma2Label || (space === 'S' ? 'γ₂n₂' : 'γ₂n₂');
  const t1L = theta1Label || (space === 'S' ? 'θ₁n₁' : 'θ₁(n−n₂)');
  const t2L = theta2Label || (space === 'S' ? 'θ₂n₂' : 'θ₂n₂');

  // arrow from (x,y) at tikz-angle deg (CCW, y-up) of length len (px)
  const arr = (x, y, deg, len, color, kind, label, lx, ly, anchor = 'middle', key) => {
    const rad = deg * Math.PI / 180;
    const x2 = x + len * Math.cos(rad);
    const y2 = y - len * Math.sin(rad);
    const dash = kind === 'dash' ? '5 4' : kind === 'dot' ? '1.5 4' : 'none';
    const mk = color === jk ? `url(#${idJk})` : color === ab ? `url(#${idAb})` : `url(#${idAh})`;
    return /*#__PURE__*/React.createElement("g", {
      key: key
    }, /*#__PURE__*/React.createElement("line", {
      x1: x,
      y1: y,
      x2: x2,
      y2: y2,
      stroke: color,
      strokeWidth: "1.6",
      strokeDasharray: dash,
      strokeLinecap: "round",
      markerEnd: mk
    }), /*#__PURE__*/React.createElement("text", {
      x: lx,
      y: ly,
      fill: color,
      fontSize: "13",
      textAnchor: anchor
    }, label));
  };
  const node = (x, y, label, lx, ly, anchor = 'middle', key) => /*#__PURE__*/React.createElement("g", {
    key: key
  }, /*#__PURE__*/React.createElement("circle", {
    cx: x,
    cy: y,
    r: "4",
    fill: ink
  }), /*#__PURE__*/React.createElement("text", {
    x: lx,
    y: ly,
    fill: ink,
    fontSize: "13.5",
    textAnchor: anchor
  }, label));
  const defs = /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("marker", {
    id: idAh,
    markerUnits: "userSpaceOnUse",
    markerWidth: "11",
    markerHeight: "11",
    refX: "8.6",
    refY: "5",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L9,5 L0,9 Z",
    fill: ink
  })), /*#__PURE__*/React.createElement("marker", {
    id: idJk,
    markerUnits: "userSpaceOnUse",
    markerWidth: "11",
    markerHeight: "11",
    refX: "8.6",
    refY: "5",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L9,5 L0,9 Z",
    fill: jk
  })), /*#__PURE__*/React.createElement("marker", {
    id: idAb,
    markerUnits: "userSpaceOnUse",
    markerWidth: "11",
    markerHeight: "11",
    refX: "8.6",
    refY: "5",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L9,5 L0,9 Z",
    fill: ab
  })));
  if (space === 'S') {
    // tikz coords: s=38 px/unit, origin at (110,360)
    const P = (tx, ty) => [110 + 38 * tx, 360 - 38 * ty];
    const [ox, oy] = P(0, 0);
    const [axx] = P(8, 0);
    const [, ayy] = P(0, 8);
    const [Ax, Ay] = P(6, 0);
    const [Bx, By] = P(6, 4);
    const [Cx, Cy] = P(0, 4);
    const L = 46;
    return /*#__PURE__*/React.createElement("svg", {
      className: className,
      viewBox: "0 0 560 440",
      width: width,
      style: {
        maxWidth: '100%',
        height: 'auto',
        fontFamily: 'var(--font-mono)',
        overflow: 'visible',
        ...style
      },
      role: "img",
      "aria-label": "State-transition diagram on S"
    }, defs, /*#__PURE__*/React.createElement("line", {
      x1: ox,
      y1: oy,
      x2: axx + 14,
      y2: oy,
      stroke: mut,
      strokeWidth: "1.3",
      markerEnd: `url(#${idAh})`
    }), /*#__PURE__*/React.createElement("line", {
      x1: ox,
      y1: oy,
      x2: ox,
      y2: ayy - 14,
      stroke: mut,
      strokeWidth: "1.3",
      markerEnd: `url(#${idAh})`
    }), /*#__PURE__*/React.createElement("text", {
      x: axx + 26,
      y: oy + 18,
      fill: mut,
      fontSize: "14",
      textAnchor: "middle"
    }, "n\u2081"), /*#__PURE__*/React.createElement("text", {
      x: ox - 22,
      y: ayy - 16,
      fill: mut,
      fontSize: "14",
      textAnchor: "middle"
    }, "n\u2082"), node(ox, oy, '(0,0)', ox + 34, oy - 12, 'middle', 'o'), arr(ox, oy, 0, L, ink, 'solid', 'λ₁', ox + L * 0.55, oy + 18, 'middle', 'o1'), arr(ox, oy, 90, L, ink, 'solid', 'λ₂', ox - 14, oy - L * 0.55, 'end', 'o2'), node(Ax, Ay, '(n₁,0)', Ax - 4, Ay + 34, 'middle', 'a'), arr(Ax, Ay, 0, L, ink, 'solid', 'λ₁', Ax + L * 0.6, Ay + 18, 'middle', 'a1'), arr(Ax, Ay, 90, L, ink, 'solid', 'λ₂', Ax + 12, Ay - L * 0.55, 'start', 'a2'), arr(Ax, Ay, 180, L, ink, 'solid', 'μ', Ax - L * 0.6, Ay + 18, 'middle', 'a3'), gamma1 && arr(Ax, Ay, 135, L, jk, 'dash', g1L, Ax - L * 0.9, Ay - L * 0.78, 'end', 'a4'), theta1 && arr(Ax, Ay - 12, 180, L, ab, 'dot', t1L, Ax - L * 0.6, Ay - 20, 'middle', 'a5'), node(Bx, By, '(n₁,n₂)', Bx - 12, By + 34, 'end', 'b'), arr(Bx, By, 0, L, ink, 'solid', 'λ₁', Bx + L * 0.6, By + 18, 'middle', 'b1'), arr(Bx, By, 90, L, ink, 'solid', 'λ₂', Bx + 12, By - L * 0.55, 'start', 'b2'), arr(Bx, By, 180, L, ink, 'solid', 'μ', Bx - L * 0.62, By + 18, 'middle', 'b3'), gamma1 && arr(Bx, By, 135, L, jk, 'dash', g1L, Bx - L * 0.9, By - L * 0.78, 'end', 'b4'), gamma2 && arr(Bx, By, -45, L, jk, 'dash', g2L, Bx + L * 0.82, By + L * 0.9, 'start', 'b5'), theta1 && arr(Bx, By - 12, 180, L, ab, 'dot', t1L, Bx - L * 0.62, By - 20, 'middle', 'b6'), theta2 && arr(Bx, By, -90, L, ab, 'dot', t2L, Bx - 9, By + L + 4, 'end', 'b7'), node(Cx, Cy, '(0,n₂)', Cx - 12, Cy - 10, 'end', 'c'), arr(Cx, Cy, 0, L, ink, 'solid', 'λ₁', Cx + L * 0.6, Cy + 18, 'middle', 'c1'), arr(Cx, Cy, 90, L, ink, 'solid', 'λ₂', Cx + 12, Cy - L * 0.55, 'start', 'c2'), arr(Cx, Cy, -90, L, ink, 'solid', 'μ', Cx - 10, Cy + 24, 'end', 'c3'), gamma2 && arr(Cx, Cy, -45, L, jk, 'dash', g2L, Cx + L * 0.82, Cy + L * 0.9, 'start', 'c4'), theta2 && arr(Cx + 12, Cy, -90, L, ab, 'dot', t2L, Cx + 16, Cy + L + 14, 'middle', 'c5'), /*#__PURE__*/React.createElement("circle", {
      cx: ox - 48,
      cy: oy + 44,
      r: "3.5",
      fill: ink
    }), /*#__PURE__*/React.createElement("text", {
      x: ox - 48,
      y: oy + 66,
      fill: ink,
      fontSize: "13",
      textAnchor: "middle"
    }, "idle"), /*#__PURE__*/React.createElement("path", {
      d: `M ${ox - 52},${oy + 36} C ${ox - 66},${oy - 10} ${ox - 40},${oy - 16} ${ox - 8},${oy - 5}`,
      fill: "none",
      stroke: ink,
      strokeWidth: "1.5",
      markerEnd: `url(#${idAh})`
    }), /*#__PURE__*/React.createElement("path", {
      d: `M ${ox - 2},${oy + 8} C ${ox - 6},${oy + 42} ${ox - 22},${oy + 50} ${ox - 40},${oy + 47}`,
      fill: "none",
      stroke: ink,
      strokeWidth: "1.5",
      markerEnd: `url(#${idAh})`
    }), /*#__PURE__*/React.createElement("text", {
      x: ox - 74,
      y: oy - 18,
      fill: ink,
      fontSize: "12.5",
      textAnchor: "middle"
    }, "\u03BB\u2081+\u03BB\u2082"), /*#__PURE__*/React.createElement("text", {
      x: ox + 16,
      y: oy + 40,
      fill: ink,
      fontSize: "12.5",
      textAnchor: "start"
    }, "\u03BC"));
  }

  // ---- space === 'Stilde' ----
  const P = (tx, ty) => [110 + 30 * tx, 380 - 30 * ty];
  const [ox, oy] = P(0, 0);
  const [axx] = P(10, 0);
  const [, ayy] = P(0, 10);
  const [Vx, Vy] = P(0, 4.6);
  const [Dx, Dy] = P(6, 6);
  const [Ux, Uy] = P(3, 9);
  const L = 38;
  return /*#__PURE__*/React.createElement("svg", {
    className: className,
    viewBox: "0 0 560 440",
    width: width,
    style: {
      maxWidth: '100%',
      height: 'auto',
      fontFamily: 'var(--font-mono)',
      overflow: 'visible',
      ...style
    },
    role: "img",
    "aria-label": "State-transition diagram on the alternative state space"
  }, defs, /*#__PURE__*/React.createElement("line", {
    x1: ox,
    y1: oy,
    x2: axx + 12,
    y2: oy,
    stroke: mut,
    strokeWidth: "1.3",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("line", {
    x1: ox,
    y1: oy,
    x2: ox,
    y2: ayy - 12,
    stroke: mut,
    strokeWidth: "1.3",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("text", {
    x: axx + 24,
    y: oy + 18,
    fill: mut,
    fontSize: "14",
    textAnchor: "middle"
  }, "n\u2082"), /*#__PURE__*/React.createElement("text", {
    x: ox - 12,
    y: ayy - 18,
    fill: mut,
    fontSize: "13.5",
    textAnchor: "end"
  }, "n = n\u2081+n\u2082"), /*#__PURE__*/React.createElement("line", {
    x1: ox,
    y1: oy,
    x2: P(10, 10)[0],
    y2: P(10, 10)[1],
    stroke: mut,
    strokeWidth: "1.2",
    strokeDasharray: "2 5",
    strokeLinecap: "round"
  }), node(ox, oy, '(0,0)', ox + 34, oy + 20, 'middle', 'o'), arr(ox, oy, 90, L, ink, 'solid', 'λ₁', ox - 13, oy - L * 0.55, 'end', 'o1'), arr(ox, oy, 45, L, ink, 'solid', 'λ₂', ox + L * 0.5 + 9, oy - L * 0.5 - 10, 'start', 'o2'), node(Vx, Vy, '(0,n)', Vx - 12, Vy + 5, 'end', 'v'), arr(Vx, Vy, 90, L, ink, 'solid', 'λ₁', Vx - 13, Vy - L * 0.55, 'end', 'v1'), arr(Vx, Vy, 45, L, ink, 'solid', 'λ₂', Vx + L * 0.5 + 9, Vy - L * 0.5 - 10, 'start', 'v2'), arr(Vx, Vy, -90, L, ink, 'solid', 'μ', Vx + 12, Vy + L * 0.72, 'start', 'v3'), gamma1 && arr(Vx, Vy, 0, L, jk, 'dash', space === 'S' ? g1L : 'γ₁n', Vx + L * 0.62, Vy - 8, 'middle', 'v4'), theta1 && arr(Vx - 11, Vy, -90, L, ab, 'dot', 'θ₁n', Vx - 22, Vy + L * 0.72, 'end', 'v5'), node(Dx, Dy, '(n,n)', Dx + 36, Dy + 20, 'middle', 'd'), arr(Dx, Dy, 90, L, ink, 'solid', 'λ₁', Dx + 10, Dy - L * 0.55, 'start', 'd1'), arr(Dx, Dy, 45, L, ink, 'solid', 'λ₂', Dx + L * 0.6 + 9, Dy - L * 0.6 - 10, 'start', 'd2'), arr(Dx, Dy, 225, L, ink, 'solid', 'μ', Dx - L * 0.5 - 12, Dy + L * 0.5 + 4, 'end', 'd3'), gamma2 && arr(Dx, Dy, 180, L, jk, 'dash', g2L === 'γ₂n₂' ? 'γ₂n' : g2L, Dx - L * 0.55, Dy - 10, 'end', 'd4'), theta2 && arr(Dx + 8, Dy - 8, 225, L, ab, 'dot', 'θ₂n', Dx - L * 0.5 + 26, Dy + L * 0.5 + 18, 'start', 'd5'), node(Ux, Uy, '(n₂,n)', Ux + 40, Uy + 20, 'middle', 'u'), arr(Ux, Uy, 90, L * 0.92, ink, 'solid', 'λ₁', Ux + 10, Uy - L * 0.5, 'start', 'u1'), arr(Ux, Uy, 45, L * 0.95, ink, 'solid', 'λ₂', Ux + L * 0.6 + 9, Uy - L * 0.6 - 8, 'start', 'u2'), arr(Ux, Uy, -90, L * 0.85, ink, 'solid', 'μ', Ux + 12, Uy + L * 0.62, 'start', 'u3'), gamma1 && arr(Ux, Uy, 0, L, jk, 'dash', g1L, Ux + L + 8, Uy + 4, 'start', 'u4'), gamma2 && arr(Ux, Uy, 180, L * 0.85, jk, 'dash', g2L, Ux - L * 0.5, Uy - 10, 'end', 'u5'), theta1 && arr(Ux - 11, Uy, -90, L * 0.85, ab, 'dot', t1L, Ux - 22, Uy + L * 0.62, 'end', 'u6'), theta2 && arr(Ux, Uy, 225, L * 0.85, ab, 'dot', t2L, Ux - L * 0.85, Uy + L * 1.15, 'end', 'u7'), /*#__PURE__*/React.createElement("circle", {
    cx: ox - 50,
    cy: oy + 38,
    r: "3.5",
    fill: ink
  }), /*#__PURE__*/React.createElement("text", {
    x: ox - 50,
    y: oy + 60,
    fill: ink,
    fontSize: "13",
    textAnchor: "middle"
  }, "idle"), /*#__PURE__*/React.createElement("path", {
    d: `M ${ox - 54},${oy + 30} C ${ox - 68},${oy - 12} ${ox - 40},${oy - 16} ${ox - 8},${oy - 5}`,
    fill: "none",
    stroke: ink,
    strokeWidth: "1.5",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("path", {
    d: `M ${ox - 2},${oy + 8} C ${ox - 8},${oy + 38} ${ox - 24},${oy + 44} ${ox - 42},${oy + 41}`,
    fill: "none",
    stroke: ink,
    strokeWidth: "1.5",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("text", {
    x: ox - 78,
    y: oy - 16,
    fill: ink,
    fontSize: "12.5",
    textAnchor: "middle"
  }, "\u03BB=\u03BB\u2081+\u03BB\u2082"), /*#__PURE__*/React.createElement("text", {
    x: ox + 14,
    y: oy + 36,
    fill: ink,
    fontSize: "12.5",
    textAnchor: "start"
  }, "\u03BC"));
}
Object.assign(__ds_scope, { FlowDiagram });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/math/FlowDiagram.jsx", error: String((e && e.message) || e) }); }

// components/math/QueueDiagram.jsx
try { (() => {
/**
 * QueueDiagram — the recurring two-class / one-server schematic of the
 * thesis: Queue 1 (priority) on top, Queue 2 below, both feeding a single
 * exponential server μ. Geometry mirrors the thesis TikZ figures
 * (figures/model-*-queue.tikz): open-sided hatched queues, straight
 * arrival/feed/departure arrows, a straight dashed jockeying arrow (1→2)
 * and a dotted class-1 abandonment arrow. Pure SVG on the palette.
 */
function QueueDiagram({
  lambda1 = 'λ₁',
  lambda2 = 'λ₂',
  mu = 'μ',
  jockey = false,
  // false | true (γ₁, straight dashed 1→2)
  jockey2 = false,
  // false | true (γ₂, straight dashed 2→1)
  abandon = false,
  // false | true (θ₁, dotted, class-1 leaves upward)
  abandon2 = false,
  // false | true (θ₂, dotted, class-2 leaves downward)
  jockeyLabel = 'γ₁',
  jockey2Label = 'γ₂',
  abandonLabel = 'θ₁',
  abandon2Label = 'θ₂',
  width = 520,
  className = '',
  style = {}
}) {
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const idAh = `qd-ah-${uid}`,
    idJk = `qd-ah-jk-${uid}`,
    idAb = `qd-ah-ab-${uid}`;
  const c1 = 'var(--class-1)';
  const c2 = 'var(--class-2)';
  const ink = 'var(--ink-900)';
  const jk = 'var(--mech-jockey)';
  const ab = 'var(--mech-abandon)';

  // hatch cell lines inside a queue rect (x 110..230)
  const hatch = (y0, y1, stroke) => {
    const lines = [];
    for (let x = 122; x <= 218; x += 12) {
      lines.push(/*#__PURE__*/React.createElement("line", {
        key: x,
        x1: x,
        y1: y0,
        x2: x,
        y2: y1,
        stroke: stroke,
        strokeWidth: "1",
        opacity: "0.45"
      }));
    }
    return lines;
  };
  return /*#__PURE__*/React.createElement("svg", {
    className: className,
    viewBox: "0 0 560 300",
    width: width,
    style: {
      maxWidth: '100%',
      height: 'auto',
      fontFamily: 'var(--font-mono)',
      overflow: 'visible',
      ...style
    },
    role: "img",
    "aria-label": "Two-class single-server queue"
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("marker", {
    id: idAh,
    markerUnits: "userSpaceOnUse",
    markerWidth: "13",
    markerHeight: "13",
    refX: "10.5",
    refY: "6",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L11,6 L0,11 Z",
    fill: ink
  })), /*#__PURE__*/React.createElement("marker", {
    id: idJk,
    markerUnits: "userSpaceOnUse",
    markerWidth: "13",
    markerHeight: "13",
    refX: "10.5",
    refY: "6",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L11,6 L0,11 Z",
    fill: jk
  })), /*#__PURE__*/React.createElement("marker", {
    id: idAb,
    markerUnits: "userSpaceOnUse",
    markerWidth: "13",
    markerHeight: "13",
    refX: "10.5",
    refY: "6",
    orient: "auto"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M0,1 L11,6 L0,11 Z",
    fill: ab
  }))), /*#__PURE__*/React.createElement("path", {
    d: "M110,70 H230 V116 H110",
    fill: "var(--terracotta-50)",
    stroke: "none"
  }), hatch(74, 112, c1), /*#__PURE__*/React.createElement("path", {
    d: "M110,70 H230 V116 H110",
    fill: "none",
    stroke: c1,
    strokeWidth: "1.75",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "44",
    y1: "93",
    x2: "103",
    y2: "93",
    stroke: ink,
    strokeWidth: "1.75",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("text", {
    x: "74",
    y: "83",
    fill: c1,
    fontSize: "16",
    textAnchor: "middle"
  }, lambda1), /*#__PURE__*/React.createElement("path", {
    d: "M110,184 H230 V230 H110",
    fill: "var(--pine-50)",
    stroke: "none"
  }), hatch(188, 226, c2), /*#__PURE__*/React.createElement("path", {
    d: "M110,184 H230 V230 H110",
    fill: "none",
    stroke: c2,
    strokeWidth: "1.75",
    strokeLinejoin: "round"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "44",
    y1: "207",
    x2: "103",
    y2: "207",
    stroke: ink,
    strokeWidth: "1.75",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("text", {
    x: "74",
    y: "197",
    fill: c2,
    fontSize: "16",
    textAnchor: "middle"
  }, lambda2), /*#__PURE__*/React.createElement("line", {
    x1: "230",
    y1: "93",
    x2: "379",
    y2: "138",
    stroke: ink,
    strokeWidth: "1.75",
    markerEnd: `url(#${idAh})`
  }), /*#__PURE__*/React.createElement("line", {
    x1: "230",
    y1: "207",
    x2: "379",
    y2: "162",
    stroke: ink,
    strokeWidth: "1.75",
    markerEnd: `url(#${idAh})`
  }), jockey && /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
    x1: jockey2 ? 150 : 170,
    y1: "120",
    x2: jockey2 ? 150 : 170,
    y2: "181",
    stroke: jk,
    strokeWidth: "1.9",
    strokeDasharray: "5 4",
    markerEnd: `url(#${idJk})`
  }), /*#__PURE__*/React.createElement("text", {
    x: jockey2 ? 138 : 158,
    y: "155",
    fill: jk,
    fontSize: "15",
    textAnchor: "end"
  }, jockeyLabel)), jockey2 && /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
    x1: jockey ? 190 : 170,
    y1: "184",
    x2: jockey ? 190 : 170,
    y2: "123",
    stroke: jk,
    strokeWidth: "1.9",
    strokeDasharray: "5 4",
    markerEnd: `url(#${idJk})`
  }), /*#__PURE__*/React.createElement("text", {
    x: jockey ? 202 : 182,
    y: "155",
    fill: jk,
    fontSize: "15",
    textAnchor: "start"
  }, jockey2Label)), abandon && /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
    x1: "170",
    y1: "66",
    x2: "170",
    y2: "23",
    stroke: ab,
    strokeWidth: "1.9",
    strokeDasharray: "1.5 4",
    strokeLinecap: "round",
    markerEnd: `url(#${idAb})`
  }), /*#__PURE__*/React.createElement("text", {
    x: "182",
    y: "34",
    fill: ab,
    fontSize: "15",
    textAnchor: "start"
  }, abandonLabel)), abandon2 && /*#__PURE__*/React.createElement("g", null, /*#__PURE__*/React.createElement("line", {
    x1: "170",
    y1: "234",
    x2: "170",
    y2: "277",
    stroke: ab,
    strokeWidth: "1.9",
    strokeDasharray: "1.5 4",
    strokeLinecap: "round",
    markerEnd: `url(#${idAb})`
  }), /*#__PURE__*/React.createElement("text", {
    x: "182",
    y: "272",
    fill: ab,
    fontSize: "15",
    textAnchor: "start"
  }, abandon2Label)), /*#__PURE__*/React.createElement("circle", {
    cx: "420",
    cy: "150",
    r: "34",
    fill: "var(--surface)",
    stroke: ink,
    strokeWidth: "1.75"
  }), /*#__PURE__*/React.createElement("text", {
    x: "420",
    y: "158",
    fill: ink,
    fontSize: "21",
    textAnchor: "middle"
  }, mu), /*#__PURE__*/React.createElement("line", {
    x1: "454",
    y1: "150",
    x2: "543",
    y2: "150",
    stroke: ink,
    strokeWidth: "1.75",
    markerEnd: `url(#${idAh})`
  }));
}
Object.assign(__ds_scope, { QueueDiagram });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/math/QueueDiagram.jsx", error: String((e && e.message) || e) }); }

// components/math/TheoremBox.jsx
try { (() => {
const KINDS = {
  theorem: {
    label: 'Theorem',
    color: 'var(--terracotta-600)',
    soft: 'var(--terracotta-50)',
    italic: false
  },
  lemma: {
    label: 'Lemma',
    color: 'var(--pine-600)',
    soft: 'var(--pine-50)',
    italic: false
  },
  corollary: {
    label: 'Corollary',
    color: 'var(--ochre-600)',
    soft: 'var(--ochre-50)',
    italic: false
  },
  definition: {
    label: 'Definition',
    color: 'var(--plum-600)',
    soft: 'var(--plum-50)',
    italic: false
  },
  remark: {
    label: 'Remark',
    color: 'var(--ink-500)',
    soft: 'var(--surface-sunken)',
    italic: false
  },
  claim: {
    label: 'Claim',
    color: 'var(--terracotta-600)',
    soft: 'var(--terracotta-50)',
    italic: false
  },
  approximation: {
    label: 'Approximation',
    color: 'var(--ochre-600)',
    soft: 'var(--ochre-50)',
    italic: false
  }
};

/**
 * TheoremBox — an amsthm-style callout (theorem / lemma / definition …)
 * with a coloured kind tag, a number and an optional title. Body content
 * is set in the display serif; drop <Equation> children inside for math.
 */
function TheoremBox({
  kind = 'theorem',
  number = null,
  title = null,
  children,
  className = '',
  style = {}
}) {
  const k = KINDS[kind] || KINDS.theorem;
  return /*#__PURE__*/React.createElement("div", {
    className: className,
    style: {
      background: 'var(--surface-card)',
      border: '1px solid var(--border-subtle)',
      borderRadius: 'var(--radius-md)',
      boxShadow: 'var(--shadow-sm)',
      overflow: 'hidden',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: 'var(--space-3)',
      padding: 'var(--space-3) var(--space-5)',
      background: k.soft,
      borderBottom: `1px solid var(--border-faint)`
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 'var(--fw-semibold)',
      fontSize: 'var(--fs-label)',
      letterSpacing: 'var(--ls-label)',
      textTransform: 'uppercase',
      color: k.color
    }
  }, k.label, number != null ? ` ${number}` : ''), title && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: 'var(--font-display)',
      fontStyle: 'italic',
      fontSize: 'var(--fs-caption)',
      color: 'var(--text-muted)'
    }
  }, title)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: 'var(--space-5)',
      fontFamily: 'var(--font-display)',
      fontSize: 'var(--fs-lead)',
      lineHeight: 'var(--lh-normal)',
      color: 'var(--text-body)'
    }
  }, children));
}
Object.assign(__ds_scope, { TheoremBox });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/math/TheoremBox.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Chip = __ds_scope.Chip;

__ds_ns.Figure = __ds_scope.Figure;

__ds_ns.ModelBadge = __ds_scope.ModelBadge;

__ds_ns.StatCallout = __ds_scope.StatCallout;

__ds_ns.BirthDeathChain = __ds_scope.BirthDeathChain;

__ds_ns.Equation = __ds_scope.Equation;

__ds_ns.FlowDiagram = __ds_scope.FlowDiagram;

__ds_ns.QueueDiagram = __ds_scope.QueueDiagram;

__ds_ns.TheoremBox = __ds_scope.TheoremBox;

})();
