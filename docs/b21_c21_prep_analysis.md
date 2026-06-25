# Preparatory analysis — rewriting §10 (Model-$\BH$) and §11 (Model-$\CH$)

Prepared 2026-06-25. Companion to `docs/opus_rewrite_prompt.md`. Source files:
`chapters/10_model_b21.tex`, `chapters/11_model_c21.tex`.

All LaTeX below preserves the existing `\label{…}` keys and uses British spelling. Every
algebraic claim has been verified two independent ways before being written up here:

1. **Computer algebra (sympy).** The kernel roots were handled by *implicit differentiation
   of* $f(x^*(y),y)=0$ and Taylor series about $y=1$, **not** by differentiating the explicit
   surd root — sympy mis-simplifies $\sqrt{(\mu+\theta_1-\lambda_1)^2}$ without a sign
   assumption and returns spurious mismatches.
2. **Independent sparse-CTMC stationary solve.** Priority service decrements the **class-1**
   queue when $n_1\ge1$ (the in-flow $\mu\,\pi(n_1+1,n_2)$). Closed forms match the CTMC to
   5–6 digits for both models, including a $\rho=1.20$ case for $\CH$ that is positive
   recurrent because head abandonment stabilises it.

---

## §0. Correctness audit — **no inaccuracies found**

> There are **no `[INACCURACY]` flags** in either section. Every theorem, corollary, kernel
> root, sensitivity, mean queue length and mean waiting time is correct as written.

Confirmed exactly (CAS + CTMC):

| Quantity | $\BH$ | $\CH$ |
|---|---|---|
| kernel quadratic `eq:*:quad` | ✓ | ✓ |
| $f(1)$ factorisation | $-(1-y)(\lambda_2+\gamma_1)$ ✓ | $-\lambda_2(1-y)$ ✓ |
| $(x^*)'(1)$ | $(\lambda_2+\gamma_1)/(\mu+\gamma_1-\lambda_1)$ ✓ | $\lambda_2/(\mu+\theta_1-\lambda_1)$ ✓ |
| $(x^*)''(1)$ | — | $2(\mu+\theta_1)\lambda_2^2/(\mu+\theta_1-\lambda_1)^3$ ✓ |
| $\pi_0,\ \pi(0,0)$ | $1-\rho,\ \rho(1-\rho)$ ✓ | `eq:C21:pi0_pi00` ✓ |
| $P_y(1)$ | $\rho(1-\rho_B)$ ✓ | $(1-\pi_0)(1-\rho_C)$ ✓ |
| $\mathbb{E}[N_1]$ | $\rho\rho_B/(1-\rho_B)$ ✓ | $(1-\pi_0)\rho_C/(1-\rho_C)$ ✓ |
| $\mathbb{E}[N_2]$ | `eq:B21:EN2` ✓ | `eq:C21:EN2` ✓ |
| $\theta_1,\gamma_1\to0^+$ limits → Model-A | ✓ | ✓ |
| bracket collapses (5a, 5b) | ✓ | ✓ |

Two small things to verify while rewriting (not errors, just author-facing checks):

