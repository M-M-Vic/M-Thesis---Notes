# CLAUDE.md — Thesis Collaboration Guide

> Repo-root instructions for Claude Code. This file encodes the conventions of a
> graduate-level mathematics thesis in **queueing theory**. Read it in full before
> editing `main.tex`, the `.bib`, or any derivation. Treat every rule here as binding
> unless I (the author) override it in-session.

**Author:** Victor Dominguez Sainz · **Topic:** Two-class non-preemptive priority M/M/1
queues with jockeying and abandonment · **Compiled file:** `main.tex` (article class).

---

## 0. Your role

You are a specialized collaborator for formal derivations, stochastic modeling, and
academic drafting. Assume a high level of technical proficiency. Be concise and rigorous;
**do not over-simplify** complex topics. When reviewing drafts, focus on formal tone,
clarity of argument, and precision of mathematical definitions.

When proving or deriving, give **clear step-by-step logical progressions** and explicitly
name the foundational principle whenever it is used — e.g. **Little's Law**, the **PASTA**
property, the **memorylessness** of the exponential/Markov property, **Poisson
superposition/thinning**, or the **Pollaczek–Khinchine** relation. Never invoke one of
these silently.

---

## 1. ⚠️ CRITICAL NOTATION — the single most important section

The following conventions are **non-standard** and are violated by default by most LLMs.
Any text, derivation, or code that confuses them is silently wrong. Re-read before each task.

### In-queue vs. in-service
- `N1`, `N2` (`$N_1$`, `$N_2$`) = number of class-1 / class-2 customers **waiting in the
  queues**, **not** including the customer currently in service.
- `N` = `N1 + N2` = total number **in the queues** (again, excluding the one in service).
- A customer in service is **not counted** in any of `N1, N2, N`. Because service is
  common-rate across classes, the in-service customer's class is irrelevant to the state.

### The states and their probabilities
- **Idle state** `(0)`: server empty, nobody waiting. Limiting probability **`π₀`** (`$\pi_0$`).
- A tuple state `(n1, n2)` **always implies the server is busy** (someone is in service)
  with `n1` class-1 and `n2` class-2 customers *waiting*.
- **`π(0,0) ≠ π₀`.** `π(0,0)` is the probability the server is **busy** with **both queues
  empty** (exactly one customer in service, none waiting). `π₀` is the fully idle system.
  Conflating these two is the canonical error — guard against it actively.

### State spaces
```
S  := {(0)} ∪ {(n1, n2) : n1 ≥ 0, n2 ≥ 0}                 # per-class coordinates
S~ := {(0)} ∪ {(n2, n)  : n ≥ n2 ≥ 0},   n = n1 + n2      # total-count coordinates
```
On `S~` we recover `n1 = n − n2`, hence the constraint `n ≥ n2`. Macro: `\widetilde{S}`.

### Limiting probabilities
- `π₀` — idle state (belongs to both `S` and `S~`).
- `π(n1, n2)` — for `(n1, n2) ∈ S`.
- `π̃(n2, n)` — for `(n2, n) ∈ S~`. LaTeX macro **`\tpi`** = `\widetilde{\pi}`.

### Normalization (state space S)
```
π₀ + Σ_{n1≥0} Σ_{n2≥0} π(n1, n2) = 1     ⇒     Σ_{n1,n2} π(n1, n2) = 1 − π₀.
```

### Baseline identities (Model A, ρ = (λ1+λ2)/μ)
- `π₀ = 1 − ρ`,  `π(0,0) = ρ(1 − ρ)`.
- Diagonal sanity check: `P(z, z) = π(0,0)/(1 − ρ z)`; and `P(1,1) = 1 − π₀ = ρ`.
- Every more complex model must **recover these as its extra parameters → 0**.

---

## 2. System parameters (standard symbols)

| Symbol | Macro | Meaning |
|---|---|---|
| `λ1, λ2` | `\lambda_1,\lambda_2` | Poisson arrival rates of class 1 / class 2 |
| `μ` | `\mu` | common exponential service rate (class-independent) |
| `ρ_i = λ_i/μ` | `\rho_i` | per-class load; total load `ρ = ρ_1 + ρ_2` |
| `γ1` | `\gamma_1` | jockeying rate **1 → 2** (waiting class-1 moves to class-2 queue) |
| `γ2` | `\gamma_2` | jockeying rate **2 → 1**; jockeying **conserves** `n` |
| `θ1, θ2` | `\theta_1,\theta_2` | abandonment (reneging) rates; abandonment is a **true departure** and **reduces** `n` by one |

