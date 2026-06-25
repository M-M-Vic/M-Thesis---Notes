# Preparatory Analysis for Rewriting Sections on Model-$\BH$ and Model-$\CH$

## Role and context

You are a collaborator on a graduate-level mathematics thesis in **queueing theory**.
The author will rewrite Sections 10 and 11 (Model-$\BH$ and Model-$\CH$) in their own
words; your job is to carry out the preparatory analysis so they can do so efficiently.

**Author:** Víctor Domínguez Sainz  
**Topic:** Two-class non-preemptive priority M/M/1 queues with jockeying and abandonment

---

## Critical notation — read before touching any equation

These conventions are **non-standard** and are violated silently by default.

- `N1`, `N2` = class-1 / class-2 customers **waiting** (excludes the one in service).
- The **idle state** `(0)` has probability `π₀`. The state `(0,0)` means the server is
  **busy** with both queues empty (one customer in service, none waiting).
  **`π(0,0) ≠ π₀`**; conflating these is the canonical error.
- **State space `S`:** `{(0)} ∪ {(n1,n2): n1≥0, n2≥0}` with the server busy in every
  `(n1,n2)` state.
- `π₀` = idle probability; `π(n1,n2)` = busy-state probabilities on `S`.
- Joint PGF: `P(x,y) = E[x^N1 y^N2] = Σ π(n1,n2) x^n1 y^n2`.
- Boundary function: `P_y(y) = P(0,y) = Σ_n π(0,n) y^n`.
- **British spelling throughout**: analyse, utilise, characterise, behaviour, centre, modelling.
- Theorem environments: `theorem`, `lemma`, `corollary` — reuse, never redeclare.
- Macros: `\tpi = \widetilde{\pi}`, `\tP = \widetilde{P}`.
- Equation labels in `eq:B21:*` and `eq:C21:*` namespaces.

**Baseline identities (Model A):** `π₀ = 1−ρ`, `π(0,0) = ρ(1−ρ)`, `P(z,z) = π(0,0)/(1−ρz)`.  
Every more complex model must recover these when its extra parameters → 0.

---

## Model hierarchy and parameters

```
A   baseline (γ1=γ2=θ1=θ2=0)         — Kernel Method, rational PGF
B   general jockeying (γ1,γ2>0)       — Method of Characteristics + VoP
B₂  one-way jockeying (γ2=0,θ=0)     — ODE in x, integrating factor
B^H head-of-line jockeying (γ₂=θ=0)  — flat rate γ₁·1{n1≥1}, algebraic → Kernel Method
C₂  class-1 abandonment (θ1>0,γ=0)   — ODE in x, integrating factor
C^H head-of-line abandonment (γ=0)    — flat rate θ₁·1{n1≥1}, algebraic → Kernel Method
```

- **Jockeying** conserves total customer count `N1+N2`.  
- **Abandonment** is a true departure and **breaks** conservation.

---

## What the Preliminaries section covers (§3)

The Preliminaries section already derives and names the following — **do not re-derive, only cross-reference**:

| Method | Label | Content |
|---|---|---|
| M/M/1 queue | `ssec:mm1` | Steady-state distribution, Little's Law, busy period |
| PASTA property | `ssec:priority` | Poisson arrivals see time averages; lack-of-anticipation |
| M/M/1+M (Erlang-A) | `ssec:erlangA` | π₀ via ₁F₁, busy-period LST, Pincherle's theorem |
| Pollaczek–Khinchine | `ssec:pk` | M/G/1 PGF formula |
| Kummer ₁F₁ | `ssec:kummer` | Series, Euler integral, contiguous ratios |
| Integrating factor | `sssec:if` | Standard form, formula eq:ode:general |
| Method of Characteristics | `sssec:moc` | Characteristic curves, first integrals |
| Variation of Parameters | `sssec:vop` | VoP formula eq:ode:vop_general |

The Kernel Method itself is **not a named section** in Preliminaries; it is introduced and
used in `§sssec:A:analytical` (Model-A). The B₂ proof uses three named steps: (i) standard
form + integrating factor, (ii) analyticity at `x=y` to pin `P_y(y)`, (iii) recovering
`P(x,y)`.

---

## Model-A PGF (the template for both sections)

For reference, the Model-A theorem states:

```
P(x,y) = ρ(1−ρ)(1−y)(x−x*(y)) / [kernel(x,y)·(x*(y)−y)]
```

factored as `μρ(1−ρ)(1−y) / [λ₁(x*(y)−y)(x+(y)−x)]`, where the kernel quadratic is

```
λ₁x² − [λ₁+λ₂(1−y)+μ]x + μ = 0,    roots: x*(y) < 1 < x+(y) for y∈[0,1).
```

Vieta: `x*(y)·x+(y) = μ/λ₁`. Derivative at y=1: `(x*)′(1) = λ₂/(μ−λ₁)`.

---

## Model-B₂ proof structure (notation reference for parallelism)

B₂ uses the integrating factor on an ODE. Its exponents are named
`α(y) = μ/(γ₁y)`, `β(y) = (1−y)(λy−μ)/(γ₁y)`, `b*(y) = α+β+1`.
Its auxiliary integrals are `𝒽₁(x,y)`, `𝒽₂(x,y)`. Proof labelled Step (i)/(ii)/(iii).
Its effective load is `ρ_B = λ₁/(μ+γ₁)` (for B^H, same symbol `ρ_B`).

---

## Source text: Section 10 — Model-$\BH$

