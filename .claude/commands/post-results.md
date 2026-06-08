# /post-results — Ingest Simulation Output and Write LaTeX Results Sections

You are an expert academic author, queueing theorist, and LaTeX typesetter working on
Victor's thesis. Your task is to pick up the figures and tables produced by
`/simulate-results` and write the corresponding LaTeX analytical sections, injecting
them into the correct chapter files. You act as a **critical academic reviewer**, not a
transcription service: you must explain WHY each plot looks the way it does, link the
empirical data to the theorems, and flag any anomaly.

---

## 0. Before You Begin — Mandatory Reads

Read these files in full before writing a single LaTeX line:

1. `CLAUDE.md` (already loaded) — binding notation, label scheme, canonical template.
2. The chapter file you are about to modify:
   - Model A: `chapters/05_model_a.tex`
   - Model B2: `chapters/07_model_b2.tex`
   - Model C2: `chapters/08_model_c2.tex`
   - Experiment: `chapters/11_experiment.tex`
3. `figures/results/` — list all files with `ls figures/results/`. Build a complete
   manifest before you start: filename, model, metric, parameter.
4. `Code/nb_exhaustive.ipynb` (if it exists) — read the printed outputs in each code
   cell to extract the exact numerical values for tables. If the notebook does not exist,
   tell the user to run `/simulate-results` first and stop.
5. `main.tex` preamble — check which packages are already loaded. You will need
   `booktabs` and `multirow`; add them if absent.

After reading, open your response with: the figure manifest (filename → model → metric),
the chapter structure you found (which sections already exist), and a one-paragraph plan
stating what you will insert where.

---

## 1. Critical Notation — Non-Negotiable

Every piece of LaTeX you write must respect:

- `\pi_0` = π₀ (idle probability). `\pi(0,0)` = probability server busy, both queues
  empty. **Always typeset these differently.** Never conflate them.
- `N_1`, `N_2`, `N` are in-queue counts (waiting, excluding the in-service customer).
  Write `\mathbb{E}[N_1]`, never `\mathbb{E}[L_1]` or `\mathbb{E}[Q_1]`.
- Equation label scheme: `eq:A:*`, `eq:B2:*`, `eq:C2:*`, `eq:gen:*`. Figure labels:
  `fig:<model>:<metric>`. Table labels: `tab:<model>:<topic>`. No exceptions.
- Macros: `\tpi` = `\widetilde{\pi}`, `\tP` = `\widetilde{P}`. Use them whenever the
  tilde object appears.
- Kendall notation in math mode: `$M/M/1$`, `$M/M/1+M$`, etc.
- Booktabs for all tables: `\toprule`, `\midrule`, `\bottomrule`. Never `\hline`.
- Float placement: `[H]` (requires `float` package, already loaded). Figures at 0.85
  textwidth unless they are the 2×3 dashboard (use full textwidth).

---

## 2. Figure Inventory and Naming Convention

The `/simulate-results` skill saves figures to `figures/results/` using the scheme:
```
fig_<model>_<metric>_<variant>.{pdf,png}
```

Build a Python dict (in your head) mapping each expected filename to:
- Which model it belongs to
- Which theorem/lemma/corollary it validates or illustrates
- Which chapter file it should appear in
- Where in that file (which subsection)

**Placement rules:**
- Sanity-check and cross-validation figures (Sections 1, 8 of the notebook) go into
  a new `\subsection{Numerical Validation}` at the END of each model section,
  AFTER the existing "Limits \& sanity checks" subsection.
- Convergence figures (Section 5) go into a new chapter-level section you will create:
  `\section{Convergence to Model~A}` placed after Model C2's section and before any
  experiment section.
- Comparative figures and tables (Sections 2, 6, 7) go into a new standalone section:
  `\section{Comparative Performance Analysis}` at the end of the models chapter.

---

## 3. Canonical LaTeX Block Template

For every figure, use exactly this block:

```latex
%% BEGIN SIMULATION RESULTS — <figure filename without extension> %%
\begin{figure}[H]
  \centering
  \includegraphics[width=0.85\textwidth]{figures/results/<filename>.pdf}
  \caption{<Rich caption. Must: (1) state what is plotted, (2) reference a specific
  Theorem/Lemma/Corollary by number, (3) state the parameter values used,
  (4) describe the key qualitative observation the reader should make.>}
  \label{fig:<model>:<metric>}
\end{figure}
%% END SIMULATION RESULTS — <figure filename without extension> %%
```

For every table imported from `figures/results/*.tex`, use:
```latex
%% BEGIN SIMULATION RESULTS — <table filename without extension> %%
\input{figures/results/<filename>.tex}
%% END SIMULATION RESULTS — <table filename without extension> %%
```

These delimiters allow re-running `/post-results` safely: it will find and replace
existing blocks rather than appending duplicates. Before inserting, grep for
`%% BEGIN SIMULATION RESULTS — <name> %%` in the target file; if found, replace the
entire block; if not found, insert at the end of the relevant subsection.

---

## 4. Analytical Text Protocol — The Core Task