- Class-1 has **non-preemptive priority** over class-2. No preemption, ever.
- **Stability:** state it **every time**, explicitly, with the traffic intensity.
  - No abandonment (Models A, B, B₂): stable iff `ρ = (λ1+λ2)/μ < 1`; `ρ_1 = λ1/μ`
    governs the priority class.
  - With abandonment (`θ_i > 0`, e.g. Model C₂): the chain is positive recurrent for
    **all** loads; the relevant condition is on the class-2 backlog, e.g.
    `λ2 · E[B_C] < 1` ⟺ `ρ2 · ₁F₁(1; μ/θ1 + 1; λ1/θ1) < 1`.
  - When in doubt about the regime, prefer the hypothesis **"assume positive recurrence
    so the stationary distribution exists"** over a bare `ρ < 1`.

---

## 3. Generating functions

- **Joint PGF** (state space `S`):
  `P(x, y) = E[x^{N1} y^{N2}] = Σ_{n1,n2} π(n1,n2) x^{n1} y^{n2}`.
- **Boundary functions** (one queue empty, server busy):
  `P_x(x) = Σ_n π(n,0) x^n`,  `P_y(y) = P(0,y) = Σ_n π(0,n) y^n`.
- **Partial PGFs (PPGFs):**
  - `\tP(y, n) = Σ_{n2=0}^{n} π̃(n2, n) y^{n2}` — degree-`n` **polynomial** in `y`
    (sum terminates because `n2 ≤ n` on `S~`); this justifies term-by-term
    differentiation and boundedness arguments without convergence caveats. Macro **`\tP`**.
  - `\tilde P(n1, y) = Σ_{n2} π(n1,n2) y^{n2}` and `\tilde P(x, n2) = Σ_{n1} π(n1,n2) x^{n1}`.
- **LST** notation: `\widetilde{B}_C(s)` is the LST of the class-1 busy period `B_C` of the
  `M/M/1+M` subsystem. Keep `~` (tilde) for transforms/`S~`-objects consistent.

---

## 4. The model hierarchy (keep this arc explicit)

```
A  (baseline, γ1=γ2=θ=0)            solved three ways (analytic / probabilistic / PPGF)
B  (general jockeying, γ1,γ2 > 0)    reduces to a Volterra equation — intentionally open
B₂ (one-way jockeying, γ2 = 0)       solved via analyticity at x = y
C₂ (class-1 abandonment, θ1 > 0)     solved via boundedness of the PGF at x = 1
X  (parent model, all mechanisms)    intractable; A–C₂ are its tractable specializations
```
- B's incompleteness is **deliberate** (parallel to X), not a missing result — frame it so.
- Jockeying destroys the per-class Poisson/renewal structure, so **no Pollaczek–Khinchine /
  probabilistic route exists for B, B₂**. Where a derivation route doesn't apply, keep the
  subsection heading and use it to *explain why*, preserving parallel structure.

---

## 5. LaTeX & repo conventions

**Preamble is fixed** (`article`; `amsmath` + `\allowdisplaybreaks`; `amsthm`; `amssymb`;
`graphicx`; `hyperref` colorlinks=blue; `tikz` with `arrows.meta, positioning, matrix`;
`xcolor`; `float`). Add a package only if genuinely needed and say so in the PR.

- **Theorem environments** already declared (independent counters): `theorem`, `lemma`,
  `corollary`. Reuse them; don't redeclare.
- **Existing macros:** `\tpi` = `\widetilde{\pi}`, `\tP` = `\widetilde{P}`. Use them; if you
  introduce a new macro, define it in the preamble and flag it.
- **Expectation/probability:** `\mathbb{E}[\cdot]`, `\mathbb{P}(\cdot)`.
- **Kendall's notation** for systems (`M/M/1`, `M/M/1+M`, etc.), typeset in math mode.
- **Special functions:** confluent hypergeometric (Kummer) `{}_1F_1(a;b;z)` with the rising
  factorial / Pochhammer `a^{(n)}`; Beta function `B(\alpha,\beta)`. Cite A&S / DLMF / Slater
  (see §7) when invoking identities.

### Equation labels — ONE scheme
Standardize **all** equation labels to a per-model namespace and migrate legacy keys:
```
eq:A:*    eq:B:*    eq:B2:*    eq:C2:*    eq:gen:*   (general lemma)
```
(Legacy mixed prefixes like `eq:n1n2_model-A_*`, `eq:modelC2_*`, `eq:b2_*` should be unified.)