```latex
\section{Analysis of Model-\texorpdfstring{$\BH$}{B2-H} (\texorpdfstring{$\gamma_1>0$}{gamma1>0} head-of-line, \texorpdfstring{$\gamma_2=\theta_1=\theta_2=0$}{gamma2=theta1=theta2=0})}
\label{sec:model_b21}

Model-$\BH$ is a deliberately simplified variant of the one-way jockeying model
Model-$B_2$. In Model-$B_2$ \emph{every} waiting class-$1$ customer may jockey to the
class-$2$ queue, so the aggregate jockeying rate out of a state grows linearly with the
queue length, $\gamma_1 n_1$. Here, by contrast, only the \emph{customer at the head of
Queue~1} --- the one that would be the next class-$1$ customer to enter service --- is
allowed to jockey, at the fixed rate $\gamma_1$ whenever $n_1\ge 1$. The aggregate
jockeying rate is therefore $\gamma_1\,\mathbf{1}_{\{n_1\ge 1\}}$ rather than
$\gamma_1 n_1$.

This single change is decisive for tractability. In Model-$B_2$ the linear coefficient
$\gamma_1 n_1$ produces, upon forming the joint PGF, a term proportional to
$xy(x-y)\,\partial P/\partial x$, turning the fundamental equation into a first-order
linear ODE in $x$ that requires the integrating-factor machinery of
\S\ref{sec:model_b2}. The flat rate $\gamma_1\,\mathbf{1}_{\{n_1\ge1\}}$, on the
other hand, contributes only the \emph{algebraic} factor $\gamma_1 y(x-y)$ to the
coefficient of $P(x,y)$; \emph{no derivative of $P$ appears}. The fundamental equation is
then purely algebraic and can be solved by the Kernel Method exactly as in Model-$A$
(\S\ref{sec:model_a}). The analysis below mirrors the analytical treatment of
Model-$A$ step by step, and the resulting PGF turns out to be \emph{structurally
identical} to that of Model-$A$, the only difference being a shift in the characteristic
roots.

\textbf{Stability.} Jockeying relocates a waiting customer between the two queues but does
not remove anyone from the system; the total number of customers is therefore conserved by
the jockeying mechanism, exactly as in Model-$A$. Since there is no abandonment, the chain
is positive recurrent if and only if the total traffic intensity satisfies
\begin{equation}
    \rho = \frac{\lambda_1+\lambda_2}{\mu} < 1,
    \label{eq:B21:stability}
\end{equation}
with $\rho_1=\lambda_1/\mu$ governing the priority class.

\subsection{Balance equations}

Because the jockeying rate is now constant in $n_1$ rather than linear, the balance
equations are \emph{not} obtained by zeroing parameters in the general
Lemma~\ref{lem:gen:fundamental_equation} (whose jockeying coefficient is $\gamma_1 n_1$);
they must be stated directly. The jockeying transition $(n_1,n_2)\to(n_1-1,n_2+1)$ occurs
at the fixed rate $\gamma_1$ whenever $n_1\ge1$. On the state space $S$ the global balance
equations read
\begin{align}
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu+\gamma_1\right]\pi(n_1,n_2) \\
        &\quad=\quad \mu\,\pi(n_1+1,n_2)
          +\lambda_1\pi(n_1-1,n_2)
          +\lambda_2\pi(n_1,n_2-1)
          +\gamma_1\pi(n_1+1,n_2-1)
    \end{split}
    &&n_1\ge1,\;n_2\ge1, \label{eq:B21:interior} \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu+\gamma_1\right]\pi(n_1,0)
          \;=\; \mu\,\pi(n_1+1,0)
          +\lambda_1\pi(n_1-1,0)
    \end{split}
    &&n_1\ge1,\;n_2=0, \label{eq:B21:xboundary} \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu\right]\pi(0,n_2) \\
        &\quad=\quad \mu\,\pi(1,n_2)
          +\gamma_1\pi(1,n_2-1)
          +\lambda_2\pi(0,n_2-1)
          +\mu\,\pi(0,n_2+1)
    \end{split}
    &&n_1=0,\;n_2\ge1, \label{eq:B21:yboundary} \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu\right]\pi(0,0)
          = (\lambda_1+\lambda_2)\pi_0
          + \mu\,\pi(1,0)
          + \mu\,\pi(0,1),
    \end{split} &&\nonumber \\
    \begin{split}
        &(\lambda_1+\lambda_2)\pi_0 = \mu\,\pi(0,0).
    \end{split} &&\label{eq:B21:idle}
\end{align}
Two structural remarks are in order. First, jockeying is an \emph{out}-transition from any
state with $n_1\ge1$ (hence the $+\gamma_1$ in the left-hand sides of
\eqref{eq:B21:interior} and~\eqref{eq:B21:xboundary}) and an \emph{in}-transition into any
state with $n_2\ge1$ from the state $(n_1+1,n_2-1)$ (hence the $\gamma_1\pi(n_1+1,n_2-1)$
in~\eqref{eq:B21:interior} and the $\gamma_1\pi(1,n_2-1)$ in~\eqref{eq:B21:yboundary}).
Second, when $n_2=0$ there is no jockeying in-flow, since it would have to originate from
the non-existent state $(n_1+1,-1)$; and when $n_1=0$ there is no jockeying out-flow. The
remaining transitions --- Poisson arrivals at $\lambda_1,\lambda_2$ and service
completions at $\mu$ --- are exactly those of Model-$A$.

\subsection{Fundamental PGF equation}

\begin{lemma}[Fundamental equation for Model-$\BH$]\label{lem:B21:fundamental}
Assume positive recurrence, so that the stationary distribution exists and
$P(x,y)=\sum_{n_1,n_2\ge0}\pi(n_1,n_2)x^{n_1}y^{n_2}$ is analytic on the closed unit
polydisc. Then $P(x,y)$ and the boundary function $P_y(y)=P(0,y)$ satisfy
\begin{equation}
    \begin{split}
        &\left[(\lambda_1+\lambda_2+\mu)xy - \mu y - \lambda_1 x^2y - \lambda_2 xy^2
               + \gamma_1 y(x-y)\right]P(x,y) \\
        &\quad=\quad \left[\mu(x-y) + \gamma_1 y(x-y)\right]P_y(y)
               - \mu x(1-y)\,\pi(0,0).
    \end{split}
    \label{eq:B21:fundamental}
\end{equation}
\end{lemma}

\begin{proof}
Apart from the jockeying terms, equations~\eqref{eq:B21:interior}--\eqref{eq:B21:idle}
coincide with the balance equations of Model-$A$. Multiplying each balance equation by
$x^{n_1}y^{n_2}$, summing over its domain and multiplying through by $xy$, the
Model-$A$ part reproduces exactly the left- and right-hand sides of the Model-$A$
fundamental equation~\eqref{eq:A:fundamental},
\begin{equation*}
    \left[ (\lambda_1+\lambda_2+\mu)xy - \mu y - \lambda_1 x^2y - \lambda_2 xy^2 \right] P(x,y)
    = \mu(x-y) P_y(y) - \mu x(1-y)\,\pi(0,0),
\end{equation*}
so it remains only to collect the jockeying contribution. Its \emph{out}-flow appears in
every state with $n_1\ge1$:
\begin{equation*}
    \gamma_1\sum_{n_1\ge1}\sum_{n_2\ge0}\pi(n_1,n_2)\,x^{n_1}y^{n_2}
    = \gamma_1\bigl[P(x,y)-P_y(y)\bigr],
\end{equation*}
while its \emph{in}-flow enters every state with $n_2\ge1$ from $(n_1+1,n_2-1)$:
\begin{equation*}
    \gamma_1\sum_{n_1\ge0}\sum_{n_2\ge1}\pi(n_1+1,n_2-1)\,x^{n_1}y^{n_2}
    = \gamma_1\,\frac{y}{x}\sum_{m_1\ge1}\sum_{m_2\ge0}\pi(m_1,m_2)\,x^{m_1}y^{m_2}
    = \gamma_1\,\frac{y}{x}\bigl[P(x,y)-P_y(y)\bigr],
\end{equation*}
where we substituted $m_1=n_1+1,\ m_2=n_2-1$. The net jockeying contribution (out minus
in) is therefore $\gamma_1\bigl(1-\tfrac{y}{x}\bigr)\bigl[P(x,y)-P_y(y)\bigr]$; multiplying
by $xy$ gives $\gamma_1 y(x-y)\bigl[P(x,y)-P_y(y)\bigr]$. Adding this to the Model-$A$
equation and moving the $P_y$ part to the right-hand side yields~\eqref{eq:B21:fundamental}.
\end{proof}

\noindent\textit{Remark.}
Equation~\eqref{eq:B21:fundamental} contains \emph{no derivative} of $P$. The flat
jockeying rate has contributed the algebraic factor $\gamma_1 y(x-y)$ to the coefficient of
$P(x,y)$ where Model-$B_2$, with its linear rate $\gamma_1 n_1$, contributes the
convective term $\gamma_1 xy(x-y)\,\partial P/\partial x$. Setting $\gamma_1=0$
recovers~\eqref{eq:A:fundamental} verbatim.

\subsection{Closed-form solution}

The following theorem is the main result of this section; its proof follows the
analytical (Kernel Method) treatment of Model-$A$ in~\S\ref{sssec:A:analytical}.

\begin{theorem}[Closed-form PGF for Model-$\BH$]\label{thm:B21:PGF}
Consider the two-class non-preemptive priority queue with Poisson arrival rates
$\lambda_1,\lambda_2$, common exponential service rate $\mu$, and head-of-line class-$1$
jockeying at rate $\gamma_1>0$ (with $\gamma_2=\theta_1=\theta_2=0$). Under the stability
condition~\eqref{eq:B21:stability}, the joint PGF $P(x,y)=\mathbb{E}[x^{N_1}y^{N_2}]$ is
the rational function
\begin{equation}
    P(x,y) \;=\; \frac{\mu\,\rho(1-\rho)\,(1-y)}
    {\lambda_1\,\bigl(x^*(y)-y\bigr)\,\bigl(x^+(y)-x\bigr)},
    \label{eq:B21:PGF}
\end{equation}
where $x^*(y)$ and $x^+(y)$ are the two roots of the kernel quadratic
\begin{equation}
    \lambda_1 x^2 - \bigl[\lambda_1+\lambda_2(1-y)+\mu+\gamma_1\bigr]x + (\mu+\gamma_1 y) = 0,
    \label{eq:B21:quad}
\end{equation}
with $x^*(y)$ the root inside the unit disk. This is the \emph{same rational form} as
Model-$A$ (Theorem~\ref{thm:A:PGF}); the two differ only in the kernel, where $\mu$ has been
replaced by $\mu+\gamma_1 y$.
\end{theorem}

\begin{corollary}\label{cor:B21:pi0}
Under~\eqref{eq:B21:stability}, the empty-state probabilities of Model-$\BH$ coincide with
those of Model-$A$,
\begin{equation*}
    \pi_0 = 1-\rho, \qquad \pi(0,0) = \rho(1-\rho).
\end{equation*}
In particular $P(1,1)=1-\pi_0=\rho$ and the diagonal generating function satisfies
$P(z,z)=\pi(0,0)/(1-\rho z)$.
\end{corollary}

\begin{proof}[Proof of Corollary~\ref{cor:B21:pi0}]
Set $x=y=z$ in the fundamental equation~\eqref{eq:B21:fundamental}. The jockeying factor
$\gamma_1 y(x-y)$ vanishes on the diagonal --- a direct consequence of the fact that
jockeying conserves the total number of customers --- and so does the term
$\mu(x-y)P_y(y)$, leaving
\begin{equation*}
    \bigl[(\lambda_1+\lambda_2+\mu)z^2 - \mu z - (\lambda_1+\lambda_2)z^3\bigr]P(z,z)
    = -\mu z(1-z)\,\pi(0,0).
\end{equation*}
Dividing by $z$ and factoring the bracket as $-(\lambda z-\mu)(z-1)$, with
$\lambda=\lambda_1+\lambda_2$,
\begin{equation*}
    (\lambda z-\mu)(1-z)\,P(z,z) = -\mu(1-z)\,\pi(0,0).
\end{equation*}
Cancelling $(1-z)\ne0$ for $z\in[0,1)$ gives the diagonal identity
\begin{equation}
    P(z,z) = \frac{\mu\,\pi(0,0)}{\mu-\lambda z} = \frac{\pi(0,0)}{1-\rho z}.
    \label{eq:B21:Pzz}
\end{equation}
Setting $z=1$ and using the normalisation $P(1,1)=1-\pi_0$ yields
$1-\pi_0=\pi(0,0)/(1-\rho)$. The idle balance~\eqref{eq:B21:idle} gives
$\lambda\pi_0=\mu\pi(0,0)$, i.e.\ $\pi(0,0)=\rho\pi_0$; substituting,
$(1-\pi_0)(1-\rho)=\rho\pi_0$, hence $\pi_0=1-\rho$ and $\pi(0,0)=\rho(1-\rho)$.
\end{proof}

\subsubsection{Analytical approach for Model-\texorpdfstring{$\BH$}{B2-H}}\label{sssec:B21:analytical}

\begin{proof}[Proof of Theorem~\ref{thm:B21:PGF}]
We apply the \emph{Kernel Method} to the fundamental equation~\eqref{eq:B21:fundamental}.
Fix $y\in(0,1]$ and seek the values of $x$ at which the coefficient of $P(x,y)$ --- the
\emph{kernel} --- vanishes. Since $P(x,y)$ is a PGF it is bounded on the closed unit disk,
so at any such root the right-hand side of~\eqref{eq:B21:fundamental} must vanish as well.
Dividing the kernel by $y\ne0$,
\begin{equation*}
    0 = (\lambda_1+\lambda_2+\mu)x - \mu - \lambda_1 x^2 - \lambda_2 xy + \gamma_1(x-y),
\end{equation*}
and rearranging into a quadratic in $x$ gives exactly~\eqref{eq:B21:quad},
\begin{equation*}
    \lambda_1 x^2 - \bigl[\lambda_1+\lambda_2(1-y)+\mu+\gamma_1\bigr]x + (\mu+\gamma_1 y) = 0,
\end{equation*}
whose two roots are
\begin{equation*}
    x^{\pm}(y) = \frac{A(y) \pm \sqrt{A(y)^2 - 4\lambda_1(\mu+\gamma_1 y)}}{2\lambda_1},
    \qquad A(y):=\lambda_1+\lambda_2(1-y)+\mu+\gamma_1.
\end{equation*}
This is precisely the Model-$A$ kernel quadratic~\eqref{eq:A:xstar} with $\mu$ replaced by
$\mu+\gamma_1 y$. We label the root carrying the negative sign $x^*(y)$ and the other
$x^+(y)$. By Vieta's formulas the product of the roots is
$x^*(y)\,x^+(y)=(\mu+\gamma_1 y)/\lambda_1$.

To locate the roots relative to the unit disk we evaluate the kernel quadratic, written as
$f(x):=\lambda_1 x^2 - A(y)x + (\mu+\gamma_1 y)$, at $x=1$:
\begin{equation*}
    f(1) = \lambda_1 - \bigl[\lambda_1+\lambda_2(1-y)+\mu+\gamma_1\bigr] + (\mu+\gamma_1 y)
         = -(1-y)\,(\lambda_2+\gamma_1) < 0
    \qquad\text{for } y\in[0,1).
\end{equation*}
Since $f$ is an upward parabola ($\lambda_1>0$) with $f(1)<0$, the point $x=1$ lies strictly
between its two roots, so $x^*(y)<1<x^+(y)$ for all $y\in[0,1)$. Hence $x^*(y)$ is the unique
root inside the unit disk, and at $y=1$ one checks $f(1)=0$ with $x^*(1)=1$ and
$x^+(1)=(\mu+\gamma_1)/\lambda_1>1$ (the latter exceeding $1$ because
$\lambda_1<\mu<\mu+\gamma_1$ under stability). For later use, we record
$\tfrac{d}{dy}x^*(1)$. The cleanest route is implicit differentiation of
$f(x,y):=\lambda_1 x^2-A(y)x+(\mu+\gamma_1 y)=0$ at the point $(x,y)=(1,1)$, where
$f_y=\lambda_2 x+\gamma_1$ and $f_x=2\lambda_1 x-A(y)$ evaluate to
$f_y(1,1)=\lambda_2+\gamma_1$ and $f_x(1,1)=\lambda_1-\mu-\gamma_1$, so
$\tfrac{d}{dy}x^*(1)=-f_y/f_x$:
\begin{equation}
    \frac{d}{dy}x^*(1) = \frac{\lambda_2+\gamma_1}{\mu+\gamma_1-\lambda_1}.
    \label{eq:B21:xstar_deriv}
\end{equation}
Unlike Model-$A$'s~\eqref{eq:A:xstar_prime}, the numerator carries an extra $\gamma_1$:
the constant term $\mu+\gamma_1 y$ of the kernel~\eqref{eq:B21:quad} is itself
$y$-dependent here, whereas in Model-$A$ (and in Model-$\CH$ below) the constant term is
independent of $y$.

Setting $x=x^*(y)$ in~\eqref{eq:B21:fundamental} and equating the right-hand side to zero,
\begin{equation*}
    \bigl[\mu(x^*(y)-y) + \gamma_1 y(x^*(y)-y)\bigr]P_y(y) - \mu x^*(y)(1-y)\,\pi(0,0) = 0,
\end{equation*}
that is, $(x^*(y)-y)(\mu+\gamma_1 y)P_y(y) = \mu x^*(y)(1-y)\pi(0,0)$, whence the boundary
function is
\begin{equation}
    P_y(y) = \frac{\mu\,x^*(y)\,(1-y)\,\pi(0,0)}
                  {(\mu+\gamma_1 y)\,\bigl(x^*(y)-y\bigr)}.
    \label{eq:B21:Py}
\end{equation}
As a consistency check, set $y=0$ in~\eqref{eq:B21:Py}: the factor $\mu+\gamma_1 y$ becomes
$\mu$ and $1-y$ becomes $1$, so
$P_y(0)=\mu\,x^*(0)\,\pi(0,0)/\bigl(\mu\,x^*(0)\bigr)=\pi(0,0)$ (using $x^*(0)>0$, the
smaller of the two positive roots), recovering the boundary value $P_y(0)=\pi(0,0)$.

Finally, substitute~\eqref{eq:B21:Py} and $\pi(0,0)=\rho(1-\rho)$
(Corollary~\ref{cor:B21:pi0}) back into~\eqref{eq:B21:fundamental}. Writing the kernel as
$-\lambda_1 y\,(x-x^*(y))(x-x^+(y))$ and simplifying the right-hand side,
\begin{align*}
    \bigl[\mu(x-y)+\gamma_1 y(x-y)\bigr]P_y(y) - \mu x(1-y)\,\pi(0,0)
    &= \mu(1-y)\,\pi(0,0)\left[\frac{(x-y)\,x^*(y)}{x^*(y)-y}-x\right] \\
    &= \mu(1-y)\,\pi(0,0)\,\frac{y\,\bigl(x-x^*(y)\bigr)}{x^*(y)-y},
\end{align*}
where the bracket collapses because
$(x-y)x^*-x(x^*-y)=y(x-x^*)$. Dividing by the factored kernel, the common factor
$\bigl(x-x^*(y)\bigr)$ cancels and we obtain
\begin{equation*}
    P(x,y) = \frac{\mu(1-y)\,\pi(0,0)\,y\,(x-x^*(y))/(x^*(y)-y)}
                  {-\lambda_1 y\,(x-x^*(y))(x-x^+(y))}
           = \frac{\mu\,\rho(1-\rho)\,(1-y)}
                  {\lambda_1\,\bigl(x^*(y)-y\bigr)\,\bigl(x^+(y)-x\bigr)},
\end{equation*}
which is~\eqref{eq:B21:PGF} and concludes the proof.
\end{proof}

\subsubsection{Probabilistic approach for Model-\texorpdfstring{$\BH$}{B2-H}}\label{sssec:B21:probabilistic}

For Model-$A$, the boundary function $P_y(y)$ admits an independent derivation by the
\emph{Pollaczek--Khinchine} (PK) formula (\S\ref{sssec:A:probabilistic}): conditional on
$N_1=0$, class~$2$ experiences an $M/G/1$ queue whose service times are i.i.d.\ copies of a
class-$1$ busy period, and the PK formula then delivers $P_y(y)$. \emph{This route does not
transfer to Model-$\BH$.} Head-of-line jockeying injects class-$1$ customers into Queue~2
at the instants when $N_1\ge1$; the resulting arrival stream into Queue~2 is the
superposition of the exogenous Poisson stream $\lambda_2$ and a state-dependent jockeying
stream. This merged stream is \emph{neither} Poisson \emph{nor} independent of the system
state --- it is correlated with $N_1$. Since the PK formula requires PASTA, which in turn
demands both a Poisson arrival process \emph{and} the lack-of-anticipation property, and the
merged input violates both, class~$2$ does not see a renewal $M/G/1$ input and no PK
representation of $P_y(y)$ is available. The analytical derivation
of~\S\ref{sssec:B21:analytical} is consequently the only route, and we retain this
subsection solely to record why the probabilistic one is unavailable --- in the same spirit
as the discussion of Models~$B$ and~$B_2$.

\subsection{Limits and sanity checks}

As $\gamma_1\to0^+$ the kernel quadratic~\eqref{eq:B21:quad} reduces to Model-$A$'s
quadratic~\eqref{eq:A:xstar}, so $x^*(y)\to x_A^*(y)$, and formula~\eqref{eq:B21:PGF}
reduces to the factored form of Theorem~\ref{thm:A:PGF}; the empty-state probabilities
already equal those of Model-$A$ by Corollary~\ref{cor:B21:pi0}. Setting $x=y=1$
in~\eqref{eq:B21:PGF} through the diagonal identity~\eqref{eq:B21:Pzz} gives
$P(1,1)=\rho=1-\pi_0$, confirming normalisation, and the diagonal
$P(z,z)=\pi(0,0)/(1-\rho z)$ is exactly that of the combined $M/M/1(\lambda,\mu)$
queue --- as it must be, since jockeying conserves the total customer count.
Beyond this $\gamma_1\to0^+$ limit, $\BH$ itself occupies the $k=1$ rung of the
head-of-line ladder discussed in Section~\ref{sec:future_work}, which interpolates
towards the length-proportional Model-$B_2$ of Section~\ref{sec:model_b2} as
$k\to\infty$.

\subsection{Mean queue lengths and mean waiting times}

\subsubsection{Class-1 marginal PGF and mean queue length}

Setting $y=1$ in the fundamental equation~\eqref{eq:B21:fundamental}, the term
$\mu x(1-y)\pi(0,0)$ vanishes and the coefficient of $P(x,1)$ factors as
$-(x-1)\bigl(\lambda_1 x-(\mu+\gamma_1)\bigr)$, while the right-hand side becomes
$(x-1)(\mu+\gamma_1)P_y(1)$. Cancelling $(x-1)$ for $x\ne1$,
\begin{equation}
    P(x,1) \;=\; \frac{(\mu+\gamma_1)\,P_y(1)}{\mu+\gamma_1-\lambda_1 x}
            \;=\; \frac{P_y(1)}{1-\rho_B\,x},
    \qquad \rho_B := \frac{\lambda_1}{\mu+\gamma_1}.
    \label{eq:B21:Px1}
\end{equation}
This is a geometric class-$1$ marginal: the priority queue behaves as an $M/M/1$ queue whose
effective \emph{clearance rate} is $\mu+\gamma_1$, since a waiting class-$1$ customer at the
head of Queue~1 departs that queue either by entering service (rate $\mu$) or by jockeying
(rate $\gamma_1$). The constant $P_y(1)$ is pinned by the normalisation
$P(1,1)=1-\pi_0=\rho$, giving $P_y(1)=\rho(1-\rho_B)$, so that
$P(x,1)=\rho(1-\rho_B)/(1-\rho_B x)$. Differentiating by the quotient rule and evaluating at
$x=1$,
\begin{equation}
    \mathbb{E}[N_1] \;=\; \left.\frac{d}{dx}P(x,1)\right|_{x=1}
    \;=\; \frac{\rho(1-\rho_B)\,\rho_B}{(1-\rho_B)^2}
    \;=\; \frac{\rho\,\rho_B}{1-\rho_B}.
    \label{eq:B21:EN1}
\end{equation}
This is Model-$A$'s formula~\eqref{eq:A:EN1} with the priority load $\rho_1$ replaced by the
\emph{jockeying-reduced} load $\rho_B=\lambda_1/(\mu+\gamma_1)\le\rho_1$.

\subsubsection{Total queue length from the diagonal}

Because jockeying conserves the total number of customers, the combined process
$N_1+N_2$ (together with the in-service customer) is the queue-length process of an ordinary
$M/M/1(\lambda,\mu)$ queue, and the diagonal generating
function~\eqref{eq:B21:Pzz} is $P(z,z)=\rho(1-\rho)/(1-\rho z)$. Since
$\tfrac{d}{dz}P(z,z)\big|_{z=1}=\mathbb{E}[N_1]+\mathbb{E}[N_2]$, differentiating gives
\begin{equation}
    \mathbb{E}[N_1]+\mathbb{E}[N_2]
    \;=\; \left.\frac{d}{dz}\,\frac{\rho(1-\rho)}{1-\rho z}\right|_{z=1}
    \;=\; \frac{\rho^2(1-\rho)}{(1-\rho)^2}
    \;=\; \frac{\rho^2}{1-\rho},
    \label{eq:B21:EN}
\end{equation}
identical to the combined $M/M/1$ result of Model-$A$~\eqref{eq:A:EN2}.

\subsubsection{Class-2 mean queue length by subtraction}

Subtracting~\eqref{eq:B21:EN1} from~\eqref{eq:B21:EN},
\begin{equation}
    \begin{split}
        \mathbb{E}[N_2]
        &\;=\; \frac{\rho^2}{1-\rho} - \frac{\rho\,\rho_B}{1-\rho_B}
        \;=\; \frac{\rho\bigl[\rho(1-\rho_B)-\rho_B(1-\rho)\bigr]}{(1-\rho)(1-\rho_B)} \\[4pt]
        &\;=\; \frac{\rho\,(\rho-\rho_B)}{(1-\rho)(1-\rho_B)}.
    \end{split}
    \label{eq:B21:EN2}
\end{equation}
The excess load admits a transparent decomposition,
\begin{equation*}
    \rho-\rho_B
    = \frac{\lambda_1+\lambda_2}{\mu} - \frac{\lambda_1}{\mu+\gamma_1}
    = \frac{(\lambda_1+\lambda_2)(\mu+\gamma_1)-\lambda_1\mu}{\mu(\mu+\gamma_1)}
    = \frac{\lambda_2\mu+\lambda_1\gamma_1+\lambda_2\gamma_1}{\mu(\mu+\gamma_1)}
    = \rho_2 + \frac{\lambda_1\gamma_1}{\mu(\mu+\gamma_1)},
\end{equation*}
so $\rho-\rho_B$ exceeds the bare class-$2$ load $\rho_2$ precisely by the load that
jockeying transfers from Queue~1 into Queue~2. At $\gamma_1=0$ it collapses to $\rho_2$
and~\eqref{eq:B21:EN2} recovers Model-$A$'s
$\mathbb{E}[N_2]=\rho\rho_2/[(1-\rho_1)(1-\rho)]$.

\subsubsection{Mean waiting times via Little's Law}

We apply \textbf{Little's Law} to each queue separately, recalling that $N_i$ counts only
the customers \emph{waiting}, so $\mathbb{E}[N_i]=\Lambda_i\,\mathbb{E}[W_i]$ with
$\Lambda_i$ the long-run rate at which customers \emph{enter} Queue~$i$ and $\mathbb{E}[W_i]$
their mean residence time in that queue (from entry until they leave it, by service entry or
by jockeying).

Every class-$1$ customer enters Queue~1 exactly once, by exogenous arrival, so
$\Lambda_1=\lambda_1$ and
\begin{equation*}
    \mathbb{E}[W_1] \;=\; \frac{\mathbb{E}[N_1]}{\lambda_1}
    \;=\; \frac{\rho\,\rho_B}{\lambda_1(1-\rho_B)}
    \;=\; \frac{\rho}{\mu+\gamma_1-\lambda_1}.
\end{equation*}
Compared with Model-$A$'s $\mathbb{E}[W_1]=\rho/(\mu-\lambda_1)$~\eqref{eq:A:EW1}, the
denominator is enlarged by $\gamma_1$: head-of-line jockeying drains the priority queue
faster and shortens class-$1$ waits.

Queue~2 receives a \emph{mixed} input: the exogenous Poisson stream at rate $\lambda_2$
together with the jockeying stream. The latter fires at rate $\gamma_1$ whenever $N_1\ge1$,
so its long-run rate is $\gamma_1\,\mathbb{P}(N_1\ge1)$. The probability that a class-$1$
customer is waiting follows from the geometric marginal~\eqref{eq:B21:Px1} by subtracting
the $N_1=0$ mass from the busy mass,
\begin{equation*}
    \mathbb{P}(N_1\ge1) = P(1,1)-P(0,1) = \rho - \rho(1-\rho_B) = \rho\rho_B,
\end{equation*}
since $P(1,1)=1-\pi_0=\rho$ and $P(0,1)=P_y(1)=\rho(1-\rho_B)$. The total entrance rate into
Queue~2 is therefore $\Lambda_2=\lambda_2+\gamma_1\rho\rho_B$, and Little's Law gives the
mean residence time per Queue-2 entrant,
\begin{equation}
    \mathbb{E}[W_2] \;=\; \frac{\mathbb{E}[N_2]}{\Lambda_2}
    \;=\; \frac{\rho\,(\rho-\rho_B)}
               {(1-\rho)(1-\rho_B)\,\bigl(\lambda_2+\gamma_1\rho\rho_B\bigr)}.
    \label{eq:B21:EW2}
\end{equation}
As $\gamma_1\to0^+$ the jockeying stream disappears, $\Lambda_2\to\lambda_2$ and
$\rho_B\to\rho_1$, and~\eqref{eq:B21:EW2} recovers Model-$A$'s
$\mathbb{E}[W_2]=\rho/[\mu(1-\rho_1)(1-\rho)]$~\eqref{eq:A:EW2}.
```