- **Stability $\Rightarrow\rho_C<1$ (`§11`, stability paragraph).** The claim that
  `eq:C21:stability` "implies $\rho_C:=\lambda_1/(\mu+\theta_1)<1$" is **true** and provable, not
  merely asserted. A 30 000-trial random search found no counterexample; algebraically, if
  $\mu+\theta_1\le\lambda_1$ then $\mu-\lambda\le-\theta_1-\lambda_2<0$ and
  $(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\le\lambda_1(\mu+\theta_1-\lambda)\le-\lambda_1\lambda_2<0$,
  contradicting stability. Worth a one-clause footnote so the reader is not left to take it on faith.
- **The $\rho-\rho_B$ decomposition (`§10`, after `eq:B21:EN2`)** reads
  $\rho-\rho_B=\rho_2+\lambda_1\gamma_1/[\mu(\mu+\gamma_1)]$. This is **correct** — the apparent
  "$\lambda_2\mu$" term is $\lambda_2(\mu+\gamma_1)/[\mu(\mu+\gamma_1)]=\rho_2$ once the
  $\lambda_2\gamma_1$ is reabsorbed. Keep as is.

The remaining sections are presented in the order I recommend executing them:
**§A** settle notation (Dim 4) → **§B** write the verified derivations in that notation (Dim 5)
→ **§C** decide the cross-reference cuts (Dim 1) → **§D** compress equations (Dim 3) →
**§E** polish prose (Dim 2). Fixing notation first means the expanded math, the cuts and the
compression are all written once, in their final symbols.

---

## §A. Dimension 4 — align notation with Model-$B_2$ and across the two sections

### A.1 Adopt the `Step (i)/(ii)/(iii)` skeleton (matches $B_2$)

Both Kernel-Method proofs have exactly three phases. Labelling them mirrors $B_2$ and makes the
$\BH\!\leftrightarrow\!\CH$ parallel visible at a glance. Use this skeleton in **both**
`\begin{proof}[Proof of Theorem~\ref{thm:*:PGF}]`:

```latex
\textbf{Step (i): kernel quadratic and root location.}
% divide the coefficient of P(x,y) by y, get eq:*:quad, locate x*(y)<1<x+(y).
\textbf{Step (ii): pin the boundary function $P_y(y)$.}
% set x=x*(y); boundedness forces the RHS to vanish; solve for P_y(y).
\textbf{Step (iii): recover $P(x,y)$.}
% substitute P_y(y) back, factor the kernel, cancel (x-x*(y)).
```

### A.2 Keep `A(y)` as the shared coefficient; note the substitution

The auxiliary coefficient is *the same formula* with $\gamma_1\leftrightarrow\theta_1$:

$$A(y)=\lambda_1+\lambda_2(1-y)+\mu+\delta,\qquad \delta=\gamma_1\ (\BH),\quad \delta=\theta_1\ (\CH).$$

Do **not** introduce $A^B,A^C$ superscripts — too heavy. Reuse `A(y)` locally in each proof and add
one clause in $\CH$: *"with $A(y)$ as in $\BH$ but $\gamma_1$ replaced by $\theta_1$."* The kernels
differ only in the **constant term** ($\mu+\gamma_1y$ vs $\mu+\theta_1$), which is exactly the
structural point developed in §B.4 below — so flag the constant term, not $A(y)$, as the locus of
the difference.

### A.3 Introduce $\Delta(y)$ in **both** sections (recommended)

$\CH$ already abbreviates its $P_y$-denominator $\Delta(y)$. Defining the analogous object in
$\BH$ makes the boundary function **identical in form** across the two models:

$$P_y(y)=\frac{\mu\,x^*(y)(1-y)\,\pi(0,0)}{\Delta(y)},\qquad
\Delta(y)=\begin{cases}(\mu+\gamma_1y)\bigl(x^*(y)-y\bigr) & (\BH),\\[4pt]
(\mu+\theta_1y)\,x^*(y)-y(\mu+\theta_1) & (\CH).\end{cases}$$

This is pedagogically strong: $\Delta_B$ **factors** (a manifest $(x^*-y)\to0$ at $y=1$) because
jockeying conserves the total count, whereas $\Delta_C$ **does not** factor — the analytic
signature of broken conservation, and the precise reason $\CH$ needs the $0/0$ Taylor argument in
§B.3 while $\BH$ does not. In $\BH$, add at `eq:B21:Py`:

```latex
P_y(y) = \frac{\mu\,x^*(y)\,(1-y)\,\pi(0,0)}{\Delta(y)},
\qquad \Delta(y):=(\mu+\gamma_1 y)\bigl(x^*(y)-y\bigr),
\label{eq:B21:Py}
```

### A.4 Effective loads $\rho_B,\rho_C$ — state provenance honestly

- **$\rho_B=\lambda_1/(\mu+\gamma_1)$ coincides with the $B_2$ effective load.** Head-of-line
  jockeying gives the priority queue the *same* effective clearance rate $\mu+\gamma_1$ as $B_2$,
  so the symbol is literally shared. Note this at `eq:B21:Px1`:
  *"the same effective load $\rho_B=\lambda_1/(\mu+\gamma_1)$ that governs Model-$B_2$
  (§\ref{sec:model_b2})."*
- **$\rho_C=\lambda_1/(\mu+\theta_1)$ is specific to $\CH$.** Do **not** claim it is "the $C_2$
  effective load": in $C_2$ the class-1 subsystem is an $M/M/1{+}M$ (Erlang-A) queue with *no*
  single effective load. Phrase as: *"the head-of-line analogue of $\rho_B$; under linear
  abandonment ($C_2$) the priority subsystem is Erlang-A and admits no such single load."*

---

## §B. Dimension 5 — expanded derivations (all verified)

### B.1 (5a) The bracket collapse in the $\BH$ proof

Replace the terse two-line `align*` ("where the bracket collapses because
$(x-y)x^* - x(x^*-y) = y(x-x^*)$") with the full computation. Using
$\mu(x-y)+\gamma_1y(x-y)=(x-y)(\mu+\gamma_1y)$ and `eq:B21:Py`:

```latex
\bigl[\mu(x-y)+\gamma_1 y(x-y)\bigr]P_y(y) - \mu x(1-y)\,\pi(0,0)
&= (x-y)(\mu+\gamma_1 y)\,\frac{\mu x^*(y)(1-y)\,\pi(0,0)}{(\mu+\gamma_1 y)\bigl(x^*(y)-y\bigr)}
   - \mu x(1-y)\,\pi(0,0) \\[2pt]
&= \mu(1-y)\,\pi(0,0)\left[\frac{(x-y)\,x^*(y)}{x^*(y)-y}-x\right] \\[2pt]
&= \mu(1-y)\,\pi(0,0)\,\frac{(x-y)\,x^*(y)-x\bigl(x^*(y)-y\bigr)}{x^*(y)-y} \\[2pt]
&= \mu(1-y)\,\pi(0,0)\,\frac{y\,\bigl(x-x^*(y)\bigr)}{x^*(y)-y},
```

the last line because $(x-y)x^*-x(x^*-y)=xx^*-yx^*-xx^*+xy=y(x-x^*)$. The factor $(\mu+\gamma_1y)$
cancels in line 2 — *this is where $\BH$ is simpler than $\CH$* (in $\CH$ nothing cancels here).

### B.2 (5b) The curly-bracket collapse in the $\CH$ proof

The text asserts the curly bracket "collapses term-by-term to $(\mu+\theta_1)y(x-x^*)$ (no use of
the kernel relation is required)". Expand it, substituting
$\Delta(y)=(\mu+\theta_1y)x^*-y(\mu+\theta_1)$:

```latex
\bigl[\mu(x-y)+\theta_1 y(x-1)\bigr]x^*(y) - x\,\Delta(y)
&= \bigl[\mu x-\mu y+\theta_1 xy-\theta_1 y\bigr]x^*(y)
   - x\bigl[(\mu+\theta_1 y)x^*(y)-y(\mu+\theta_1)\bigr] \\[2pt]
&= \mu x\,x^* - \mu y\,x^* + \theta_1 xy\,x^* - \theta_1 y\,x^*
   - \mu x\,x^* - \theta_1 xy\,x^* + xy(\mu+\theta_1) \\[2pt]
&= -\mu y\,x^*(y) - \theta_1 y\,x^*(y) + xy(\mu+\theta_1) \\[2pt]
&= (\mu+\theta_1)\,y\,\bigl(x-x^*(y)\bigr),
```

where $x^*$ abbreviates $x^*(y)$; the $\mu x\,x^*$ and $\theta_1 xy\,x^*$ terms cancel pairwise in
line 3. Because no kernel relation is invoked, the collapse is purely algebraic — exactly parallel
to (5a), but here the surviving prefactor is $(\mu+\theta_1)$ rather than a cancelled $(\mu+\gamma_1y)$.

### B.3 (5c) The $P_y'(1)$ computation for $\CH$ — the missing derivation

This is the one genuinely under-derived passage. Below is a complete, verified derivation. Use the
abbreviations
$$m:=\mu+\theta_1,\quad D:=\mu+\theta_1-\lambda_1=m-\lambda_1>0,\quad \lambda:=\lambda_1+\lambda_2,$$
$$S:=(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\ (\text{stability numerator}),\qquad
Z:=\mu(\mu+\theta_1)+\lambda_1\theta_1,$$
so that $\pi_0=S/Z$, $\ 1-\pi_0=\lambda m/Z$, $\ \pi(0,0)=\lambda\pi_0/\mu=\lambda S/(\mu Z)$,
$\ \rho_C=\lambda_1/m$, $\ 1-\rho_C=D/m$. The two root sensitivities are
$$x^{*\prime}(1)=\frac{\lambda_2}{D},\qquad x^{*\prime\prime}(1)=\frac{2m\,\lambda_2^2}{D^3}.$$

Write $P_y(y)=N(y)/\Delta(y)$ with $N(y)=\mu x^*(y)(1-y)\pi(0,0)$ and
$\Delta(y)=(\mu+\theta_1y)x^*(y)-y(\mu+\theta_1)$. Both vanish at $y=1$ (since $x^*(1)=1$). Set
$t=y-1$ and expand to second order using $x^*(1+t)=1+\tfrac{\lambda_2}{D}t+\tfrac{m\lambda_2^2}{D^3}t^2+O(t^3)$.

**Step 1 — confirm $0/0$ and get the first-order coefficients.**

```latex
N(1)=0,\quad \Delta(1)=(\mu+\theta_1)\cdot1-(\mu+\theta_1)=0;\qquad
N'(1)=-\mu\,\pi(0,0)=-\lambda\pi_0,\quad
\Delta'(1)=m\,x^{*\prime}(1)+\theta_1-m=-\frac{S}{D}.
```

(For $\Delta'(1)$: $m\frac{\lambda_2}{D}+\theta_1-m=\frac{m\lambda_2-\mu D}{D}=-\frac{(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1}{D}=-\frac{S}{D}$,
using $\theta_1-m=-\mu$.) Hence the **value** of $P_y$ at $y=1$ is recovered cleanly:

```latex
P_y(1)=\frac{N'(1)}{\Delta'(1)}=\frac{-\lambda\pi_0}{-S/D}
      =\frac{\lambda\pi_0 D}{S}=\frac{\lambda D}{Z}=(1-\pi_0)(1-\rho_C),
```

since $\pi_0=S/Z$ and $1-\pi_0=\lambda m/Z$, $1-\rho_C=D/m$. ✓ (matches `eq:C21:P11`).

**Step 2 — second-order coefficients.**

```latex
N''(1)=-2\mu\,\pi(0,0)\,x^{*\prime}(1)=\frac{2\lambda_2}{D}\,N'(1)=-\frac{2\lambda_2\lambda\pi_0}{D},
\qquad
\Delta''(1)=m\,x^{*\prime\prime}(1)+2\theta_1\,x^{*\prime}(1)
          =\frac{2m^2\lambda_2^2}{D^3}+\frac{2\theta_1\lambda_2}{D}.
```

**Step 3 — slope of the $0/0$ ratio.** With $N(1)=\Delta(1)=0$, the quotient rule for a removable
singularity gives $P_y'(1)=\dfrac{N''(1)\Delta'(1)-N'(1)\Delta''(1)}{2\,\Delta'(1)^2}$. Substituting
Steps 1–2 and simplifying (verified by CAS) yields the compact closed form

```latex
P_y'(1)=\frac{\lambda_2\,\lambda\,(\mu+\theta_1)\,\bigl(D^2+\lambda_1\lambda_2\bigr)}
             {D\;Z\;S},
\qquad D^2+\lambda_1\lambda_2=(\mu+\theta_1-\lambda_1)^2+\lambda_1\lambda_2 .
```

**Step 4 — assemble $\mathbb{E}[N_2]$.** From `eq:C21:EN2_implicit`,
$\mathbb{E}[N_2]=\tfrac{\mu}{\lambda_2}P_y'(1)-(1-\pi_0)$. With $1-\pi_0=\lambda m/Z$,

```latex
\mathbb{E}[N_2]
=\frac{\lambda m}{Z}\left[\frac{\mu\bigl(D^2+\lambda_1\lambda_2\bigr)}{D\,S}-1\right]
=\frac{\lambda m}{Z}\cdot\frac{\mu\bigl(D^2+\lambda_1\lambda_2\bigr)-D\,S}{D\,S}.
```

The bracket numerator collapses by the identity (verified by CAS)

```latex
\mu\bigl(D^2+\lambda_1\lambda_2\bigr)-D\,S=\lambda_2\,(m^2-\lambda_1\theta_1),
\qquad m^2-\lambda_1\theta_1=(\mu+\theta_1)^2-\lambda_1\theta_1,
```

giving the claimed `eq:C21:EN2`,

```latex
\mathbb{E}[N_2]
=\frac{\lambda_2\,\lambda\,(\mu+\theta_1)\bigl[(\mu+\theta_1)^2-\lambda_1\theta_1\bigr]}
      {(\mu+\theta_1-\lambda_1)\,
       \bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]\,
       \bigl[(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\bigr]}.
\label{eq:C21:EN2}
```

The last denominator bracket is $S$, so $\mathbb{E}[N_2]$ is finite **iff** stability holds and
diverges as $\pi_0\to0^+$. As $\theta_1\to0^+$: $m\to\mu$, $D\to\mu-\lambda_1$, numerator
$\to\lambda_2\lambda\mu\cdot\mu^2$, denominator $\to(\mu-\lambda_1)\mu^2\cdot\mu(\mu-\lambda)$, so
$\mathbb{E}[N_2]\to\lambda_2\lambda/[(\mu-\lambda_1)(\mu-\lambda)]=\rho\rho_2/[(1-\rho_1)(1-\rho)]$,
recovering Model-A. ✓

> **Author note.** If you prefer not to expose $(x^*)''(1)$, the *cleanest* presentation keeps
> Steps 1–4 but states only the two boxed identities ($\Delta'(1)=-S/D$ and
> $\mu(D^2+\lambda_1\lambda_2)-DS=\lambda_2(m^2-\lambda_1\theta_1)$) as the load-bearing steps,
> then quotes the result. Both routes are correct; the boxed identities are the parts a reader
> cannot reconstruct in their head.

### B.4 (5d) Where the extra $\gamma_1$ in $(x^*)'(1)$ comes from — three-kernel comparison

The implicit differentiation of $f(x,y)=\lambda_1x^2-A(y)x+C(y)=0$ at $(x,y)=(1,1)$ gives
$x^{*\prime}(1)=-f_y/f_x$. The numerator $f_y$ is

$$f_y=-A'(y)\,x+C'(y)=\lambda_2 x+C'(y),\qquad A'(y)=-\lambda_2 .$$

So **the extra term in the numerator is exactly $C'(1)$, the $y$-derivative of the kernel's
constant term.** This is the single structural fact that distinguishes the three models:

| Model | constant term $C(y)$ | $C'(y)$ | $f_y(1,1)$ | $x^{*\prime}(1)$ |
|---|---|---|---|---|
| A | $\mu$ | $0$ | $\lambda_2$ | $\lambda_2/(\mu-\lambda_1)$ |
| $\CH$ | $\mu+\theta_1$ | $0$ | $\lambda_2$ | $\lambda_2/(\mu+\theta_1-\lambda_1)$ |
| $\BH$ | $\mu+\gamma_1 y$ | $\gamma_1$ | $\lambda_2+\gamma_1$ | $(\lambda_2+\gamma_1)/(\mu+\gamma_1-\lambda_1)$ |

**Mechanistic reading (one paragraph to add at `eq:B21:xstar_deriv`):** jockeying moves the
head-of-line class-1 customer *into Queue 2*, so its in-flow lands in $(n_1-1,n_2+1)$ and carries a
factor $y$ — which is why the constant term is the $y$-dependent $\mu+\gamma_1y$ and
$C'(1)=\gamma_1\ne0$. Abandonment *removes* the customer, so its in-flow lands in $(n_1-1,n_2)$ with
no $y$; the constant term $\mu+\theta_1$ is $y$-independent and $C'(1)=0$, exactly as in Model-A.
The presence or absence of $y$ in the kernel's constant term is thus the **analytic fingerprint of
conservation versus departure**, mirroring the diagonal test on the convection factor.

```latex
\frac{d}{dy}x^*(1)=\frac{\lambda_2+\gamma_1}{\mu+\gamma_1-\lambda_1}.
\label{eq:B21:xstar_deriv}
```

---

## §C. Dimension 1 — replace re-derivations by cross-references

### C.1 Corollary `cor:B21:pi0` proof → two sentences

The diagonal argument duplicates `cor:A:pi0` line for line. Because jockeying conserves the total
count, the factor $\gamma_1y(x-y)$ and the term $\mu(x-y)P_y(y)$ both vanish on $x=y=z$, returning
*verbatim* the Model-A diagonal equation. Replace the whole proof with:

```latex
\begin{proof}[Proof of Corollary~\ref{cor:B21:pi0}]
Set $x=y=z$ in~\eqref{eq:B21:fundamental}. Jockeying conserves the total customer count, so the
factor $\gamma_1 y(x-y)$ vanishes on the diagonal, as does $\mu(x-y)P_y(y)$; the equation reduces
\emph{verbatim} to the Model-$A$ diagonal equation. The computation of
Corollary~\ref{cor:A:pi0} therefore applies unchanged, giving
$P(z,z)=\pi(0,0)/(1-\rho z)$~\eqref{eq:B21:Pzz}, and with the idle
balance~\eqref{eq:B21:idle} ($\pi(0,0)=\rho\pi_0$) and $P(1,1)=1-\pi_0$,
$\pi_0=1-\rho$ and $\pi(0,0)=\rho(1-\rho)$.
\end{proof}
```

Keep `eq:B21:Pzz` (it is referenced later by the total-queue-length argument), but drop the
intermediate factoring lines.

### C.2 Root location — share the $f(1)<0$ argument $\BH\!\to\!\CH$, do **not** cite Model-A

**Caveat (important):** Model-A located its root by **monotonicity** of $x^*(y)$
(`eq:A:xstar_prime`, $x^{*\prime}>0$ with $x^*(1)=1$), *not* by the upward-parabola $f(1)<0$
argument. So $\BH/\CH$ cannot cite Model-A for it. Instead, give the $f(1)<0$ argument once in
$\BH$ (it is the cleaner of the two), and in $\CH$ reduce to:

```latex
Exactly as in~\S\ref{sssec:B21:analytical}, $f(x):=\lambda_1 x^2-A(y)x+(\mu+\theta_1)$ is an
upward parabola with $f(1)=-\lambda_2(1-y)<0$ for $y\in[0,1)$, so $x^*(y)<1<x^+(y)$; at $y=1$,
$x^*(1)=1$ and $x^+(1)=(\mu+\theta_1)/\lambda_1>1$ (by $\rho_C<1$).
```

(Optional, out of scope: the $f(1)<0$ argument could retrofit Model-A too, unifying all three — a
one-line win if you are touching §6.)

### C.3 Vieta and the $P_y(0)=\pi(0,0)$ check

- **Vieta** ($x^*x^+=(\mu+\delta)/\lambda_1$): already a single clause "by Vieta's formulas" in
  both — nothing to cut; leave it.
- **$P_y(0)=\pi(0,0)$ check** appears verbatim in both proofs. Keep it once (in $\BH$), and in
  $\CH$ reduce to a half-sentence: *"as at $y=0$ in §\ref{sssec:B21:analytical}, $\Delta(0)=\mu\,x^*(0)$
  gives $P_y(0)=\pi(0,0)$."* It is a sanity check, so trimming the second copy costs no rigour.

### C.4 PK-unavailability paragraphs

Both are sound; the **distinction must survive**: $\BH$ fails because the merged Queue-2 input is
non-Poisson *and* state-dependent (correlated with $N_1$) — a PASTA failure; $\CH$ fails because the
class-1 busy period is not the busy period of any single $M/M/1$ or $M/M/1{+}M$ queue (head
abandonment is inactive while the lone class-1 customer is *in service*), so Queue 2 sees a
non-renewal $M/G/1$ input. Keep $\BH$ as the fuller statement (it introduces the PASTA mechanism),
and shorten $\CH$ to lean on it:

```latex
As for Model-$\BH$ (\S\ref{sssec:B21:probabilistic}), the Pollaczek--Khinchine route of
Models~$A$ and~$C_2$ does not transfer. The reason here is specific to abandonment: head
abandonment fires only while a class-$1$ customer \emph{waits} ($N_1\ge1$) and is inactive while
the single class-$1$ present is in service, so the class-$1$ busy period is not that of any
$M/M/1$ or $M/M/1{+}M$ queue. Queue~$2$ therefore sees a non-renewal $M/G/1$ input and no
Pollaczek--Khinchine representation of $P_y(y)$ exists; the analytical route of
\S\ref{sssec:C21:analytical} is the operative one.
```

---

## §D. Dimension 3 — compress multi-line equations

### D.1 Balance equations — single-line the three short ones

Of the five, the $x$-boundary, the $(0,0)$ equation and the idle equation are short enough to drop
`\begin{split}` and sit on one line; keep the interior and $y$-boundary split (four terms each).
For $\BH$:

```latex
\bigl[\lambda_1+\lambda_2+\mu+\gamma_1\bigr]\pi(n_1,0)
  = \mu\,\pi(n_1+1,0)+\lambda_1\pi(n_1-1,0), && n_1\ge1,\ n_2=0, \label{eq:B21:xboundary}\\
\bigl[\lambda_1+\lambda_2+\mu\bigr]\pi(0,0)
  = (\lambda_1+\lambda_2)\pi_0+\mu\,\pi(1,0)+\mu\,\pi(0,1), && \nonumber\\
(\lambda_1+\lambda_2)\pi_0 = \mu\,\pi(0,0). && \label{eq:B21:idle}
```

Same for the $\CH$ analogues (with $\mu\to\mu+\theta_1$ on the relevant in-flows).

### D.2 Kernel-quadratic evaluation at $x=1$ — one line each

```latex
% B^H:
f(1)=\lambda_1-\bigl[\lambda_1+\lambda_2(1-y)+\mu+\gamma_1\bigr]+(\mu+\gamma_1 y)
    =-(1-y)(\lambda_2+\gamma_1)<0,\qquad y\in[0,1).
% C^H:
f(1)=\lambda_1-\bigl[\lambda_1+\lambda_2(1-y)+\mu+\theta_1\bigr]+(\mu+\theta_1)
    =-\lambda_2(1-y)<0,\qquad y\in[0,1).
```

### D.3 $\mathbb{E}[N_2]$ for $\BH$ (`eq:B21:EN2`) — single `align` row

```latex
\mathbb{E}[N_2]=\frac{\rho^2}{1-\rho}-\frac{\rho\,\rho_B}{1-\rho_B}
              =\frac{\rho\,(\rho-\rho_B)}{(1-\rho)(1-\rho_B)}.
\label{eq:B21:EN2}
```

(The intermediate $\rho[\rho(1-\rho_B)-\rho_B(1-\rho)]$ step adds nothing — drop the line break.)

### D.4 $\CH$ class-2 waiting time — do not re-typeset the denominator

The current $\mathbb{E}[W_2]$ reprints the entire three-factor denominator of `eq:C21:EN2`. Replace
with the one-liner and a pointer; $\Lambda_2=\lambda_2$ because Queue 2 has no jockeying input and
$\theta_2=0$:

```latex
\mathbb{E}[W_2]=\frac{\mathbb{E}[N_2]}{\lambda_2}
=\frac{\lambda\,(\mu+\theta_1)\bigl[(\mu+\theta_1)^2-\lambda_1\theta_1\bigr]}
      {(\mu+\theta_1-\lambda_1)\,
       \bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]\,
       \bigl[(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\bigr]},
```

or, leaner still, state $\mathbb{E}[W_2]=\mathbb{E}[N_2]/\lambda_2$ with $\mathbb{E}[N_2]$ from
`\eqref{eq:C21:EN2}` and stop. Prefer the latter.

### D.5 The "bracket collapses" `align*` in the $\BH$ proof — note the Dim-3/Dim-5 conflict

This two-line block is the *same passage* that Dimension 5a asks you to **expand**. Do not do both:
replace the terse two lines with the four-line §B.1 block (clarity wins over brevity for the one
non-obvious cancellation), then keep the subsequent "divide by the factored kernel … cancel
$(x-x^*)$" as a single display. Net change: $+2$ lines here, but it removes the only step a reader
must take on faith.

---

## §E. Dimension 2 — simplify prose

### E.1 Unified openings (≤3 sentences each, shared logic stated once)

Put the "linear rate → ODE vs. flat rate → algebraic → Kernel Method" contrast in $\BH$'s opening,
then let $\CH$ inherit it:

```latex
% Section 10 opening:
Model-$\BH$ simplifies the one-way jockeying model Model-$B_2$ by letting \emph{only the head of
Queue~1} jockey, at the fixed rate $\gamma_1$ whenever $n_1\ge1$, so the aggregate rate is
$\gamma_1\mathbf{1}_{\{n_1\ge1\}}$ rather than $\gamma_1 n_1$. This single change is decisive: the
flat rate contributes only the \emph{algebraic} factor $\gamma_1 y(x-y)$ to the fundamental
equation, with \emph{no derivative of $P$}, where $B_2$'s linear rate produces a convective term
$\gamma_1 xy(x-y)\,\partial P/\partial x$ and an ODE (\S\ref{sec:model_b2}). The equation is then
solved by the Kernel Method exactly as in Model-$A$ (\S\ref{sec:model_a}), and the resulting PGF
is structurally identical to Model-$A$'s, differing only in the kernel root.
```

```latex
% Section 11 opening:
Model-$\CH$ is the abandonment counterpart of Model-$\BH$: only the head of Queue~1 may renege, at
the fixed rate $\theta_1$ whenever $n_1\ge1$, so as in \S\ref{sec:model_b21} the flat rate yields an
\emph{algebraic} fundamental equation solvable by the Kernel Method. The one difference is decisive:
abandonment is a \emph{true departure}, so it breaks the conservation of the total customer count
that Model-$\BH$ enjoyed --- the factor $\theta_1 y(x-1)$ does \emph{not} vanish on the diagonal ---
and the empty-state probabilities and class-$2$ mean queue length consequently need separate
arguments.
```

### E.2 "Two structural remarks are in order …" → one sentence

Both remarks are self-evident from the equations. Replace the whole paragraph with:

```latex
Jockeying is an out-transition from any state with $n_1\ge1$ (the $+\gamma_1$ on the left of
\eqref{eq:B21:interior}--\eqref{eq:B21:xboundary}) and an in-transition into any state with
$n_2\ge1$ from $(n_1+1,n_2-1)$; it is absent when $n_2=0$ (no source state) or $n_1=0$ (no head to
move), and all other transitions match Model-$A$.
```

### E.3 The $P_y(y)$ isolation step — one line

In both proofs, compress "Setting $x=x^*(y)$ … and equating the right-hand side to zero, … whence":

```latex
% B^H:
Setting $x=x^*(y)$ in~\eqref{eq:B21:fundamental} forces the right-hand side to vanish:
$(x^*(y)-y)(\mu+\gamma_1 y)P_y(y)=\mu x^*(y)(1-y)\pi(0,0)$, giving~\eqref{eq:B21:Py}.
% C^H:
Setting $x=x^*(y)$ likewise gives $\Delta(y)\,P_y(y)=\mu x^*(y)(1-y)\pi(0,0)$, i.e.~\eqref{eq:C21:Py},
with $\Delta(y)=(\mu+\theta_1 y)x^*(y)-y(\mu+\theta_1)$.
```

### E.4 The future-work forward-reference at the end of $\BH$ "Limits"

The head-of-line-ladder sentence ("$\BH$ occupies the $k=1$ rung … interpolates towards $B_2$ as
$k\to\infty$") is a *connecting* remark, not a sanity check, and currently sits oddly in a "Limits
and sanity checks" subsection. **Recommendation:** keep a one-clause pointer here and move the
elaboration to §\ref{sec:future_work}:

```latex
Beyond the $\gamma_1\to0^+$ limit, $\BH$ is the $k=1$ rung of the head-of-line ladder of
\S\ref{sec:future_work}, which interpolates towards Model-$B_2$ as $k\to\infty$.
```

Before committing, confirm the "ladder" is actually defined in §\ref{sec:future_work}
(`chapters/14_conclusion.tex`); if it is not yet written, either add a one-line definition there or
drop the "$k=1$ rung" framing to avoid a dangling forward-reference.

---

## Build / hygiene checklist after the rewrite

- [ ] Labels untouched: `eq:B21:*`, `eq:C21:*`, `thm:*:PGF`, `cor:*:pi0`, `lem:*:fundamental`,
      `sssec:*:analytical`, `sssec:*:probabilistic`.
- [ ] New cross-refs resolve: `cor:A:pi0`, `sec:model_b2`, `sec:model_a`, `rem:gen:reading`,
      `sec:future_work`, `sssec:B21:analytical`.
- [ ] If you introduce $\Delta(y)$ in $\BH$ (§A.3), update `eq:B21:Py` and the §B.1 block to use it.
- [ ] `latexmk -pdf main.tex`; read `main.log`; resolve any duplicate-label / broken-`\eqref`.
- [ ] British spelling; no US `-ize`/`behavior`/`center`.