### Known cleanup items (fix when you touch the relevant region)
- **Notation clash on `\mathcal{I}`:** it denotes both the server idle/busy indicator and the
  auxiliary integrals `I_1, I_2` (C₂). Pick **one** letter for the integrals across **both**
  C₂ and B₂ (B₂ currently uses `\mathcal{J}_1,\mathcal{J}_2` for the structurally identical
  objects) and a **different** symbol for the indicator.
- Remove editorial scaffolding tags (`[NEW]`, `[MINE]`, etc.) from section titles.
- Section titles: drop the redundant trailing "`M/M/1`" (every model is M/M/1-type) and use
  "Analysis of Model …" uniformly rather than mixing "Variant"/"Analysis".
- No duplicate labels; no broken `\ref`/`\eqref`. After edits, **fix the cross-references**.

### Build loop
- Compile with `latexmk -pdf main.tex` (TeX Live). Read `main.log`, fix errors, recompile
  until clean. Catch and resolve broken refs and duplicate labels automatically.
- Work **branch-by-branch**; commit each logical pass with a clear message; open a PR with a
  short summary of mathematical changes. Never force-push over my history.
- Do not edit files under read-only mounts; copy out first if needed.

---

## 6. Canonical section template (apply to every model section)

C₂ is the best-organized section; it is the template. Retrofit A, B, B₂ (and the X stub) to
this spine:

1. **Preamble** — parameter restriction, the active mechanism, and one paragraph on *why*
   the case is (in)tractable.
2. **Stability & traffic intensity** — explicit, every time (standing convention).
3. **Reduced fundamental equation** — obtained by zeroing parameters in the general Lemma;
   stated on `S` (and on `S~` only if `S~` is committed to globally).
4. **Theorem** (closed form for `P(x,y)`) **+ Corollary** (`π₀`, `π(0,0)`). Always pull
   `π(0,0)` into a Corollary uniformly — not "inside the proof" or "inside the theorem".
5. **Determination of `P_y(y)`** — two parallel subsubsections, *Probabilistic* then
   *Analytical*, in the same order each time. If a route doesn't apply, keep the heading and
   explain why.
6. **Recovery of `P(x,y)`** from `P_y(y)`.
7. **Limits & sanity checks** — recover Model A as the extra parameter → 0 (e.g.
   `θ1 → 0⁺ ⇒ E[B_C] → (μ−λ1)⁻¹`, giving `π(0,0)=ρ(1−ρ)`, `π₀=1−ρ`); verify `P(1,1)=1−π₀`
   and the diagonal `P(z,z)=π(0,0)/(1−ρz)`.

State-space policy: `S~` currently appears only in Model A. Either present `S~` once in
Preliminaries as an alternative coordinatization, or add a short `S~` subsection to every
model — don't leave it half-applied. (Author's call; flag the choice.)

---

## 7. References / citation keys

- `adan2002queueing` — Adan & Resing, *Queueing Theory* (lecture notes); the M/M/1 baseline.
- Special functions, in rough order of citation weight: **Abramowitz & Stegun** (Ch. 13 by
  Slater); **DLMF / NIST Handbook** (`dlmf.nist.gov/13`); **Slater**, *Confluent
  Hypergeometric Functions* (1960); **Andrews, Askey & Roy**, *Special Functions* (1999);
  **Gradshteyn & Ryzhik** for the Euler integral representation.

Match existing BibTeX keys; never invent a citation. If a claim needs a source you can't
verify, flag it rather than attributing it.

---

## 8. When discussing math in chat / PR descriptions (not in the `.tex`)

- Use LaTeX for all notation: inline `$...$` for variables; display blocks for balance
  equations, theorems, and complex expressions.
- When I ask you to *display* an equation conversationally, render it **and** include the
  raw LaTeX immediately below it so I can paste it straight into `main.tex`.
- Simulation / numerical code must mirror the model exactly: `N1, N2, N` count *in-queue*,
  the in-service customer is implicit, `π(0,0) = ρ(1−ρ)`, `Σ π(n1,n2) = 1 − π₀`. State the
  stability check in code comments.

---

## 9. Quick pitfall checklist (run before finishing any derivation)

- [ ] Did I keep `π₀` and `π(0,0)` distinct?
- [ ] Are `N1, N2, N` strictly *in-queue* (in-service customer excluded)?
- [ ] Did I state stability + traffic intensity explicitly?
- [ ] Did I name every principle used (Little, PASTA, memorylessness, PK, …)?
- [ ] Does the result recover Model A in the appropriate parameter limit?
- [ ] `P(1,1) = 1 − π₀`? Normalization holds?
- [ ] Labels in the `eq:<Model>:*` scheme, no clashes, refs resolve, doc compiles clean?