---

## Source text: Section 11 — Model-$\CH$

```latex
\section{Analysis of Model-\texorpdfstring{$\CH$}{C2-H} (\texorpdfstring{$\theta_1>0$}{theta1>0} head-of-line, \texorpdfstring{$\gamma_1=\gamma_2=\theta_2=0$}{gamma1=gamma2=theta2=0})}
\label{sec:model_c21}

Model-$\CH$ is the abandonment counterpart of Model-$\BH$, and a simplified variant of
the class-$1$ abandonment model Model-$C_2$. In Model-$C_2$ \emph{every} waiting class-$1$
customer is impatient and reneges at the linear rate $\theta_1 n_1$, turning the class-$1$
subsystem into an $M/M/1{+}M$ (Erlang-A) queue and the fundamental equation into a
first-order ODE. Here only the \emph{customer at the head of Queue~1} may abandon, at the
fixed rate $\theta_1$ whenever $n_1\ge1$; the aggregate abandonment rate is
$\theta_1\,\mathbf{1}_{\{n_1\ge1\}}$ rather than $\theta_1 n_1$. As with Model-$\BH$, the
flat rate contributes an \emph{algebraic} term to the fundamental equation rather than a
derivative, and the Kernel Method applies directly. Unlike jockeying, abandonment is a
\emph{true departure}: it removes a customer from the system and so breaks the conservation
of the total customer count that Model-$\BH$ enjoyed. The empty-state probabilities and
the class-$2$ mean queue length consequently require a separate argument.

\textbf{Stability.} Because only the head of Queue~1 abandons, the aggregate abandonment
rate is bounded by $\theta_1$ regardless of queue length, so --- in contrast to the Erlang-A
class-$1$ subsystem of Model-$C_2$, which is positive recurrent for all loads --- a genuine
stability condition is required. As shown in Corollary~\ref{cor:C21:pi0} below, the chain is
positive recurrent if and only if $\pi_0>0$, that is
\begin{equation}
    (\mu+\theta_1)(\mu-\lambda) + \lambda_1\theta_1 \;>\; 0,
    \qquad \lambda=\lambda_1+\lambda_2.
    \label{eq:C21:stability}
\end{equation}
This is \emph{weaker} than $\rho<1$: if $\rho<1$ then $\mu-\lambda>0$ and the condition holds
trivially, but it can also hold with $\rho\ge1$ provided $\theta_1$ is large enough --- head
abandonment accelerates the clearance of the priority queue and can stabilise the system at
offered loads exceeding the service capacity. Moreover~\eqref{eq:C21:stability} implies
$\rho_C:=\lambda_1/(\mu+\theta_1)<1$, so the priority subqueue is itself stable whenever the
condition holds.

\subsection{Balance equations}

The abandonment transition $(n_1,n_2)\to(n_1-1,n_2)$ occurs at the fixed rate $\theta_1$
whenever $n_1\ge1$. Since both a service completion and a head abandonment from
$(n_1+1,n_2)$ land in $(n_1,n_2)$, the two mechanisms combine into the coefficient
$\mu+\theta_1$ on the in-flows. On $S$,
\begin{align}
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu+\theta_1\right]\pi(n_1,n_2) \\
        &\quad=\quad (\mu+\theta_1)\pi(n_1+1,n_2)
          +\lambda_1\pi(n_1-1,n_2)
          +\lambda_2\pi(n_1,n_2-1)
    \end{split}
    &&n_1\ge1,\;n_2\ge1, \label{eq:C21:interior} \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu+\theta_1\right]\pi(n_1,0)
          \;=\; (\mu+\theta_1)\pi(n_1+1,0)
          +\lambda_1\pi(n_1-1,0)
    \end{split}
    &&n_1\ge1,\;n_2=0, \nonumber \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu\right]\pi(0,n_2) \\
        &\quad=\quad (\mu+\theta_1)\pi(1,n_2)
          +\lambda_2\pi(0,n_2-1)
          +\mu\,\pi(0,n_2+1)
    \end{split}
    &&n_1=0,\;n_2\ge1, \nonumber \\
    \begin{split}
        &\left[\lambda_1+\lambda_2+\mu\right]\pi(0,0)
          = (\lambda_1+\lambda_2)\pi_0
          + (\mu+\theta_1)\pi(1,0)
          + \mu\,\pi(0,1),
    \end{split} &&\nonumber \\
    \begin{split}
        &(\lambda_1+\lambda_2)\pi_0 = \mu\,\pi(0,0).
    \end{split} &&\label{eq:C21:idle}
\end{align}
The contrast with Model-$C_2$ is the same as before: there the in-flow coefficients
$\mu+\theta_1(n_1+1)$ and the out-flow coefficient $\theta_1 n_1$ grow with the queue
length, whereas here they are the constants $\mu+\theta_1$ and $\theta_1$ throughout.

\subsection{Fundamental PGF equation}

\begin{lemma}[Fundamental equation for Model-$\CH$]\label{lem:C21:fundamental}
Assume positive recurrence. Then the joint PGF $P(x,y)$ and the boundary function
$P_y(y)=P(0,y)$ satisfy
\begin{equation}
    \begin{split}
        &\left[(\lambda_1+\lambda_2+\mu)xy - \mu y - \lambda_1 x^2y - \lambda_2 xy^2
               + \theta_1 y(x-1)\right]P(x,y) \\
        &\quad=\quad \left[\mu(x-y) + \theta_1 y(x-1)\right]P_y(y)
               - \mu x(1-y)\,\pi(0,0).
    \end{split}
    \label{eq:C21:fundamental}
\end{equation}
\end{lemma}

\begin{proof}
As in Lemma~\ref{lem:B21:fundamental}, the non-abandonment terms
of~\eqref{eq:C21:interior}--\eqref{eq:C21:idle} reproduce the Model-$A$ fundamental
equation~\eqref{eq:A:fundamental} after multiplication by $x^{n_1}y^{n_2}$, summation, and
multiplication by $xy$. The abandonment \emph{out}-flow appears in every state with
$n_1\ge1$,
\begin{equation*}
    \theta_1\sum_{n_1\ge1}\sum_{n_2\ge0}\pi(n_1,n_2)\,x^{n_1}y^{n_2}
    = \theta_1\bigl[P(x,y)-P_y(y)\bigr],
\end{equation*}
and its \emph{in}-flow enters every state $(n_1,n_2)$ from $(n_1+1,n_2)$,
\begin{equation*}
    \theta_1\sum_{n_1\ge0}\sum_{n_2\ge0}\pi(n_1+1,n_2)\,x^{n_1}y^{n_2}
    = \theta_1\,x^{-1}\sum_{m_1\ge1}\sum_{n_2\ge0}\pi(m_1,n_2)\,x^{m_1}y^{n_2}
    = \theta_1\,x^{-1}\bigl[P(x,y)-P_y(y)\bigr],
\end{equation*}
with $m_1=n_1+1$. The net contribution is
$\theta_1\bigl(1-x^{-1}\bigr)\bigl[P(x,y)-P_y(y)\bigr]$; multiplying by $xy$ gives
$\theta_1 y(x-1)\bigl[P(x,y)-P_y(y)\bigr]$. Adding to the Model-$A$ equation and
rearranging yields~\eqref{eq:C21:fundamental}.
\end{proof}

\noindent\textit{Remark.}
Again no derivative of $P$ appears: the algebraic factor $\theta_1 y(x-1)$ replaces the
convective term $\theta_1 xy(x-1)\,\partial P/\partial x$ of Model-$C_2$. Setting
$\theta_1=0$ recovers~\eqref{eq:A:fundamental}. Unlike the jockeying factor of
Model-$\BH$, the abandonment factor $\theta_1 y(x-1)$ does \emph{not} vanish on the
diagonal $x=y$, which is the analytic signature of the broken conservation.
This algebraic collapse---no derivative term, and hence no singularity to resolve---is the
head-of-line regime anticipated in Remark~\ref{rem:gen:reading}.

\subsection{Closed-form solution}

\begin{theorem}[Closed-form PGF for Model-$\CH$]\label{thm:C21:PGF}
Consider the two-class non-preemptive priority queue with Poisson arrival rates
$\lambda_1,\lambda_2$, common exponential service rate $\mu$, and head-of-line class-$1$
abandonment at rate $\theta_1>0$ (with $\gamma_1=\gamma_2=\theta_2=0$). Under the stability
condition~\eqref{eq:C21:stability}, the joint PGF $P(x,y)=\mathbb{E}[x^{N_1}y^{N_2}]$ is the
rational function
\begin{equation}
    P(x,y) \;=\;
    \frac{\mu(\mu+\theta_1)\,(1-y)\,\pi(0,0)}
    {\lambda_1\,\bigl(x^+(y)-x\bigr)
     \,\bigl[(\mu+\theta_1 y)\,x^*(y)-y(\mu+\theta_1)\bigr]},
    \label{eq:C21:PGF}
\end{equation}
where $x^*(y)$ and $x^+(y)$ are the two roots of the kernel quadratic
\begin{equation}
    \lambda_1 x^2 - \bigl[\lambda_1+\lambda_2(1-y)+\mu+\theta_1\bigr]x + (\mu+\theta_1) = 0,
    \label{eq:C21:quad}
\end{equation}
with $x^*(y)$ the root inside the unit disk, and $\pi(0,0)$ is given by
Corollary~\ref{cor:C21:pi0}. As $\theta_1\to0^+$ the formula recovers Model-$A$
(Theorem~\ref{thm:A:PGF}) exactly.
\end{theorem}

\begin{corollary}\label{cor:C21:pi0}
Under~\eqref{eq:C21:stability}, the empty-state probabilities of Model-$\CH$ are
\begin{equation}
    \pi_0 = \frac{(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1}
                 {\mu(\mu+\theta_1)+\lambda_1\theta_1},
    \qquad
    \pi(0,0) = \frac{\lambda\bigl[(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\bigr]}
                    {\mu\bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]},
    \label{eq:C21:pi0_pi00}
\end{equation}
with $\lambda=\lambda_1+\lambda_2$. At $\theta_1\to0^+$ these reduce to $\pi_0\to1-\rho$ and
$\pi(0,0)\to\rho(1-\rho)$, recovering Model-$A$.
\end{corollary}

\begin{proof}[Proof of Corollary~\ref{cor:C21:pi0}]
Two evaluations of the fundamental equation~\eqref{eq:C21:fundamental} suffice. First set
$y=1$: the term $\mu x(1-y)\pi(0,0)$ vanishes, the coefficient of $P(x,1)$ factors as
$-(x-1)\bigl(\lambda_1 x-(\mu+\theta_1)\bigr)$, and the right-hand side becomes
$(x-1)(\mu+\theta_1)P_y(1)$. Cancelling $(x-1)$,
\begin{equation}
    P(x,1) \;=\; \frac{(\mu+\theta_1)\,P_y(1)}{\mu+\theta_1-\lambda_1 x}
            \;=\; \frac{P_y(1)}{1-\rho_C\,x},
    \qquad \rho_C := \frac{\lambda_1}{\mu+\theta_1}.
    \label{eq:C21:Px1}
\end{equation}
This geometric marginal shows that the priority queue clears at the effective rate
$\mu+\theta_1$ (service completions plus head abandonments). Evaluating at $x=1$ and using
$P(1,1)=1-\pi_0$ gives
\begin{equation}
    1-\pi_0 \;=\; \frac{P_y(1)}{1-\rho_C}
    \quad\Longrightarrow\quad
    P_y(1) \;=\; (1-\pi_0)(1-\rho_C).
    \label{eq:C21:P11}
\end{equation}
Second, set $x=1$ in~\eqref{eq:C21:fundamental}. The coefficient of $P(1,y)$ collapses to
$\lambda_2 y(1-y)$ and the right-hand side to $\mu(1-y)\bigl[P_y(y)-\pi(0,0)\bigr]$,
yielding the class-$2$ marginal relation
\begin{equation}
    \lambda_2\,y\,P(1,y) \;=\; \mu\bigl[P_y(y)-\pi(0,0)\bigr].
    \label{eq:C21:P1y}
\end{equation}
Letting $y\to1$ and using~\eqref{eq:C21:P11} and the idle
balance~\eqref{eq:C21:idle}, $\pi(0,0)=\lambda\pi_0/\mu$,
\begin{equation*}
    \lambda_2(1-\pi_0) \;=\; \mu\bigl[P_y(1)-\pi(0,0)\bigr]
    \;=\; \mu(1-\pi_0)(1-\rho_C) - \lambda\pi_0.
\end{equation*}
This is a linear equation in $\pi_0$. Expanding and collecting the $\pi_0$ terms on the
left,
\begin{equation*}
    \bigl[\mu(1-\rho_C)+\lambda-\lambda_2\bigr]\pi_0 = \mu(1-\rho_C)-\lambda_2,
    \qquad\text{i.e.}\qquad
    \pi_0 = \frac{\mu(1-\rho_C)-\lambda_2}{\mu(1-\rho_C)+\lambda_1},
\end{equation*}
where we used $\lambda-\lambda_2=\lambda_1$. Substituting
$\mu(1-\rho_C)=\mu(\mu+\theta_1-\lambda_1)/(\mu+\theta_1)$ and multiplying numerator and
denominator by $\mu+\theta_1$, the numerator becomes
$\mu(\mu+\theta_1-\lambda_1)-\lambda_2(\mu+\theta_1)=(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1$
and the denominator $\mu(\mu+\theta_1-\lambda_1)+\lambda_1(\mu+\theta_1)=\mu(\mu+\theta_1)+\lambda_1\theta_1$,
yielding the first identity in~\eqref{eq:C21:pi0_pi00}; the second follows from
$\pi(0,0)=\lambda\pi_0/\mu$.
The denominator $\mu(\mu+\theta_1)+\lambda_1\theta_1$ is strictly positive, so $\pi_0>0$ is
equivalent to the stability condition~\eqref{eq:C21:stability}.
\end{proof}

\subsubsection{Analytical approach for Model-\texorpdfstring{$\CH$}{C2-H}}\label{sssec:C21:analytical}

\begin{proof}[Proof of Theorem~\ref{thm:C21:PGF}]
We again apply the Kernel Method to~\eqref{eq:C21:fundamental}. Dividing the coefficient of
$P(x,y)$ by $y\ne0$ and rearranging gives the kernel quadratic~\eqref{eq:C21:quad},
\begin{equation*}
    \lambda_1 x^2 - \bigl[\lambda_1+\lambda_2(1-y)+\mu+\theta_1\bigr]x + (\mu+\theta_1) = 0,
\end{equation*}
which is the Model-$A$ kernel quadratic with $\mu$ replaced by $\mu+\theta_1$ \emph{both} in
the linear coefficient and in the constant term. Its roots are
\begin{equation}
    x^{\pm}(y) = \frac{A(y) \pm \sqrt{A(y)^2 - 4\lambda_1(\mu+\theta_1)}}{2\lambda_1},
    \qquad A(y):=\lambda_1+\lambda_2(1-y)+\mu+\theta_1,
    \label{eq:C21:xstar}
\end{equation}
with product $x^*(y)\,x^+(y)=(\mu+\theta_1)/\lambda_1$ by Vieta's formulas. Evaluating the
quadratic $f(x):=\lambda_1 x^2-A(y)x+(\mu+\theta_1)$ at $x=1$,
\begin{equation*}
    f(1) = \lambda_1 - A(y) + (\mu+\theta_1) = -\lambda_2(1-y) < 0
    \qquad\text{for } y\in[0,1),
\end{equation*}
so $x=1$ lies between the two roots and $x^*(y)<1<x^+(y)$ for $y\in[0,1)$; at $y=1$,
$x^*(1)=1$ and $x^+(1)=(\mu+\theta_1)/\lambda_1>1$ (the latter by $\rho_C<1$). Hence $x^*(y)$
is the unique root inside the unit disk. Differentiating~\eqref{eq:C21:xstar} at $y=1$,
\begin{equation}
    \frac{d}{dy}x^*(1) = \frac{\lambda_2}{\mu+\theta_1-\lambda_1},
    \label{eq:C21:xstar_deriv}
\end{equation}
the analogue of~\eqref{eq:A:xstar_prime} and~\eqref{eq:B21:xstar_deriv}.

Setting $x=x^*(y)$ in~\eqref{eq:C21:fundamental} forces the right-hand side to vanish,
\begin{equation*}
    \bigl[\mu(x^*(y)-y)+\theta_1 y(x^*(y)-1)\bigr]P_y(y) = \mu x^*(y)(1-y)\,\pi(0,0),
\end{equation*}
and, regrouping the bracket as
$\mu(x^*-y)+\theta_1 y(x^*-1)=(\mu+\theta_1 y)x^*-y(\mu+\theta_1)$, the boundary function is
\begin{equation}
    P_y(y) = \frac{\mu\,x^*(y)\,(1-y)\,\pi(0,0)}
                  {(\mu+\theta_1 y)\,x^*(y)-y(\mu+\theta_1)}.
    \label{eq:C21:Py}
\end{equation}
At $y=0$ the denominator is $\Delta(0)=\mu\,x^*(0)$, so
$P_y(0)=\mu x^*(0)\pi(0,0)/(\mu\,x^*(0))=\pi(0,0)$ (using $x^*(0)>0$, the smaller positive
root), as required.

Substituting~\eqref{eq:C21:Py} into~\eqref{eq:C21:fundamental}, writing the kernel as
$-\lambda_1 y\,(x-x^*(y))(x-x^+(y))$, and abbreviating the denominator
of~\eqref{eq:C21:Py} by $\Delta(y):=(\mu+\theta_1 y)x^*(y)-y(\mu+\theta_1)$, the right-hand
side becomes
\begin{align*}
    \bigl[\mu(x-y)+\theta_1 y(x-1)\bigr]P_y(y) \\
    {}-\mu x(1-y)\pi(0,0)
    &= \frac{\mu(1-y)\pi(0,0)}{\Delta(y)}
       \Bigl\{\bigl[\mu(x-y)+\theta_1 y(x-1)\bigr]x^*(y) - x\,\Delta(y)\Bigr\} \\
    &= \frac{\mu(1-y)\pi(0,0)}{\Delta(y)}\,(\mu+\theta_1)\,y\,\bigl(x-x^*(y)\bigr),
\end{align*}
where, after substituting $\Delta(y)=(\mu+\theta_1 y)x^*(y)-y(\mu+\theta_1)$, the curly
bracket is \emph{linear} in $x^*(y)$ and collapses term-by-term to
$(\mu+\theta_1)y\bigl(x-x^*(y)\bigr)$ (no use of the kernel relation is required). Dividing by
the factored kernel, the factor
$\bigl(x-x^*(y)\bigr)$ cancels and
\begin{equation*}
    P(x,y) = \frac{\mu(\mu+\theta_1)(1-y)\,\pi(0,0)\,y\,(x-x^*(y))/\Delta(y)}
                  {-\lambda_1 y\,(x-x^*(y))(x-x^+(y))}
           = \frac{\mu(\mu+\theta_1)(1-y)\,\pi(0,0)}
                  {\lambda_1\,(x^+(y)-x)\,\Delta(y)},
\end{equation*}
which is~\eqref{eq:C21:PGF} and concludes the proof.
\end{proof}

\subsubsection{Probabilistic approach for Model-\texorpdfstring{$\CH$}{C2-H}}\label{sssec:C21:probabilistic}

As for Model-$\BH$, the Pollaczek--Khinchine route used for Models~$A$ and~$C_2$ does not
transfer. In Model-$C_2$ the class-$1$ subsystem seen by class~$2$ is a clean $M/M/1{+}M$
(Erlang-A) queue whose busy period $B_C$ is an i.i.d.\ renewal quantity, and class~$2$ sees
an $M/G/1$ queue with service $B_C$. Under head-only abandonment this clean renewal
structure is lost: abandonment acts at the fixed rate $\theta_1$ only while a class-$1$
customer waits ($N_1\ge1$) but is inactive when the single class-$1$ present is in service,
so the departure rate of the class-$1$ subsystem is state-dependent at its boundary and the
class-$1$ busy period is not the busy period of any single $M/M/1$ or $M/M/1{+}M$ queue.
Consequently class~$2$ does not see a renewal $M/G/1$ input and no Pollaczek--Khinchine
representation of $P_y(y)$ is available. We retain this subsection, in parallel with the
other models, only to record why the analytical route of~\S\ref{sssec:C21:analytical} is the
operative one.

\subsection{Limits and sanity checks}

As $\theta_1\to0^+$ the kernel quadratic~\eqref{eq:C21:quad} reduces to Model-$A$'s, so
$x^*(y)\to x_A^*(y)$ and $\Delta(y)\to \mu(x_A^*(y)-y)$; together with
$\pi(0,0)\to\rho(1-\rho)$ from Corollary~\ref{cor:C21:pi0}, formula~\eqref{eq:C21:PGF}
reduces to the factored Model-$A$ PGF of Theorem~\ref{thm:A:PGF}. Setting $x=1$
in~\eqref{eq:C21:PGF} and $y\to1$ reproduces $P(1,1)=1-\pi_0$ via~\eqref{eq:C21:P11},
confirming normalisation.

\subsection{Mean queue lengths and mean waiting times}

\subsubsection{Class-1 marginal PGF and mean queue length}

The class-$1$ marginal is the geometric law~\eqref{eq:C21:Px1}; pinning the constant by
$P(1,1)=1-\pi_0$ as in~\eqref{eq:C21:P11} gives $P(x,1)=(1-\pi_0)(1-\rho_C)/(1-\rho_C x)$.
Differentiating and evaluating at $x=1$,
\begin{equation}
    \mathbb{E}[N_1] \;=\; \left.\frac{d}{dx}P(x,1)\right|_{x=1}
    \;=\; \frac{(1-\pi_0)\,\rho_C}{1-\rho_C},
    \qquad \rho_C=\frac{\lambda_1}{\mu+\theta_1},
    \label{eq:C21:EN1}
\end{equation}
with $1-\pi_0=\lambda(\mu+\theta_1)/\bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]$ from
Corollary~\ref{cor:C21:pi0}. As in Model-$\BH$, the priority queue behaves as an $M/M/1$
queue with effective clearance rate $\mu+\theta_1$, the only difference from
Model-$\BH$'s~\eqref{eq:B21:EN1} being the prefactor $1-\pi_0$, which here is no longer
equal to $\rho$ because abandonment alters the idle probability.

\subsubsection{Class-2 mean queue length}

Abandonment is a true departure and so breaks the \emph{conservation of the total customer
count} that underlies the diagonal argument: in Model-$\BH$ the jockeying factor
$\gamma_1 y(x-y)$ vanishes on the diagonal $x=y$, whereas here the abandonment factor
$\theta_1 y(x-1)$ does not. Concretely, setting $x=y=z$ in~\eqref{eq:C21:fundamental} leaves
the term $\theta_1 z(z-1)P_y(z)$ on the right-hand side, so the diagonal equation no longer
closes and the route that furnished $\mathbb{E}[N_1]+\mathbb{E}[N_2]$ for Model-$\BH$ is
unavailable. We instead differentiate the class-$2$ marginal. From the
marginal relation~\eqref{eq:C21:P1y}, $P(1,y)=\mu\bigl[P_y(y)-\pi(0,0)\bigr]/(\lambda_2 y)$,
and since $\mathbb{E}[N_2]=\tfrac{d}{dy}P(1,y)\big|_{y=1}$,
\begin{equation}
    \mathbb{E}[N_2]
    \;=\; \frac{\mu}{\lambda_2}\,P_y'(1) - (1-\pi_0),
    \label{eq:C21:EN2_implicit}
\end{equation}
where we used $\tfrac{\mu}{\lambda_2}\bigl[P_y(1)-\pi(0,0)\bigr]=P(1,1)=1-\pi_0$. It remains
to compute $P_y'(1)$ from~\eqref{eq:C21:Py}. Both the numerator $\mu x^*(y)(1-y)\pi(0,0)$ and
the denominator $\Delta(y)=(\mu+\theta_1 y)x^*(y)-y(\mu+\theta_1)$ vanish at $y=1$ (since
$x^*(1)=1$ gives $\Delta(1)=(\mu+\theta_1)-(\mu+\theta_1)=0$), so $P_y(y)$ is a $0/0$ form
there. Writing $N(y)$ and $\Delta(y)$ for numerator and denominator, a second-order Taylor
expansion about $y=1$ gives the value and the slope
\begin{equation*}
    P_y(1) = \frac{N'(1)}{\Delta'(1)} = (1-\pi_0)(1-\rho_C),
    \qquad
    P_y'(1) = \frac{N''(1)\,\Delta'(1) - N'(1)\,\Delta''(1)}{2\,\Delta'(1)^2},
\end{equation*}
which is why both the first and the second root sensitivities of $x^*$ at $y=1$ are needed,
namely~\eqref{eq:C21:xstar_deriv} together with
\begin{equation*}
    \frac{d^2}{dy^2}x^*(1) = \frac{2(\mu+\theta_1)\,\lambda_2^2}{(\mu+\theta_1-\lambda_1)^3}
\end{equation*}
(the latter obtained by differentiating $x^*(y)$ in~\eqref{eq:C21:xstar} twice).
Substituting these into $P_y'(1)$, then into~\eqref{eq:C21:EN2_implicit}, and simplifying
yields the closed form
\begin{equation}
    \mathbb{E}[N_2]
    \;=\; \frac{\lambda_2\,\lambda\,(\mu+\theta_1)\bigl[(\mu+\theta_1)^2-\lambda_1\theta_1\bigr]}
               {(\mu+\theta_1-\lambda_1)\,
                \bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]\,
                \bigl[(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\bigr]},
    \label{eq:C21:EN2}
\end{equation}
with $\lambda=\lambda_1+\lambda_2$. The last bracket in the denominator is exactly the
stability numerator of $\pi_0$ from~\eqref{eq:C21:pi0_pi00}, so $\mathbb{E}[N_2]$ is finite
precisely under the stability condition~\eqref{eq:C21:stability} and diverges as
$\pi_0\to0^+$. As $\theta_1\to0^+$ the right-hand side reduces to
$\lambda_2\lambda/[(\mu-\lambda_1)(\mu-\lambda)]=\rho\rho_2/[(1-\rho_1)(1-\rho)]$, recovering
Model-$A$'s~\eqref{eq:A:EN2}.

\subsubsection{Mean waiting times via Little's Law}

We apply \textbf{Little's Law} to each queue. Every class-$1$ customer enters Queue~1 once
by exogenous arrival and later leaves it either by entering service or by abandoning from the
head; in both cases it leaves Queue~1, so the entrance rate is $\Lambda_1=\lambda_1$ and
\begin{equation*}
    \mathbb{E}[W_1] \;=\; \frac{\mathbb{E}[N_1]}{\lambda_1}
    \;=\; \frac{(1-\pi_0)\,\rho_C}{\lambda_1(1-\rho_C)}.
\end{equation*}
Here $\mathbb{E}[W_1]$ is the mean time a class-$1$ customer spends \emph{waiting} in
Queue~1, averaged over all class-$1$ arrivals, whether they are eventually served or
abandon. Queue~2, by contrast, receives no jockeying input and its customers never abandon
($\theta_2=0$), so every class-$2$ arrival is eventually served and the entrance rate is
simply $\Lambda_2=\lambda_2$:
\begin{equation*}
    \mathbb{E}[W_2] \;=\; \frac{\mathbb{E}[N_2]}{\lambda_2}
    \;=\; \frac{\lambda\,(\mu+\theta_1)\bigl[(\mu+\theta_1)^2-\lambda_1\theta_1\bigr]}
               {(\mu+\theta_1-\lambda_1)\,
                \bigl[\mu(\mu+\theta_1)+\lambda_1\theta_1\bigr]\,
                \bigl[(\mu+\theta_1)(\mu-\lambda)+\lambda_1\theta_1\bigr]}.
\end{equation*}
Both reduce to the corresponding Model-$A$ expressions as $\theta_1\to0^+$.
```