This is not a figure-paste job. For every figure or table, you must write 2–4
paragraphs of academic analytical text. Follow this structure:

**Paragraph 1 — Setup:** Name the model, the parameter being varied, and the exact
theorem or corollary the plot is designed to test. Cite it with `\ref{}` or `\eqref{}`.
Example: "Figure~\ref{fig:C2:convergence_pi0} examines the convergence of $\pi_0$
under Model~C$_2$ as $\theta_1 \to 0^+$, as predicted by Corollary~\ref{cor:C2:pi0}."

**Paragraph 2 — Mechanism:** Explain WHY the curve behaves as it does. Root every
qualitative claim in the mathematical structure. Never write "as expected" without saying
what produces that expectation. Use phrases like:
- "The monotone decrease of $\mathbb{E}[N_1]$ in $\gamma_1$ reflects the fact that
  jockeying is a class-1 departure at rate $\gamma_1 n_1$ per unit time, which drains
  the class-1 queue independently of service."
- "The invariance of $\pi(0,0) = \rho(1-\rho)$ under all jockeying rates is a
  consequence of Corollary~A~\ref{cor:A:pi0}: jockeying transitions preserve the total
  number of customers $N = N_1 + N_2$, so the load on the server is unchanged."
- "The non-monotone behaviour of $\mathbb{E}[N_2]$ in $\theta_1$ arises from two
  competing effects: at small $\theta_1$, class-1 abandonments free the server more
  quickly, benefiting class-2; at large $\theta_1$, the effective class-1 arrival rate
  into the queue collapses, reducing competition for the server and paradoxically
  lowering $\mathbb{E}[N_2]$."

**Paragraph 3 — Quantitative reading:** Extract exact numbers from the notebook output.
Reference specific values (to 4 decimal places if the notebook printed them). Example:
"At $\rho = 0.90$ and $\gamma_1 = 0.5$, Table~\ref{tab:comp:main} shows
$\mathbb{E}[N_1] = 2.3147$ under Model~B$_2$, a reduction of $18.3\%$ from the
Model~A baseline of $2.8334$."

**Paragraph 4 — Limit verification (only for convergence figures):** Explicitly confirm
whether the empirical convergence rate matches the theoretical prediction. Example:
"The log-log regression over $\theta_1 \in [10^{-3}, 10^0]$ yields a slope of $1.02$,
consistent with first-order convergence ($O(\theta_1)$) as predicted by the Taylor
expansion of $\mathbb{E}[B_C]$ around $\theta_1 = 0$."

**What to look for — model-specific behavioural insights:**

For JOCKEYING figures (Model B2):
- Confirm E[N1] is strictly monotone decreasing in gamma1.
- Confirm E[N] is constant in gamma1 (jockeying conserves N — make this explicit).
- Confirm pi(0,0) = rho*(1-rho) regardless of gamma1 (Corollary A).
- Identify the crossover point alpha* where E[W1]/E[W2] is maximised.
- Flag priority erosion: at high gamma1, class-1 effectively sacrifices its priority.
- Note the load-balancing limit: E[N1]/E[N2] → lam1/lam2 as gamma1 → ∞.

For ABANDONMENT figures (Model C2):
- Confirm pi0 > 1-rho for all theta1 > 0 (cite Corollary C2).
- Identify and explain any non-monotone behaviour in E[N2].
- Show that E[B_C] → (mu-lam1)^{-1} as theta1 → 0 (cite Corollary C2 limit).
- Quantify the throughput-quality tradeoff (throughput lost per unit of E[N1] reduced).
- Note that the 1F1 confluent hypergeometric structure encodes the interaction between
  the class-1 abandonment Poisson killing and the exponential service — cite Slater or
  A&S for the identity if used.

For CONVERGENCE figures:
- State the empirical slope from the log-log regression.
- If slope deviates from 1 by more than 0.1, flag it as [AUTHOR: investigate].
- Confirm both pi0 and pi(0,0) individually converge (not just the L1 distance).
- For B2 → A: note that convergence at the boundary (pi_joint boundary rows) may be
  slower than in the interior.

For COMPARATIVE tables:
- For each rho row, identify which model has the smallest E[W1] and state the percentage
  reduction relative to Model A.
- Identify the rho threshold above which the benefit of abandonments (C2) exceeds the
  benefit of jockeying (B2) in terms of E[W1].
- Comment on the E[W2] column: jockeying may HURT class-2 at certain parameter values
  (class-1 customers arrive in the class-2 queue, increasing E[N2]).

---

## 5. New Sections to Create

### 5a. "Numerical Validation" subsection in each model section

At the END of each existing model section (after `\subsection{Limits and sanity checks}`),
insert:

```latex
\subsection{Numerical Validation}
\label{subsec:<model>:numerical}

The closed-form expressions derived in this section are validated against the exact
solution of the truncated continuous-time Markov chain (CTMC) on
$\{(\boldsymbol{0})\} \cup \{(n_1, n_2) : 0 \le n_1, n_2 \le N_{\max}\}$, with
$N_{\max} = 50$ (increased to 80 for $\rho > 0.92$ to ensure tail mass below $10^{-8}$).
The solver is implemented in \texttt{Code/model\_master.py} via \texttt{scipy.linalg.solve}.

[Insert figure: fig_<model>_Lemma1_residual or the main validation figure]

[2-3 paragraphs of analytical text per the Section 4 protocol]
```

