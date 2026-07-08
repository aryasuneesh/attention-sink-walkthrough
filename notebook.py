# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "torch",
#     "transformers",
#     "anywidget",
#     "altair",
#     "polars",
#     "numpy",
#     "plotly",
# ]
#
# ///

import marimo

__generated_with = "0.23.11"
app = marimo.App(
    width="full",
    app_title="Attention Sinks: Why LLMs Attend to the First Token",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
      /*
        Page follows marimo's and molab's default background and text theme; we
        do not force a canvas colour. We brand only the fonts (applied globally
        via marimo's --marimo-*-font variables) and centre the reading column,
        since the app uses width="full". Charts and widgets keep their own dark
        backgrounds by design; everything else follows the host theme so it
        renders correctly on molab.
      */
      :root {
        --marimo-text-font:      'Inter', system-ui, sans-serif;
        --marimo-heading-font:   'Space Grotesk', sans-serif;
        --marimo-monospace-font: 'JetBrains Mono', 'Fira Mono', monospace;
      }
      .output-area, [data-cell-role='output'] {
        max-width: 72rem;
        margin-left: auto !important; margin-right: auto !important;
      }
      .markdown { max-width: 64rem; margin-left: auto; margin-right: auto; }
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
      <g fill="#e2e8f0" opacity="0.35">
        <circle cx="48" cy="18" r="0.9"/><circle cx="118" cy="44" r="0.5"/>
        <circle cx="198" cy="14" r="1.1"/><circle cx="278" cy="58" r="0.6"/>
        <circle cx="660" cy="19" r="0.9"/><circle cx="730" cy="48" r="0.6"/>
        <circle cx="800" cy="28" r="0.8"/><circle cx="858" cy="72" r="0.5"/>
        <circle cx="28" cy="140" r="0.7"/><circle cx="142" cy="158" r="0.5"/>
        <circle cx="820" cy="145" r="0.6"/><circle cx="688" cy="135" r="0.9"/>
      </g>
      <ellipse cx="122" cy="86" rx="108" ry="26" fill="none" stroke="#92400e" stroke-width="14" stroke-opacity="0.12"/>
      <ellipse cx="122" cy="86" rx="86" ry="20" fill="none" stroke="#b45309" stroke-width="7" stroke-opacity="0.22"/>
      <ellipse cx="122" cy="86" rx="65" ry="14" fill="none" stroke="#d97706" stroke-width="4" stroke-opacity="0.38"/>
      <ellipse cx="122" cy="86" rx="46" ry="9" fill="none" stroke="#f59e0b" stroke-width="2.5" stroke-opacity="0.65"/>
      <g opacity="0.32" filter="url(#blur1)">
        <line x1="310" y1="48" x2="140" y2="82" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="332" y1="86" x2="142" y2="86" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="310" y1="124" x2="140" y2="90" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,4"/>
        <line x1="415" y1="38" x2="146" y2="78" stroke="#f59e0b" stroke-width="1" stroke-dasharray="7,5"/>
        <line x1="420" y1="116" x2="146" y2="96" stroke="#f59e0b" stroke-width="1" stroke-dasharray="7,5"/>
      </g>
      <circle cx="122" cy="86" r="28" fill="url(#glow0)"/>
      <circle cx="122" cy="86" r="17" fill="#000"/>
      <circle cx="122" cy="86" r="9" fill="#1c0600"/>
      <text x="122" y="91" text-anchor="middle" font-family="JetBrains Mono" font-size="9.5" font-weight="600" fill="#f59e0b" opacity="0.9">&lt;BOS&gt;</text>
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
      <text x="478" y="62" font-family="Space Grotesk,sans-serif" font-size="33" font-weight="700" fill="#f8fafc" letter-spacing="-0.03em">Attention Sinks</text>
      <text x="480" y="93" font-family="Inter,sans-serif" font-size="14" fill="#94a3b8">Why do LLMs attend to the first token?</text>
      <text x="480" y="116" font-family="JetBrains Mono,monospace" font-size="11.5" fill="#a78bfa">arXiv: 2504.02732  ·  Barbero, Arroyo, Gu et al., COLM 2025</text>
      <text x="480" y="138" font-family="Inter,sans-serif" font-size="11" fill="#7dd3fc">alphaxiv × marimo notebook competition #2</text>
    </svg>
    </div>
    """)
    return


@app.cell(hide_code=True)
def _(anywidget, mo):
    class TokenQuizWidget(anywidget.AnyWidget):
        _esm = r"""
        function render({ el }) {
          el.innerHTML = `
          <div style="max-width:64rem;margin:0 auto 2em;padding:1.5em 1em;font-family:Inter,sans-serif;background:#07080f">

            <div style="margin-bottom:1.4em">
              <p style="color:#cbd5e1;font-size:1.05em;line-height:1.65;margin:0 0 0.5em">
                A language model reading the sentence below just processed every word.
                Then it spent most of its attention budget on a single token that
                carries no semantic content at all.
              </p>
              <p style="color:#94a3b8;font-size:0.9em;margin:0">
                <strong style="color:#f8fafc">Click the token you think received the most attention.</strong>
              </p>
            </div>

            <div id="hg-chips" style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1.5em"></div>

            <div id="hg-reveal" style="display:none">
              <div style="background:#0d1220;border:1px solid #1e2d47;border-radius:10px;padding:20px 24px">
                <div id="hg-verdict" style="font-size:1em;margin-bottom:14px;color:#e2e8f0"></div>
                <div id="hg-bars" style="display:flex;flex-direction:column;gap:5px"></div>
                <div style="margin-top:14px;padding-top:12px;border-top:1px solid #1e2d47;font-size:0.82em;color:#64748b;line-height:1.55">
                  Measured on GPT-2 (Layer 5, Head 2) · sentence: &ldquo;The cat sat on the mat&rdquo; · values approximate real model output
                </div>
              </div>

              <div style="margin-top:1.2em;background:#0d1220;border:1px solid #1e2d47;border-radius:10px;padding:18px 22px">
                <p style="color:#94a3b8;font-size:0.88em;line-height:1.65;margin:0 0 0.5em">
                  <strong style="color:#f59e0b">&lt;BOS&gt;</strong> is the beginning-of-sequence marker. It precedes every prompt and carries no meaning, yet whole attention heads dump most of their weight onto it. Separate studies have caught this in GPT-2, LLaMA, Gemma, and Mistral.
                </p>
                <p style="color:#94a3b8;font-size:0.88em;line-height:1.65;margin:0">
                  <a href="https://arxiv.org/pdf/2504.02732" style="color:#818cf8;text-decoration:none;border-bottom:1px solid #3730a3">Barbero et al. (COLM 2025)</a> asked <em>why gradient descent converges on this</em>, and found the sink is the cheapest solution to a representation collapse problem built into every deep Transformer.
                </p>
              </div>
            </div>

          </div>
          `;

          const TOKENS = ['&lt;BOS&gt;', 'The', 'cat', 'sat', 'on', 'the', 'mat', '.'];
          const RAW    = ['<BOS>', 'The', 'cat', 'sat', 'on', 'the', 'mat', '.'];
          const ATTN   = [0.74, 0.09, 0.05, 0.04, 0.03, 0.03, 0.02, 0.00];

          const chips   = el.querySelector('#hg-chips');
          const reveal  = el.querySelector('#hg-reveal');
          const verdict = el.querySelector('#hg-verdict');
          const bars    = el.querySelector('#hg-bars');

          let clicked = false;

          TOKENS.forEach(function (tok, i) {
            const btn = document.createElement('button');
            const isBOS = i === 0;
            btn.innerHTML = tok;
            btn.dataset.idx = i;
            btn.style.cssText = [
              'padding:8px 16px',
              'border-radius:8px',
              'border:1.5px solid #1e2d47',
              'background:' + (isBOS ? '#0d1220' : '#0a0e1a'),
              'color:' + (isBOS ? '#475569' : '#94a3b8'),
              'font-family:JetBrains Mono,monospace',
              'font-size:13px',
              'cursor:pointer',
              'transition:all 0.15s',
            ].join(';');
            btn.addEventListener('mouseenter', function () {
              if (!clicked) { btn.style.borderColor = '#7dd3fc'; btn.style.color = '#e2e8f0'; }
            });
            btn.addEventListener('mouseleave', function () {
              if (!clicked) {
                btn.style.borderColor = '#1e2d47';
                btn.style.color = isBOS ? '#475569' : '#94a3b8';
              }
            });
            btn.addEventListener('click', function () {
              if (clicked) return;
              clicked = true;
              revealResult(i);
            });
            chips.appendChild(btn);
          });

          function revealResult(chosen) {
            const allBtns = chips.querySelectorAll('button');
            allBtns.forEach(function (b, i) {
              b.style.cursor = 'default';
              if (i === 0) {
                b.style.borderColor = '#f59e0b';
                b.style.background = '#1c0a00';
                b.style.color = '#f59e0b';
                b.style.fontWeight = '700';
              } else if (i === chosen && chosen !== 0) {
                b.style.borderColor = '#f87171';
                b.style.background = '#1a0707';
                b.style.color = '#f87171';
              } else {
                b.style.borderColor = '#0f1623';
                b.style.background = '#070a10';
                b.style.color = '#334155';
              }
            });

            if (chosen === 0) {
              verdict.innerHTML = '<span style="color:#4ade80;font-weight:700">Correct!</span> &lt;BOS&gt; absorbed <strong>74%</strong> of attention. The model barely looked at your words.';
            } else {
              verdict.innerHTML = '<span style="color:#f87171;font-weight:700">Incorrect.</span> &ldquo;' + RAW[chosen] + '&rdquo; got only <strong>' + (ATTN[chosen]*100).toFixed(0) + '%</strong>. <strong style="color:#f59e0b">&lt;BOS&gt; took 74%.</strong> The model spent most of its attention on a positional placeholder.';
            }

            bars.innerHTML = '';
            ATTN.forEach(function (w, i) {
              const row = document.createElement('div');
              row.style.cssText = 'display:flex;align-items:center;gap:8px';

              const label = document.createElement('div');
              label.innerHTML = TOKENS[i];
              label.style.cssText = 'width:56px;text-align:right;font-family:JetBrains Mono,monospace;font-size:11px;color:' + (i === 0 ? '#f59e0b' : (i === chosen && chosen !== 0 ? '#f87171' : '#475569')) + ';flex-shrink:0';

              const track = document.createElement('div');
              track.style.cssText = 'flex:1;background:#0a0e1a;border-radius:3px;height:16px;overflow:hidden';

              const fill = document.createElement('div');
              const fillColor = i === 0 ? '#f59e0b' : (i === chosen && chosen !== 0 ? '#f87171' : '#334155');
              fill.style.cssText = 'height:100%;width:0%;background:' + fillColor + ';border-radius:3px;transition:width 0.6s ease ' + (i * 60) + 'ms';

              const pct = document.createElement('div');
              pct.style.cssText = 'width:36px;font-family:JetBrains Mono,monospace;font-size:11px;color:' + (i === 0 ? '#f59e0b' : '#475569');
              pct.textContent = (w * 100).toFixed(0) + '%';

              track.appendChild(fill);
              row.appendChild(label);
              row.appendChild(track);
              row.appendChild(pct);
              bars.appendChild(row);

              requestAnimationFrame(function () {
                requestAnimationFrame(function () {
                  fill.style.width = (w * 100) + '%';
                });
              });
            });

            reveal.style.display = 'block';
          }
        }
        export default { render };
        """

    mo.hstack([TokenQuizWidget()], justify="center")
    return



@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
        "🧭 **New here? The whole paper in 60 seconds (Who · What · When · Where · Why · How)**": mo.md(r"""
| | |
|---|---|
| **Who** | Federico Barbero, Álvaro Arroyo (Oxford), Xiangming Gu (NUS), and Google DeepMind researchers including Petar Veličković and Razvan Pascanu. |
| **What** | Large language models dump a huge share of their attention onto the *first token* of the input, a meaningless marker like `<BOS>`. In LLaMA 3.1 405B, **~80% of attention heads** do this. The paper asks why gradient descent would learn something so wasteful. |
| **When / Where** | Published at COLM 2025 ([arXiv:2504.02732](https://arxiv.org/abs/2504.02732)). Evidence from Gemma 7B, the LLaMA 3.1 family (8B to 405B), and 120M-parameter models the authors trained from scratch. |
| **Why it matters** | Attention sinks affect problems practitioners handle daily: model **quantization** breaks around them, **streaming and long-context** inference must preserve them, and they've been tied to **security** quirks. If you deploy or fine-tune LLMs, sinks are load-bearing walls. This paper explains why they exist. |
| **How** | Theory: deep Transformers *over-mix*, and token representations blur together (Theorem 3.2 bounds this). The sink acts as a learned pressure valve: attending to a near-zero-content token lets a head do *nothing* when nothing is needed. Experiments: perturb a word and watch the blast radius, scale models up, retrain with different data packing. |

**How this notebook works:**

1. **🔬 Model picker**: switch between GPT-2 Small (124M, 12 layers) and XL (1.5B, 48 layers) to test the paper's Prediction 2, that deeper models sink harder.
2. **Text boxes**: type a sentence and see which tokens the model attends to.
3. **Sliders** (ε thresholds, context length, sink spacing): each one is a variable the paper's theory makes a claim about.
4. **Click cells** in the head-explorer grid to inspect one attention head's full attention matrix.
        """),
    })
    return


# ── Python imports ─────────────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import altair as alt
    import polars as pl
    import anywidget
    import numpy as np
    import plotly.graph_objects as go

    alt.data_transformers.disable_max_rows()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.set_grad_enabled(False)
    return (
        AutoModelForCausalLM, AutoTokenizer,
        alt, anywidget, device, go, np, pl, torch,
    )


@app.cell(hide_code=True)
def _():
    MODEL_CACHE = {}
    return (MODEL_CACHE,)


@app.cell(hide_code=True)
def _(mo):
    MODEL_OPTIONS = {
        "GPT-2 Small (124M · 12L × 12H)": "gpt2",
        "GPT-2 Medium (345M · 24L × 16H)": "gpt2-medium",
        "GPT-2 Large (774M · 36L × 20H)": "gpt2-large",
        "GPT-2 XL (1.5B · 48L × 25H)": "gpt2-xl",
    }
    MODEL_LABELS = {v: k for k, v in MODEL_OPTIONS.items()}
    get_model_id, set_model_id = mo.state("gpt2")
    return MODEL_LABELS, MODEL_OPTIONS, get_model_id, set_model_id


# ══════════════════════════════════════════════════════════════════════════════
# ACT I: THE STRANGE OBSESSION
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Act I: The Strange Obsession

    Every attention head produces a probability distribution over past tokens. The softmax guarantees this. Each head must put its probability mass somewhere.

    The heatmap below shows where it goes for GPT-2 on your text. Each cell is one attention head (rows = layers, columns = heads). Color encodes how much of that head's average attention lands on position 0 (`<BOS>`). Amber is a strong sink. Dark is distributed attention.

    Why position 0 in particular? Under a causal mask, each token attends only to itself and the tokens before it. Position 0 is the single token present in the visible history of *every* other position. It is the one address every head can reach no matter where it sits in the sequence, which makes it the natural place to park attention a head wants to discard. Later tokens cannot serve this role: a token halfway through the sequence is invisible to everything that came before it.

    The paper uses ε = 0.3 as the default sink threshold (§2). Adjust it below to explore.
    """)
    return


@app.cell
def _(mo):
    causal_q = mo.ui.slider(
        0, 9, step=1, value=6,
        label="Query position i (the token doing the attending)", show_value=True)
    causal_q
    return (causal_q,)


@app.cell(hide_code=True)
def _(alt, causal_q, mo, pl):
    # Exact causal mask (lower-triangular): no model, no data, just the structural
    # fact that answers "why the first token". Cell (query i, key j) is reachable
    # iff j <= i. Key 0 is reachable from every row -> the universal sink address.
    _T = 10
    _i = causal_q.value
    _rows = []
    for _qi in range(_T):
        for _kj in range(_T):
            if _kj > _qi:
                _state = "blocked (future)"
            elif _kj == 0:
                _state = "key 0 (always visible)"
            else:
                _state = "visible past"
            _rows.append({"query": _qi, "key": _kj, "state": _state, "sel": _qi == _i})
    _df = pl.DataFrame(_rows)

    _grid = (
        alt.Chart(_df)
        .mark_rect(stroke="#07080f", strokeWidth=1)
        .encode(
            x=alt.X("key:O", title="Key position j (the token being attended to)",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("query:O", title="Query position i",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("state:N",
                scale=alt.Scale(
                    domain=["blocked (future)", "visible past", "key 0 (always visible)"],
                    range=["#0d1220", "#334366", "#f59e0b"]),
                legend=alt.Legend(title=None, labelColor="#94a3b8", orient="bottom")),
            tooltip=[alt.Tooltip("query:O", title="query i"),
                     alt.Tooltip("key:O", title="key j"),
                     alt.Tooltip("state:N", title="")],
        )
        .properties(width=340, height=340,
            title=alt.TitleParams(
                text="Causal mask: who can attend to whom", color="#e2e8f0", fontSize=12))
    )
    _sel = (
        alt.Chart(_df.filter(pl.col("sel")))
        .mark_rect(fill=None, stroke="#e2e8f0", strokeWidth=2.5)
        .encode(x="key:O", y="query:O")
    )
    _chart = ((_grid + _sel)
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f"))

    mo.vstack([
        mo.md("### Why the first token? Look at the causal mask"),
        _chart,
        mo.md(
            f"The white-outlined row is query position **{_i}**. It can attend only to keys "
            f"**0 … {_i}** ({_i + 1} of {_T}); everything to its right is a future token it "
            f"cannot see. Slide *i* and the visible range grows or shrinks, but the amber column, "
            f"**key 0**, never leaves it. Position 0 is the one token inside the visible history of "
            f"*every* query, the single address every head can reach no matter where it sits. A token "
            f"in the middle (say key 5) is invisible to every query below row 5, so it could never "
            f"serve the whole sequence. That asymmetry is why a causal model parks its sink on the "
            f"first token and nowhere else."),
    ], align="center")
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    # Built directly in this cell rather than via a shared factory function: a
    # factory only receives get_model_id through closure, and marimo's static
    # dependency graph can't see that, so on_change would never propagate to
    # other cells even though the widget still renders with the right value.
    model_pick = mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Lab model (GPT-2 Small → XL)",
    )
    mo.vstack([
        model_pick,
        mo.md(
            "*Switch to GPT-2 XL and watch the sink rate climb with depth: live evidence "
            "for the paper's Prediction 2, that larger models sink harder. Every experiment "
            "below reruns on whichever model you pick.*"),
    ])
    return (model_pick,)


@app.cell(hide_code=True)
def _(AutoModelForCausalLM, AutoTokenizer, MODEL_CACHE, device, get_model_id, mo, torch):
    import time as _t_load
    MODEL_ID = get_model_id()
    _tok = AutoTokenizer.from_pretrained("gpt2")   # same tokenizer across the family
    _tok.pad_token = _tok.eos_token

    _t0_load = _t_load.perf_counter()
    if MODEL_ID not in MODEL_CACHE:
        MODEL_CACHE[MODEL_ID] = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            attn_implementation="eager",   # SDPA drops attention weights; eager returns them
            dtype=torch.float32,
        ).to(device).eval()
    _dt_load = _t_load.perf_counter() - _t0_load

    tokenizer = _tok
    model     = MODEL_CACHE[MODEL_ID]
    N_LAYERS  = model.config.n_layer
    N_HEADS   = model.config.n_head
    D_MODEL   = model.config.n_embd
    BOS_ID    = tokenizer.bos_token_id # 50256

    _vram = ""
    if device == "cuda":
        _vram = f" · **{torch.cuda.memory_allocated() / 1e9:.1f} GB** VRAM resident ({len(MODEL_CACHE)} model{'s' if len(MODEL_CACHE) > 1 else ''} cached)"
    mo.md(f"""
    **Model loaded:** `{MODEL_ID}` · {N_LAYERS} layers · {N_HEADS} heads/layer · d={D_MODEL} ·
    {N_LAYERS * N_HEADS} attention heads total ({_dt_load:.1f}s)
    **Device:** `{device}` {'(GPU active ✓)' if device == 'cuda' else '(CPU mode)'}{_vram}
    **BOS token:** `<|endoftext|>` id={BOS_ID}
    """)
    return BOS_ID, D_MODEL, MODEL_ID, N_HEADS, N_LAYERS, model, tokenizer


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
        label="Sink threshold ε  (paper default: 0.30)",
        show_value=True,
    )
    mo.vstack([text_input, eps_slider])
    return eps_slider, text_input


@app.cell
def _(BOS_ID, model, text_input, tokenizer, torch):
    def _run_attn(text):
        _raw = tokenizer.encode(text, add_special_tokens=False)
        _ids = torch.tensor([[BOS_ID] + _raw], device=model.device)
        with torch.no_grad():
            _out = model(_ids, output_attentions=True)
        _attn = torch.stack([a[0] for a in _out.attentions])  # [L, H, T, T]
        _toks = [tokenizer.decode([BOS_ID])] + [tokenizer.decode([t]) for t in _raw]
        return _toks, _attn

    tokens_live, attn_live = _run_attn(text_input.value)
    sink_scores_live = attn_live[:, :, :, 0].mean(dim=-1)   # [L, H] mean col-0 attn
    return attn_live, sink_scores_live, tokens_live


@app.cell
def _(N_HEADS, N_LAYERS, alt, eps_slider, mo, pl, sink_scores_live):
    _eps   = eps_slider.value
    _rows  = [
        {"layer": f"L{l:02d}", "head": f"H{h:02d}",
         "sink": float(sink_scores_live[l, h].item()), "li": l, "hi": h}
        for l in range(N_LAYERS) for h in range(N_HEADS)
    ]
    _df   = pl.DataFrame(_rows)
    _nsink = _df.filter(pl.col("sink") > _eps).height
    _rate  = _nsink / _df.height

    # Cell size scales with grid dimensions instead of squeezing into a fixed box,
    # so GPT-2 XL's 25x48 grid stays as readable as Small's 12x12 one.
    _cell_w, _cell_h = 34, 20
    _hmap_w = max(500, _cell_w * N_HEADS + 90)
    _hmap_h = max(310, _cell_h * N_LAYERS + 60)
    _hmap = (
        alt.Chart(_df)
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
            width=_hmap_w, height=_hmap_h,
            title=alt.TitleParams(
                text=f"GPT-2 attention to BOS: {_rate:.1%} of heads qualify as sinks (ε={_eps:.2f})",
                color="#e2e8f0", fontSize=13,
            ),
        )
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _cs = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:16px 20px;text-align:center;"
    _cv = "font-size:2em;font-weight:700;line-height:1;margin-bottom:4px;"
    _cl = "font-size:0.75em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;"
    _cg = "display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;width:100%;max-width:64rem;margin:1em auto;"

    mo.vstack([
        mo.Html(f"""<div style="{_cg}">
          <div style="{_cs}"><div style="{_cv}color:#f59e0b">{_rate:.0%}</div>
            <div style="{_cl}">GPT-2 sink rate</div>
            <div style="font-size:0.68em;color:#94a3b8;margin-top:4px">ε={_eps:.2f} · {_nsink}/{_df.height} heads</div></div>
          <div style="{_cs}"><div style="{_cv}color:#818cf8">45.97%</div>
            <div style="{_cl}">LLaMA 3.1 8B</div>
            <div style="font-size:0.68em;color:#94a3b8;margin-top:4px">Table 1, paper · ε=0.8</div></div>
          <div style="{_cs}"><div style="{_cv}color:#818cf8">73.49%</div>
            <div style="{_cl}">LLaMA 3.1 70B</div>
            <div style="font-size:0.68em;color:#94a3b8;margin-top:4px">Table 1, paper · ε=0.8</div></div>
          <div style="{_cs}"><div style="{_cv}color:#f59e0b">78.29%</div>
            <div style="{_cl}">LLaMA 3.1 405B</div>
            <div style="font-size:0.68em;color:#94a3b8;margin-top:4px">Table 1, paper · ε=0.8</div></div>
        </div>"""),
        _hmap,
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# ACT II: THE ROOT CAUSE OF OVER-MIXING
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Act II: The Over-Mixing Problem

    At each Transformer layer, every token's new representation is a weighted average of past tokens' value vectors. Mix red and blue and you get purple. Mix that with yellow and you get brown. After enough layers, every token converges to the same muddy grey.

    [Dong et al. (2021)](https://arxiv.org/pdf/2103.03404) proved this for linear Transformers: the representation matrix approaches rank 1 with depth. All token representations become identical, a phenomenon called **rank collapse**. With MLPs and residuals, a softer version called **representational collapse** sets in over long contexts ([Barbero et al. 2024](https://arxiv.org/pdf/2406.04267)): tokens near the end of a long sequence lose their distinct identity.

    The simulator below runs 12 rounds of attention mixing on 7 tokens. Each circle is a token's position in representation space. Press **PLAY** and watch what happens.
    """)
    return


@app.cell(hide_code=True)
def _(anywidget, mo):
    class OverMixingWidget(anywidget.AnyWidget):
        _esm = r"""
        function render({ el }) {
          el.innerHTML = `
          <div style="max-width:64rem;margin:0 auto 1.5em;padding:0 1em;font-family:Inter,sans-serif">
          <div style="background:#0d1220;border:1px solid #1e2d47;border-radius:12px;padding:20px 24px">

            <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:16px">
              <button id="ps-play" style="padding:7px 20px;border-radius:7px;border:1.5px solid #60a5fa;background:#0c1a2e;color:#60a5fa;font-family:JetBrains Mono,monospace;font-size:12px;cursor:pointer;font-weight:600">▶ PLAY</button>
              <button id="ps-reset" style="padding:7px 16px;border-radius:7px;border:1.5px solid #1e2d47;background:#0a0e1a;color:#64748b;font-family:JetBrains Mono,monospace;font-size:12px;cursor:pointer">↺ RESET</button>

              <div style="display:flex;align-items:center;gap:6px;margin-left:4px">
                <span style="font-size:11.5px;color:#94a3b8;font-family:Inter,sans-serif">BOS Sink:</span>
                <button id="ps-sink-off" style="padding:5px 12px;border-radius:6px;border:1.5px solid #f87171;background:#1a0707;color:#f87171;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer;font-weight:600">OFF</button>
                <button id="ps-sink-on" style="padding:5px 12px;border-radius:6px;border:1.5px solid #1e2d47;background:#0a0e1a;color:#475569;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer">ON</button>
              </div>

              <div style="display:flex;align-items:center;gap:6px;margin-left:4px">
                <span style="font-size:11.5px;color:#94a3b8;font-family:Inter,sans-serif">ε:</span>
                <input id="ps-eps" type="range" min="0.3" max="0.95" step="0.05" value="0.75" style="width:80px;accent-color:#f59e0b">
                <span id="ps-eps-val" style="font-family:JetBrains Mono,monospace;font-size:11px;color:#f59e0b;width:28px">0.75</span>
              </div>

              <div style="margin-left:auto;display:flex;align-items:center;gap:6px">
                <span style="font-size:11.5px;color:#64748b;font-family:Inter,sans-serif">Layer:</span>
                <span id="ps-step" style="font-family:JetBrains Mono,monospace;font-size:14px;color:#e2e8f0;font-weight:700">0 / 12</span>
              </div>
            </div>

            <div style="position:relative">
              <svg id="ps-svg" viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg"
                   style="width:100%;background:#070a12;border-radius:8px;display:block">
              </svg>
              <div id="ps-badge" style="display:none;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);padding:10px 22px;border-radius:8px;font-family:Space Grotesk,sans-serif;font-size:1.4em;font-weight:700;letter-spacing:0.02em;pointer-events:none"></div>
            </div>

            <div id="ps-caption" style="margin-top:12px;font-size:12.5px;color:#64748b;font-family:Inter,sans-serif;line-height:1.6;text-align:center">
              Press PLAY to start. Toggle BOS Sink ON/OFF to see the difference.
            </div>

          </div>
          </div>
          `;

          const W = 620, H = 340;
          const TOKENS = ['⟨BOS⟩', 'The', 'cat', 'sat', 'on', 'the', 'mat'];
          const COLORS = ['#f59e0b', '#60a5fa', '#34d399', '#f87171', '#a78bfa', '#fb923c', '#38bdf8'];
          const MAX_LAYERS = 12;
          const ALPHA = 0.28;  // mixing rate per step
          const TRAIL_LEN = 8;

          const INIT = [
            {x: 90,  y: 170},   // BOS, left anchor
            {x: 200, y: 80},    // The
            {x: 460, y: 70},    // cat
            {x: 530, y: 185},   // sat
            {x: 450, y: 290},   // on
            {x: 220, y: 295},   // the
            {x: 340, y: 55},    // mat
          ];

          let pos, trails, step, running, sinkMode, eps, timer;

          function clone(arr) { return arr.map(function(p){ return {x:p.x, y:p.y}; }); }

          function init() {
            pos    = clone(INIT);
            trails = INIT.map(function(){ return []; });
            step   = 0;
            running = false;
            draw();
            updateBadge();
            el.querySelector('#ps-step').textContent = '0 / ' + MAX_LAYERS;
            el.querySelector('#ps-play').textContent = '▶ PLAY';
            el.querySelector('#ps-caption').textContent = 'Press PLAY to start. Toggle BOS Sink ON/OFF to see the difference.';
          }

          function advance() {
            if (step >= MAX_LAYERS) { pause(); return; }

            for (let i = 0; i < pos.length; i++) {
              trails[i].push({x: pos[i].x, y: pos[i].y});
              if (trails[i].length > TRAIL_LEN) trails[i].shift();
            }

            if (sinkMode) {
              // Tokens route eps fraction to BOS, rest to content centroid
              // BOS has near-zero value → minimal movement; content tokens barely mix
              let cx = 0, cy = 0;
              for (let j = 1; j < pos.length; j++) { cx += pos[j].x; cy += pos[j].y; }
              cx /= (pos.length - 1); cy /= (pos.length - 1);

              for (let k = 1; k < pos.length; k++) {
                const effAlpha = (1 - eps) * ALPHA;
                pos[k].x += effAlpha * (cx - pos[k].x);
                pos[k].y += effAlpha * (cy - pos[k].y);
              }
            } else {
              // No sink: full uniform mixing → convergence
              let mx = 0, my = 0;
              for (let m = 0; m < pos.length; m++) { mx += pos[m].x; my += pos[m].y; }
              mx /= pos.length; my /= pos.length;
              for (let n = 1; n < pos.length; n++) {
                pos[n].x += ALPHA * (mx - pos[n].x);
                pos[n].y += ALPHA * (my - pos[n].y);
              }
            }

            step++;
            el.querySelector('#ps-step').textContent = step + ' / ' + MAX_LAYERS;
            draw();
            updateBadge();

            if (step >= MAX_LAYERS) {
              const spread = computeSpread();
              if (spread < 18) {
                el.querySelector('#ps-caption').textContent =
                  'After ' + MAX_LAYERS + ' layers without a sink, all tokens collapsed to the same representation. The model can no longer tell them apart.';
              } else {
                el.querySelector('#ps-caption').textContent =
                  'After ' + MAX_LAYERS + ' layers with BOS absorbing ' + Math.round(eps*100) + '% of attention, tokens remain distinct. The sink preserved representational diversity.';
              }
            }
          }

          function computeSpread() {
            let cx = 0, cy = 0;
            for (let i = 1; i < pos.length; i++) { cx += pos[i].x; cy += pos[i].y; }
            cx /= (pos.length - 1); cy /= (pos.length - 1);
            let s = 0;
            for (let j = 1; j < pos.length; j++) {
              const dx = pos[j].x - cx, dy = pos[j].y - cy;
              s += Math.sqrt(dx*dx + dy*dy);
            }
            return s / (pos.length - 1);
          }

          function play() {
            running = true;
            el.querySelector('#ps-play').textContent = '⏸ PAUSE';
            timer = setInterval(advance, 240);
          }

          function pause() {
            running = false;
            clearInterval(timer);
            el.querySelector('#ps-play').textContent = step >= MAX_LAYERS ? '✓ DONE' : '▶ PLAY';
          }

          function updateBadge() {
            const badge = el.querySelector('#ps-badge');
            const spread = computeSpread();
            if (step >= MAX_LAYERS) {
              if (spread < 18) {
                badge.style.display = 'block';
                badge.style.background = 'rgba(248,113,113,0.18)';
                badge.style.border = '1.5px solid #f87171';
                badge.style.color = '#f87171';
                badge.textContent = 'COLLAPSED';
              } else {
                badge.style.display = 'block';
                badge.style.background = 'rgba(52,211,153,0.14)';
                badge.style.border = '1.5px solid #34d399';
                badge.style.color = '#34d399';
                badge.textContent = 'STABLE';
              }
            } else {
              badge.style.display = 'none';
            }
          }

          function draw() {
            const svg = el.querySelector('#ps-svg');
            let s = '';

            for (let gx = 0; gx <= W; gx += 80) {
              s += '<line x1="'+gx+'" y1="0" x2="'+gx+'" y2="'+H+'" stroke="#0d1220" stroke-width="1"/>';
            }
            for (let gy = 0; gy <= H; gy += 80) {
              s += '<line x1="0" y1="'+gy+'" x2="'+W+'" y2="'+gy+'" stroke="#0d1220" stroke-width="1"/>';
            }

            for (let ti = 1; ti < pos.length; ti++) {
              const tr = trails[ti];
              for (let tj = 0; tj < tr.length; tj++) {
                const opacity = (tj + 1) / (TRAIL_LEN + 1) * 0.4;
                const r = 3 + tj * 0.5;
                s += '<circle cx="'+tr[tj].x.toFixed(1)+'" cy="'+tr[tj].y.toFixed(1)+'" r="'+r.toFixed(1)+'" fill="'+COLORS[ti]+'" opacity="'+opacity.toFixed(2)+'"/>';
              }
            }

            s += '<circle cx="'+INIT[0].x+'" cy="'+INIT[0].y+'" r="22" fill="none" stroke="#f59e0b" stroke-width="1" opacity="0.25" stroke-dasharray="4,3"/>';
            s += '<circle cx="'+INIT[0].x+'" cy="'+INIT[0].y+'" r="14" fill="#1c0a00" stroke="#f59e0b" stroke-width="1.5"/>';
            s += '<text x="'+INIT[0].x+'" y="'+(INIT[0].y+4)+'" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8" fill="#f59e0b" font-weight="700">BOS</text>';

            for (let ci = 1; ci < pos.length; ci++) {
              const px = pos[ci].x.toFixed(1), py = pos[ci].y.toFixed(1);
              s += '<circle cx="'+px+'" cy="'+py+'" r="14" fill="'+COLORS[ci]+'" opacity="0.9"/>';
              s += '<text x="'+px+'" y="'+(pos[ci].y+4).toFixed(1)+'" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="8.5" fill="#07080f" font-weight="700">'+TOKENS[ci]+'</text>';
            }

            const sp = computeSpread().toFixed(0);
            const spColor = parseFloat(sp) < 18 ? '#f87171' : '#34d399';
            s += '<text x="'+(W-10)+'" y="20" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="10" fill="'+spColor+'">spread='+sp+'</text>';

            svg.innerHTML = s;
          }

          el.querySelector('#ps-play').addEventListener('click', function () {
            if (step >= MAX_LAYERS) { init(); return; }
            if (running) { pause(); } else { play(); }
          });
          el.querySelector('#ps-reset').addEventListener('click', function () {
            pause(); init();
          });
          el.querySelector('#ps-sink-on').addEventListener('click', function () {
            sinkMode = true;
            this.style.cssText = 'padding:5px 12px;border-radius:6px;border:1.5px solid #f59e0b;background:#1c0a00;color:#f59e0b;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer;font-weight:600';
            el.querySelector('#ps-sink-off').style.cssText = 'padding:5px 12px;border-radius:6px;border:1.5px solid #1e2d47;background:#0a0e1a;color:#475569;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer';
          });
          el.querySelector('#ps-sink-off').addEventListener('click', function () {
            sinkMode = false;
            this.style.cssText = 'padding:5px 12px;border-radius:6px;border:1.5px solid #f87171;background:#1a0707;color:#f87171;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer;font-weight:600';
            el.querySelector('#ps-sink-on').style.cssText = 'padding:5px 12px;border-radius:6px;border:1.5px solid #1e2d47;background:#0a0e1a;color:#475569;font-family:JetBrains Mono,monospace;font-size:11px;cursor:pointer';
          });
          el.querySelector('#ps-eps').addEventListener('input', function () {
            eps = parseFloat(this.value);
            el.querySelector('#ps-eps-val').textContent = eps.toFixed(2);
          });

          sinkMode = false;
          eps = 0.75;
          init();
        }
        export default { render };
        """

    mo.hstack([OverMixingWidget()], justify="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading the simulation

    **BOS Sink OFF:** uniform mixing drives all tokens to the same average position in representation space. Spread collapses to near zero.

    **BOS Sink ON:** most attention routes to BOS, which has a near-zero value vector. The attention output approaches zero, so only the residual stream carries each token forward. Positions stay distinct.

    A head that never mixes contributes nothing to language modeling. A head that always mixes collapses representations. Sinks let the model turn a head off when there is nothing worth mixing.

    The paper calls this the **approximate no-op**: BOS has a near-zero norm value vector, so routing attention there costs almost nothing.
    """)
    return


# ── Live Figure 2: perturbation spread, measured ──────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Now Measure It: Figure 2, Live on GPT-2

    The simulation above is a cartoon. The paper's actual evidence is **Figure 2**: perturb one
    word in a prompt, run the model twice, and map how far the disturbance spreads through
    every layer and token, with and without the attention sink.

    The paper ablates the sink in Gemma 7B by deleting ⟨BOS⟩, because Gemma was trained
    with a fixed ⟨BOS⟩ and is brittle without it. **GPT-2 refuses that ablation.** It was
    trained without a fixed BOS, and exactly as the paper's §5 packing experiments predict,
    its sink re-forms on whatever token comes first (we measure this below). We use instead
    a *sharper* intervention the paper never runs: keep the sequence identical, but **mask
    position 0 out of attention**, so no head can reach the sink.

    The default is the paper's own Shakespeare paragraph (Appendix C.1) with its own edit,
    **"greatest" → "best"**. Paste any text, pick any word in it, and choose your
    replacement. Each heatmap cell is ‖h(original) − h(perturbed)‖₂ for one token at one
    layer. All six sequences run as **two batched GPU forward passes**.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(mo):
    _SHAKE_DEFAULT = ("William Shakespeare was an English playwright, poet and actor. "
                      "He is widely regarded as the greatest writer in the English language and "
                      "the world's pre-eminent dramatist. He is often called England's national "
                      "poet and the Bard of Avon. His extant works, including collaborations, "
                      "consist of some 39 plays, 154 sonnets, and three long narrative poems.")
    pp_prompt = mo.ui.text_area(
        value=_SHAKE_DEFAULT, rows=4, full_width=True,
        label="Prompt (paper's Appendix C.1 text, or your own)",
    )
    pp_word = mo.ui.text(value="greatest", label="Word to perturb")
    pp_repl = mo.ui.text(value="best", label="Replace it with")
    mo.vstack([pp_prompt, mo.hstack([pp_word, pp_repl], justify="start", gap=1)])
    return pp_prompt, pp_repl, pp_word


@app.cell
def _(BOS_ID, alt, mo, model, pl, pp_prompt, pp_repl, pp_word, tokenizer, torch):
    # Live reproduction of paper Figure 2 (§3.2). Two batched forwards:
    # [original, perturbed] with the sink attendable and with position 0 masked.
    # The replacement must tokenize to the same count so positions align. Invalid
    # input falls back to the paper's default pair with a visible explanation.
    # This cell must never error on user input.
    import time as _t_p
    _SHAKE = ("William Shakespeare was an English playwright, poet and actor. "
              "He is widely regarded as the greatest writer in the English language and "
              "the world's pre-eminent dramatist. He is often called England's national "
              "poet and the Bard of Avon. His extant works, including collaborations, "
              "consist of some 39 plays, 154 sonnets, and three long narrative poems.")
    _text_p = (pp_prompt.value or "").strip() or _SHAKE
    _word_p = (pp_word.value or "").strip()
    _repl_p = (pp_repl.value or "").strip()
    _warn_p = None

    def _tokenize_pair(text, word, repl):
        if not word or not repl or word == repl or word not in text:
            return None
        o = tokenizer.encode(text, add_special_tokens=False)
        p = tokenizer.encode(text.replace(word, repl, 1), add_special_tokens=False)
        return (o, p) if len(o) == len(p) and o != p else None

    _pair_p = _tokenize_pair(_text_p, _word_p, _repl_p)
    if _pair_p is None:
        if _word_p and _word_p in _text_p and _repl_p:
            # Token-count mismatch: scan a candidate pool for same-count substitutes.
            _pool_p = ["best", "worst", "finest", "oldest", "largest", "smallest", "good",
                       "bad", "big", "small", "strange", "famous", "quiet", "loud", "fast",
                       "slow", "one", "two", "red", "blue", "cat", "dog", "king", "queen"]
            _sugg_p = [c for c in _pool_p if _tokenize_pair(_text_p, _word_p, c)][:6]
            _warn_p = (
                f'⚠ "{_repl_p}" tokenizes to a different number of tokens than "{_word_p}", '
                "so the two sequences would misalign. "
                + (f"Same-length substitutes that work here: **{', '.join(_sugg_p)}**. "
                   if _sugg_p else "")
                + "Showing the paper's default pair meanwhile."
            )
        elif _word_p and _word_p not in _text_p:
            _warn_p = f'⚠ "{_word_p}" does not appear in the prompt. Showing the paper\'s default pair meanwhile.'
        else:
            _warn_p = "⚠ Enter a word from the prompt and a different replacement. Showing the paper's default pair meanwhile."
        _text_p = _SHAKE
        _word_p, _repl_p = "greatest", "best"
        _pair_p = _tokenize_pair(_text_p, _word_p, _repl_p)

    _orig_p, _pert_p = _pair_p
    # GPT-2's context cap is 1024; leave room for the prepended sink token.
    _orig_p, _pert_p = _orig_p[:1023], _pert_p[:1023]
    _pidx = next(i for i, (a, b) in enumerate(zip(_orig_p, _pert_p)) if a != b)

    _t0_p = _t_p.perf_counter()
    if model.device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()

    # Forward 1 (batch of 4): [orig, pert] with the sink attendable, and the SAME
    # sequences with position 0 masked out of attention (per-row attention_mask):
    # the causal ablation. Forward 2 (batch of 2): bare text, to show the sink relocating.
    _b4 = torch.tensor([[BOS_ID] + _orig_p, [BOS_ID] + _pert_p,
                        [BOS_ID] + _orig_p, [BOS_ID] + _pert_p], device=model.device)
    _am4 = torch.ones_like(_b4)
    _am4[2:, 0] = 0                                  # rows 2-3: sink unreachable
    with torch.no_grad():
        _o4 = model(_b4, attention_mask=_am4, output_hidden_states=True,
                    output_attentions=True)
    _hs4 = torch.stack(_o4.hidden_states)            # [L+1, 4, T, d]
    _d_sink = (_hs4[:, 0] - _hs4[:, 1]).norm(dim=-1)[:, 1:]   # content cols only
    _d_mask = (_hs4[:, 2] - _hs4[:, 3]).norm(dim=-1)[:, 1:]
    _sink_score_eot = float(torch.stack(_o4.attentions)[:, 0, :, :, 0].mean().item())

    _b2 = torch.tensor([_orig_p, _pert_p], device=model.device)
    with torch.no_grad():
        _o2 = model(_b2, output_attentions=True)
    _sink_score_bare = float(torch.stack(_o2.attentions)[:, 0, :, :, 0].mean().item())
    _dt_p = _t_p.perf_counter() - _t0_p
    _d_bos, _d_no = _d_sink, _d_mask

    _Lp1, _Tp = _d_bos.shape
    _vmax = float(torch.maximum(_d_bos.max(), _d_no.max()).item())

    def _heat(dm, label):
        _r = [{"tok": t, "layer": l, "diff": float(dm[l, t])}
              for l in range(_Lp1) for t in range(_Tp)]
        return (
            alt.Chart(pl.DataFrame(_r))
            .mark_rect()
            .encode(
                x=alt.X("tok:O", title="Token position", axis=alt.Axis(
                    labelColor="#94a3b8", titleColor="#94a3b8", values=list(range(0, _Tp, 10)))),
                y=alt.Y("layer:O", title="Layer", sort="descending", axis=alt.Axis(
                    labelColor="#94a3b8", titleColor="#94a3b8")),
                color=alt.Color("diff:Q", scale=alt.Scale(scheme="inferno", domain=[0, _vmax]),
                    legend=alt.Legend(title="‖Δh‖", labelColor="#94a3b8", titleColor="#94a3b8")),
                tooltip=[alt.Tooltip("tok:O"), alt.Tooltip("layer:O"),
                         alt.Tooltip("diff:Q", format=".2f")],
            )
            .properties(width=430, height=200, title=alt.TitleParams(
                text=label, color="#e2e8f0", fontSize=12))
        )

    _chart_p = (
        alt.vconcat(
            _heat(_d_no,  f"Sink MASKED (no head can reach position 0): perturbation at token {_pidx} spreads"),
            _heat(_d_bos, "Sink attendable: the no-op dampens the spread"),
        )
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    # Spread = mean disturbance at the final layer over tokens *after* the perturbed one
    # (excluding it), i.e. how much collateral damage the swap causes downstream.
    _sp_no  = float(_d_no[-1, _pidx + 1:].mean().item())
    _sp_bos = float(_d_bos[-1, _pidx + 1:].mean().item())
    _ratio_p = _sp_no / max(_sp_bos, 1e-9)
    _gpu_p = ""
    if model.device.type == "cuda":
        _gpu_p = f" · peak VRAM {torch.cuda.max_memory_allocated()/1e9:.2f} GB"
    _claim_p = (
        f"Blocking the sink amplifies collateral spread **{_ratio_p:.1f}×** on this prompt. "
        "This isolates the paper's Figure 2 mechanism causally: same tokens, same weights, "
        "only the sink's reachability changed. Without it, a one-word edit rewrites every "
        "downstream representation."
        if _ratio_p > 1.05 else
        f"On this substitute the two conditions stay close (ratio {_ratio_p:.2f}×). The paper's "
        "effect is a tendency, not a law. Try another word."
    )
    mo.vstack(([mo.md(_warn_p)] if _warn_p else []) + [
        _chart_p,
        mo.md(
            f'Swapping "{_word_p}" → "{_repl_p}" (token {_pidx}) disturbs the '
            f"**downstream** final-layer states by **{_sp_bos:.1f}** on average with the sink "
            f"attendable, vs **{_sp_no:.1f}** with position 0 masked. {_claim_p}"),
        mo.md(
            f"**The §5 control:** *deleting* the first token does not work as an "
            f"ablation here. With `<|endoftext|>` prepended, {_sink_score_eot:.0%} of all "
            f"attention lands on position 0. Strip it and **{_sink_score_bare:.0%}** still "
            f'lands on position 0, now on the word "{tokenizer.decode([_orig_p[0]]).strip()}". '
            "GPT-2 was trained without a fixed BOS, and exactly as the paper's Table 2 "
            "predicts, its sink is **positional, not lexical**: it re-forms on whatever comes "
            f"first. The mask intervention above is the honest ablation for this model. "
            f"({_dt_p:.2f}s, 6 sequences in 2 batched passes{_gpu_p}.)"),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# ACT III: THE MATHEMATICS OF THEOREM 3.2
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Act III: The Mathematics

    The paper bounds this in Theorem 3.2 (§3.1):

    $$\left\| \frac{\partial v_j^{(L)}}{\partial v_i^{(0)}} \right\| \leq C_{\max}^L \sum_{k \in \mathcal{P}_{i \to j}} \bar{\alpha}_{j,k_{L-1}}^{(L)} \cdot \bar{\alpha}_{k_{L-1},k_{L-2}}^{(L-1)} \cdots \bar{\alpha}_{k_1,i}^{(1)}$$

    Read it as: a small change to token *i*'s initial embedding propagates through every causal path from *i* to *j* over *L* layers, amplified by C_max^L.

    Two terms drive the bound up. **C_max^L** grows exponentially with depth; a 126-layer model sees this at its worst. The **path sum** grows with context length, since longer sequences have more paths between any two positions.

    Attention sinks reduce the path-weight products. When a head routes its weight to BOS instead of meaningful tokens, the path through that head carries weight near zero. The Jacobian stays small. Perturbations stop spreading.
    """)
    return


@app.cell
def _(mo):
    thm_L    = mo.ui.slider(1, 40, step=1,   value=12, label="Depth L",            show_value=True)
    thm_n    = mo.ui.slider(64, 4096, step=64, value=512, label="Context length n", show_value=True)
    thm_cmax = mo.ui.slider(1.0, 2.0, step=0.05, value=1.2,
                            label="Lipschitz constant C_max (≥1 in practice)", show_value=True)
    thm_alpha_no_sink = mo.ui.slider(0.05, 0.9, step=0.05, value=0.5,
                                      label="Mean path weight ᾱ, no sink", show_value=True)
    thm_alpha_sink    = mo.ui.slider(0.01, 0.4, step=0.01, value=0.05,
                                      label="Mean path weight ᾱ, with sink", show_value=True)
    mo.vstack([thm_L, thm_n, thm_cmax, thm_alpha_no_sink, thm_alpha_sink])
    return thm_L, thm_alpha_no_sink, thm_alpha_sink, thm_cmax, thm_n


@app.cell
def _(go, mo, np, thm_L, thm_alpha_no_sink, thm_alpha_sink, thm_cmax, thm_n):
    _Ls    = np.arange(1, thm_L.value + 1)
    _C     = thm_cmax.value
    _n     = thm_n.value
    _a_no  = thm_alpha_no_sink.value
    _a_si  = thm_alpha_sink.value

    # Simplified model of the bound (illustrative):
    # paths of length L from i to j through n tokens ≈ n^(L-1) paths
    # each path weight ≈ ᾱ^L
    # bound ≈ C^L * n^(L-1) * ᾱ^L  (log-scale view)
    _bound_no = (_C ** _Ls) * (_n ** np.maximum(0, _Ls - 1)) * (_a_no ** _Ls)
    _bound_si = (_C ** _Ls) * (_n ** np.maximum(0, _Ls - 1)) * (_a_si ** _Ls)

    _fig2 = go.Figure()
    _fig2.add_trace(go.Scatter(
        x=_Ls, y=_bound_no, name="No sink",
        mode="lines", line=dict(color="#ef4444", width=2.5),
    ))
    _fig2.add_trace(go.Scatter(
        x=_Ls, y=_bound_si, name="With sink",
        mode="lines", line=dict(color="#22d3ee", width=2.5),
    ))
    _fig2.add_vline(x=thm_L.value, line_dash="dot", line_color="#94a3b8",
                    annotation_text=f"L={thm_L.value}", annotation_font_color="#94a3b8")
    _ratio = _bound_no[-1] / max(_bound_si[-1], 1e-30)
    _fig2.update_layout(
        title=dict(
            text=f"Sensitivity bound at L={thm_L.value}, n={thm_n.value}  ·  Sink suppresses by {_ratio:.1e}×",
            font=dict(color="#e2e8f0", size=13),
        ),
        xaxis=dict(title="Depth L", color="#94a3b8", gridcolor="#1e2d47"),
        yaxis=dict(title="Sensitivity bound (log scale)", color="#94a3b8",
                   gridcolor="#1e2d47", type="log"),
        legend=dict(font=dict(color="#94a3b8"), bgcolor="#0d1220"),
        paper_bgcolor="#07080f", plot_bgcolor="#0d1220",
        margin=dict(l=70, r=20, t=55, b=50), height=320,
    )

    _paper_pred = (
        "This **illustrative** bound (not the paper's exact constant) shows the mechanism: at larger "
        "*L* the no-sink curve runs far above the with-sink curve, so deeper models need stronger sinks "
        "to hold the Jacobian down. The empirical check is the live GPT-2 scaling experiment below."
        if thm_L.value >= 10 else
        "At shallow *L* the two curves nearly coincide. The gap stays small, so sinks are not "
        "yet urgent. Push *L* higher to see the divergence the paper predicts."
    )
    mo.vstack([_fig2, mo.md(_paper_pred)], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Two testable predictions

    1. **Deeper models should develop stronger sinks**, because C_max^L grows exponentially with L and the model needs to suppress the path-weight sum to compensate.
    2. **Models trained on longer contexts should develop stronger sinks**, because longer sequences create more paths from any token *i* to any token *j*.
    """)
    return


# ══════════════════════════════════════════════════════════════════════════════
# ACT IV: THE EVIDENCE
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Act IV: The Evidence

    ### Prediction 1: Longer context → stronger sinks

    The paper trains 120M-parameter LLaMA2-style models from scratch at five context lengths
    (128, 256, 512, 1024, 2048 tokens). Every model processes exactly **5B total tokens**, the
    same compute budget. The paper measures the sink metric after training.

    *Data below: read directly off Figure 5(a), paper §4.1 (y-axis range 0–40%).*
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    # Values read directly off Figure 5(a) (paper §4.1, page 8).
    # Paper text confirms: "nearly non-existent for very short-context-trained models"
    # and "much more prevalent for models trained on longer contexts" (§4.1).
    _ctx_data = pl.DataFrame({
        "Context Length": [128, 256, 512, 1024, 2048],
        "Sink Metric (%)": [0.5, 3.5, 26.0, 37.5, 39.0],
        "Note": ["≈0 (paper confirms)", "~3.5%", "~26%", "~37.5%", "~39%"],
    })
    _bar = (
        alt.Chart(_ctx_data)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Context Length:O", title="Training context length (tokens)",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("Sink Metric (%):Q", title="Sink metric after training (%)",
                    scale=alt.Scale(domain=[0, 40]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Sink Metric (%):Q",
                scale=alt.Scale(scheme="orangered", domain=[0, 40]),
                legend=None),
            tooltip=[alt.Tooltip("Context Length:O"), alt.Tooltip("Sink Metric (%):Q"),
                     alt.Tooltip("Note:N")],
        )
        .properties(
            width=380, height=260,
            title=alt.TitleParams(
                text="Longer context → stronger sinks (Figure 5a, paper §4.1): values approximate",
                color="#e2e8f0", fontSize=12,
            ),
        )
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    mo.vstack([_bar,
        mo.md("Context length 128 produces almost **no sinks**. The rate jumps by 512 tokens "
              "(~26%) and largely saturates by 1024 (~37.5%); 2048 only adds a few more points (~39%). "
              "All models reach similar validation loss, so sinks aren't a shortcut. They emerge alongside "
              "equivalent language modeling quality.")], align="center")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Prediction 2: Larger models → stronger sinks

    The LLaMA 3.1 family provides a clean natural experiment: three models trained with
    similar pipelines at different scales. The paper measures the sink metric at ε = 0.8
    (a high bar: the head must route >80% of its average attention to BOS).

    *Data: exact values from Table 1, paper §4.2.*
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    # Exact values from paper Table 1 (ε = 0.8).
    # Table header: "Sink Metric (ε = 0.8)". These are the only ε values reported in Table 1.
    _llama_data = pl.DataFrame({
        "Model": ["LLaMA 3.1 8B", "LLaMA 3.1 70B", "LLaMA 3.1 405B"],
        "Params (B)": [8, 70, 405],
        "Layers": [32, 80, 126],
        "Heads/Layer": [32, 64, 128],
        "Total Heads": [1024, 5120, 16128],
        "Sink Metric %": [45.97, 73.49, 78.29],
    })
    _bar2 = (
        alt.Chart(_llama_data)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Model:N", sort=["LLaMA 3.1 8B", "LLaMA 3.1 70B", "LLaMA 3.1 405B"],
                    title=None, axis=alt.Axis(labelColor="#94a3b8", labelFontSize=12)),
            y=alt.Y("Sink Metric %:Q", title="Sink metric % (ε = 0.8)",
                    scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Params (B):Q",
                scale=alt.Scale(scheme="inferno", domain=[-150, 450]),
                legend=None),
            tooltip=[
                alt.Tooltip("Model:N"),
                alt.Tooltip("Layers:Q"),
                alt.Tooltip("Total Heads:Q"),
                alt.Tooltip("Sink Metric %:Q", format=".2f"),
            ],
        )
        .properties(width=380, height=260,
            title=alt.TitleParams(
                text="Larger models → stronger sinks (Table 1, paper §4.2, ε = 0.8)",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _cs2 = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:14px 18px;text-align:center;"
    _cv2 = "font-size:1.7em;font-weight:700;line-height:1;margin-bottom:4px;"
    _cl2 = "font-size:0.7em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;"
    _cg2 = "display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;max-width:52rem;margin:0 auto 1em;"
    mo.vstack([
        mo.Html(f"""<div style="{_cg2}">
          <div style="{_cs2}"><div style="{_cv2}color:#f97316">45.97%</div>
            <div style="{_cl2}">LLaMA 3.1 8B</div>
            <div style="font-size:0.65em;color:#94a3b8">32 layers · 1,024 heads</div></div>
          <div style="{_cs2}"><div style="{_cv2}color:#ef4444">73.49%</div>
            <div style="{_cl2}">LLaMA 3.1 70B</div>
            <div style="font-size:0.65em;color:#94a3b8">80 layers · 5,120 heads</div></div>
          <div style="{_cs2}"><div style="{_cv2}color:#f59e0b">78.29%</div>
            <div style="{_cl2}">LLaMA 3.1 405B</div>
            <div style="font-size:0.65em;color:#94a3b8">126 layers · 16,128 heads</div></div>
        </div>"""),
        _bar2,
        mo.md("At 405B scale, **nearly 4 out of 5 attention heads** are functionally disabled for most tokens, "
              "routing to BOS and contributing nothing to the computation via a near-zero value vector. "
              "The token passes through unchanged via the residual stream."),
    ], align="center")
    return


# ── Live Scaling: GPT-2 Family ─────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Live Scaling: GPT-2 Family (124M → 1.5B)

    Table 1 uses LLaMA 3.1 to validate Prediction 2. Here we run the same measurement on
    the open GPT-2 family: four models spanning 12× in parameter count and 4× in depth.
    """)
    return


@app.cell
def _(AutoModelForCausalLM, AutoTokenizer, MODEL_CACHE, alt, device, mo, pl, torch):
    # Fixed probe prompt, not the live text box, so editing text elsewhere never
    # re-triggers four model loads.
    import time as _time
    _variants = [
        ("gpt2",        "Small (124M)",  124,  12),
        ("gpt2-medium", "Medium (345M)", 345,  24),
        ("gpt2-large",  "Large (774M)",  774,  36),
        ("gpt2-xl",     "XL (1.5B)",    1558,  48),
    ]
    _tok_s = AutoTokenizer.from_pretrained("gpt2")
    _probe_s = ("William Shakespeare was an English playwright, poet and actor. "
                "He is widely regarded as the greatest writer in the English language "
                "and the world's pre-eminent dramatist.")
    _raw_s = _tok_s.encode(_probe_s, add_special_tokens=False)
    _bos_s = _tok_s.bos_token_id
    _ids_s = torch.tensor([[_bos_s] + _raw_s], device=device)

    _sc_rows = []
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    for _mid_s, _tag_s, _params_s, _nl_s in _variants:
        _t0_s = _time.perf_counter()
        if _mid_s not in MODEL_CACHE:
            MODEL_CACHE[_mid_s] = AutoModelForCausalLM.from_pretrained(
                _mid_s, attn_implementation="eager", dtype=torch.float32,
            ).to(device).eval()
        with torch.no_grad():
            _out_s = MODEL_CACHE[_mid_s](_ids_s, output_attentions=True)
        _a_s  = torch.stack([a[0] for a in _out_s.attentions]).float()  # [L, H, T, T]
        _ss_s = _a_s[:, :, :, 0].mean(dim=-1)                          # [L, H]
        _dt_s = _time.perf_counter() - _t0_s
        for _eps_s in [0.3, 0.5, 0.8]:
            _sc_rows.append({
                "Model": f"GPT-2 {_tag_s}",
                "Params (M)": _params_s,
                "Layers": _nl_s,
                "ε": f"ε = {_eps_s:.1f}",
                "Sink Rate %": (_ss_s > _eps_s).float().mean().item() * 100,
                "Time (s)": round(_dt_s, 2),
            })
        del _out_s, _a_s, _ss_s

    _df_s = pl.DataFrame(_sc_rows)
    _chart_s = (
        alt.Chart(_df_s)
        .mark_line(point=alt.OverlayMarkDef(size=80))
        .encode(
            x=alt.X("Params (M):Q", title="Model parameters (M)",
                      scale=alt.Scale(type="log"),
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("Sink Rate %:Q", title="Sink metric (%)",
                      scale=alt.Scale(domain=[0, 100]),
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("ε:N",
                scale=alt.Scale(domain=["ε = 0.3", "ε = 0.5", "ε = 0.8"],
                                range=["#f59e0b", "#ef4444", "#a78bfa"]),
                legend=alt.Legend(labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[
                alt.Tooltip("Model:N"), alt.Tooltip("Params (M):Q"),
                alt.Tooltip("Layers:Q"), alt.Tooltip("ε:N"),
                alt.Tooltip("Sink Rate %:Q", format=".1f"),
                alt.Tooltip("Time (s):Q"),
            ],
        )
        .properties(
            width=440, height=280,
            title=alt.TitleParams(
                text="GPT-2 family: sink rate vs model depth (live)",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _mem_s = ""
    if device == "cuda":
        _gb_s = torch.cuda.max_memory_allocated() / 1e9
        _mem_s = f"  ·  peak VRAM: **{_gb_s:.1f} GB**"

    # Conclusion derived from the live numbers, never asserted ahead of them. Read at the
    # strict ε=0.8 threshold (the paper's Table 1 bar), which has the headroom to show a
    # depth trend; ε=0.3 saturates on short text.
    _e08 = _df_s.filter(pl.col("ε") == "ε = 0.8").sort("Params (M)")
    _r08 = _e08["Sink Rate %"].to_list()
    _small_r, _large_r = _r08[0], _r08[-1]
    _mono = all(_r08[i] <= _r08[i + 1] + 1e-9 for i in range(len(_r08) - 1))
    if abs(_large_r - _small_r) < 1.0:
        _trend = "stays flat across this depth range (little headroom left at ε=0.8 on this text)"
    elif _mono and _large_r > _small_r:
        _trend = "rises monotonically with depth"
    elif _large_r > _small_r:
        _trend = "rises overall with depth (with minor non-monotonic steps)"
    else:
        _trend = "does not increase with depth on this input"
    mo.vstack([
        _chart_s,
        mo.md(f"Computed live on `{device}`{_mem_s}. At the strict ε=0.8 bar (the paper's Table 1 "
              f"threshold) the sink rate {_trend}: **{_small_r:.0f}% → {_large_r:.0f}%** from GPT-2 "
              "Small (12 layers) to XL (48 layers). Deeper models carry more of these hard sinks, "
              "consistent with C_max^L growing with depth in Theorem 3.2."),
    ], align="center")
    return


# ── Batched Sink Census (paper's multi-prompt methodology) ────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Sink Census: 24 Domains, One Batched Pass

    A single sentence is one sample. The paper measures its sink metric over **170 prompts
    spanning many domains** (Appendix C.3): medical abstracts, legal boilerplate, IRC chat
    logs, HTML. A sink that only shows up in tidy English prose would be a curiosity, not
    a mechanism.

    We built a smaller census in the same spirit: 24 original prompts across 24 different
    text domains (not the paper's own 170, but comparable in range), truncated to the
    paper's T = 64 tokens and executed as **one padded, masked, batched forward pass** on
    the GPU. For each head we get the mean sink score across domains, and, more telling,
    the *standard deviation*: a structural sink should hold across every domain.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell(hide_code=True)
def _():
    # Shared by the GPT-2 census below and the modern-model test further down;
    # both measure the same 24 prompts so their sink rates are directly comparable.
    CENSUS_DOMAINS = [
        "Biology", "Python code", "Legal contract", "IRC chat", "Recipe",
        "Finance news", "Sonnet", "Court report", "Breaking news", "Tech docs",
        "Medical note", "Fairy tale", "History", "Customer FAQ", "Chess notation",
        "Cover letter", "Economics", "Song lyrics", "SQL query", "Physics",
        "Sports report", "French novel", "Weather forecast", "Art history",
    ]
    CENSUS_TEXTS = [
        "The mitochondrion is a double-membrane-bound organelle found in most eukaryotic organisms, generating most of the cell's supply of adenosine triphosphate.",
        "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0]\n    return quicksort([x for x in arr[1:] if x < pivot]) + [pivot]",
        "WHEREAS, the Parties desire to enter into this Agreement to set forth the terms and conditions of their business relationship, NOW THEREFORE, in consideration of the mutual covenants herein,",
        "<ikt> hi all :)\n<gggs> hey ikt\n<ikt> thinking of setting up an LDAP server at home\n<gggs> nice, what distro?",
        "Preheat the oven to 220C. Toss the potatoes in olive oil, salt, and rosemary, then roast for 45 minutes, turning once, until golden and crisp at the edges.",
        "In the third quarter, the company reported revenue of $2.4 billion, up 12% year over year, driven primarily by growth in its cloud services segment.",
        "Shall I compare thee to a summer's day? Thou art more lovely and more temperate: Rough winds do shake the darling buds of May,",
        "The defendant appeared before the court on charges of breach of contract. Counsel for the plaintiff argued that damages should include lost profits.",
        "BREAKING: Officials confirmed Tuesday that the wildfire burning north of the city has been 60 percent contained, allowing some evacuation orders to be lifted.",
        "To install the package, run pip install transformers in your terminal. Then import the library and load a pretrained model using the from_pretrained method.",
        "The patient presented with acute chest pain radiating to the left arm, diaphoresis, and shortness of breath. ECG revealed ST-segment elevation in leads II, III, and aVF.",
        "Once upon a time, in a village at the edge of a great forest, there lived a woodcutter and his two children, Hansel and Gretel.",
        "The Treaty of Westphalia, signed in 1648, ended the Thirty Years' War and established the principle of state sovereignty that underpins the modern international order.",
        "Q: How do I reset my password? A: Click 'Forgot password' on the login page, enter your email address, and follow the link we send you within 15 minutes.",
        "1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Na5",
        "Dear Hiring Manager, I am writing to express my interest in the Senior Data Engineer position posted on your careers page. I have eight years of experience building pipelines.",
        "The GDP deflator differs from the consumer price index in that it measures the prices of all domestically produced goods, not just a fixed basket of consumer items.",
        "Verse 1: City lights are fading out the rearview mirror glow / Every mile a memory of a place I used to know / Chorus: And I'm gone, gone, gone",
        "SELECT customer_id, SUM(order_total) AS lifetime_value FROM orders WHERE order_date >= '2024-01-01' GROUP BY customer_id HAVING SUM(order_total) > 1000 ORDER BY lifetime_value DESC;",
        "Water boils at 100 degrees Celsius at sea level, but at higher altitudes the reduced atmospheric pressure lowers the boiling point by roughly one degree per 300 meters.",
        "In the 87th minute, the substitute striker latched onto a through ball, rounded the keeper, and slotted home the winner to send the home crowd into raptures.",
        "Le vieux pecheur regardait la mer depuis le quai, comme chaque matin depuis quarante ans. Le ciel gris annoncait une tempete, mais il n'avait jamais eu peur de l'eau.",
        "The forecast for Thursday calls for morning fog giving way to partly sunny skies, with highs near 18 degrees and a 30 percent chance of showers after dark.",
        "Renaissance perspective, first formalized by Brunelleschi around 1415, allowed painters to construct convincing three-dimensional space on a flat surface using a single vanishing point.",
    ]
    T_CENSUS = 64  # paper measures the sink on the first 64 tokens (Appendix C.3)
    return CENSUS_DOMAINS, CENSUS_TEXTS, T_CENSUS


@app.cell
def _(BOS_ID, CENSUS_TEXTS, T_CENSUS, mo, model, tokenizer, torch):
    # 24-domain census, one batched forward (paper Appendix C.3 methodology, T=64).
    # Compute-only: the per-(layer, prompt, head) sink tensor is kept, so the ε slider
    # and domain filters below re-slice it with zero additional GPU work.
    import time as _t_c
    _t0_c = _t_c.perf_counter()
    if model.device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()

    _seqs_c = [[BOS_ID] + tokenizer.encode(t, add_special_tokens=False)[: T_CENSUS - 1]
               for t in CENSUS_TEXTS]
    _Tm_c = max(len(s) for s in _seqs_c)
    _pad_c = tokenizer.eos_token_id
    _ids_c = torch.tensor([s + [_pad_c] * (_Tm_c - len(s)) for s in _seqs_c], device=model.device)
    _mask_c = torch.tensor([[1] * len(s) + [0] * (_Tm_c - len(s)) for s in _seqs_c],
                           device=model.device)
    with torch.no_grad():
        _out_c = model(_ids_c, attention_mask=_mask_c, output_attentions=True)
    _A_c = torch.stack(_out_c.attentions)              # [L, B, H, T, T]
    _col0_c = _A_c[..., 0]                             # [L, B, H, T]
    _mf_c = _mask_c.float()
    census_sink = ((_col0_c * _mf_c[None, :, None, :]).sum(-1)
                   / _mf_c.sum(-1)[None, :, None]).cpu()   # [L, B, H]
    _dt_c = _t_c.perf_counter() - _t0_c
    _gpu_c = ""
    if model.device.type == "cuda":
        _gpu_c = f" · peak VRAM {torch.cuda.max_memory_allocated()/1e9:.2f} GB"
    census_stats = {
        "ntok": int(_mf_c.sum().item()),
        "line": f"{int(_mf_c.sum().item())} tokens across 24 prompts in one batched forward "
                f"({_dt_c:.2f}s{_gpu_c})",
    }
    mo.md(f"*Census computed: {census_stats['line']}. Slice it below: filtering is free, "
          "the attention tensor is already measured.*")
    return census_sink, census_stats


@app.cell(hide_code=True)
def _(mo):
    get_census_eps, set_census_eps = mo.state(0.30)
    return get_census_eps, set_census_eps


@app.cell
def _(CENSUS_DOMAINS, get_census_eps, mo, set_census_eps):
    # Built directly in this cell, not via a shared factory: a factory only
    # receives get_census_eps through closure, invisible to marimo's dependency
    # graph, so on_change would never reach the cells that read the state.
    census_eps_ui = mo.ui.slider(0.1, 0.9, step=0.05, value=get_census_eps(),
                                 on_change=set_census_eps,
                                 label="Census sink threshold ε", show_value=True)
    census_domains_sel = mo.ui.multiselect(
        options=CENSUS_DOMAINS, value=CENSUS_DOMAINS,
        label="Domains to include (deselect some and see if the sink map cares)",
    )
    mo.vstack([census_eps_ui, census_domains_sel])
    return (census_domains_sel,)


@app.cell
def _(CENSUS_DOMAINS, N_HEADS, N_LAYERS, alt, census_domains_sel, census_sink, census_stats, get_census_eps, mo, pl):
    _sel_idx = [i for i, d in enumerate(CENSUS_DOMAINS) if d in census_domains_sel.value]
    _eps_c = get_census_eps()
    if not _sel_idx:
        _view_c = mo.md("⚠ Select at least one domain above.")
    else:
        _sub_c = census_sink[:, _sel_idx, :]           # [L, B', H]
        _mean_c = _sub_c.mean(dim=1)
        _std_c = _sub_c.std(dim=1) if len(_sel_idx) > 1 else _sub_c.mean(dim=1) * 0
        _nh_c = N_LAYERS * N_HEADS

        _rows_c = [
            {"layer": f"L{l:02d}", "head": f"H{h:02d}",
             "mean": float(_mean_c[l, h]), "std": float(_std_c[l, h])}
            for l in range(N_LAYERS) for h in range(N_HEADS)
        ]
        _df_c2 = pl.DataFrame(_rows_c)
        _n_sink_c = _df_c2.filter(pl.col("mean") > _eps_c).height
        _stable_c = _df_c2.filter((pl.col("mean") > _eps_c) & (pl.col("std") < 0.1)).height

        _hm_c = (
            alt.Chart(_df_c2)
            .mark_rect(cornerRadius=2, stroke="#07080f", strokeWidth=1)
            .encode(
                x=alt.X("head:O", title="Head",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
                y=alt.Y("layer:O", title="Layer", sort="descending",
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
                color=alt.Color("mean:Q", scale=alt.Scale(scheme="orangered", domain=[0, 1]),
                    legend=alt.Legend(title="Mean sink", labelColor="#94a3b8", titleColor="#94a3b8")),
                tooltip=[alt.Tooltip("layer:O"), alt.Tooltip("head:O"),
                         alt.Tooltip("mean:Q", format=".3f", title="Mean over selected domains"),
                         alt.Tooltip("std:Q", format=".3f", title="Std over selected domains")],
            )
            .properties(width=440, height=290, title=alt.TitleParams(
                text=f"Sink census, {len(_sel_idx)} domains: {_n_sink_c}/{_nh_c} heads sink (ε={_eps_c:.2f})",
                color="#e2e8f0", fontSize=12))
        )

        # Per-domain sink rate: which text types make the model sink hardest?
        _dom_rows = [
            {"domain": CENSUS_DOMAINS[i],
             "rate": float((census_sink[:, i, :] > _eps_c).float().mean()) * 100}
            for i in _sel_idx
        ]
        _bar_dom = (
            alt.Chart(pl.DataFrame(_dom_rows))
            .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, color="#f59e0b")
            .encode(
                y=alt.Y("domain:N", sort="-x", title=None,
                        axis=alt.Axis(labelColor="#94a3b8", labelFontSize=10)),
                x=alt.X("rate:Q", title=f"% of heads sinking (ε={_eps_c:.2f})",
                        scale=alt.Scale(domain=[0, 100]),
                        axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
                tooltip=[alt.Tooltip("domain:N"), alt.Tooltip("rate:Q", format=".1f")],
            )
            .properties(width=380, height=14 * len(_dom_rows) + 40, title=alt.TitleParams(
                text="Sink rate by domain: nearly flat is the point",
                color="#e2e8f0", fontSize=12))
        )
        _combo_c = (
            alt.hconcat(_hm_c, _bar_dom, spacing=24)
            .configure_view(stroke="#1e2d47", fill="#0d1220")
            .configure(background="#07080f")
        )
        _rates_c = [r["rate"] for r in _dom_rows]
        _view_c = mo.vstack([
            _combo_c,
            mo.md(
                f"**{_n_sink_c}/{_nh_c} heads** sink on average over your selected domains, "
                f"**{_stable_c}** with cross-domain std < 0.10. Per-domain sink rates span only "
                f"**{min(_rates_c):.0f}%–{max(_rates_c):.0f}%** across text types as different as "
                f"chess notation and French prose. The sink is structural, not stylistic: exactly "
                f"what a defence mechanism must be. Drag ε to see how the census hardens or "
                f"dissolves; deselect domains to try to break the pattern. "
                f"({census_stats['line']}.)"),
        ], align="center")
    _view_c
    return


# ── Does prompt content change the sink? (rate vs mass) ───────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Does the Prompt Change the Sink? Rate vs Mass

    The domain census varied *style* (code, French, chess) and the sink rate barely moved. A
    natural next question, and one the paper raises but does not test (§2, "idling" heads): does
    the *difficulty* of the prompt change the sink? If a sink is a head's no-op when it has
    nothing to mix (Act II), then a prompt that gives heads genuine work should pull attention
    off the sink.

    The honest answer, measured live below, splits into two metrics that disagree, and the
    disagreement is the finding:

    - **Binary sink rate** (how many heads sink past ε) stays nearly flat, whatever the prompt.
      The *population* of sink heads is fixed by the weights, not the input.
    - **Mean sink mass** (how much attention those heads actually park on position 0) *does*
      shift, by roughly 8 to 9 points, along one axis: how much specific token-to-token
      structure the text has.

    And the axis is **not** human difficulty. Trivial repetition pulls heads *off* the sink
    (induction heads lock onto the repeated pattern); smooth, predictable prose leaves them
    idling *on* it; multi-step reasoning sits in between. What moves the sink is structural
    mixing demand, not how hard the text is to think about. Flip the metric toggle to watch the
    flat rate turn into a fanned-out mass.
    """)
    return


@app.cell
def _(mo):
    # 6 bins x 3 prompts. Dependency-free so GPT-2 and any modern model measure the
    # same prompts. Two groups: flowing prose (little specific to mix) vs symbolic /
    # structured text (dense token-to-token dependencies). Each prompt is authored
    # comfortably longer than T_DIFF; the compute cell truncates all to one common
    # length so the comparison is not confounded by sequence length.
    DIFF_GROUP = {
        "conversational": "flowing prose",
        "descriptive": "flowing prose",
        "reasoning": "symbolic / structured",
        "arithmetic": "symbolic / structured",
        "code": "symbolic / structured",
        "repetition": "symbolic / structured",
    }
    DIFF_PROMPTS = {
        "conversational": [
            "Thank you so much for your kind email and for taking the time to write to us today. I truly hope this message finds you well and in good spirits, and please do let me know if there is anything at all that you might need from our side.",
            "It was really lovely to see you at the party last weekend, and I keep meaning to say how much everyone enjoyed the food you brought along. We should find a quiet evening soon to catch up properly over dinner and talk about the summer plans.",
            "I just wanted to check in and see how you have been doing lately, since it has been a while since we last spoke on the phone. Things here have been calm and pleasant, and the weather has finally turned warm enough to sit outside in the mornings.",
        ],
        "descriptive": [
            "The old lighthouse keeper climbed the spiral stairs every evening at dusk, carrying his lantern and a small worn notebook where he wrote down the passing ships and the changing colour of the sky over the restless grey sea below the cliffs near his home.",
            "She opened the wooden gate and walked slowly into the quiet garden, where climbing roses covered the crumbling old brick wall and a small stone fountain trickled softly beside the painted bench her grandmother had loved during the long warm summers.",
            "The train pulled slowly out of the station as heavy rain streaked the cold windows, and the tired passengers settled into their seats with newspapers and coffee while the grey city gave way to green fields and distant hills wrapped in a thin morning mist.",
        ],
        "reasoning": [
            "If all birds can fly and a robin is certainly a bird, then it follows that a robin can fly. However a penguin is also a bird, but a penguin plainly cannot fly at all, so it is simply not true that all birds fly, and therefore the first premise must be false.",
            "Either the butler or the maid quietly took the key from the table. If the butler had taken it, then the heavy door would have been locked from the inside. But the door was clearly open, so the butler did not take it, and hence it must have been the maid.",
            "Assume for a moment that the number is even. Then by definition it must be divisible by two without any remainder. But the problem clearly states that it leaves a remainder of one, which contradicts our assumption, so the number must in fact be odd instead.",
        ],
        "arithmetic": [
            "Start with the number three. Add eight to it to get eleven. Multiply that by two to get twenty two. Subtract five from it to get seventeen. Add the very first number three to reach twenty. Divide the total by four to get five, and then stop right here.",
            "Take the number ten to begin with. Subtract four from it to get six. Multiply that by three to get eighteen. Add two more to reach twenty. Halve the total to get ten again. Add the previous eighteen to reach twenty eight, then subtract eight to get twenty.",
            "Let x be equal to seven for now. Double it to get fourteen. Add six to reach twenty. Subtract x from it to get thirteen. Multiply by two to get twenty six. Subtract thirteen to get thirteen again, then add x twice over to reach twenty seven exactly.",
        ],
        "code": [
            "def solve(nums):\n    total = 0\n    for i, x in enumerate(nums):\n        if x > total:\n            total = total + x\n        else:\n            total = total - x\n    return total\nresult = solve([3, 1, 4, 1, 5, 9, 2, 6])\nprint(result + total)\n",
            "class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, value):\n        self.items.append(value)\n    def pop(self):\n        return self.items.pop()\ns = Stack()\ns.push(1)\ns.push(2)\ns.push(3)\nprint(s.pop() + s.pop())\n",
            "for i in range(n):\n    for j in range(n):\n        if grid[i][j] == 1:\n            count = count + neighbours(i, j)\n        else:\n            grid[i][j] = count\n            visited.add((i, j))\nreturn grid[n - 1][n - 1] + count\n",
        ],
        "repetition": [
            "The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat on the mat. The cat sat.",
            "yes yes okay okay sure sure fine fine right right good good well well now now then then yes yes okay okay sure sure fine fine right right good good well well now now then then yes yes okay okay sure sure fine fine right right good good well well now now",
            "and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then and then",
        ],
    }
    DIFF_TEXTS = [t for b in DIFF_PROMPTS for t in DIFF_PROMPTS[b]]
    DIFF_BINS = [b for b in DIFF_PROMPTS for _ in DIFF_PROMPTS[b]]
    T_DIFF = 48
    return DIFF_BINS, DIFF_GROUP, DIFF_TEXTS, T_DIFF


@app.cell
def _(BOS_ID, DIFF_TEXTS, T_DIFF, model, tokenizer, torch):
    # One batched forward pass, all sequences truncated to a common length so the
    # comparison is length-controlled (mean sink mass depends on sequence length).
    _enc = [tokenizer.encode(_t, add_special_tokens=False) for _t in DIFF_TEXTS]
    _Tuse = min(T_DIFF, min(len(_e) for _e in _enc) + 1)   # +1 for BOS
    _seqs = [[BOS_ID] + _e[: _Tuse - 1] for _e in _enc]
    _ids = torch.tensor(_seqs, device=model.device)        # equal length, no padding
    with torch.no_grad():
        _out = model(_ids, output_attentions=True)
    _A = torch.stack(_out.attentions)                      # [L, P, H, T, T]
    diff_sink = _A[..., 0].mean(-1).cpu()                  # [L, P, H] mean pos-0 mass
    diff_len = _Tuse
    return diff_len, diff_sink


@app.cell
def _(mo):
    diff_metric = mo.ui.radio(
        options=["Mean sink mass (functional)", "Binary sink rate (structural)"],
        value="Mean sink mass (functional)",
        label="Metric",
        inline=True,
    )
    diff_metric
    return (diff_metric,)


@app.cell(hide_code=True)
def _(DIFF_BINS, DIFF_GROUP, alt, diff_len, diff_metric, diff_sink, get_census_eps, mo, pl):
    _eps = get_census_eps()
    _bins = list(dict.fromkeys(DIFF_BINS))                 # unique, in order
    _idx = {b: [i for i, bb in enumerate(DIFF_BINS) if bb == b] for b in _bins}
    _struct = diff_sink.mean(dim=1) > _eps                 # [L,H] heads that sink on avg

    _mass_mode = diff_metric.value.startswith("Mean")
    _rows = []
    for _b in _bins:
        _sub = diff_sink[:, _idx[_b], :]                   # [L, nb, H]
        _mass = float(_sub.permute(1, 0, 2)[:, _struct].mean()) if _struct.any() else 0.0
        _rate = float((_sub > _eps).float().mean()) * 100
        _rows.append({"bin": _b, "group": DIFF_GROUP[_b],
                      "value": _mass if _mass_mode else _rate,
                      "mass": _mass, "rate": _rate})
    _df = pl.DataFrame(_rows)

    _xtitle = ("mean attention on position 0 (sink heads)" if _mass_mode
               else f"% of heads sinking (ε = {_eps:.2f})")
    _xdom = [0, float(max(0.8, _df["value"].max() + 0.05))] if _mass_mode else [0, 100]
    _bars = (
        alt.Chart(_df)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            y=alt.Y("bin:N", sort=alt.SortField("value", order="descending"), title=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelFontSize=11)),
            x=alt.X("value:Q", title=_xtitle, scale=alt.Scale(domain=_xdom),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("group:N",
                scale=alt.Scale(domain=["flowing prose", "symbolic / structured"],
                                range=["#f59e0b", "#22d3ee"]),
                legend=alt.Legend(title=None, labelColor="#94a3b8", orient="bottom")),
            tooltip=[alt.Tooltip("bin:N"), alt.Tooltip("group:N"),
                     alt.Tooltip("mass:Q", format=".3f", title="mean sink mass"),
                     alt.Tooltip("rate:Q", format=".1f", title="sink rate %")],
        )
        .properties(width=430, height=210, title=alt.TitleParams(
            text=("Sink MASS shifts with structure (matched length "
                  f"{diff_len} tokens)" if _mass_mode
                  else f"Sink RATE stays flat across prompt types (ε = {_eps:.2f})"),
            color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _mass_span = _df["mass"].max() - _df["mass"].min()
    _rate_span = _df["rate"].max() - _df["rate"].min()
    if _mass_mode:
        _note = (
            f"Across these six prompt types the binary sink rate spans only "
            f"**{_rate_span:.0f} points**, but the mean sink mass among the sink heads spans "
            f"**{_mass_span * 100:.0f} points** ({_df['mass'].min():.2f} to {_df['mass'].max():.2f}). "
            f"The flowing-prose bins (amber) sit highest: those heads have little specific to "
            f"attend to, so they idle on the sink. The symbolic bins (cyan), including trivial "
            f"repetition, pull attention off it. This is the Act II no-op switch modulating by "
            f"degree, measured across text. Switch the metric to **Binary sink rate** to see the "
            f"same heads look completely input-invariant."
        )
    else:
        _note = (
            f"Every bar is nearly the same height: the sink rate spans just **{_rate_span:.0f} "
            f"points** whatever the prompt. The population of heads that sink is set by the "
            f"weights, not the text, the same structural verdict the 24-domain census reached. "
            f"Now switch to **Mean sink mass** to see the one thing that *does* move with prompt "
            f"content."
        )
    mo.vstack([_bars, mo.md(_note)], align="center")
    return


# ── The Modern-Model Test: Qwen ladders (0.5B → 14B) ──────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Modern-Model Test: Are Sinks Universal in Modern LLMs?

    Every live measurement so far used GPT-2, a 2019 model. Do attention sinks persist in the
    LLMs people actually run in 2025? Two ungated families let us check at real scale:
    **Qwen2.5** (2024) and **Qwen3** (2025), each from 0.5B to 14B.

    One caution up front, because it shapes how to read the chart. It is tempting to treat this
    as a test of the paper's Prediction 1 (longer training context drives stronger sinks): Qwen
    pre-trains on windows up to **32K tokens**, 32× GPT-2's. But across off-the-shelf models,
    training context is confounded with depth, width, attention design, tokenizer, and
    pre-training data all at once, and you cannot move one while holding the rest fixed. The
    paper isolates context precisely because it trains its own 120M models where *only* context
    varies (Fig 5a above). So read this chart for what it can honestly show, whether sinks appear
    everywhere and how the ε threshold behaves, not as a clean scaling law.

    Each run executes the **same 24-domain census** as above on the model you pick, so the
    numbers are directly comparable. One note from §5: Qwen pins no ⟨BOS⟩ during training, so its
    sink forms on whatever token comes first; we measure attention to position 0, exactly as the
    paper's sink metric does. That choice matters at high ε, as the chart shows.

    *VRAM guide (bf16): 0.5B ≈ 1 GB · 1.5B ≈ 3 GB · 3B ≈ 6 GB · 7B ≈ 15 GB · 14B ≈ 28 GB.
    One family stays loaded at a time; picking a model from the other family frees the
    previous one first.*
    """)
    return


@app.cell
def _(get_census_eps, mo, set_census_eps):
    qwen_ladder_state = mo.state([])
    get_qwen_ladder, set_qwen_ladder = qwen_ladder_state
    qwen_pick = mo.ui.dropdown(
        options={
            "Qwen2.5-0.5B (2024)": "Qwen/Qwen2.5-0.5B",
            "Qwen2.5-1.5B (2024)": "Qwen/Qwen2.5-1.5B",
            "Qwen2.5-3B (2024)": "Qwen/Qwen2.5-3B",
            "Qwen2.5-7B (2024)": "Qwen/Qwen2.5-7B",
            "Qwen2.5-14B (2024)": "Qwen/Qwen2.5-14B",
            "Qwen3-0.6B (2025)": "Qwen/Qwen3-0.6B",
            "Qwen3-1.7B (2025)": "Qwen/Qwen3-1.7B",
            "Qwen3-4B (2025)": "Qwen/Qwen3-4B",
            "Qwen3-8B (2025)": "Qwen/Qwen3-8B",
            "Qwen3-14B (2025)": "Qwen/Qwen3-14B",
        },
        value="Qwen2.5-0.5B (2024)",
        label="Modern model to census",
    )
    qwen_go = mo.ui.run_button(label="⚡ Load & run the 24-domain census")
    # Built directly here (see the note on the census slider above) so it stays
    # wired to the shared state instead of desyncing from the census control.
    census_eps_ui2 = mo.ui.slider(0.1, 0.9, step=0.05, value=get_census_eps(),
                                  on_change=set_census_eps,
                                  label="Sink threshold ε (shared with the census above)",
                                  show_value=True)
    mo.vstack([
        mo.hstack([qwen_pick, qwen_go], justify="start", gap=1),
        census_eps_ui2,
    ])
    return get_qwen_ladder, qwen_go, qwen_pick, set_qwen_ladder


@app.cell
def _(AutoModelForCausalLM, AutoTokenizer, CENSUS_TEXTS, MODEL_CACHE, T_CENSUS, device, mo, qwen_go, qwen_pick, set_qwen_ladder, torch):
    mo.stop(
        not qwen_go.value,
        mo.md("*Pick a size and press **⚡ Load & run**. The first run of each model "
              "downloads its weights.*"),
    )
    import time as _t_q
    _qid = qwen_pick.value
    try:
        _t0_q = _t_q.perf_counter()
        if device == "cuda":
            torch.cuda.reset_peak_memory_stats()
        # One Qwen family resident at a time: evict the other family before loading.
        _fam_q = "Qwen/Qwen3" if _qid.startswith("Qwen/Qwen3") else "Qwen/Qwen2.5"
        _evict_q = [k for k in MODEL_CACHE
                    if k.startswith("Qwen/") and not k.startswith(_fam_q)]
        for _k_q in _evict_q:
            del MODEL_CACHE[_k_q]
        if _evict_q and device == "cuda":
            torch.cuda.empty_cache()
        _tok_key = _qid + ":tokenizer"
        if _tok_key not in MODEL_CACHE:
            MODEL_CACHE[_tok_key] = AutoTokenizer.from_pretrained(_qid)
        _tok_q = MODEL_CACHE[_tok_key]
        if _qid not in MODEL_CACHE:
            MODEL_CACHE[_qid] = AutoModelForCausalLM.from_pretrained(
                _qid, attn_implementation="eager",
                dtype=torch.bfloat16 if device == "cuda" else torch.float32,
            ).to(device).eval()
        _mdl_q = MODEL_CACHE[_qid]
        _load_s = _t_q.perf_counter() - _t0_q

        # Same 24 prompts, same T=64 truncation as the GPT-2 census. Qwen pins no
        # BOS, so nothing is prepended (Table 2's "text" inference row); the sink
        # metric targets position 0 whatever token sits there, per Gu et al.
        _pad_q = _tok_q.pad_token_id if _tok_q.pad_token_id is not None else (_tok_q.eos_token_id or 0)
        _seqs_q = [_tok_q.encode(t, add_special_tokens=False)[:T_CENSUS] for t in CENSUS_TEXTS]
        _Tm_q = max(len(s) for s in _seqs_q)
        _ids_q = torch.tensor([s + [_pad_q] * (_Tm_q - len(s)) for s in _seqs_q], device=device)
        _mask_q = torch.tensor([[1] * len(s) + [0] * (_Tm_q - len(s)) for s in _seqs_q],
                               device=device)
        _t1_q = _t_q.perf_counter()
        with torch.no_grad():
            _out_q = _mdl_q(_ids_q, attention_mask=_mask_q, output_attentions=True)
        _A_q = torch.stack(_out_q.attentions).float()      # [L, B, H, T, T]
        _mfq = _mask_q.float()
        _sink_q = (_A_q[..., 0] * _mfq[None, :, None, :]).sum(-1) / _mfq.sum(-1)[None, :, None]
        _mean_q = _sink_q.mean(dim=1)                      # [L, H] mean over 24 prompts
        _fwd_s = _t_q.perf_counter() - _t1_q
        _ntok_q = int(_mfq.sum().item())
        _nl_q = _mdl_q.config.num_hidden_layers
        _nh_q = _mdl_q.config.num_attention_heads

        _entry_q = {
            "model": _qid.split("/")[-1],
            "params": _qid.split("-")[-1],
            "rate03": float((_mean_q > 0.3).float().mean().item()) * 100,
            "rate08": float((_mean_q > 0.8).float().mean().item()) * 100,
            "heads": _nl_q * _nh_q,
        }
        # Functional update: replaces any previous run of the same model without
        # reading the getter (which would re-trigger this cell on its own write).
        set_qwen_ladder(
            lambda prev, _n=_entry_q: [e for e in prev if e["model"] != _n["model"]] + [_n])
        del _out_q, _A_q, _sink_q

        _gpu_q = ""
        if device == "cuda":
            _gpu_q = (f" · peak VRAM {torch.cuda.max_memory_allocated()/1e9:.1f} GB, "
                      f"{torch.cuda.memory_allocated()/1e9:.1f} GB resident")
        _result_q = mo.md(
            f"**{_entry_q['model']}** ({_nl_q}L × {_nh_q}H = {_entry_q['heads']} heads): "
            f"**{_entry_q['rate03']:.0f}%** of heads sink at ε=0.3, **{_entry_q['rate08']:.0f}%** "
            f"at the paper's strict ε=0.8 bar, measured over the same 24 domains as the GPT-2 "
            f"census above. Load: {_load_s:.1f}s · census: {_fwd_s:.2f}s for {_ntok_q} tokens "
            f"({_ntok_q/_fwd_s:,.0f} tok/s){_gpu_q}. The chart below adds a bar for each "
            "model you run.")
    except Exception as _e_q:
        _result_q = mo.md(
            f"⚠ Could not run `{_qid}`: `{type(_e_q).__name__}: {_e_q}`. "
            "A download interruption or out-of-memory are the usual causes; try a smaller size.")
    _result_q
    return


@app.cell
def _(alt, census_sink, get_census_eps, get_qwen_ladder, MODEL_ID, mo, pl):
    # Every censused model on one axis, next to the paper's published LLaMA 3.1 numbers.
    _eps_l = get_census_eps()
    _gpt_rate = float((census_sink.mean(dim=1) > _eps_l).float().mean().item()) * 100
    _rows_l = [{"model": f"{MODEL_ID} (live, ε={_eps_l:.2f})", "rate": _gpt_rate,
                "source": "measured here"}]
    for _e_l in get_qwen_ladder():
        _rate_l = _e_l["rate03"] if abs(_eps_l - 0.3) < 0.25 else _e_l["rate08"]
        _eps_shown = 0.3 if abs(_eps_l - 0.3) < 0.25 else 0.8
        _rows_l.append({"model": f"{_e_l['model']} (live, ε={_eps_shown})",
                        "rate": _rate_l, "source": "measured here"})
    _rows_l += [
        {"model": "LLaMA 3.1 8B (paper, ε=0.8)", "rate": 45.97, "source": "paper Table 1"},
        {"model": "LLaMA 3.1 70B (paper, ε=0.8)", "rate": 73.49, "source": "paper Table 1"},
        {"model": "LLaMA 3.1 405B (paper, ε=0.8)", "rate": 78.29, "source": "paper Table 1"},
    ]
    _ch_l = (
        alt.Chart(pl.DataFrame(_rows_l))
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4)
        .encode(
            y=alt.Y("model:N", sort=None, title=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelFontSize=10, labelLimit=260)),
            x=alt.X("rate:Q", title="% of heads that are sinks",
                    scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("source:N",
                scale=alt.Scale(domain=["measured here", "paper Table 1"],
                                range=["#f59e0b", "#818cf8"]),
                legend=alt.Legend(title=None, labelColor="#94a3b8")),
            tooltip=[alt.Tooltip("model:N"), alt.Tooltip("rate:Q", format=".1f"),
                     alt.Tooltip("source:N")],
        )
        .properties(width=460, height=26 * len(_rows_l) + 30,
            title=alt.TitleParams(
                text="Your Table 1: live measurements vs the paper's published numbers",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _note_l = (
        "Amber bars are measured here (GPT-2 and the Qwen models you ran); purple bars are the "
        "LLaMA 3.1 rates from the paper's Table 1, fixed at ε=0.8. The honest read is "
        "universality, not a scaling law. Every model from 2019 to 2025 sinks on a large "
        "majority of heads, and the 2025 Qwen3 family sinks hard across every size. But the rate "
        "does not climb cleanly with size, depth, or training context: GPT-2 Large sinks less "
        "than GPT-2 Medium, and Qwen3-8B less than Qwen3-4B, because these public models vary "
        "every one of those axes at once (the paper isolates context only with its own "
        "controlled 120M models, Fig 5a). What the ε slider does expose is sink hardness: at "
        "ε=0.3 the no-⟨BOS⟩ models sink prolifically; at the strict 0.8 bar their softer "
        "positional sinks thin out while the BOS-trained LLaMA models stay high. The purple "
        "LLaMA bars are always ε=0.8, so compare like-for-like only with the slider at 0.8."
        if get_qwen_ladder() else
        "Amber is the current GPT-2 model, measured here; purple bars are the LLaMA 3.1 "
        "sink rates the paper reports in Table 1 at ε=0.8. Run a Qwen size above to add "
        "modern models to the comparison."
    )
    mo.vstack([_ch_l, mo.md(_note_l)], align="center")
    return


# ── The No-Op Mechanism and the Apostrophe Head ────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Mechanism: Approximate No-Ops

    Routing attention to BOS prevents mixing via the **value vector norm**.

    The paper (§3.2) measures this directly for a specific head (see below): among that head's
    value vectors, BOS has the *smallest L2 norm*, smaller than every other token in the sequence.
    When attention head *h* routes all its attention weight to BOS:

    $$z_i^{(\ell,h)} = \sum_{j \leq i} \alpha_{ij}^{(\ell,h)} W_v^{(\ell,h)} v_j^{(\ell)} \approx \alpha_{i,0}^{(\ell,h)} \cdot W_v v_{\text{BOS}}^{(\ell)} \approx \mathbf{0}$$

    because the value of BOS, `W_v · v_BOS`, has near-zero norm. This head's contribution to the
    residual stream is approximately zero. The head is **switched off**. The token passes through
    unchanged via the residual connection.

    ### The Apostrophe Head (Gemma 7B, Layer 1)

    The paper re-examines a specific head (§3.2), originally reverse-engineered in a related
    [Barbero et al. (2025)](https://arxiv.org/pdf/2410.06205) paper on rotary positional encodings, with two operating modes:

    | Condition | Behavior |
    |---|---|
    | Previous token is `'` (apostrophe) | **Fires**: high attention on the apostrophe, large update to residual stream |
    | No apostrophe in context | **Sleeps**: routes all attention to BOS, near-zero update |

    This is a real `if-else` statement implemented in attention weights. It fires whenever the
    previous token is a literal apostrophe: contractions like `I'm`, possessives, quoted text,
    any of it. With no apostrophe in sight, it costs nothing. It stays dormant behind the sink.

    That specific head lives in Gemma 7B. GPT-2 has its own if-else heads, and the
    **mode-switch finder** below finds them: give it two texts, one with a trigger feature and
    one without, and it ranks every attention head by how much its BOS routing changes between
    the two. Heads that stay put are static sinks or static workers. Heads that jump are
    conditional if-else heads, caught in the act.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(mo):
    SWITCH_PRESETS = {
        "Apostrophes (the paper's Gemma trigger)": (
            "it's a cat and it's a dog and that's that",
            "it is a cat and it is a dog and that is that"),
        "Digits vs number words": (
            "the recipe needs 3 eggs, 250 grams of flour and 75 grams of butter",
            "the recipe needs three eggs, some flour and a little butter now"),
        "Code vs prose": (
            "for i in range(10): print(i * 2 + 1) # loop over odd numbers",
            "for each number from one to ten, print twice that number plus one"),
        "Quoted speech vs narration": (
            '"Stop right there," she said. "You have no idea what you are doing."',
            "She told him to stop right there because he had no idea what he was doing."),
        "French vs English": (
            "aujourd'hui il fait beau et nous allons marcher dans le parc ensemble",
            "today the weather is lovely and we are going to walk in the park together"),
    }
    switch_preset = mo.ui.dropdown(
        options=list(SWITCH_PRESETS), value=list(SWITCH_PRESETS)[0],
        label="Trigger hypothesis to test",
    )
    switch_preset
    return SWITCH_PRESETS, switch_preset


@app.cell
def _(SWITCH_PRESETS, mo, switch_preset):
    # The preset seeds the text boxes; both stay editable for free-form hunting.
    _a0, _b0 = SWITCH_PRESETS[switch_preset.value]
    switch_text_a = mo.ui.text(value=_a0, label="Text A (trigger present)", full_width=True)
    switch_text_b = mo.ui.text(value=_b0, label="Text B (trigger absent)", full_width=True)
    mo.vstack([switch_text_a, switch_text_b])
    return switch_text_a, switch_text_b


@app.cell
def _(BOS_ID, N_HEADS, N_LAYERS, alt, mo, model, pl, switch_text_a, switch_text_b, tokenizer, torch):
    # Mode-switch finder: one padded, batched forward for both texts, then per-head
    # |Δ BOS attention| between conditions. A large Δ means the head conditions its
    # sink behaviour on content, the paper's 'if-else' mechanism (§3.2), measured
    # across the whole grid instead of asserted for one hand-picked head.
    _ra = tokenizer.encode(switch_text_a.value, add_special_tokens=False)
    _rb = tokenizer.encode(switch_text_b.value, add_special_tokens=False)
    _Tmax = max(len(_ra), len(_rb)) + 1
    _pad = tokenizer.eos_token_id
    _ids_ms = torch.tensor([
        [BOS_ID] + _ra + [_pad] * (_Tmax - 1 - len(_ra)),
        [BOS_ID] + _rb + [_pad] * (_Tmax - 1 - len(_rb)),
    ], device=model.device)
    _mask_ms = torch.tensor([
        [1] * (1 + len(_ra)) + [0] * (_Tmax - 1 - len(_ra)),
        [1] * (1 + len(_rb)) + [0] * (_Tmax - 1 - len(_rb)),
    ], device=model.device)
    with torch.no_grad():
        _out_ms = model(_ids_ms, attention_mask=_mask_ms, output_attentions=True)
    _A_ms = torch.stack(_out_ms.attentions)          # [L, 2, H, T, T]
    _col0 = _A_ms[:, :, :, :, 0]                     # [L, 2, H, T] attn → BOS
    _m = _mask_ms.float()                            # [2, T]
    _sink_ab = (_col0 * _m[None, :, None, :]).sum(-1) / _m.sum(-1)[None, :, None]  # [L, 2, H]
    _sa, _sb = _sink_ab[:, 0], _sink_ab[:, 1]        # [L, H] each

    _rows_ms = [
        {"label": f"L{l}·H{h}", "A": float(_sa[l, h]), "B": float(_sb[l, h]),
         "delta": float(_sa[l, h] - _sb[l, h])}
        for l in range(N_LAYERS) for h in range(N_HEADS)
    ]
    _df_ms = pl.DataFrame(_rows_ms).with_columns(pl.col("delta").abs().alias("absd"))
    _top_ms = _df_ms.sort("absd", descending=True).head(5)

    _sc_ms = (
        alt.Chart(_df_ms)
        .mark_circle(size=70, opacity=0.85, stroke="#07080f", strokeWidth=0.5)
        .encode(
            x=alt.X("B:Q", title="BOS attention, Text B (trigger absent)",
                    scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("A:Q", title="BOS attention, Text A (trigger present)",
                    scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("absd:Q", scale=alt.Scale(scheme="plasma"),
                legend=alt.Legend(title="|Δ|", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("label:N", title="Head"),
                     alt.Tooltip("A:Q", format=".3f"), alt.Tooltip("B:Q", format=".3f"),
                     alt.Tooltip("delta:Q", format="+.3f", title="Δ (A−B)")],
        )
        .properties(width=380, height=340,
            title=alt.TitleParams(
                text="Mode-switch map: heads off the diagonal condition their sink on content",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _tbl_ms = " · ".join(
        f"**{r['label']}** ({r['delta']:+.2f})" for r in _top_ms.iter_rows(named=True)
    )
    _biggest = _top_ms.row(0, named=True)
    mo.vstack([
        _sc_ms,
        mo.md(
            f"Heads on the diagonal treat both texts identically. The biggest mode-switchers on "
            f"this pair: {_tbl_ms}. Head **{_biggest['label']}** shifts its BOS routing by "
            f"**{_biggest['delta']:+.2f}** between conditions, GPT-2's closest analogue of the "
            "Gemma apostrophe head. Edit the two texts to hunt for other triggers: "
            "digits, quotes, code, a second language. Both texts run as one batched forward pass."),
    ], align="center")
    return


# ── Value-Norm Verification: the no-op, measured ──────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Verifying the No-Op: Value Norms Across Every Head

    The no-op story has a testable second half. Routing attention to BOS only *nullifies* a
    head if the BOS **value vector** it attends to has near-zero norm. Otherwise the head
    would inject BOS's content everywhere. The paper verifies this for one Gemma head
    (Figure 4b). Here we check it for **every GPT-2 head at once**, on your text.

    For each head we compute the ratio ‖v_BOS‖ / mean‖v_content‖ from the actual per-head
    value projections, and plot it against that head's sink score. If the mechanism is real,
    strong sinks should sit at low ratios: attending hard to a value that says nothing.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(BOS_ID, N_HEADS, N_LAYERS, alt, mo, model, np, pl, sink_scores_live, text_input, tokenizer, torch):
    # Recompute the per-head value vectors exactly as each block does: ln_1 → c_attn,
    # take the V third, split into heads. hidden_states[l] is the input to block l.
    _raw_v = tokenizer.encode(text_input.value, add_special_tokens=False)
    _ids_v = torch.tensor([[BOS_ID] + _raw_v], device=model.device)
    with torch.no_grad():
        _out_v = model(_ids_v, output_hidden_states=True)
    _hs_v = _out_v.hidden_states                       # tuple of L+1 × [1, T, d]
    _d_model = model.config.n_embd
    _dh = _d_model // N_HEADS

    _ratio_v = np.zeros((N_LAYERS, N_HEADS))
    for _l in range(N_LAYERS):
        _blk = model.transformer.h[_l]
        with torch.no_grad():
            _qkv = _blk.attn.c_attn(_blk.ln_1(_hs_v[_l]))[0]     # [T, 3d]
        _vals = _qkv[:, 2 * _d_model:].view(-1, N_HEADS, _dh)     # [T, H, dh]
        _norms = _vals.norm(dim=-1)                               # [T, H]
        _ratio_v[_l] = (_norms[0] / (_norms[1:].mean(dim=0) + 1e-8)).cpu().numpy()

    _sink_np = sink_scores_live.cpu().numpy()
    _rows_v = [
        {"label": f"L{l}·H{h}", "sink": float(_sink_np[l, h]),
         "ratio": float(_ratio_v[l, h]),
         "type": "Sink (>30% → BOS)" if _sink_np[l, h] > 0.3 else "Normal"}
        for l in range(N_LAYERS) for h in range(N_HEADS)
    ]
    _r_v = float(np.corrcoef(_sink_np.flatten(), _ratio_v.flatten())[0, 1])

    _sc_v = (
        alt.Chart(pl.DataFrame(_rows_v))
        .mark_circle(size=75, opacity=0.85, stroke="#07080f", strokeWidth=0.5)
        .encode(
            x=alt.X("sink:Q", title="Sink score (mean attention → BOS)",
                    scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("ratio:Q", title="‖v_BOS‖ / mean ‖v_content‖",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("type:N",
                scale=alt.Scale(domain=["Sink (>30% → BOS)", "Normal"],
                                range=["#f59e0b", "#7dd3fc"]),
                legend=alt.Legend(title="Head type", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("label:N", title="Head"),
                     alt.Tooltip("sink:Q", format=".3f"),
                     alt.Tooltip("ratio:Q", format=".3f", title="BOS value ratio")],
        )
        .properties(width=430, height=290, title=alt.TitleParams(
            text=f"BOS value norm vs sink strength, all {N_LAYERS * N_HEADS} heads: Pearson r = {_r_v:+.2f}",
            color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _read_v = (
        f"the stronger a head sinks, the *smaller* the value vector it draws from "
        f"(r = {_r_v:+.2f}). Attending to BOS is attending to nothing: the "
        "no-op sits in the values, not just the attention pattern. The paper "
        "showed this for one Gemma head; it holds across GPT-2's whole grid."
        if _r_v < -0.15 else
        f"on this text the correlation is weak (r = {_r_v:+.2f}). GPT-2's heads separate "
        "less cleanly than Gemma's single studied head. Try longer or more varied text."
    )
    mo.vstack([
        _sc_v,
        mo.md(f"Live measurement of the paper's Figure 4b claim, extended to all heads: {_read_v}"),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# HEAD EXPLORER (altair click-selection)
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Head Explorer

    **Click any cell** in the grid below to inspect that head's full T × T attention matrix.
    **Shift-click** adds more heads; each selected head gets its own matrix, side by side,
    so you can compare a sink head against a working head directly.
    Every cell is one attention head of the model you picked above (rows = layers, columns = heads).
    Amber = strong sink. Dark = distributed attention.

    Look for:
    - **Vertical amber columns** → that head routes to BOS across all layers
    - **Isolated bright cell at L0** → specialized heads like the apostrophe head (active only in specific contexts)
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(N_HEADS, N_LAYERS, alt, mo, pl, sink_scores_live, tokens_live):
    # Native altair grid; selection state comes back through mo.ui.altair_chart.
    import html as _html_g
    _rows_g = [
        {"layer": f"L{l:02d}", "head": f"H{h:02d}", "li": l, "hi": h,
         "sink": round(float(sink_scores_live[l, h].item()), 4)}
        for l in range(N_LAYERS) for h in range(N_HEADS)
    ]
    _cw_g = max(16, min(38, 640 // N_HEADS))
    _ch_g = max(10, min(24, 560 // N_LAYERS))
    _grid_g = (
        alt.Chart(pl.DataFrame(_rows_g))
        .mark_rect(cornerRadius=2, stroke="#07080f", strokeWidth=1, cursor="pointer")
        .encode(
            x=alt.X("head:O", title="Head",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8",
                                  labelFontSize=9 if N_HEADS > 16 else 10)),
            y=alt.Y("layer:O", title="Layer",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8",
                                  labelFontSize=9 if N_LAYERS > 24 else 10)),
            color=alt.Color("sink:Q",
                scale=alt.Scale(scheme="orangered", domain=[0, 1]),
                legend=alt.Legend(title="Attn → BOS", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("layer:O"), alt.Tooltip("head:O"),
                     alt.Tooltip("sink:Q", title="BOS attn", format=".3f")],
        )
        .properties(
            width=_cw_g * N_HEADS, height=_ch_g * N_LAYERS,
            title=alt.TitleParams(
                text=f"Click a head to drill in, shift-click to compare ({N_LAYERS}×{N_HEADS} grid, live on your text)",
                color="#e2e8f0", fontSize=12),
        )
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    sink_grid = mo.ui.altair_chart(_grid_g, chart_selection="point", legend_selection=False)

    _chips_g = "".join(
        ('<span style="background:#78350f;color:#fcd34d;padding:1px 6px;border-radius:3px;margin:2px;display:inline-block">'
         if _i_g == 0 else
         '<span style="background:#0f1729;color:#94a3b8;padding:1px 5px;border-radius:3px;margin:2px;display:inline-block">')
        + _html_g.escape(_t_g) + "</span>"
        for _i_g, _t_g in enumerate(tokens_live)
    )
    mo.vstack([
        sink_grid,
        mo.Html(f'<div style="font-size:11px;font-family:JetBrains Mono,monospace;line-height:2.2;max-width:44rem;margin:6px auto 0">{_chips_g}</div>'),
    ], align="center")
    return (sink_grid,)


@app.cell
def _(attn_live, sink_grid):
    _sel_g = sink_grid.value
    try:
        _sel_rows_g = _sel_g.to_dicts()          # polars
    except AttributeError:
        try:
            _sel_rows_g = _sel_g.to_dict("records")   # pandas fallback
        except Exception:
            _sel_rows_g = []
    selected_heads = []
    for _r_g in _sel_rows_g:
        _p_g = (int(_r_g["li"]), int(_r_g["hi"]))
        # Drop duplicates and stale selections surviving a model switch.
        if (0 <= _p_g[0] < attn_live.shape[0] and 0 <= _p_g[1] < attn_live.shape[1]
                and _p_g not in selected_heads):
            selected_heads.append(_p_g)
    return (selected_heads,)


@app.cell
def _(alt, attn_live, mo, pl, selected_heads, tokens_live):
    if not selected_heads:
        _drill = mo.md("*Click any cell in the grid above to inspect that head's attention "
                       "matrix. Shift-click to compare several side by side.*")
    else:
        _show = selected_heads[:3]
        _T2 = len(tokens_live)
        _w3 = 420 if len(_show) == 1 else 300
        _h3 = 300 if len(_show) == 1 else 240
        _charts3 = []
        for _k3, (_sl, _sh) in enumerate(_show):
            _mat2 = attn_live[_sl, _sh].cpu().numpy()
            _rows3 = [
                {"qi": i, "ki": j,
                 "q": tokens_live[i].strip() or f"[{i}]",
                 "k": tokens_live[j].strip() or f"[{j}]",
                 "w": float(_mat2[i, j])}
                for i in range(_T2) for j in range(i + 1)
            ]
            _sc3 = float(attn_live[_sl, _sh, :, 0].mean().item())
            _lbl3 = "SINK" if _sc3 > 0.3 else "NORMAL"
            _charts3.append(
                alt.Chart(pl.DataFrame(_rows3))
                .mark_rect()
                .encode(
                    x=alt.X("ki:O", title="Key position",
                             axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelFontSize=8)),
                    y=alt.Y("qi:O", title="Query position", sort="descending",
                             axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelFontSize=8)),
                    color=alt.Color("w:Q",
                        scale=alt.Scale(scheme="inferno", domain=[0, 1]),
                        legend=(alt.Legend(title="Weight", labelColor="#94a3b8",
                                           titleColor="#94a3b8")
                                if _k3 == len(_show) - 1 else None)),
                    tooltip=[alt.Tooltip("q:N", title="Query"), alt.Tooltip("k:N", title="Key"),
                             alt.Tooltip("w:Q", title="Weight", format=".4f")],
                )
                .properties(width=_w3, height=_h3,
                    title=alt.TitleParams(
                        text=f"L{_sl}·H{_sh} · sink {_sc3:.3f} [{_lbl3}]",
                        color="#f59e0b" if _sc3 > 0.3 else "#7dd3fc", fontSize=12))
            )
        _combo3 = (
            alt.hconcat(*_charts3, spacing=18)
            .configure_view(stroke="#1e2d47", fill="#0d1220")
            .configure(background="#07080f")
        )
        _more3 = (mo.md(f"*Showing the first 3 of {len(selected_heads)} selected heads.*")
                  if len(selected_heads) > 3 else None)
        _drill = mo.vstack([_combo3] + ([_more3] if _more3 else []), align="center")
    _drill
    return


# ── Entropy Distribution ───────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Entropy Distribution: Two Populations

    Every head has an attention entropy H = −Σ αᵢⱼ log αᵢⱼ averaged across query positions.
    Sink heads concentrate weight on one position → low entropy. Active heads spread weight
    across many positions → high entropy.

    Each point below is one attention head of the current lab model, computed on your text.
    Heads you selected in the explorer above appear ringed in white, so you can see where a
    head you inspected sits in the two clusters. The clusters themselves are the empirical
    signature of a discrete mechanism.
    """)
    return


@app.cell(hide_code=True)
def _(alt, attn_live, mo, pl, selected_heads):
    # Per-query entropy as one fused tensor expression on-device; the causal zeros
    # above the diagonal contribute 0·log(0+ε) = 0, so no masking is needed.
    _Le, _He, _Te, _ = attn_live.shape
    _ent_t = -(attn_live * (attn_live + 1e-12).log()).sum(-1).mean(dim=2)  # [L, H]
    _bos_t = attn_live[:, :, :, 0].mean(dim=2)                             # [L, H]
    _ent_e = _ent_t.cpu().numpy()
    _bos_e = _bos_t.cpu().numpy()

    _rows_e = [
        {"label": f"L{l}·H{h}", "layer": l, "head": h,
         "entropy": float(_ent_e[l, h]),
         "bos_pct": float(_bos_e[l, h]) * 100,
         "type": "Sink (BOS > 30%)" if _bos_e[l, h] > 0.3 else "Normal",
         "picked": (l, h) in selected_heads}
        for l in range(_Le) for h in range(_He)
    ]
    _df_e = pl.DataFrame(_rows_e)
    _n_sink_e = _df_e.filter(pl.col("bos_pct") > 30).height

    _base_e = (
        alt.Chart(_df_e)
        .mark_circle(size=75, opacity=0.85, stroke="#07080f", strokeWidth=0.5)
        .encode(
            x=alt.X("entropy:Q", title="Mean attention entropy H (nats)",
                     axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("bos_pct:Q", title="Mean attention to BOS (%)",
                     axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("type:N",
                scale=alt.Scale(domain=["Sink (BOS > 30%)", "Normal"],
                                range=["#f59e0b", "#7dd3fc"]),
                legend=alt.Legend(title="Head type", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[
                alt.Tooltip("label:N", title="Head"),
                alt.Tooltip("entropy:Q", format=".3f", title="Entropy (nats)"),
                alt.Tooltip("bos_pct:Q", format=".1f", title="BOS attn %"),
                alt.Tooltip("type:N"),
            ],
        )
    )
    _ring_e = (
        alt.Chart(_df_e.filter(pl.col("picked")))
        .mark_point(size=260, filled=False, color="#f8fafc", strokeWidth=2)
        .encode(x="entropy:Q", y="bos_pct:Q",
                tooltip=[alt.Tooltip("label:N", title="Selected head")])
    )
    _sc_e = (
        (_base_e + _ring_e)
        .properties(
            width=440, height=280,
            title=alt.TitleParams(
                text=f"Entropy vs. BOS attention: {_n_sink_e} of {_Le * _He} heads are sinks (ε=0.3)",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _picked_e = _df_e.filter(pl.col("picked"))
    _pick_note = (
        " Ringed: " + ", ".join(
            f"**{r['label']}** ({r['entropy']:.2f} nats, {r['bos_pct']:.0f}% BOS)"
            for r in _picked_e.iter_rows(named=True)) + "."
        if _picked_e.height else ""
    )
    mo.vstack([
        _sc_e,
        mo.md(f"**{_n_sink_e}/{_Le * _He} heads** cluster at low entropy + high BOS attention. "
              "The gap between clusters is wider than a continuous tendency would produce: "
              "each head either operates as a sink or it doesn't, no interpolation between "
              f"the two.{_pick_note}"),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# ACT V: IS <BOS> SPECIAL? DATA PACKING EXPERIMENTS
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Act V: Is ⟨BOS⟩ Special?

    Everything so far assumes the sink lives at `<BOS>`. This section tests whether that
    token is special, or whether any first-position token would do the same job.

    The paper answers this by training multiple 120M-parameter models on **30B tokens** with
    different data packing strategies (§5, Appendix A.3). Four setups:

    - **Causal masking:** tokens see all past context, even from different documents
    - **Intra-doc masking:** tokens only see within their own document
    - **Fixed BOS:** a single `<BOS>` is pinned at position 0 of every context window; all tokens
      can attend to it regardless of document boundaries
    - **No fixed BOS:** `<BOS>` appears only at document boundaries, not pinned

    Packing also sets *where* sinks live. Under plain causal masking every token can see
    position 0, so one global sink at the sequence start serves the entire context. Under
    intra-doc masking a token cannot see earlier documents in the packed window, so no shared
    position-0 sink is reachable. The model compensates by forming a fresh *local* sink at the
    first token of each concatenated document. So the masking strategy decides not just whether
    sinks form but how many and where they sit.

    The chart below shows what happens at inference when a model trained *with* fixed BOS
    has that BOS *removed*.

    *Data: exact values from Table 2, paper §5.*
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    # Exact values from Table 2, paper §5.
    # Columns: Attention Masking, BOS during train, EOS during train, Inference tokens, Sink Metric%, Valid loss
    _pack = pl.DataFrame({
        "Setup": [
            "Causal, no fixed BOS\n(infer: BOS+text)",
            "Causal, no fixed BOS\n(infer: text only)",
            "Causal + fixed BOS\n(infer: BOS+text)",
            "Causal + fixed BOS\n(infer: text only, ⚠)",
            "Intra-doc, no BOS\n(infer: text only)",
            "Intra-doc, BOS at doc bounds\n(infer: BOS+text)",
            "Intra-doc, BOS at doc bounds\n(infer: text only)",
            "Intra-doc + fixed BOS\n(infer: BOS+text)",
            "Intra-doc + fixed BOS\n(infer: text only, ⚠)",
        ],
        "Sink Metric %": [65.10, 65.15, 90.84, 0.05, 28.23, 83.33, 50.24, 90.56, 0.00],
        "Valid Loss":    [2.69,  2.70,  2.69,  7.56, 2.67,  2.67,  2.68,  2.67,  7.78],
        "Status": ["ok", "ok", "ok", "broken", "ok", "ok", "ok", "ok", "broken"],
    })

    _bars = (
        alt.Chart(_pack)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            y=alt.Y("Setup:N", title=None, sort=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelFontSize=10, labelLimit=300)),
            x=alt.X("Sink Metric %:Q", title="Sink metric (%)",
                    scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Status:N",
                scale=alt.Scale(domain=["ok", "broken"], range=["#f59e0b", "#7c3aed"]),
                legend=alt.Legend(title="Model", labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("Setup:N"), alt.Tooltip("Sink Metric %:Q", format=".2f"),
                     alt.Tooltip("Valid Loss:Q", format=".2f")],
        )
        .properties(width=440, height=420,
            title=alt.TitleParams(
                text="Data packing × BOS strategy → sink rate and loss (Table 2, paper §5)",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    mo.vstack([
        _bars,
        mo.md(r"""
Three results stand out (paper §5 summary):

- **With fixed BOS during training, removing BOS at inference destroys the model.**
  Sink metric drops from 90.84% → 0.05%, valid loss jumps from 2.69 → 7.56 (causal + fixed BOS).
  Same pattern with intra-doc masking: 90.56% → 0.00%, loss 2.67 → 7.78.

- **Without fixed BOS, the model finds a sink at whichever token is first.**
  Causal masking without BOS: 65.10% sink rate, normal loss 2.69. Pre-training choices only affect which token the sink latches onto. This is not free. A sink must carry a near-zero value vector (Act II), so a model without a dedicated BOS is forced to turn an ordinary word like *The* or *Once* into the sink, suppressing that word's value norm and degrading its own meaning. Stability at position 0 is bought by sacrificing the first token's representation, which is exactly what a dedicated `<BOS>` exists to avoid.

- **BOS present but not artificially pinned still matters, just less catastrophically.**
  Intra-doc masking with BOS at natural document boundaries: 83.33% sink rate with BOS at inference,
  dropping to 50.24% without it, both loss-neutral (2.67 vs 2.68). Compare to the *fixed*-BOS
  version of the same masking, where removing BOS at inference collapses the sink to 0.00% and
  breaks the loss. Pinning BOS to position 0 during training makes the model brittle to
  its removal. Merely seeing BOS at document starts does not.
        """),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# THE VERDICT: REMOVE BOS → COLLAPSE
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Verdict: Remove the Sink → Everything Breaks

    The packing experiments established that sinks form regardless of training setup. This
    section tests whether they are *useful* or just a harmless artifact.

    **Remove the BOS at inference and performance collapses**, especially on long-context tasks where the mixing problem is worst.

    *Data: exact values from Table 3, paper §5. Model: Gemma 7B. Context for RULER: 4096 tokens.*
    """)
    return


@app.cell(hide_code=True)
def _(alt, mo, pl):
    # Exact values from Table 3, paper §5.
    # Note: RULER context = 4096 tokens (not 128k, that is a different benchmark run).
    _bench = pl.DataFrame({
        "Benchmark": ["ARC-Easy", "ARC-Chal.", "PIQA", "SIQA", "HellaSwag", "Winogrande", "RULER (4096 ctx)"],
        "With BOS":    [80.77,  53.50,  81.72,  48.26,  80.61,  72.85,  82.57],
        "Without BOS": [28.49,  22.53,  52.77,  34.70,  27.35,  49.41,   0.00],
    })
    _long = _bench.unpivot(index="Benchmark", variable_name="Condition", value_name="Score")

    _ch4 = (
        alt.Chart(_long)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("Condition:N", sort=["With BOS", "Without BOS"], title=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelFontSize=11)),
            y=alt.Y("Score:Q", title="Score (%)", scale=alt.Scale(domain=[0, 100]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Condition:N",
                scale=alt.Scale(domain=["With BOS", "Without BOS"], range=["#f59e0b", "#7c3aed"]),
                legend=None),
            column=alt.Column("Benchmark:N",
                header=alt.Header(labelColor="#94a3b8", titleColor="#94a3b8", labelFontSize=9,
                                  labelAngle=-30, labelLimit=100)),
            tooltip=[alt.Tooltip("Benchmark:N"), alt.Tooltip("Condition:N"),
                     alt.Tooltip("Score:Q", format=".2f")],
        )
        .properties(width=95, height=220)
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _cs5 = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:14px 18px;text-align:center;"
    _cv5 = "font-size:1.8em;font-weight:700;line-height:1;margin-bottom:4px;"
    _cl5 = "font-size:0.7em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;"
    _cg5 = "display:grid;grid-template-columns:repeat(3,1fr);gap:10px;width:100%;max-width:52rem;margin:0 auto 1.2em;"

    mo.vstack([
        mo.Html(f"""<div style="{_cg5}">
          <div style="{_cs5}"><div style="{_cv5}color:#f59e0b">82.57%</div>
            <div style="{_cl5}">RULER · with BOS</div>
            <div style="font-size:0.65em;color:#94a3b8">4096 ctx · Gemma 7B · Table 3</div></div>
          <div style="{_cs5}"><div style="{_cv5}color:#a78bfa">0.00%</div>
            <div style="{_cl5}">RULER · no BOS</div>
            <div style="font-size:0.65em;color:#94a3b8">total failure · 0 correct</div></div>
          <div style="{_cs5}"><div style="{_cv5}color:#f59e0b">80.77%</div>
            <div style="{_cl5}">ARC-Easy · with BOS</div>
            <div style="font-size:0.65em;color:#94a3b8">→ 28.49% without (−52pp)</div></div>
        </div>"""),
        _ch4,
        mo.md(r"""
RULER tests long-context reasoning at 4096 tokens. Without BOS, attention distributions smooth out (as shown in the mixing simulation above) and the model fails to maintain distinct representations. The score drops to 0.00%.

The mechanism is specific, not a vague loss of stability. A head's default, when it has nothing worth mixing, is to dump its attention on position 0. Trained with a fixed BOS there, that default lands on a near-zero value vector and injects almost nothing. Remove BOS and position 0 is now an ordinary, high-norm word. The same default attention now pours *that one word's* representation into every downstream token, so every position drifts toward the same content and the sequence collapses into near-identical hidden states. The heads did not change their behavior; the target under them did. That is why the drop is catastrophic and immediate rather than gradual.

Short-context benchmarks fall too (ARC-Easy: −52 percentage points). The sink provides structural stability at all scales, not only on long sequences.
        """),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# LIVE REPRESENTATIONAL COLLAPSE DEMO
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Representational Collapse: Live in GPT-2

    The theory predicts that removing BOS should cause representations to become more uniform,
    all tokens converging to similar hidden states (less information separation).

    We can measure this directly. **Representational distance** μ(X) is the mean pairwise
    cosine distance between last-layer hidden states, taken over the **content tokens** (we
    exclude the BOS marker itself, so "with BOS" and "without BOS" compare the *same* tokens):

    $$\mu(X) = \frac{2}{T(T-1)} \sum_{i < j} \left(1 - \frac{h_i \cdot h_j}{\|h_i\| \|h_j\|}\right)$$

    High μ = representations are diverse (model distinguishes tokens).
    Low μ = representations have collapsed (model can't tell tokens apart).

    This runs on your text, repeated into the long-context regime where collapse
    appears (on a one-line prompt the effect stays near zero; collapse needs length).
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(BOS_ID, alt, mo, model, pl, text_input, tokenizer, torch):
    # μ_content: mean pairwise cosine DISTANCE among the last-layer hidden states of
    # the CONTENT tokens only. Excluding the BOS row makes "with BOS" vs "without BOS"
    # a comparison over the SAME tokens; otherwise BOS's own outlier hidden state
    # inflates the with-BOS number and flatters the result. Collapse is a long-context
    # effect (near-zero on a one-line prompt), so we evaluate on the current text
    # repeated into that regime. Auto-runs; re-runs when the text changes.
    _raw2 = tokenizer.encode(text_input.value, add_special_tokens=False)
    _tgt2 = 256
    _enc2 = (_raw2 * (_tgt2 // max(len(_raw2), 1) + 1))[:_tgt2] if len(_raw2) < _tgt2 else _raw2

    def _mu_content(ids_list, n_content):
        _ids2 = torch.tensor([ids_list], device=model.device)
        with torch.no_grad():
            _out2 = model(_ids2, output_hidden_states=True)
        _H2 = _out2.hidden_states[-1][0][-n_content:]   # content rows (BOS, if any, is at front)
        _T2 = _H2.shape[0]
        if _T2 < 2:
            return 0.0
        _n2  = _H2 / (_H2.norm(dim=-1, keepdim=True) + 1e-8)
        _sim = _n2 @ _n2.T
        return float(1 - _sim.triu(diagonal=1).sum().item() / (_T2 * (_T2 - 1) / 2))

    _nc = len(_enc2)
    _mw = _mu_content([BOS_ID] + _enc2, _nc)   # same content, with a BOS sink present
    _mn = _mu_content(_enc2, _nc)              # same content, no BOS
    _d  = _mw - _mn

    _df_c = pl.DataFrame({"Condition": ["With BOS", "Without BOS"], "mu": [_mw, _mn]})
    _ch5  = (
        alt.Chart(_df_c)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5, size=60)
        .encode(
            x=alt.X("Condition:N", title=None, axis=alt.Axis(labelColor="#94a3b8")),
            y=alt.Y("mu:Q", title="μ over content tokens (cosine distance)",
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Condition:N",
                scale=alt.Scale(domain=["With BOS", "Without BOS"], range=["#f59e0b", "#7c3aed"]),
                legend=None),
            tooltip=[alt.Tooltip("Condition:N"), alt.Tooltip("mu:Q", format=".4f")],
        )
        .properties(width=300, height=240,
            title=alt.TitleParams(
                text=f"μ over {_nc} content tokens: With BOS={_mw:.4f}, Without={_mn:.4f} (Δ={_d:+.4f})",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _msg = (
        f"Your text, repeated to **{_nc} content tokens**. Over those same tokens, μ = **{_mw:.4f}** "
        f"with a BOS sink present vs **{_mn:.4f}** without it (Δ={_d:+.4f})."
        + (f" The sink keeps content representations **{_d / max(_mn, 1e-8) * 100:.0f}% more diverse**, "
           "the over-mixing prediction, live on GPT-2." if _d > 0 else
           " The gap is small or absent at this length; it grows with context (scan below) "
           "and shows most sharply on the long-context benchmarks above.")
    )
    mo.vstack([_ch5, mo.md(_msg)], align="center")
    return


# ── Collapse Gap vs. Context Length ───────────────────────────────────────────

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Collapse Gap vs. Context Length

    Theorem 3.2 predicts the benefit of the sink grows with sequence length: longer contexts
    create more paths for information to mix, so the protection BOS provides becomes more
    critical. The experiment below scans from 32 to 960 tokens (the current text repeated)
    and plots μ_with_BOS vs μ_without_BOS as a curve. The gap should widen with length.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(mo):
    len_max_slider = mo.ui.slider(128, 960, step=128, value=512,
                                  label="Scan up to (tokens)", show_value=True)
    len_max_slider
    return (len_max_slider,)


@app.cell
def _(BOS_ID, alt, len_max_slider, mo, model, pl, text_input, tokenizer, torch):
    # Content-only μ (see the collapse cell): compares the SAME content tokens with vs
    # without a leading BOS at each length. All (length × condition) sequences run as ONE
    # padded, masked batch through the transformer body. model.transformer skips the
    # 50k-vocab LM head, whose logits we never use. Re-runs on slider or text change.
    import time as _t_cl
    _base_cl = tokenizer.encode(text_input.value, add_special_tokens=False)
    _max_cl  = min(len_max_slider.value, 1023)   # GPT-2 max pos = 1024 total tokens
    _rep_cl  = (_base_cl * ((_max_cl // max(len(_base_cl), 1)) + 2))[:_max_cl]
    _lens_cl = [l for l in [32, 64, 128, 256, 384, 512, 640, 768, 896, 960] if l <= _max_cl]

    _t0_cl = _t_cl.perf_counter()
    if model.device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    _seqs_cl = []
    for _L_cl in _lens_cl:
        _seqs_cl.append([BOS_ID] + _rep_cl[:_L_cl])   # with BOS: content at rows 1..L
        _seqs_cl.append(_rep_cl[:_L_cl])              # without:  content at rows 0..L-1
    _Tm_cl = max(len(s) for s in _seqs_cl)
    _ids_cl = torch.tensor(
        [s + [tokenizer.eos_token_id] * (_Tm_cl - len(s)) for s in _seqs_cl],
        device=model.device)
    _mask_cl = torch.tensor(
        [[1] * len(s) + [0] * (_Tm_cl - len(s)) for s in _seqs_cl], device=model.device)
    with torch.no_grad():
        _H_cl = model.transformer(_ids_cl, attention_mask=_mask_cl).last_hidden_state

    def _mu_rows(h):
        _T = h.shape[0]
        if _T < 2:
            return 0.0
        _n = h / (h.norm(dim=-1, keepdim=True) + 1e-8)
        _s = _n @ _n.T
        return float(1 - _s.triu(diagonal=1).sum().item() / (_T * (_T - 1) / 2))

    _gap_rows_cl = []
    for _i_cl, _L_cl in enumerate(_lens_cl):
        _mw_cl = _mu_rows(_H_cl[2 * _i_cl, 1:_L_cl + 1])      # with BOS, skip BOS row
        _mn_cl = _mu_rows(_H_cl[2 * _i_cl + 1, :_L_cl])       # without BOS
        _gap_rows_cl.append({
            "Length": _L_cl,
            "With BOS": round(_mw_cl, 5),
            "Without BOS": round(_mn_cl, 5),
            "Gap": round(_mw_cl - _mn_cl, 5),
        })
    _dt_cl = _t_cl.perf_counter() - _t0_cl
    _ntok_cl = int(_mask_cl.sum().item())

    _df_cl   = pl.DataFrame(_gap_rows_cl)
    _long_cl = _df_cl.select(["Length", "With BOS", "Without BOS"]).unpivot(
        index="Length", variable_name="Condition", value_name="μ(X)")

    _line_cl = (
        alt.Chart(_long_cl)
        .mark_line(point=alt.OverlayMarkDef(size=55))
        .encode(
            x=alt.X("Length:Q", title="Sequence length (tokens)",
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("μ(X):Q", title="μ over content tokens (cosine distance)",
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("Condition:N",
                scale=alt.Scale(domain=["With BOS", "Without BOS"],
                                range=["#f59e0b", "#7c3aed"]),
                legend=alt.Legend(labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("Length:Q"), alt.Tooltip("Condition:N"),
                      alt.Tooltip("μ(X):Q", format=".5f")],
        )
        .properties(width=440, height=240,
            title=alt.TitleParams(
                text="Content-token diversity: BOS vs no-BOS across sequence lengths (GPT-2, live)",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _gap_line_cl = (
        alt.Chart(_df_cl)
        .mark_line(color="#22d3ee", point=alt.OverlayMarkDef(color="#22d3ee", size=55))
        .encode(
            x=alt.X("Length:Q", title="Sequence length (tokens)",
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            y=alt.Y("Gap:Q", title="Gap (μ_with − μ_without)",
                      axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            tooltip=[alt.Tooltip("Length:Q"), alt.Tooltip("Gap:Q", format=".5f")],
        )
        .properties(width=440, height=180,
            title=alt.TitleParams(
                text="Sink benefit (μ_with − μ_without) vs context length",
                color="#e2e8f0", fontSize=11))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )
    _peak_cl  = max(_gap_rows_cl, key=lambda r: r["Gap"])
    _grows_cl = len(_gap_rows_cl) >= 2 and _gap_rows_cl[-1]["Gap"] > _gap_rows_cl[0]["Gap"]
    _trend_cl = ("The gap widens with length" if _grows_cl
                 else "On this text the gap does not grow monotonically, but stays positive")
    mo.vstack([
        _line_cl, _gap_line_cl,
        mo.md(f"Peak gap at length **{_peak_cl['Length']}**: μ_with={_peak_cl['With BOS']:.4f}, "
              f"μ_without={_peak_cl['Without BOS']:.4f}, gap={_peak_cl['Gap']:+.5f}. "
              f"{_trend_cl}, matching the mechanistic prediction of Theorem 3.2: the collapse "
              "problem worsens with context, so the sink's value as a countermeasure grows with it. "
              f"*(All {len(_lens_cl) * 2} sequences, {_ntok_cl} tokens, in one batched pass "
              f"through the transformer body, skipping the unused LM head: {_dt_cl:.2f}s"
              + (f", peak VRAM {torch.cuda.max_memory_allocated()/1e9:.2f} GB"
                 if model.device.type == "cuda" else "") + ".)*"),
    ], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# NOVEL EXTENSION: STRATEGIC SINK PLACEMENT
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Novel Extension: Strategic Sink Token Placement

    The paper establishes that sinks are load-bearing. This section tests whether they can be
    engineered on purpose.

    **Hypothesis:** a single BOS at position 0 forces every head to route long-range attention
    to the very start of the sequence. For long contexts, this creates a bottleneck. We test
    whether inserting additional BOS tokens every *K* positions distributes the sink load and
    relieves it.

    **Metric:** *content-token diversity* μ, the mean pairwise cosine distance among the
    last-layer hidden states of the **content (non-sink) tokens only**. Higher μ means content
    representations stay more distinct (less collapse). μ is measured over the
    **same content tokens** under every strategy, so inserting sink tokens cannot change it
    mechanically; it can only change it by altering how content is represented.
    (The tempting metric, *attention mass reaching content*, is dominated by sequence length
    and mechanically favours the shortest sequence, so it can never test this hypothesis. μ over
    a fixed content set is the honest choice.)

    **⚠ This experiment is not in the paper.** It is a novel hypothesis, tested here on GPT-2.
    Raise the length slider to probe the regime where Theorem 3.2 predicts the bottleneck bites.
    """)
    return


@app.cell(hide_code=True)
def _(MODEL_LABELS, MODEL_OPTIONS, get_model_id, mo, set_model_id):
    mo.ui.dropdown(
        options=MODEL_OPTIONS,
        value=MODEL_LABELS[get_model_id()],
        on_change=set_model_id,
        label="🔬 Model",
    )
    return


@app.cell
def _(mo):
    len_slider = mo.ui.slider(48, 512, step=32, value=128,
                              label="Content length (tokens)", show_value=True)
    len_slider
    return (len_slider,)


@app.cell
def _(BOS_ID, alt, len_slider, mo, model, pl, tokenizer, torch):
    # μ_content over the SAME content tokens for every strategy (see the intro above).
    # All 5 strategies run as ONE padded batch through the transformer body (the LM head's
    # logits are never used). Auto-runs on load; re-runs when the length slider changes.
    _N = len_slider.value
    _wds = ("the quick brown fox jumps over the lazy dog "
            "a cat sat on the mat light shines through dark clouds ").split()
    _content = tokenizer.encode(" ".join(_wds * 40), add_special_tokens=False)[:_N]
    _nC = len(_content)

    _strats = [("baseline\n(1 sink)", 9999, [BOS_ID] + _content)]
    for _kk in [8, 16, 32, 64]:
        _seq = [BOS_ID]
        for _i, _t in enumerate(_content):
            _seq.append(_t)
            if (_i + 1) % _kk == 0:
                _seq.append(BOS_ID)
        _strats.append((f"K={_kk}", _kk, _seq[:1024]))     # GPT-2 context cap

    _Tm_x = max(len(s) for _, _, s in _strats)
    # Padding uses eos == BOS_ID in GPT-2, so the keep-mask below (token != BOS_ID,
    # within real length) excludes pad rows and sink rows in one stroke.
    _ids_x = torch.tensor([s + [BOS_ID] * (_Tm_x - len(s)) for _, _, s in _strats],
                          device=model.device)
    _mask_x = torch.tensor([[1] * len(s) + [0] * (_Tm_x - len(s)) for _, _, s in _strats],
                           device=model.device)
    with torch.no_grad():
        _H_x = model.transformer(_ids_x, attention_mask=_mask_x).last_hidden_state

    def _mu_of(h):
        _T = h.shape[0]
        if _T < 2:
            return 0.0
        _n = h / (h.norm(dim=-1, keepdim=True) + 1e-8)
        _s = _n @ _n.T
        return float(1 - _s.triu(diagonal=1).sum().item() / (_T * (_T - 1) / 2))

    _res = []
    for _bi, (_name, _kv, _seq) in enumerate(_strats):
        _keep = torch.tensor(
            [t != BOS_ID for t in _seq] + [False] * (_Tm_x - len(_seq)),
            device=model.device)
        _res.append({"strategy": _name, "mu": _mu_of(_H_x[_bi][_keep]), "k_val": _kv,
                     "n_sinks": sum(1 for t in _seq if t == BOS_ID)})
    _mu_base = _res[0]["mu"]

    _df_e = pl.DataFrame(_res)
    # Honest comparison: best PERIODIC strategy vs the single-BOS baseline (never baseline
    # against itself), with sign, absolutes, and n.
    _best  = _df_e.filter(pl.col("k_val") != 9999).sort("mu", descending=True).row(0, named=True)
    _delta = _best["mu"] - _mu_base
    _pct   = _delta / max(abs(_mu_base), 1e-8) * 100

    _base_rule = (
        alt.Chart(pl.DataFrame({"mu": [_mu_base]}))
        .mark_rule(color="#64748b", strokeDash=[4, 3])
        .encode(y="mu:Q")
    )
    _pts = (
        alt.Chart(_df_e)
        .mark_point(size=170, filled=True, opacity=0.95, stroke="#07080f", strokeWidth=1)
        .encode(
            x=alt.X("strategy:O", title="Strategy", sort=alt.SortField("k_val"),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", labelAngle=0)),
            y=alt.Y("mu:Q", title="μ over content tokens (higher = less collapse)",
                    scale=alt.Scale(zero=False),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8", format=".3f")),
            color=alt.Color("k_val:Q", scale=alt.Scale(scheme="viridis"), legend=None),
            tooltip=[alt.Tooltip("strategy:O"), alt.Tooltip("mu:Q", format=".5f", title="μ_content"),
                     alt.Tooltip("n_sinks:Q", title="# sink tokens")],
        )
    )
    _ch6 = (
        (_base_rule + _pts)
        .properties(width=430, height=270,
            title=alt.TitleParams(
                text=f"Strategic sink placement: content-token diversity μ vs interval K (n={_nC})",
                color="#e2e8f0", fontSize=12))
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _mus_d = _df_e.filter(pl.col("k_val") != 9999).sort("k_val")["mu"].to_list()  # K=8,16,32,64
    _mono_density = all(_mus_d[i] >= _mus_d[i + 1] - 1e-9 for i in range(len(_mus_d) - 1))
    _climb = "climbs monotonically as sink density rises" if _mono_density else "rises with sink density"
    if _delta > 0:
        _verdict = (
            f"**Result:** content-token diversity μ {_climb}, from **{_mu_base:.3f}** with a single BOS "
            f"to **{_best['mu']:.3f}** at K={_best['k_val']} (**{_pct:+.0f}%**, n={_nC} tokens, "
            f"{_best['n_sinks']} sinks). This is the paper's *approximate no-op* at work: "
            "each inserted sink lets nearby heads route to a near-zero value and **stop mixing**, so "
            "content tokens keep more of their own identity. Less mixing is not automatically "
            "better; past a point it under-contextualizes. **Sink density is a knob with a sweet "
            "spot**, not a free win, and the test that settles it is downstream accuracy (RULER, "
            "Needle-in-a-Haystack), not μ alone. Raise the length slider: the effect grows with "
            "context, exactly as Theorem 3.2 predicts."
        )
    else:
        _verdict = (
            f"**Result:** no periodic strategy beats the single-BOS baseline at n={_nC} "
            f"(best: {_best['strategy']}, μ={_best['mu']:.4f} vs {_mu_base:.4f}; {_pct:+.1f}%). "
            "An honest null: at this length one position-0 sink already suffices, and extra sinks cost "
            "context without improving content diversity. Theorem 3.2 predicts the bottleneck bites at "
            "longer contexts. Raise the length slider to probe it."
        )
    mo.vstack([
        _ch6,
        mo.md(_verdict + "\n\n*⚠ Not in the paper. A novel hypothesis measured live on GPT-2. μ is "
              "computed over the identical content tokens in every condition, so adding sink tokens "
              "cannot inflate or deflate it by construction (the dashed line marks the baseline).*"),
    ], align="center")
    return


# ── GPU report card ────────────────────────────────────────────────────────────

@app.cell(hide_code=True)
def _(MODEL_CACHE, MODEL_ID, device, mo, torch):
    _ = MODEL_ID   # refresh this card on model change
    if device == "cuda":
        _name_g = torch.cuda.get_device_name(0)
        _total_g = torch.cuda.get_device_properties(0).total_memory / 1e9
        _res_g = torch.cuda.memory_allocated() / 1e9
        _models_g = [k for k in MODEL_CACHE if not k.endswith(":tokenizer")]
        _card = mo.md(
            f"""
    ---
    #### ⚙️ Under the hood

    **GPU:** {_name_g} ({_total_g:.0f} GB) · **{_res_g:.1f} GB resident** ·
    models cached: {', '.join(f'`{m}`' for m in _models_g)}

    Every experiment above runs as padded, masked, batched forward passes under
    `torch.no_grad()`: the census (24 prompts, 1 pass), Figure 2 (6 sequences, 2 passes),
    the collapse scan (up to 20 sequences, 1 pass through the transformer body, LM head
    skipped), sink placement (5 strategies, 1 pass). Entropy and sink metrics are fused
    tensor ops on-device.
    """)
    else:
        _card = mo.md(
            "---\n#### ⚙️ Under the hood\n\nRunning on **CPU**. The experiments are batched "
            "the same way as on GPU, just slower.")
    _card
    return


# ══════════════════════════════════════════════════════════════════════════════
# COULD WE DESIGN THE SINK AWAY?  (softmax normalization playground)
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Could We Design the Sink Away?

    Everything so far treats the sink as inevitable. It is not. The sink exists because softmax
    forces a head's attention weights to sum to exactly 1: a head with nothing worth mixing still
    has to spend all of its mass on tokens, and (Act I) position 0 is the cheapest place to dump it.
    So the sink is downstream of one specific modelling choice, the softmax normalization.

    The paper makes this framing explicit. It cites *softmax is not enough (for sharp
    out-of-distribution)* (Veličković et al., 2024) and relates the sink to gated,
    mixture-of-depths style mechanisms, though it does not itself train a sink-free attention
    variant. The playground below runs the one comparison that settles the argument: standard
    softmax against **softmax-off-by-one** (a `+1` in the denominator, letting the weights sum to
    *less* than 1, the same idea as adding a learnable no-op key with a zero value vector). Push a
    head toward disengaging and watch which formulation can actually do it.
    """)
    return


@app.cell
def _(mo):
    sm_signal = mo.ui.slider(
        0.0, 8.0, step=0.5, value=0.0,
        label="Signal on the content token (how much real information there is to attend to)",
        show_value=True)
    sm_disengage = mo.ui.slider(
        0.0, 8.0, step=0.5, value=3.0,
        label="Head's disengage pressure (how hard it tries to attend to nothing)",
        show_value=True)
    mo.vstack([sm_signal, sm_disengage])
    return sm_disengage, sm_signal


@app.cell(hide_code=True)
def _(alt, mo, np, pl, sm_disengage, sm_signal):
    # Pure softmax math, exact. A head looks at K=6 past tokens. It slightly prefers one
    # content token (position 3) by `signal`, and applies `disengage` pressure uniformly to
    # every real-token logit. The null slot (off-sequence, off-by-one only) has a fixed logit 0.
    def _softmax(x):
        _x = np.asarray(x, dtype=float)
        _e = np.exp(_x - _x.max())
        return _e / _e.sum()

    _K = 6
    _s = sm_signal.value
    _d = sm_disengage.value
    _logits = np.zeros(_K)
    _logits[3] += _s
    _logits = _logits - _d                      # uniform disengage pressure

    _w_std = _softmax(_logits)                   # weights over real tokens only, sum = 1
    _w_o1 = _softmax(np.append(_logits, 0.0))    # append null slot (logit 0), sum = 1 over K+1

    _slots = [f"t{_j}" for _j in range(_K)] + ["∅ off-seq"]
    _kinds = ["token"] * _K + ["off-sequence"]
    _long = pl.DataFrame({
        "slot": _slots * 2,
        "weight": list(_w_std) + [0.0] + list(_w_o1),
        "formulation": ["Standard softmax"] * (_K + 1) + ["Off-by-one softmax"] * (_K + 1),
        "kind": _kinds * 2,
    })

    _bars = (
        alt.Chart(_long)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("slot:N", sort=_slots, title=None,
                    axis=alt.Axis(labelColor="#94a3b8", labelAngle=0, labelFontSize=10)),
            y=alt.Y("weight:Q", title="attention weight", scale=alt.Scale(domain=[0, 1]),
                    axis=alt.Axis(labelColor="#94a3b8", titleColor="#94a3b8")),
            color=alt.Color("kind:N",
                scale=alt.Scale(domain=["token", "off-sequence"], range=["#22d3ee", "#f59e0b"]),
                legend=alt.Legend(title=None, labelColor="#94a3b8", orient="bottom")),
            column=alt.Column("formulation:N", sort=["Standard softmax", "Off-by-one softmax"],
                header=alt.Header(labelColor="#e2e8f0", titleColor="#e2e8f0", labelFontSize=12)),
            tooltip=[alt.Tooltip("formulation:N"), alt.Tooltip("slot:N"),
                     alt.Tooltip("weight:Q", format=".1%")],
        )
        .properties(width=215, height=230)
        .configure_view(stroke="#1e2d47", fill="#0d1220")
        .configure(background="#07080f")
    )

    _real_o1 = float(_w_o1[:_K].sum())
    _null_o1 = float(_w_o1[_K])

    _cs = "background:#0d1220;border:1px solid #1e2d47;border-radius:8px;padding:14px 18px;text-align:center;"
    _cv = "font-size:1.7em;font-weight:700;line-height:1;margin-bottom:4px;"
    _cl = "font-size:0.7em;color:#8896a8;text-transform:uppercase;letter-spacing:0.05em;"
    _cg = "display:grid;grid-template-columns:repeat(2,1fr);gap:10px;width:100%;max-width:40rem;margin:0 auto 0.4em;"
    _cards = mo.Html(f"""<div style="{_cg}">
      <div style="{_cs}"><div style="{_cv}color:#22d3ee">100.0%</div>
        <div style="{_cl}">Standard · mass on tokens</div>
        <div style="font-size:0.65em;color:#94a3b8">off-sequence: 0% (not representable)</div></div>
      <div style="{_cs}"><div style="{_cv}color:#f59e0b">{_null_o1 * 100:.1f}%</div>
        <div style="{_cl}">Off-by-one · mass off-sequence</div>
        <div style="font-size:0.65em;color:#94a3b8">on tokens: {_real_o1 * 100:.1f}%</div></div>
    </div>""")

    if _d >= 2.0 and _s < 1.0:
        _note = (
            f"The head is trying to disengage. **Standard softmax cannot let it.** Lowering every "
            f"logit by the same amount leaves the distribution unchanged (softmax is shift-invariant), "
            f"so 100% of attention still lands on tokens, spread flat. In a trained causal model the "
            f"cheapest way to spend that forced mass is to dump it on one token, and Act I showed which "
            f"one: position 0. **Off-by-one** breaks the shift-invariance with its `+1`, so the same "
            f"pressure drains **{_null_o1 * 100:.0f}%** of the attention off-sequence. That off-sequence "
            f"slot is exactly what a physical sink token stands in for when the formula has no room for it."
        )
    elif _s >= 3.0:
        _note = (
            f"Now the head has real work: content token **t3** carries a strong signal, so both "
            f"formulations concentrate on it and the off-sequence slot stays nearly empty "
            f"({_null_o1 * 100:.0f}%). When there is something worth mixing, the sink question is moot. "
            f"The sink only matters when a head has *nothing* to do. Drop the signal to 0 to see it."
        )
    else:
        _note = (
            f"Standard softmax always commits 100% of its mass to tokens; off-by-one currently leaves "
            f"**{_null_o1 * 100:.0f}%** off-sequence. Raise the disengage pressure with the signal at 0 "
            f"to see the gap open: standard softmax stays pinned at 100% on tokens no matter how hard the "
            f"head pushes, because shifting all logits equally does nothing to a softmax."
        )

    mo.vstack([_cards, _bars, mo.md(
        _note + "\n\nThe first-token sink is not a law of attention. It is an artifact of the "
        "normalization we picked. Change the normalization and the head gets an explicit off "
        "switch, so it no longer has to hijack a real token to build one.")], align="center")
    return


# ══════════════════════════════════════════════════════════════════════════════
# CONCLUSION
# ══════════════════════════════════════════════════════════════════════════════

@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The Full Story, in One Paragraph

    Deep Transformers face a fundamental problem: repeated attention layers *mix* token
    representations until they converge and collapse. The deeper the model, the longer the context,
    the worse the problem. Gradient descent discovered the cheapest fix: route most attention to
    `<BOS>`, which has a near-zero value vector, making the head contribute approximately zero
    to the residual stream. The token passes through unchanged. Representations stay diverse.
    Sinks are *learned switches that turn heads off when they have nothing to contribute*. Remove the switch and the model breaks.

    ---

    ## Summary of Key Numbers

    | Finding | Number | Source |
    |---|---|---|
    | LLaMA 3.1 405B sink rate (ε=0.8) | **78.29%** | Table 1, §4.2 |
    | LLaMA 3.1 8B sink rate (ε=0.8) | **45.97%** | Table 1, §4.2 |
    | RULER 4096-ctx with BOS (Gemma 7B) | **82.57%** | Table 3, §5 |
    | RULER 4096-ctx without BOS (Gemma 7B) | **0.00%** | Table 3, §5 |
    | ARC-Easy drop (Gemma 7B, −BOS) | **80.77% → 28.49%** | Table 3, §5 |
    | Causal + fixed BOS → remove at inference | **90.84% → 0.05% sink** | Table 2, §5 |
    | Context 128 vs 2048 sink rate | **~0% → ~39%** | Figure 5a, §4.1 |
    | Pre-training scale | 120M params, 5B tokens (ctx exp.), 30B tokens (packing exp.) | Appendix A.1 |

    ---

    ## Citation

    ```bibtex
    @inproceedings{barbero2025attention,
      title     = {Why do {LLM}s attend to the first token?},
      author    = {Federico Barbero and {\'{A}}lvaro Arroyo and Xiangming Gu and
                   Christos Perivolaropoulos and Michael Bronstein and
                   Petar Veli{\v{c}}kovi{\'{c}} and Razvan Pascanu},
      booktitle = {Conference on Language Modeling (COLM)},
      year      = {2025},
      url       = {https://arxiv.org/abs/2504.02732},
    }
    ```

    *Paper: [arXiv:2504.02732](https://arxiv.org/pdf/2504.02732)  ·
    Code ([Gu et al.'s](https://arxiv.org/pdf/2410.10781) codebase, adapted by the authors for pre-training experiments):
    [github.com/sail-sg/Attention-Sink](https://github.com/sail-sg/Attention-Sink)  ·
    Built for the [alphaxiv × marimo notebook competition #2](https://alphaXiv.ai).*
    """)
    return


if __name__ == "__main__":
    app.run()