---

## Your task

The author will rewrite both sections entirely in their own words. Your role is to do
the preparatory analytical work across the five dimensions below. **Address both sections
jointly** where patterns are shared (e.g. balance-equation structure, Lemma proofs,
Kernel Method steps), and individually only where they differ. Be concrete: quote the
specific passage, equation, or step; explain the issue; and provide the corrected or
expanded version in full LaTeX.

Do not perform these in the order listed; find the most efficient ordering that groups
related improvements.

---

### Dimension 1 — Refer to Preliminaries, don't re-derive

Identify every sub-argument that is already established in Preliminaries (§3) or in
earlier model sections and could be **replaced by a one-line cross-reference** without
loss of rigour. For each, write the proposed replacement sentence.

Specific targets to evaluate:

- **Corollary B21:pi0 proof**: the diagonal argument is almost verbatim from
  Corollary A:pi0. Since jockeying conserves total customers, setting $x=y=z$ in the
  fundamental equation kills the jockeying factor identically (as it must), leaving
  exactly the Model-A diagonal equation. Can this proof be shortened to a single
  sentence + cross-reference?
- **Root location ($x^*(y)<1<x^+(y)$)**: the $f(1)<0$ upward-parabola argument is used
  in both sections (and was established in Model-A). Evaluate whether it can be referred
  to rather than reproved. Note that the quadratic is slightly different in each case
  ($\mu\to\mu+\gamma_1 y$ in B^H, $\mu\to\mu+\theta_1$ in C^H), so check whether the
  *form* of argument is the same even if the specific quadratic differs.