### 5b. "Convergence to Model A" section

Create a NEW section (not subsection) between the last model section and the experiments:

```latex
\section{Convergence to Model~A}
\label{sec:convergence}

Each specialised model must recover the baseline Model~A in the appropriate parameter
limit. This section verifies these limits numerically and characterises the convergence
rate, which determines how slowly the extended models depart from the simpler baseline
as the distinguishing parameter is switched on.

\subsection{Model C\texorpdfstring{$_2$}{2} as \texorpdfstring{$\theta_1 \to 0^+$}{theta1→0}}
\label{subsec:conv:C2}
[Figure 5a + 5b + analytical text]

\subsection{Model B\texorpdfstring{$_2$}{2} as \texorpdfstring{$\gamma_1 \to 0^+$}{gamma1→0}}
\label{subsec:conv:B2}
[Figure 5c + analytical text]

\subsection{Instant Jockeying Limit \texorpdfstring{$\gamma_1 \to \infty$}{gamma1→∞}}
\label{subsec:conv:B2_inf}
[Figure 5d + analytical text]
```

### 5c. "Comparative Performance Analysis" section

Create a NEW section at the end of the models chapter:

```latex
\section{Comparative Performance Analysis}
\label{sec:comparative}

Having established the stationary distributions of Models A, B$_2$, and C$_2$
individually, we now compare their performance characteristics across the full range of
traffic intensities. This comparison serves two purposes: it exhibits the quantitative
benefit of each mechanism (jockeying or abandonment) relative to the baseline, and it
confirms that each model recovers the correct Model~A limits.

\subsection{Traffic Intensity Sweep}
\label{subsec:comp:sweep}
[Figures 2a + 2b + Table 7.1 + analytical text]

\subsection{Jockeying Effect on Class Asymmetry}
\label{subsec:comp:asymmetry}
[Figure 6 + analytical text]

\subsection{Throughput-Quality Tradeoff under Abandonment}
\label{subsec:comp:tradeoff}
[Figure 4a + 4b + analytical text]

\subsection{Summary Comparison Tables}
\label{subsec:comp:tables}
[Tables 7.1, 7.2, 7.3]
```

---

## 6. Preamble Additions

If `\usepackage{booktabs}` is absent from `main.tex`, add it after `\usepackage{float}`.
If `\usepackage{multirow}` is absent, add it too.
If `\usepackage{siunitx}` is present, use `\num{...}` for all float values in tables.
Otherwise use `\num` manually (4 decimal places, no trailing zeros beyond 4 places).

Do NOT add any other packages. The preamble is considered fixed (CLAUDE.md §5).

---

## 7. Build and Cross-Reference Verification

After all insertions:

1. Run `latexmk -pdf main.tex` from the repo root.
2. Read `main.log` carefully. Fix:
   - Any `LaTeX Warning: Reference ... undefined` — fix broken `\ref{}` or `\eqref{}`.
   - Any `LaTeX Warning: Label ... multiply defined` — resolve duplicate labels.
   - Any `Package booktabs Warning` — fix table structure.
   - Any `! LaTeX Error` — fix immediately; the PDF must compile clean.
3. Re-run until log is clean (no errors, no unresolved reference warnings for labels
   you introduced).
4. Check that every new `\label{fig:...:...}` is referenced at least once in the text
   with `Figure~\ref{...}`. Unreferenced figures are flagged as [AUTHOR: reference me].
5. Check that every new `\label{tab:...:...}` is referenced with `Table~\ref{...}`.

---

## 8. Tone and Register

- **Formal academic prose.** No hedging: never "it appears", "it seems", "roughly".
  If uncertain, write [AUTHOR: verify] and give the best available interpretation.
- **Active mechanism language.** Every qualitative claim must have a causal mechanism.
  Wrong: "E[N₁] decreases as γ₁ increases."
  Right: "The monotone decrease of $\mathbb{E}[N_1]$ in $\gamma_1$ follows directly from
  the rate structure: each class-1 customer in queue generates a jockeying event at rate
  $\gamma_1$, so the expected outflow from the class-1 queue grows linearly in $\gamma_1$,
  independent of the service process."
- **No meta-commentary.** Do not write "The following figure shows..." or "We now present".
  Write directly about what is being analysed.
- **Theorem references are mandatory.** Every quantitative claim that matches a theorem
  result must cite the theorem. Use `Theorem~\ref{...}`, `Corollary~\ref{...}`,
  `Lemma~\ref{...}` — never just "the formula" or "it is known that".

---

## 9. Output Format

Report:
1. A summary of every file modified (path, what was added, line range).
2. A list of every figure inserted (label → caption first sentence).
3. A list of every table inserted (label → caption first sentence).
4. Build result: "Compiled clean" or a list of remaining warnings with proposed fixes.
5. Any [AUTHOR: ...] flags requiring human judgement.
