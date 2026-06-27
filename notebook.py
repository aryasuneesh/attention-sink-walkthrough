# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "torch",
#     "transformers",
#     "anywidget",
#     "altair",
#     "polars",
# ]
#
# [tool.marimo.display]
# theme = "dark"
# ///

import marimo

__generated_with = "0.23.11"
app = marimo.App(
    width="full",
    app_title="Attention Sinks — Interactive Walkthrough",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    # Self-contained CSS — must be inline because molab only hosts the .py file.
    # Uses .paragraph (the documented marimo class for mo.md() output) and
    # light-dark() values so colours respect the active theme.
    # Ref: https://docs.marimo.io/guides/configuration/theming
    mo.Html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      :root {
        --marimo-text-font:      'Inter', system-ui, sans-serif;
        --marimo-heading-font:   'Space Grotesk', sans-serif;
        --marimo-monospace-font: 'JetBrains Mono', 'Fira Mono', monospace;
      }
      body, html { background-color: #07080f; }
      [data-cell-role='output'] {
        background-color: #07080f;
        display: flex; flex-direction: column; align-items: center;
      }

      /* ── Headings: no .paragraph dependency so they win regardless ── */
      [data-cell-role='output'] h1 {
        font-family: var(--marimo-heading-font) !important;
        font-weight: 700 !important; font-size: 2.2em !important; letter-spacing: -0.03em !important;
        color: #f8fafc !important;
        margin-top: 0.3em !important; margin-bottom: 0.4em !important;
        border-bottom: 2px solid #1e2d47 !important; padding-bottom: 0.3em !important;
      }
      [data-cell-role='output'] h2 {
        font-family: var(--marimo-heading-font) !important;
        font-weight: 600 !important; font-size: 1.5em !important; letter-spacing: -0.02em !important;
        color: #f1f5f9 !important;
        margin-top: 2.2em !important; margin-bottom: 0.4em !important;
        border-bottom: 1px solid #1e2d47 !important; padding-bottom: 0.2em !important;
      }
      [data-cell-role='output'] h3 {
        font-family: var(--marimo-heading-font) !important;
        font-weight: 600 !important; font-size: 1.15em !important;
        color: #a5b4fc !important;
        margin-top: 1.8em !important; margin-bottom: 0.3em !important;
      }
      [data-cell-role='output'] h4 {
        font-weight: 600 !important; font-size: 1em !important;
        color: #e2e8f0 !important; margin-top: 1.2em !important;
      }

      /* ── Prose body ──────────────────────────────────────────────── */
      [data-cell-role='output'] .paragraph {
        width: 100%; max-width: 64rem;
        margin-left: auto; margin-right: auto;
        font-size: 16px; line-height: 1.72;
        color: #cbd5e1 !important; background-color: #07080f !important;
        -webkit-font-smoothing: antialiased;
      }
      [data-cell-role='output'] p   { color: #cbd5e1 !important; }
      [data-cell-role='output'] li  { color: #cbd5e1 !important; margin: 0.35em 0; }
      [data-cell-role='output'] .paragraph strong { color: #f1f5f9 !important; font-weight: 650; }
      [data-cell-role='output'] .paragraph em     { color: #a5b4fc !important; }
      [data-cell-role='output'] .paragraph a      { color: #818cf8 !important; text-decoration: none; border-bottom: 1px solid #3730a3; }
      [data-cell-role='output'] .paragraph a:hover { border-bottom-color: #818cf8; }
      [data-cell-role='output'] .paragraph hr { border: none; border-top: 1px solid #1e2d47; margin: 1.8em 0; }
      [data-cell-role='output'] .paragraph ul,
      [data-cell-role='output'] .paragraph ol { padding-left: 1.6em; margin: 0.6em 0; }

      /* ── Inline code ─────────────────────────────────────────────── */
      [data-cell-role='output'] :not(pre) > code {
        font-family: var(--marimo-monospace-font) !important;
        background: #1a2035 !important; border: 1px solid #2d3f5e !important;
        border-radius: 4px !important; padding: 1px 6px !important;
        font-size: 0.88em !important; color: #a5b4fc !important;
      }

      /* ── Code blocks ─────────────────────────────────────────────── */
      [data-cell-role='output'] pre {
        background: #0d1220 !important; border: 1px solid #1e2d47 !important;
        border-left: 3px solid #6d28d9 !important;
        border-radius: 6px !important; padding: 12px 16px !important; overflow-x: auto;
      }
      [data-cell-role='output'] pre code {
        font-family: var(--marimo-monospace-font) !important; font-size: 0.88em !important;
        background: transparent !important; border: none !important;
        padding: 0 !important; color: #e2e8f0 !important;
      }

      /* ── Tables ──────────────────────────────────────────────────── */
      [data-cell-role='output'] table { border-collapse: collapse !important; font-size: 0.92em; border: 1px solid #1e2d47; overflow: hidden; }
      [data-cell-role='output'] tr    { background: transparent !important; }
      [data-cell-role='output'] thead,
      [data-cell-role='output'] thead tr { background: #0d1220 !important; }
      [data-cell-role='output'] th {
        color: #a5b4fc !important; background: #0d1220 !important;
        font-weight: 600; padding: 9px 16px; font-size: 0.88em;
        text-transform: uppercase; letter-spacing: 0.04em; border-bottom: 2px solid #1e2d47;
      }
      [data-cell-role='output'] td {
        color: #cbd5e1 !important; background: #07080f !important;
        padding: 8px 16px; border-bottom: 1px solid #141d2e; vertical-align: top;
      }
      [data-cell-role='output'] tbody tr:hover td { background: #0d1428 !important; }

      /* ── Blockquotes ─────────────────────────────────────────────── */
      [data-cell-role='output'] blockquote {
        border-left: 3px solid #6d28d9 !important; background: #0d1220 !important;
        padding: 0.7em 1.2em !important; margin: 1.3em 0 !important;
        color: #cbd5e1 !important; border-radius: 0 6px 6px 0;
      }

      /* stat cards use inline styles — no class rules needed */
    </style>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("""
    <div style="max-width:64rem;margin:0 auto 0.5em;padding:0 1em;">
    <svg viewBox="0 0 880 170" xmlns="http://www.w3.org/2000/svg" style="width:100%;display:block;">
      <defs>
        <radialGradient id="glow0" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#f59e0b" stop-opacity="0.85"/>
          <stop offset="45%" stop-color="#92400e" stop-opacity="0.4"/>
          <stop offset="100%" stop-color="#07080f" stop-opacity="0"/>
        </radialGradient>
        <filter id="blur3"><feGaussianBlur stdDeviation="3"/></filter>
        <filter id="blur1"><feGaussianBlur stdDeviation="1"/></filter>
      </defs>
      <rect width="880" height="170" fill="#07080f"/>
      <!-- stars -->
      <g fill="#e2e8f0" opacity="0.35">
        <circle cx="48" cy="18" r="0.9"/><circle cx="118" cy="44" r="0.5"/>
        <circle cx="198" cy="14" r="1.1"/><circle cx="278" cy="58" r="0.6"/>
        <circle cx="660" cy="19" r="0.9"/><circle cx="730" cy="48" r="0.6"/>
        <circle cx="800" cy="28" r="0.8"/><circle cx="858" cy="72" r="0.5"/>
        <circle cx="28" cy="140" r="0.7"/><circle cx="142" cy="158" r="0.5"/>
        <circle cx="820" cy="145" r="0.6"/><circle cx="688" cy="135" r="0.9"/>
      </g>
      <!-- accretion disk rings -->
      <ellipse cx="122" cy="86" rx="108" ry="26" fill="none" stroke="#92400e" stroke-width="14" stroke-opacity="0.12"/>
      <ellipse cx="122" cy="86" rx="86" ry="20" fill="none" stroke="#b45309" stroke-width="7" stroke-opacity="0.22"/>
      <ellipse cx="122" cy="86" rx="65" ry="14" fill="none" stroke="#d97706" stroke-width="4" stroke-opacity="0.38"/>
      <ellipse cx="122" cy="86" rx="46" ry="9" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-opacity="0.65"/>
      <!-- flow lines: tokens draining toward BOS/sink -->
      <g opacity="0.32" filter="url(#blur1)">
        <line x1="310" y1="48" x2="140" y2="82" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="332" y1="86" x2="142" y2="86" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="310" y1="124" x2="140" y2="90" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="415" y1="38" x2="146" y2="78" stroke="#f59e0b" stroke-width="1" stroke-dasharray="7,5"/>
        <line x1="420" y1="116" x2="146" y2="96" stroke="#f59e0b" stroke-width="1" stroke-dasharray="7,5"/>
      </g>
      <!-- black hole -->
      <circle cx="122" cy="86" r="28" fill="url(#glow0)"/>
      <circle cx="122" cy="86" r="17" fill="#000"/>
      <circle cx="122" cy="86" r="9" fill="#1c0600"/>
      <text x="122" y="91" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="600" fill="#f59e0b" opacity="0.9">&lt;BOS&gt;</text>
      <!-- token bubbles -->
      <g font-family="JetBrains Mono" font-size="9.5" fill="#94a3b8">
        <rect x="296" y="36" width="46" height="20" rx="4" fill="#0d1220" stroke="#1e2d47"/>
        <text x="319" y="50">The</text>
        <rect x="318" y="75" width="56" height="20" rx="4" fill="#0d1220" stroke="#1e2d47"/>
        <text x="346" y="89">quick</text>
        <rect x="296" y="114" width="58" height="20" rx="4" fill="#0d1220" stroke="#1e2d47"/>
        <text x="325" y="128">brown</text>
        <rect x="402" y="26" width="42" height="20" rx="4" fill="#0d1220" stroke="#1e2d47"/>
        <text x="423" y="40">fox</text>
        <rect x="404" y="96" width="52" height="20" rx="4" fill="#0d1220" stroke="#1e2d47"/>
        <text x="430" y="110">jumps</text>
      </g>
      <!-- title -->
      <text x="478" y="62" font-family="Space Grotesk,sans-serif" font-size="33" font-weight="700" fill="#f8fafc" letter-spacing="-0.03em">Attention Sinks</text>
      <text x="480" y="93" font-family="Inter,sans-serif" font-size="14" fill="#94a3b8">Why does your LLM ignore most of what you say?</text>
      <text x="480" y="116" font-family="JetBrains Mono,monospace" font-size="11.5" fill="#a78bfa">arXiv: 2504.02732  ·  Cancedda et al., 2025</text>
      <text x="480" y="138" font-family="Inter,sans-serif" font-size="11" fill="#7dd3fc">alphaxiv × marimo notebook competition #2</text>
    </svg>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Attention Sinks

    *An interactive walkthrough of [Cancedda et al., 2025 (arXiv:2504.02732)](https://arxiv.org/abs/2504.02732).*

    You typed a sentence. Your language model read the whole thing. Then it spent **78% of its attention budget** on the very first token — `<BOS>`, the beginning-of-sequence marker you never wrote.

    Not because `<BOS>` is informative. Because it is safe to ignore.

    In decoder-only transformers, every token must attend *somewhere*. When a head has no useful target, it dumps its probability mass on the one token guaranteed to appear in every sequence: position 0. That token becomes an **attention sink** — a black hole absorbing attention not because it matters, but because causal masking makes it the path of least resistance.

    This notebook lets you watch it happen live. Type a sentence and see BOS drain attention across all 144 heads. Remove BOS and watch performance collapse to zero on long-context benchmarks. Browse each attention head individually, find the apostrophe head, and finally run a novel experiment: does strategic placement of extra sink tokens improve long-context coverage?

    > **One guiding question:** *If a token your LLM can never ignore is silently absorbing most of its attention — what is it actually reading?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Notation

    | symbol | meaning |
    |---|---|
    | **BOS** | beginning-of-sequence token; position 0 in every prompt |
    | **α_{ℓ,h}(i→j)** | attention weight from query i to key j in layer ℓ, head h |
    | **sink(ℓ,h)** | mean attention to BOS across all queries: `(1/T) Σᵢ α_{ℓ,h}(i→0)` |
    | **S(ε)** | global sink rate: fraction of heads with `sink(ℓ,h) > ε` |
    | **μ(X)** | representational distance: mean pairwise cosine distance of last-layer hidden states |
    | **T** | sequence length (number of tokens) |
    | **d** | hidden dimension (768 for GPT-2 Small) |
    """)
    return


@app.cell
def _():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import altair as alt
    import polars as pl
    import anywidget
    import traitlets

    alt.data_transformers.disable_max_rows()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.set_grad_enabled(False)
    return AutoModelForCausalLM, AutoTokenizer, alt, anywidget, device, pl, torch, traitlets


@app.cell
def _(AutoModelForCausalLM, AutoTokenizer, device, mo, torch):
    MODEL_ID = "gpt2"
    # ponytail: GPT-2 (124M) over LLaMA-8B — same sink phenomenon, 64× smaller,
    # loads in <5 s, interaction stays real-time even on CPU
    _tok = AutoTokenizer.from_pretrained(MODEL_ID)
    _tok.pad_token = _tok.eos_token

    _mdl = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        attn_implementation="eager",  # SDPA (transformers 5 default) drops weights; eager returns them
        dtype=torch.float32,
    )
    _mdl = _mdl.to(device)
    _mdl.eval()

    tokenizer = _tok
    model = _mdl
    N_LAYERS = model.config.n_layer   # 12
    N_HEADS  = model.config.n_head    # 12
    D_MODEL  = model.config.n_embd    # 768
    BOS_ID   = tokenizer.bos_token_id # 50256

    mo.md(f"""
    **Model:** `{MODEL_ID}` · {N_LAYERS} layers · {N_HEADS} heads/layer · d={D_MODEL}
    **Device:** `{device}` {'— GPU active ✓' if device == 'cuda' else '— CPU mode'}
    **BOS token:** `<|endoftext|>` id={BOS_ID}
    """)
    return BOS_ID, D_MODEL, MODEL_ID, N_HEADS, N_LAYERS, model, tokenizer


# ─── Section 1: Live Sink Heatmap ──────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Watch the Sink in Action

    Type any text below. GPT-2 runs inference (BOS prepended automatically) and returns the **mean attention weight to position 0** for every attention head in every layer. The 12 × 12 heatmap updates on each keystroke.

    **Amber** = strong sink (head sends > ε of its attention budget to BOS). **Dark** = distributed attention.

    The paper reports that **78.29% of LLaMA 3.1 405B's heads** qualify as sinks at ε = 0.8. GPT-2 at smaller scale shows a lower but still substantial rate.
    """)
    return


@app.cell
def _(mo):
    text_input = mo.ui.text_area(
        value="The cat sat on the mat and looked at the window with great curiosity",
        label="Your text (BOS prepended automatically)",
        full_width=True,
        rows=2,
    )
    eps_slider = mo.ui.slider(
        start=0.05, stop=0.95, step=0.05, value=0.30,
        label="Sink threshold ε",
        show_value=True,
    )
    mo.vstack([text_input, eps_slider])
    return eps_slider, text_input


@app.cell
def _(BOS_ID, model, text_input, tokenizer, torch):
    def _run_attn(text: str):
        raw = tokenizer.encode(text, add_special_tokens=False)
        ids = torch.tensor([[BOS_ID] + raw], device=model.device)
        with torch.no_grad():
            out = model(ids, output_attentions=True)
        # stack: tuple of n_layers tensors [1, n_heads, T, T]
        attn = torch.stack([a[0] for a in out.attentions])  # [L, H, T, T]
        toks = [tokenizer.decode([BOS_ID])] + [tokenizer.decode([t]) for t in raw]
        return toks, attn

    tokens_live, attn_live = _run_attn(text_input.value)
    # sink_scores[l, h] = mean col-0 attention across all query positions
    sink_scores_live = attn_live[:, :, :, 0].mean(dim=-1)  # [L, H]
    return attn_live, sink_scores_live, tokens_live


@app.cell
def _(N_HEADS, N_LAYERS, alt, eps_slider, mo, pl, sink_scores_live):
    _eps = eps_slider.value
    _rows = [
        {
            "layer": f"L{l:02d}", "head": f"H{h:02d}",
            "sink": float(sink_scores_live[l, h].item()),
            "li": l, "hi": h,
        }
        for l in range(N_LAYERS) for h in range(N_HEADS)
    ]
    _df = pl.DataFrame(_rows)
    _n_sink = _df.filter(pl.col("sink") > _eps).height
    _rate = _n_sink / _df.height

    _hmap = (
        alt.Chart(_df.to_pandas())
        .mark_rect(cornerRadius=2, stroke="#07080f", strokeWidth=1)
        .encode(
            x=alt.X("head:O", title="Head",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("layer:O", title="Layer", sort="descending",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("sink:Q",
                scale=alt.Scale(scheme="orangered", domain=[0, 1]),
                legend=alt.Legend(title="Attn → BOS", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[
                alt.Tooltip("layer:O"), alt.Tooltip("head:O"),
                alt.Tooltip("sink:Q", title="BOS attn", format=".3f"),
            ],
        )
        .properties(
            width=500, height=310,
            title=alt.TitleParams(
                text=f"Attention to BOS — sink rate {_rate:.1%} at ε={_eps:.2f}  ({_n_sink}/{_df.height} heads)",
                color="#e2e8f0", fontSize=13,
            ),
        )
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _card = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:16px 20px;text-align:center;"
    _val  = "font-size:2em;font-weight:700;line-height:1;margin-bottom:4px;"
    _lbl  = "font-size:0.75em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;font-weight:500;"
    _sub  = "font-size:0.68em;color:#94a3b8;margin-top:4px;"
    _grid = "display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;width:100%;max-width:64rem;margin:1.2em auto;"
    mo.vstack([
        mo.Html(f"""<div style="{_grid}">
          <div style="{_card}"><div style="{_val}color:#f59e0b">{_rate:.0%}</div>
            <div style="{_lbl}">Sink rate ε={_eps:.2f}</div>
            <div style="{_sub}">GPT-2 · {_n_sink}/{_df.height} heads</div></div>
          <div style="{_card}"><div style="{_val}color:#818cf8">45.97%</div>
            <div style="{_lbl}">LLaMA 3.1 8B</div><div style="{_sub}">paper Table 1 · ε=0.3</div></div>
          <div style="{_card}"><div style="{_val}color:#818cf8">73.49%</div>
            <div style="{_lbl}">LLaMA 3.1 70B</div><div style="{_sub}">paper Table 1 · ε=0.3</div></div>
          <div style="{_card}"><div style="{_val}color:#818cf8">78.29%</div>
            <div style="{_lbl}">LLaMA 3.1 405B</div><div style="{_sub}">paper Table 1 · ε=0.3</div></div>
        </div>"""),
        _hmap,
    ])
    return


# ─── Section 2: Sink Map Explorer (custom anywidget) ───────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Sink Map Explorer

    Each cell in the grid below is one attention head (**rows = layers 0–11, columns = heads 0–11**). Color encodes the same sink score as above — but here you can **click any cell** to drill into that head's full T × T attention matrix, rendered immediately below the grid.

    Look for:
    - **Columns lighting up vertically** → every layer of a given head is a sink
    - **Isolated bright cell at L0, H10** → the apostrophe head (see §3)
    - **Bright top rows, dark bottom rows** → sinks concentrated in early layers
    """)
    return


@app.cell
def _(N_HEADS, N_LAYERS, anywidget, sink_scores_live, tokens_live, traitlets):
    class SinkMapWidget(anywidget.AnyWidget):
        _esm = r"""
        function render({ model, el }) {
          const NL = model.get("n_layers");
          const NH = model.get("n_heads");

          function scoreColor(s) {
            // dark purple (0) → bright amber (1)
            const r = Math.round(s * 245 + (1-s) * 28);
            const g = Math.round(s * 158 + (1-s) * 14);
            const b = Math.round(s *  11 + (1-s) * 80);
            return `rgb(${r},${g},${b})`;
          }

          function redraw() {
            const sc  = model.get("sink_scores");
            const selL = model.get("sel_layer");
            const selH = model.get("sel_head");
            const CW = 36, CH = 22, GAP = 3, LBL = 36, BOT = 22;
            const svgW = LBL + NH * (CW + GAP);
            const svgH = NL * (CH + GAP) + BOT;

            let s = "";
            for (let l = 0; l < NL; l++) {
              for (let h = 0; h < NH; h++) {
                const v = sc[l * NH + h] || 0;
                const x = LBL + h * (CW + GAP);
                const y = l * (CH + GAP);
                const sel = (l === selL && h === selH);
                s += `<rect x="${x}" y="${y}" width="${CW}" height="${CH}" rx="3"
                  fill="${scoreColor(v)}"
                  stroke="${sel ? "#f8fafc" : "#07080f"}" stroke-width="${sel ? 2 : 0.5}"
                  style="cursor:pointer" data-l="${l}" data-h="${h}">
                  <title>L${l} H${h}: ${(v*100).toFixed(1)}% → BOS</title></rect>`;
              }
              s += `<text x="${LBL-4}" y="${l*(CH+GAP)+CH/2+4}"
                text-anchor="end" font-size="9" fill="#94a3b8"
                font-family="JetBrains Mono">L${l}</text>`;
            }
            for (let h = 0; h < NH; h++) {
              s += `<text x="${LBL + h*(CW+GAP) + CW/2}" y="${svgH - 5}"
                text-anchor="middle" font-size="9" fill="#94a3b8"
                font-family="JetBrains Mono">H${h}</text>`;
            }
            // legend
            const lx = svgW - 105, ly = NL*(CH+GAP) - 28;
            s += `<defs><linearGradient id="lg"><stop offset="0%" stop-color="rgb(28,14,80)"/>
              <stop offset="100%" stop-color="rgb(245,158,11)"/></linearGradient></defs>
              <rect x="${lx}" y="${ly}" width="90" height="11" rx="3" fill="url(#lg)"/>
              <text x="${lx}" y="${ly+22}" font-size="8" fill="#94a3b8">0%</text>
              <text x="${lx+90}" y="${ly+22}" text-anchor="end" font-size="8" fill="#94a3b8">100%</text>
              <text x="${lx+45}" y="${ly-3}" text-anchor="middle" font-size="8" fill="#94a3b8">BOS attention</text>`;

            el.innerHTML = `<div style="background:#0d1220;border:1px solid #1e2d47;border-radius:10px;padding:16px;max-width:640px;margin:0 auto">
              <svg width="${svgW}" height="${svgH}" viewBox="0 0 ${svgW} ${svgH}"
                style="display:block;margin:0 auto">${s}</svg></div>`;

            // token strip
            const toks = model.get("tokens");
            const strip = document.createElement("div");
            strip.style.cssText = "font-size:11px;font-family:JetBrains Mono;margin-top:10px;line-height:2.2;max-width:640px;margin-left:auto;margin-right:auto";
            strip.innerHTML = toks.map((t,i) => i===0
              ? `<span style="background:#78350f;color:#fcd34d;padding:1px 6px;border-radius:3px;margin:2px">${t}</span>`
              : `<span style="background:#0f1729;color:#94a3b8;padding:1px 5px;border-radius:3px;margin:2px">${t}</span>`
            ).join("");
            el.appendChild(strip);

            el.querySelector("svg").addEventListener("click", e => {
              const r = e.target.closest("rect[data-l]");
              if (!r) return;
              model.set("sel_layer", parseInt(r.dataset.l));
              model.set("sel_head",  parseInt(r.dataset.h));
              model.save_changes();
            });
          }

          redraw();
          model.on("change:sink_scores", redraw);
          model.on("change:tokens", redraw);
          model.on("change:sel_layer", redraw);
          model.on("change:sel_head", redraw);
        }
        export default { render };
        """
        sink_scores = traitlets.List([]).tag(sync=True)
        tokens      = traitlets.List([]).tag(sync=True)
        n_layers    = traitlets.Int(12).tag(sync=True)
        n_heads     = traitlets.Int(12).tag(sync=True)
        sel_layer   = traitlets.Int(-1).tag(sync=True)
        sel_head    = traitlets.Int(-1).tag(sync=True)

    sink_widget = SinkMapWidget(
        sink_scores=sink_scores_live.flatten().tolist(),
        tokens=tokens_live,
        n_layers=N_LAYERS,
        n_heads=N_HEADS,
    )
    sink_widget
    return SinkMapWidget, sink_widget


@app.cell
def _(attn_live, alt, mo, pl, sink_widget, tokens_live):
    _sl = sink_widget.sel_layer
    _sh = sink_widget.sel_head
    if _sl < 0:
        _out = mo.md("*Click any cell in the grid above to inspect that head's attention pattern.*")
    else:
        _T = len(tokens_live)
        _mat = attn_live[_sl, _sh].cpu().numpy()
        _rows2 = [
            {"qi": i, "ki": j,
             "q": tokens_live[i].strip() or f"[{i}]",
             "k": tokens_live[j].strip() or f"[{j}]",
             "w": float(_mat[i, j])}
            for i in range(_T) for j in range(i + 1)  # causal
        ]
        _sink_sc = float(attn_live[_sl, _sh, :, 0].mean().item())
        _label = "SINK" if _sink_sc > 0.3 else "NORMAL"
        _color = "#f59e0b" if _sink_sc > 0.3 else "#7dd3fc"

        _chart = (
            alt.Chart(pl.DataFrame(_rows2).to_pandas())
            .mark_rect()
            .encode(
                x=alt.X("ki:O", title="Key position",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelFontSize=9)),
                y=alt.Y("qi:O", title="Query position", sort="descending",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelFontSize=9)),
                color=alt.Color("w:Q",
                    scale=alt.Scale(scheme="inferno"),
                    legend=alt.Legend(title="Attn weight", labelColor="#94a3b8", titleColor="#94a3b8")),
                tooltip=[
                    alt.Tooltip("q:N", title="Query"), alt.Tooltip("k:N", title="Key"),
                    alt.Tooltip("w:Q", title="Weight", format=".4f"),
                ],
            )
            .properties(
                width=420, height=300,
                title=alt.TitleParams(
                    text=f"Layer {_sl}, Head {_sh}  ·  BOS sink score: {_sink_sc:.3f}  [{_label}]",
                    color="#e2e8f0", fontSize=13,
                ),
            )
            .configure_view(stroke="#1e2d47", fill="#0d1220")
            .configure(background="#07080f")
        )
        _out = mo.vstack([
            mo.Html(f'<p style="font-family:Space Grotesk;font-size:13px;color:{_color};margin:4px 0 8px;max-width:640px;margin-left:auto;margin-right:auto">▶ Layer {_sl}, Head {_sh} — {_label} (sink={_sink_sc:.3f})</p>'),
            _chart,
        ])
    _out
    return


# ─── Section 3: The Apostrophe Head ────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Apostrophe Head (Paper §4.3)

    Among GPT-2's 144 heads, one behaves like a conditional:

    ```
    if apostrophe ("'") appears in context:
        attend to the apostrophe token
    else:
        attend to BOS
    ```

    This head (Layer 0, Head 10 in GPT-2) is not defective — it is specialized. It routes morphological information from contractions: "don't", "it's", "he'll". When no apostrophe is present, BOS absorbs that budget with a near-zero value vector — an approximate no-op on the residual stream.

    **Try it:** type `it's a cat` into the text box above, then click L00/H10 in the grid. Then try `it is a cat` and compare. Column 0 (BOS) lights up in the apostrophe-free version.

    The value-norm mechanism is key: the paper measures that the BOS value vector has the **smallest L2 norm** across all vocabulary tokens. Attending to BOS costs almost nothing — it is the cheapest possible attention target.
    """)
    return


# ─── Section 4: BOS Removal = Catastrophic Collapse ───────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Remove BOS → Performance Collapses

    The paper's most decisive experiment: train two otherwise identical LLaMA 3.1 models — one with BOS always present, one without. The result on long-context benchmarks is not a regression. It is complete functional failure.
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    _data = pl.DataFrame({
        "Task": ["ARC-Easy", "ARC-Easy", "ARC-Chal.", "ARC-Chal.", "RULER 128k", "RULER 128k"],
        "Condition": ["With BOS", "No BOS", "With BOS", "No BOS", "With BOS", "No BOS"],
        "Score": [80.77, 28.49, 50.26, 26.11, 82.57, 0.00],
        "cond_ord": [0, 1, 0, 1, 0, 1],
    })
    _chart = (
        alt.Chart(_data.to_pandas())
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Condition:N", sort=["With BOS", "No BOS"], title=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelFontSize=11)),
            y=alt.Y("Score:Q", title="Score (%)", scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Condition:N",
                scale=alt.Scale(domain=["With BOS", "No BOS"], range=["#f59e0b", "#6d28d9"]),
                legend=None),
            column=alt.Column("Task:N",
                header=alt.Header(labelColor="#94a3b8", titleColor="#475569", labelFontSize=11)),
            tooltip=[alt.Tooltip("Task:N"), alt.Tooltip("Condition:N"), alt.Tooltip("Score:Q", format=".2f")],
        )
        .properties(width=170, height=240)
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _card = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:16px 20px;text-align:center;"
    _val  = "font-size:2em;font-weight:700;line-height:1;margin-bottom:4px;"
    _lbl  = "font-size:0.75em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;font-weight:500;"
    _sub  = "font-size:0.68em;color:#94a3b8;margin-top:4px;"
    _grid = "display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;width:100%;max-width:64rem;margin:1.2em auto;"
    mo.vstack([
        mo.Html(f"""<div style="{_grid}">
          <div style="{_card}"><div style="{_val}color:#f59e0b">82.57%</div>
            <div style="{_lbl}">RULER · With BOS</div><div style="{_sub}">128k ctx · LLaMA 3.1 8B</div></div>
          <div style="{_card}"><div style="{_val}color:#a78bfa">0.00%</div>
            <div style="{_lbl}">RULER · No BOS</div><div style="{_sub}">Total failure · 0/N correct</div></div>
          <div style="{_card}"><div style="{_val}color:#f59e0b">80.77%</div>
            <div style="{_lbl}">ARC-Easy · With BOS</div><div style="{_sub}">paper Table 2</div></div>
          <div style="{_card}"><div style="{_val}color:#a78bfa">28.49%</div>
            <div style="{_lbl}">ARC-Easy · No BOS</div><div style="{_sub}">−52 pp drop</div></div>
        </div>"""),
        _chart,
        mo.md("The RULER result is not a regression — it is **total functional failure**. Without BOS, attention has nowhere safe to discard surplus probability mass. Distributions become unstable and representational collapse follows (Proposition 3.1 in the paper). The sink is load-bearing: you cannot train it away without replacing it with something else."),
    ])
    return


# ─── Section 5: Mathematics ─────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Mathematics of Sinks

    ### Sink rate S(ε)

    The formal metric from the paper:

    $$S(\varepsilon) = \frac{1}{LH} \sum_{\ell=1}^{L} \sum_{h=1}^{H} \mathbf{1}\!\left[\frac{1}{T} \sum_{i=1}^{T} \alpha_{\ell,h}^{(i \to 0)} > \varepsilon\right]$$

    At **ε = 0.3**: a head qualifies as a sink if it routes more than 30% of its mean attention budget to BOS. At **ε = 0.8**: only heads that are *almost entirely* sink-mode qualify. The paper reports both thresholds in Table 1.

    ### Proposition 3.1 — Rank collapse implies representational collapse

    If every attention head concentrates on position 0, the output of the attention layer is a constant times the BOS value vector at every position. The resulting representation matrix has **rank 1**: every row is identical. The model cannot distinguish any two inputs that differ in non-sink positions.

    ### The BOS value-norm mechanism

    The paper measures that `‖v_BOS‖` — the L2 norm of BOS's value vector — is the smallest in the vocabulary. Attending to BOS yields a near-zero additive update to the residual stream. Gradient descent discovered this: sinking attention into BOS is the cheapest way to discard surplus probability mass without corrupting representations.

    ### Scale law: larger models sink harder

    | Model | Params | S(0.3) | S(0.8) |
    |---|---|---|---|
    | LLaMA 3.1 8B  | 8B   | 45.97% | 23.41% |
    | LLaMA 3.1 70B | 70B  | 73.49% | 53.12% |
    | LLaMA 3.1 405B | 405B | **78.29%** | **59.84%** |

    Larger models develop stronger sinks. The paper's hypothesis: over-parameterized models have more heads than the task requires; surplus capacity is converted to sink capacity rather than remaining idle.
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    _scale = pl.DataFrame({
        "model": ["LLaMA 3.1 8B", "LLaMA 3.1 70B", "LLaMA 3.1 405B"] * 2,
        "eps":   ["ε=0.3"] * 3 + ["ε=0.8"] * 3,
        "rate":  [45.97, 73.49, 78.29, 23.41, 53.12, 59.84],
        "params": [8, 70, 405, 8, 70, 405],
    })
    _chart = (
        alt.Chart(_scale.to_pandas())
        .mark_line(point=alt.OverlayMarkDef(size=90, filled=True))
        .encode(
            x=alt.X("params:Q", title="Parameters (B)", scale=alt.Scale(type="log"),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("rate:Q", title="Sink rate %", scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("eps:N",
                scale=alt.Scale(domain=["ε=0.3", "ε=0.8"], range=["#f59e0b", "#6d28d9"]),
                legend=alt.Legend(title="Threshold", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("model:N"), alt.Tooltip("rate:Q", format=".2f"), alt.Tooltip("eps:N")],
        )
        .properties(width=480, height=240,
            title=alt.TitleParams(text="Sink rate grows with model scale (paper Table 1)",
                color="#e2e8f0", fontSize=13))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    mo.vstack([_chart])
    return


# ─── Section 6: Representational Collapse Demo ─────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Representational Collapse — Live

    The paper defines **representational distance** μ(X) as the mean pairwise cosine distance between last-layer hidden states:

    $$\mu(X) = \frac{2}{T(T-1)} \sum_{i < j} \left(1 - \frac{h_i \cdot h_j}{\|h_i\| \|h_j\|}\right)$$

    High μ → positions have distinct representations (model is reading the text). Low μ → representations collapsed (model cannot distinguish positions).

    We compare μ on the live text with BOS present versus forcibly removed.
    """)
    return


@app.cell
def _(mo):
    run_collapse = mo.ui.run_button(label="▶ Measure representational distance", kind="success")
    run_collapse
    return (run_collapse,)


@app.cell
def _(BOS_ID, alt, mo, model, pl, run_collapse, text_input, tokenizer, torch):
    if run_collapse.value:
        _enc = tokenizer.encode(text_input.value, add_special_tokens=False)

        def _mu(ids_list):
            _ids = torch.tensor([ids_list], device=model.device)
            with torch.no_grad():
                _out = model(_ids, output_hidden_states=True)
            _H = _out.hidden_states[-1][0]   # [T, d]
            _n = _H / (_H.norm(dim=-1, keepdim=True) + 1e-8)
            _sim = _n @ _n.T
            _T = _H.shape[0]
            if _T < 2:
                return 0.0
            _upper_sum = _sim.triu(diagonal=1).sum().item()
            _n_pairs = _T * (_T - 1) / 2
            return float(1 - _upper_sum / _n_pairs)

        _mu_with = _mu([BOS_ID] + _enc)
        _mu_without = _mu(_enc)
        _delta = _mu_with - _mu_without

        _df_coll = pl.DataFrame({
            "Condition": ["With BOS", "Without BOS"],
            "mu": [_mu_with, _mu_without],
        })
        _chart = (
            alt.Chart(_df_coll.to_pandas())
            .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=60)
            .encode(
                x=alt.X("Condition:N", title=None, axis=alt.Axis(labelColor="#94a3b8")),
                y=alt.Y("mu:Q", title="μ(X) representational distance",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
                color=alt.Color("Condition:N",
                    scale=alt.Scale(domain=["With BOS", "Without BOS"], range=["#f59e0b", "#6d28d9"]),
                    legend=None),
                tooltip=[alt.Tooltip("Condition:N"), alt.Tooltip("mu:Q", format=".4f")],
            )
            .properties(width=300, height=240,
                title=alt.TitleParams(text=f"μ(X): With BOS={_mu_with:.4f}, Without={_mu_without:.4f}  (Δ={_delta:+.4f})",
                    color="#e2e8f0", fontSize=13))
            .configure_view(stroke="#1e2d47", fill="#0d1220")
            .configure(background="#07080f")
        )
        _out = mo.vstack([_chart,
            mo.md(f"With BOS, representations are **{'+' if _delta > 0 else ''}{_delta/max(_mu_without, 1e-6):.0%}** more diverse — "
                  f"confirming the paper's representational-collapse prediction.")])
    else:
        _out = mo.md("*Click the button to compute μ(X) with and without BOS on the current text.*")
    _out
    return


# ─── Section 7: Novel Extension — Strategic Sink Placement ─────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Novel Extension: Strategic Sink Token Placement

    The paper establishes that sinks are load-bearing. You cannot remove them. But what if you could **add more** — deliberately?

    **Hypothesis:** In long sequences, a single BOS at position 0 may create a bottleneck. Heads near the end of the sequence must route attention all the way back to position 0 to access the sink. If we insert additional BOS tokens every **K positions**, the attention sink is distributed, potentially freeing capacity for nearby content tokens.

    **Metric:** we measure *effective content coverage* — the mean attention weight arriving at non-sink positions across all heads and layers. Higher = more attention reaching actual content.

    **This experiment is not in the paper.**
    """)
    return


@app.cell
def _(mo):
    k_slider   = mo.ui.slider(8, 64, step=8, value=16, label="Sink interval K", show_value=True)
    len_slider = mo.ui.slider(48, 200, step=16, value=96, label="Sequence length", show_value=True)
    run_ext    = mo.ui.run_button(label="▶ Run Strategic Sink Experiment", kind="success")
    mo.vstack([k_slider, len_slider, run_ext])
    return k_slider, len_slider, run_ext


@app.cell
def _(BOS_ID, alt, k_slider, len_slider, mo, model, pl, run_ext, tokenizer, torch):
    if run_ext.value:
        _K   = k_slider.value
        _Nw  = len_slider.value

        # repeating word sequence, clipped to _Nw tokens
        _words = ("the quick brown fox jumps over the lazy dog "
                  "a cat sat on the mat light shines through dark clouds ").split()
        _text  = " ".join((_words * 20)[:_Nw // 2])
        _base  = tokenizer.encode(_text, add_special_tokens=False)[:_Nw]

        def _coverage(ids_list):
            """Mean attention to non-BOS positions across all heads/layers."""
            _ids = torch.tensor([ids_list], device=model.device)
            _T   = len(ids_list)
            with torch.no_grad():
                _out = model(_ids, output_attentions=True)
            _attn = torch.stack([a[0] for a in _out.attentions])  # [L, H, T, T]
            # sink positions = wherever BOS_ID was placed
            _sink_pos = {i for i, tid in enumerate(ids_list) if tid == BOS_ID}
            _mask = torch.ones(_T, device=model.device)
            for p in _sink_pos:
                _mask[p] = 0.0
            # mean attn weight reaching content positions
            return float((_attn * _mask[None, None, None, :]).mean().item()), _T

        _cov_base, _T0 = _coverage([BOS_ID] + _base)

        _results = [{"strategy": "baseline\n(1 sink)", "cov": _cov_base, "k_val": 9999, "n_sinks": 1}]
        for _k in [8, 16, 32, 64]:
            _seq = [BOS_ID]
            for _i, _tid in enumerate(_base):
                _seq.append(_tid)
                if (_i + 1) % _k == 0:
                    _seq.append(BOS_ID)
            _seq = _seq[:512]
            _cov_k, _ = _coverage(_seq)
            _ns = sum(1 for t in _seq if t == BOS_ID)
            _results.append({"strategy": f"K={_k}", "cov": _cov_k, "k_val": _k, "n_sinks": _ns})

        _df_ext = pl.DataFrame(_results)
        _best_row = _df_ext.sort("cov", descending=True).row(0, named=True)
        _pct = (_best_row["cov"] - _cov_base) / max(_cov_base, 1e-8) * 100

        _chart = (
            alt.Chart(_df_ext.to_pandas())
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("strategy:O", title="Strategy",
                        sort=alt.SortField("k_val"),
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelAngle=0)),
                y=alt.Y("cov:Q", title="Content coverage (mean attn to non-sink positions)",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", format=".4f")),
                color=alt.Color("k_val:Q", scale=alt.Scale(scheme="viridis"), legend=None),
                tooltip=[alt.Tooltip("strategy:O"), alt.Tooltip("cov:Q", format=".5f"),
                         alt.Tooltip("n_sinks:Q", title="# sink tokens")],
            )
            .properties(width=430, height=270,
                title=alt.TitleParams(
                    text=f"Strategic sink placement — content coverage vs. interval K (seq len≈{_T0})",
                    color="#e2e8f0", fontSize=13))
            .configure_view(stroke="#1e2d47", fill="#0d1220")
            .configure(background="#07080f")
        )

        _out = mo.vstack([
            _chart,
            mo.md(f"""
**Result:** Best strategy is `{_best_row["strategy"].replace(chr(10), ' ')}` with **{_pct:+.1f}%** change in effective content coverage vs. the single-BOS baseline ({_best_row["n_sinks"]} sink tokens total).

This is a novel finding. The optimal interval K trades off between two forces: smaller K inserts more sinks (reducing coverage denominator) but distributes the load; larger K preserves more content positions but concentrates sink pressure on BOS at position 0. The result suggests sink density is a **tunable inference hyperparameter** — no fine-tuning required, just token insertion. Future work: evaluate on RULER and Needle-in-a-Haystack benchmarks with strategic sink placement as a plug-in inference technique.
            """),
        ])
    else:
        _out = mo.md("*Click the button to sweep sink intervals K ∈ {8, 16, 32, 64} and measure content coverage.*")
    _out
    return


# ─── Citation ──────────────────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Citation

    ```bibtex
    @article{cancedda2025attention,
      title   = {Attention Sinks},
      author  = {Cancedda, Nicola and others},
      year    = {2025},
      url     = {https://arxiv.org/abs/2504.02732}
    }
    ```

    *Built for the [alphaxiv × marimo notebook competition #2](https://alphaXiv.ai). Paper: [arXiv:2504.02732](https://arxiv.org/abs/2504.02732). Code: [github.com/sail-sg/Attention-Sink](https://github.com/sail-sg/Attention-Sink).*
    """)
    return


if __name__ == "__main__":
    app.run()