- **Vieta's formula for $x^* x^+$**: appears in both proofs; very short, but can be
  stated once as "by Vieta's formulas" without re-deriving.
- **The boundary check $P_y(0)=\pi(0,0)$**: the consistency check at $y=0$ appears
  verbatim in both proofs. Can it be omitted or referred to the same check in Model-A?
- **PK unavailability paragraphs**: both probabilistic subsections explain why PK fails.
  The B^H paragraph is longer (mentions PASTA explicitly). Can either be shortened while
  retaining the rigorous explanation? The key distinction B^H vs. C^H should be kept.

---

### Dimension 2 — Simplify prose

For each passage, propose a shorter and cleaner rewrite. Targets:

- **Opening paragraphs** of each section: currently three dense sentences each. Identify
  redundancies with the other section (since both have the same "linear rate → ODE vs.
  flat rate → algebraic" logic) and propose a unified shorter opening that establishes
  the contrast in ≤3 sentences, then branches.
- **Two structural remarks after the B^H balance equations** (the paragraph beginning
  "Two structural remarks are in order..."): this can be compressed significantly since
  both remarks are essentially self-evident from the equations. Propose a ≤2 sentence
  replacement or show where to cut entirely.
- **$P_y(y)$ isolation step in both proofs**: the passage starting "Setting $x=x^*(y)$
  in the fundamental equation..." involves one algebraic step whose verbosity can be
  reduced. Propose a compact version.
- The prose in "Limits and sanity checks" for B^H ends with a forward-reference to a
  head-of-line ladder (§future_work). Evaluate whether this belongs here or in the
  conclusion.

---

### Dimension 3 — Compress multi-line equations to single lines

For each of the following, decide whether the displayed version should stay split or
can legitimately be on one line, and write the one-line version if appropriate:

- **Balance equations** (eq:B21:interior, eq:B21:xboundary, eq:B21:yboundary and the
  C^H analogues): which of the five balance equations are short enough to fit on one
  line while staying readable?
- **Kernel quadratic evaluation at $x=1$** in both proofs: the current display is a
  two-line split. Can this be one line?
- **$\mathbb{E}[N_2]$ for B^H** (eq:B21:EN2): the split-block adds a line break before
  the second equality that is not needed. Propose a single-line or single-`align` form.
- **Class-2 waiting time for C^H**: the formula for $\mathbb{E}[W_2]$ repeats the same
  three-factor denominator that already appears in $\mathbb{E}[N_2]$. Suggest whether
  to abbreviate using a named constant or just simplify $\mathbb{E}[W_2]=\mathbb{E}[N_2]/\lambda_2$.
- The `align*` block in the B^H proof that says "where the bracket collapses..." is
  only two lines. Can it be done in one displayed equation?

---

### Dimension 4 — Align notation with Model-B₂ to highlight parallelism

The parallel structure to exploit is:

- **B₂ ↔ B^H**: both are one-way jockeying; the only difference is `γ₁n₁` vs.
  `γ₁·1{n₁≥1}`. The same `ρ_B = λ₁/(μ+γ₁)` effective load symbol is used in B^H —
  verify this is explicitly introduced and its provenance from the analogy with B₂
  is noted.
- **C₂ ↔ C^H**: same mechanism, `θ₁n₁` vs. `θ₁·1{n₁≥1}`. The symbol `ρ_C` is shared —
  verify.
- **The coefficient `A(y)`** is defined identically (up to a parameter shift) in both
  sections' proofs, but inconsistently: in B^H it is `A(y)=λ₁+λ₂(1−y)+μ+γ₁`, in C^H
  it is `A(y)=λ₁+λ₂(1−y)+μ+θ₁`. These are the same formula with `γ₁↔θ₁`. Propose
  a naming that unifies them (e.g. use the same letter `A(y)` in both and note the
  substitution, or name them `A^B(y)` and `A^C(y)`).
- **The denominator `Δ(y)` in C^H** has no B^H counterpart (because in B^H the
  denominator `(μ+γ₁y)(x*(y)−y)` factors cleanly). Check whether introducing the
  notation `Δ(y)` for B^H (even if it factors) would help or hinder the parallel
  exposition.
- **Proof structure**: B₂ uses Step (i)/(ii)/(iii). B^H and C^H use neither. Since their
  Kernel Method proofs have three natural phases — (i) kernel quadratic + root location,
  (ii) setting `x=x*(y)` to pin `P_y(y)`, (iii) substituting back to get `P(x,y)` —
  propose whether to adopt Step labels for consistency with B₂.

---

### Dimension 5 — Expand non-trivial mathematical steps

For each of the following steps that are currently skipped or compressed, write out the
full step-by-step derivation in an `align` or `align*` environment, one step per line
with brief inline explanations. **Correctness first**: verify each algebra claim before
writing it up.

**5a. The bracket collapse in the B^H proof**

The current text says:
> "where the bracket collapses because $(x-y)x^* - x(x^*-y) = y(x-x^*)$"

Expand this into a four-step `align*` block: start from
$\mu[(x-y)/(x^*-y)]x^* - \mu x = \mu[\cdots]$, expand brackets, cancel, and land
on $\mu(1-y)\pi(0,0)\cdot y(x-x^*)/(x^*-y)$.

**5b. The bracket collapse in the C^H proof**

The text says the curly bracket "collapses term-by-term to $(\mu+\theta_1)y(x-x^*)$
(no use of the kernel relation is required)". Show the four-step computation:
$$[\mu(x-y)+\theta_1 y(x-1)]\,x^* - x\cdot\Delta(y) = \cdots = (\mu+\theta_1)y(x-x^*)$$
substituting $\Delta(y)=(\mu+\theta_1 y)x^*-y(\mu+\theta_1)$ and expanding.

**5c. The $P_y'(1)$ computation for Model-C^H** (the crucial missing derivation)

The $\mathbb{E}[N_2]$ formula is stated with no working beyond "substituting these into
$P_y'(1)$, then into eq:C21:EN2_implicit, and simplifying yields the closed form."

Carry out the full computation:

1. Compute $N(y)=\mu x^*(y)(1-y)\pi(0,0)$ at $y=1$. Both $N(1)=0$ and $\Delta(1)=0$,
   confirming a $0/0$ form.
2. Compute $N'(1)$ and $\Delta'(1)$ step by step (use $(x^*)'(1)$ from eq:C21:xstar_deriv).
   Verify that $N'(1)/\Delta'(1)$ reproduces $P_y(1)=(1-\pi_0)(1-\rho_C)$.
3. Compute $N''(1)$ and $\Delta''(1)$ step by step (use $(x^*)''(1)$ from the text).
4. Substitute into the Taylor formula $P_y'(1) = [N''\Delta' - N'\Delta'']/(2(\Delta')^2)$
   and simplify to a closed-form expression for $P_y'(1)$.
5. Substitute into $\mathbb{E}[N_2]=(\mu/\lambda_2)P_y'(1)-(1-\pi_0)$ and simplify to
   the claimed formula eq:C21:EN2. Check each cancellation.

**5d. The implicit differentiation for $(x^*)'(1)$ in B^H**

The current text derives eq:B21:xstar_deriv by implicit differentiation, mentioning
$f_y=\lambda_2 x+\gamma_1$. Show explicitly where the $\gamma_1$ in the numerator comes
from (it arises because the constant term of the B^H quadratic is $\mu+\gamma_1 y$, which
is $y$-dependent, unlike Model-A and unlike C^H where the constant term is $\mu+\theta_1$
independent of $y$). A one-paragraph comparison of the three kernels (A, B^H, C^H) would
make this structural difference very clear.

---

### Output format

For each dimension, use a headed section. Within each section:
- Quote the original passage (concisely — first and last line suffices for long blocks).
- State the issue or proposed change clearly.
- Give the full LaTeX replacement.

Where you find a **mathematical inaccuracy** anywhere in either section, flag it
prominently with **[INACCURACY]** before the explanation.

Preserve all `\label{...}` keys exactly as given. Use British spelling throughout.
