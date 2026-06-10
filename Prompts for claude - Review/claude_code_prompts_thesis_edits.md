# Claude Code Prompt Playbook — Thesis Revision

**How to use:** Run one prompt per Claude Code session (or per conversation turn), in order within each phase. Phases A–C are independent of each other internally; tasks inside a phase touch disjoint files unless noted. Commit after every task with the suggested commit message so any task can be reverted in isolation.

**Global constraints to paste at the top of EVERY session:**

```
GLOBAL RULES (apply to every task):
- Never alter the mathematical content of any equation, theorem statement, or proof step unless the task explicitly says so. Prose insertions only, unless stated.
- After every edit, run the full LaTeX build (latexmk or the repo's build script) and confirm zero new errors/warnings about undefined references or labels.
- Do not renumber or relabel equations; never hardcode equation numbers — use \eqref/\ref with existing labels.
- Preserve the author's voice: formal, first-person-plural academic English. No bullet lists inside thesis prose.
- At the end, output: (1) list of files changed, (2) a unified diff summary, (3) build status.
```

---

## PHASE 0 — Recon and baseline (run first, once)

### P0.1 — Repo map and build baseline

```
Task: Establish a baseline before any edits.
1. Map the repository: list every .tex file and which thesis section it contains; locate the main file, the bibliography file, the figure-generation code (simulation scripts / notebook builder), and any results data files (CSV/JSON) consumed by the tex.
2. Run the full build. Save the compile log. Report: pass/fail, all warnings about undefined references, multiply-defined labels, and overfull boxes.
3. Grep the whole repo for: "AUTHOR:", "TODO", "FIXME", "XXX", "??". Report every hit with file and line number.
4. Write the map to docs/REPO_MAP.md (create docs/ if absent) so later sessions can read it instead of re-exploring.
Do not edit any thesis content in this task.
Commit: "chore: repo map + build baseline"
```

---

## PHASE A — Mechanical hygiene (safe, local, no interference)

### A1 — Typo and copy-edit sweep

```
Task: Fix typos and grammar ONLY. No restructuring, no rewording of correct sentences.
Known instances to fix (search and correct, there may be more nearby):
- abstract: "custonmer" -> "customer"; "probability generation function" -> "probability generating function"; fix the broken sentence "Model-B is left open, with a Volterra-type integral equation when it comes to finding the boundary for the queue length of Class-2 that falls beyond the scope of this thesis; However, ..." -> split into two grammatical sentences, lowercase "however".
- Intro "Methods": "regilarity" -> "regularity"; "obtained my means of" -> "obtained by means of".
- Section 4: "no only" -> "not only"; "assymetric" -> "asymmetric"; "phenomenons" -> "phenomena"; "whe following" -> "the following".
- Section 3.4: delete the duplicated M/G/1 definition sentence (the paragraph defines the M/G/1 queue twice in a row; keep the second, complete version).
- Section 6.1.2: "fundamental blobal balance equation" -> "fundamental global balance equation"; "class-2 customers are will not be taken into service" -> "class-2 customers will not be taken into service"; "arrivale rate" -> "arrival rate".
- Standardise capitalisation of "Class-1/class-1" — pick ONE convention (recommend lowercase "class-1" in running text, as in most of the document) and apply repo-wide with careful word-boundary regex; do NOT touch math mode or labels.
Also run a spell-check pass (e.g., aspell with a LaTeX filter) over all .tex files and fix unambiguous misspellings; list ambiguous ones in the final report instead of guessing.
Acceptance: build passes; git diff contains only prose-level character changes.
Commit: "fix: typo and copy-edit sweep (no content changes)"
```

### A2 — Cross-reference style and micro-corrections

```
Task: Normalise cross-references and fix three precise technical slips. No other changes.
1. Repo-wide: references to sections must read "Section~\ref{...}" or "\S\ref{...}" consistently (pick whichever dominates). Fix bare parenthetical forms like "as stated before 3.3", "the dedicated section for Model-C2 (9)", "(3.3)" used as a section reference. Equation references must use \eqref.
2. Section 4, Stability paragraph: "Model-A ... requires ρ ≤ 1" -> strict inequality "ρ < 1" (positive recurrence requires strict). Verify the same statement is strict everywhere else (it is in (105)); make this instance match.
3. Section 4, same paragraph: it cites the M/M/1 behaviour with "(3.3)" — the M/M/1 section is 3.1 and Erlang-A is 3.3. Point each claim at the correct subsection.
4. Verify Table 1 / Table 3 cross-references in the intro point at the right tables after the fix in B1 (if B1 already ran, re-check; otherwise just fix the reference style).
Acceptance: build passes; grep shows no remaining bare numeric section references.
Commit: "fix: cross-reference style + stability strictness"
```

---

## PHASE B — Global conventions (run BEFORE any new prose is written)

### B1 — Notation unification for head-of-line models + table reconciliation

```
Task: The head-of-line variants are typeset inconsistently (B^1_2, B12, B½, C^1_2 ...). Unify.
1. Define two macros in the preamble: \BH (renders as B_2^{\mathrm{H}}) and \CH (renders as C_2^{\mathrm{H}}) — or, if the author's existing macro file suggests another convention, propose it in the report but implement the H-superscript ("head-of-line") version.
2. Replace every occurrence of the head-of-line model names (text and math) with the macros. Be exhaustive: section titles, table cells, figure captions, axis labels are generated by the notebook builder — update the plotting code label strings too so regenerated figures match.
3. Reconcile Table 1 (intro, "Models studied") and Table 3 (Section 4, "Nested family"): Table 3 currently omits the two head-of-line variants. Add two rows to Table 3 with their parameter restrictions (gamma_1 head-of-line rate, all else 0; theta_1 head-of-line rate, all else 0) and a footnote that their mechanism rate is constant 1{n1>=1}, not n1, so they are NOT obtained by zeroing parameters of Model-X — mirror the wording already used in Section 10.1.
4. Do NOT regenerate figures in this task; only patch the label strings in code. Figure regeneration happens in D2.
Acceptance: build passes; grep for the old notations returns zero hits in .tex; report lists plotting-code files touched.
Commit: "refactor: unified head-of-line notation (\BH, \CH) + Table 1/3 reconciliation"
```

### B2 — Restructure: move Model-X analysis after Model-B; fix the roadmap

```
Task: Section 5 (Analysis of Model-X) forward-references the machinery of Sections 6-7 (it literally says "The proof follows the five steps of Model-B" before Model-B exists). Fix by reordering.
1. In the main file, move the \input/\include for the Model-X analysis section so the order becomes: Preliminaries (3), Model description (4), Model-A (currently 6), Model-B (currently 7), Model-X (currently 5), Model-B2 (8), Model-C2 (9), head-of-line models (10, 11), Comparison (12), Results (13). Equation/section numbers will shift — that is fine because all references are by label (verify; fix any hardcoded numbers you find).
2. Inside the Model-X section, adjust the opening paragraph: it currently introduces Model-X as the first analysis; rewrite the first paragraph (3-5 sentences max) so it reads as the synthesis/culmination: "Having solved A and identified the Volterra obstruction in B, we now show that the full model retains both obstructions simultaneously..." Keep all math untouched. Phrases like "As in Model-B" now point backwards and become correct — verify each "as in Model-B"/"in contrast to Model-B" claim still reads correctly in the new order.
3. Rewrite the "Structure of the thesis" paragraph in the Introduction to list ALL sections in their new actual order, including Section 5's new position and Sections 10-11, with one clause of rationale for the ordering (baseline -> obstruction -> synthesis -> tractable specialisations -> head-of-line collapse -> comparison -> validation).
4. Check the abstract's narrative order matches; adjust the abstract's clause order ONLY if it contradicts the new structure (full abstract rewrite is task F3, do not do it here).
Acceptance: build passes with zero undefined/changed references; PDF section order matches the roadmap paragraph.
Commit: "refactor: reorder Model-X after Model-B; rewrite thesis roadmap"
```

---

## PHASE C — Mathematical-prose tissue (independent insertions, one file each)

### C1 — Interpretive paragraph after Lemma 1

```
Task: Insert one paragraph (no math display needed beyond inline) immediately after the statement of Lemma 1 / equation (42) in the PGF-derivation section, BEFORE the proof, titled as an unnumbered remark or plain paragraph "Reading the fundamental equation."
Content it must convey (write in the author's formal voice, ~8-12 sentences):
- The algebraic coefficient of P is the Model-A kernel: flux balance of arrivals and services.
- The x-convection coefficient xy[gamma1(x-y)+theta1(x-1)] encodes the mechanisms: the factor (x-y) vanishes on the diagonal x=y, the analytic signature that jockeying conserves the total customer count; the factor (x-1) vanishes at x=1, the signature that abandonment respects normalisation but destroys conservation. Symmetrically for the y-convection.
- The right-hand side carries the two boundary unknowns: P_y(y) (empty priority queue) and pi(0,0).
- Foreshadow: every solution technique in the thesis is dictated by WHERE these factors place the singularity — kernel root inside the disc (A), interior point x=y with negative exponent (B2: analyticity pinning), boundary x=1 with positive exponent (C2: boundedness pinning), or full collapse to algebra (head-of-line). Cross-reference the comparison table in Section 12 with \ref.
Then, in Sections 8 (B2 Stage 2), 9.3 (C2), and the Remark after Lemma 4, add ONE back-reference sentence each ("as anticipated in the remark following Lemma~\ref{...}") — locate the right insertion points; keep each to a single sentence.
Acceptance: build passes; no equations modified.
Commit: "docs: interpretive remark after Lemma 1 + back-references"
```

### C2 — Justify the Hadamard finite part in Model-B, Step 5

```
Task: In the Model-B section, Step 5 of the proof of Claim 2 (around equations (180)-(184)), insert 3-4 sentences justifying the finite-part regularisation, at the point where the Hadamard finite part is first invoked.
Content: the 0 x infinity product limit (180) is the only well-defined object; neither the vanishing prefactor nor the divergent integral is meaningful in isolation; the asymptotic expansion y(t;z) - t ~ (Gamma/gamma1)(z-t) already performed in Step 2 verifies the limit is finite and equals the known diagonal value, so the regularisation introduces no new assumption — it is a bookkeeping device for a limit that exists. Add one standard citation for Hadamard finite-part integrals if the bibliography has a suitable reference; if not, add a \citationneeded-style TODO comment in the source (not in PDF output) and flag it in the report.
Acceptance: build passes; insertion is <= 5 sentences.
Commit: "docs: justify Hadamard finite-part step in Model-B"
```

### C3 — Promote the gamma1 -> 0 singular-limit discussion to a Remark (Model-B2)

```
Task: In the Model-B2 section, the discussion "Reduction to Model-A as gamma1 -> 0+" is currently embedded at the end of the proof of Theorem 3 (after equation (215), the paragraph starting "The no-jockeying limit is cleanest..."). 
1. Cut that entire discussion (both paragraphs: the normal-families argument AND the Kummer-ratio reading with equation (217)) out of the proof environment.
2. Paste it immediately after the proof as a numbered Remark (use the document's existing remark environment) titled "The singular limit gamma1 -> 0+". Keep all math verbatim, including equations (216)-(217) — they keep their labels.
3. Add one connecting sentence at the old location inside the proof: "The recovery of Model-A in the limit gamma1 -> 0+ is deferred to Remark~\ref{...} below, as the limit is singular and merits separate discussion."
Acceptance: build passes; equations (216)-(217) unchanged and still referenced correctly from Section 12/13 if they are.
Commit: "refactor: promote B2 singular-limit discussion to Remark"
```

### C4 — Three small rigor patches

```
Task: Three independent one-paragraph rigor additions. Do all three; touch nothing else.
1. Section 4 (or Section 5 Stability paragraph): the positive-recurrence claim for Model-X currently reads "behaves like some sort of M/M/1+M". Replace the hand-wave with a one-line Foster-Lyapunov argument: with V(n1,n2)=n1+n2 the drift in any busy state is lambda - mu - theta1 n1 - theta2 n2, which is <= -epsilon outside a finite set for any theta1,theta2>0; cite Foster's criterion (add bib entry if missing, e.g., Meyn & Tweedie or Foster 1953; if the repo bibliography lacks one, add the entry).
2. Model-C2 section, stability condition (229): sufficiency comes from the M/G/1 reduction; add 2-3 sentences for necessity: if lambda2 E[B_C] >= 1 the embedded M/G/1 of class-2 customers is null/transient, hence so is the joint chain (class-2 count is a deterministic function of the joint state). Keep it brief and honest about the level of rigor.
3. Section 6.1.2 (Model-A probabilistic proof): the step P(N1=0 | busy) = 1 - rho1 is asserted. Insert one sentence of justification: under non-preemptive priority with common service rate mu, the class-1 queue-plus-service process is the queue-length process of an autonomous M/M/1(lambda1, mu) (class-2 service occupancy is exchangeable with class-1 service for the class-1 count because the residual service is Exp(mu) regardless of class, cf. Section 3.2), whence the geometric law applies.
Acceptance: build passes; each insertion <= 4 sentences; new bib entries compile.
Commit: "docs: rigor patches (Foster-Lyapunov, C2 necessity, P(N1=0|busy))"
```

### C5 — Reframe Section 6.2 / Theorem 2 as a characterised methodological limitation

```
Task: Restructure the alternative-state-space subsection (6.2) WITHOUT deleting any analysis.
1. Demote "Theorem 2" to "Approximation 1" (or the repo's proposition environment with title "Heuristic approximation"). Update all references to it repo-wide (Table 9 in the Results section calls it "Theorem 2" — update the table cell and any prose mentions).
2. Retitle the subsection: "Analysis of Model-A on \widetilde{S}: scope and limitations of the partial-PGF recursion".
3. PROVE the currently-assumed geometric decay: insert a short lemma or displayed derivation showing pi(0,n) decays geometrically in n, derived from the exact Model-A solution — use the boundary function P_y(y) (equation (115)): P_y is analytic in a disc of radius > 1 (its nearest singularity is where x*(y)=y, i.e., y=1/rho>1), hence its coefficients pi(0,n) = O(r^{-n}) for any r < 1/rho. 3-6 lines of math, with proof.
4. Add a "failure mechanism" paragraph after the approximation: the neglected forcing mu y^n (1-y) pi(n+1,n+1) involves the diagonal states (all waiting customers class-2); using pi(n,n)=pi(0,n) and the decay rate just proved, compare the geometric rates: the forcing is negligible relative to the homogeneous solution [ytilde*(y)]^n precisely when rho1/rho is large and rho moderate, which is exactly the empirical validity region of Figure 22 (reference it). Connect explicitly to the thesis-wide theme: this is the same structural obstruction — an unknown boundary/diagonal trace coupling into an otherwise solvable recursion — that appears as the Volterra forcing in Models B and X (cross-reference).
5. State in one sentence what a rigorous closure would require (variation of constants in n reintroduces the unknown diagonal sequence) and add a pointer "see Section [Future Work]" with a \ref placeholder to be filled by task F2.
6. Abstract alignment: the abstract claims the alternative state space is explored for "Model-A, Model-B and Model-B2" — the manuscript only delivers Model-A. Fix the abstract clause to match (one clause; full abstract rewrite is F3).
Acceptance: build passes; "Theorem 2" no longer appears anywhere; Table 9 row updated; the new decay proof uses only already-established results.
Commit: "refactor: Section 6.2 reframed as characterised approximation + decay proof"
```

---

## PHASE D — Computation (simulation / notebook builder)

### D1 — Compute the missing metrics; export machine-readable results

```
Task: Extend the numerical pipeline to produce the metrics the Results prose needs. Locate the CTMC solver / simulation code and the notebook builder first (see docs/REPO_MAP.md).
Compute, at the canonical parameters (lambda1=0.3, lambda2=0.4, mu=1, mechanism parameter 0.5) AND across the rho-sweep grid already used for Table 6 (rho in {0.50, 0.70, 0.90}):
1. Class-1 loss fraction for C2 and the head-of-line C-variant: P_loss = theta1 * E[N1] / lambda1 (full-rate) and theta1 * P(N1>=1) / lambda1 (head-of-line — note the rate is constant, derive the correct expression from the CTMC directly as abandonment-flow/lambda1 rather than trusting the formula).
2. Conditional mean time-to-service of SERVED class-1 customers in C2 (and Model-A baseline = E[W1] there), via the simulation: tag customers, record waiting time conditional on service completion. Also record it for B2 where "served from queue 1" excludes jockeyed customers.
3. The maximisers alpha* of the priority ratio E[W1]/E[W2] over the class-split sweep of Figure 12, for each of the five models (read off the existing sweep data or recompute on a finer alpha grid).
4. The B2-vs-head-of-line E[N1] gap at the three loads (data exists in Table 6 — just include it).
5. P(N1>=2) for each model at the three loads (for the head-of-line gap discussion, task E2).
Export everything to results/derived_metrics.json (and a small .tex macro file results/derived_metrics.tex defining \lossCtwoSeventy etc. via \newcommand) so the prose tasks can \input it instead of hardcoding numbers.
Verify the conservation identity carried + lost = offered for C2 at each grid point and include the check in the JSON.
Acceptance: script runs end-to-end and is committed; JSON + macro file generated; numbers sanity-checked against Table 6 (e.g., loss at rho=0.70, theta1=0.5 should be approx 0.5*0.1392/0.3 ~ 0.23).
Commit: "feat: derived metrics (loss fractions, conditional latency, alpha*, P(N1>=2))"
```

### D2 — Figure consistency pass

```
Task: In the notebook builder / plotting scripts:
1. Unify colour conventions between the Figure-16 heatmap (E[N1] ratio) and the Figure-22 validity map (epsilon_inf): same direction for good/bad (recommend: green = favourable/accurate, red = unfavourable/inaccurate, consistent colormap family), and state the convention in both captions.
2. Apply the head-of-line notation macros from B1 to every legend/label/title string (the figures currently render B^1_2-style strings).
3. Regenerate ALL affected figures, confirm file names unchanged so \includegraphics paths still resolve, rebuild the PDF, and visually diff the two heatmaps (export before/after PNGs to a scratch folder and report).
Do not change any computed data in this task.
Acceptance: build passes; regenerated figures render; caption text updated to state the colour convention.
Commit: "fix: figure colour-convention + notation consistency, regenerated"
```

---

## PHASE E — Results prose (depends on D1)

### E1 — Resolve the two [AUTHOR] placeholders

```
Task: Two leftover author notes must be resolved using results/derived_metrics.tex (from task D1). 
1. Section 12.1, the bracketed note after Table 7 about conditional time-to-service: replace it with 3-5 sentences reporting the conditional mean time-to-service of served class-1 customers (numbers via the \newcommand macros), contrasting it with the unconditional E[W1] and stating explicitly which part of the apparent C2/B2 "improvement" is attrition. 
2. Section 12.3, the bracketed note in the class-asymmetry discussion: insert the three (five, if computed for all models) alpha* values read from derived_metrics, with one sentence interpreting where the priority ratio peaks and why (interior maximum: mechanism engagement vs class dominance).
Grep afterwards to confirm zero "[AUTHOR" strings remain anywhere.
Acceptance: build passes; numbers come from \input macros, not hardcoded.
Commit: "docs: resolve AUTHOR placeholders with computed metrics"
```

### E2 — Insight paragraphs for Sections 12-13

```
Task: Insert six short, surgically-placed prose additions (2-6 sentences each). Use macros from results/derived_metrics.tex for all numbers. Locations:
1. Section 12.4 (or a new short subsection 12.4.1 "The price in lost customers"): the headline loss-fraction result — at rho=0.70, theta1=0.5, approx 23% of class-1 customers are never served; juxtapose with the E[W1] drop from 1.00 to 0.46 and state the healthcare reading (abandonment = deterioration/exit). This is the thesis's strongest applied claim — write it as such.
2. Section 12.4, after the throughput panel discussion: reframe the carried+lost=offered check (0.6304+0.0696=0.70) explicitly as an independent VALIDATION of theta1*E[N1] against the throughput deficit, not merely an observation.
3. Section 12.4, the E[N2] monotonicity paragraph: upgrade the "we flag one departure" passage into a stated negative finding — name the two competing effects, state which dominates, and either (a) report the extra corner-check from D1 if computed, or (b) state an explicit conjecture of monotonicity in theta1 at all loads, flagged for future work.
4. Section 12 (where Table 8 is discussed): a dedicated paragraph on the rho=0.90 row — 10.00 (A) vs 22.38 (B2) vs 6.30 (C2) — as the single sharpest statement of the dichotomy: same discipline, opposite movements of the priority premium, both superficially "better for class 1", neither for the naive reason. 
5. Section 12.5: quantify the head-of-line gap as an empirical proxy for P(N1>=2): report P(N1>=2) at the three loads next to the full-vs-head E[N1] gaps and note they move together.
6. Section 12.4 or 13 (near Figure 16): one sentence noting the heatmap is nearer-separable in theta1 than rho — the valve strength, not the load, is the first-order control; and near Figure 9: one sentence noting the C2 pi(0,0) curve's PEAK shifts right of rho=0.5 relative to the parabola, the signature of abandonment renormalising the effective load.
Acceptance: build passes; every number from macros; no paragraph exceeds 7 sentences.
Commit: "docs: results insight paragraphs (loss fraction, dichotomy, validation framing)"
```

### E3 — Add loss-fraction column to Table 6 (or companion table)

```
Task: Extend the model-comparison tabulation.
Add a column "P_loss^{(1)}" to Table 6 (values: 0 for A, B2, head-of-line B; computed values from derived_metrics for C2 and head-of-line C), OR if the table becomes too wide, create a compact companion table immediately after it with columns: model, throughput, abandonment rate, P_loss^{(1)}, at the three loads. Update the table caption to define the metric and update any prose that enumerates Table 6's columns.
Wire the numbers through the \input macro file — the table should be regenerable from D1's pipeline (if the repo's notebook builder generates tables, extend it; otherwise hand-edit the tex but source numbers from macros).
Acceptance: build passes; table renders within margins; caption updated.
Commit: "feat: loss-fraction column in model comparison table"
```

---

## PHASE F — New sections (depends on B2 for ordering, E for numbers)

### F1 — Literature Review

```
Task: Write Section 2 (Literature). It currently contains five empty subsection headings and Table 2. Write 1.5-2.5 pages of prose filling the existing headings, in the author's voice. DO NOT delete Table 2 — the prose must walk it.
Structure and required content:
- "Non-preemptive priority queues: exact queue-length analysis": Cohen (1956) as origin of the partial-PGF technique reused in Section 6.1.3; state explicitly that the Model-A result (Theorem 1) is classical and the thesis's contribution is the unified framework around it; Stanford et al. (2014).
- "Priority queues with abandonment": Erlang-A lineage; where exact PGFs with reneging exist vs fluid/diffusion-only (Jouini & Roubos 2014; Wang et al. 2015; Zuk & Kirszenblat 2023; Baron et al. 2025); position Model-C2 as exact, single-server, CLASS-ASYMMETRIC abandonment.
- "Jockeying and priority changes": de Waal (1992) (be precise about why its Table-2 entry is "approximate"); Hu, Chan & Dong (2022); Shmelev & Zychlinski (2025); position Model-B2 as the exact single-server counterpart of the approximate multi-server upgrade literature.
- "Multi-server extensions and performance design": brief; route the multi-server refs not covered above.
- "Position of this thesis": walk Table 2 row by row in prose; one-sentence gap statement (no prior exact single-server queue-length analysis combines non-preemptive priority with jockeying or abandonment in a unified PGF framework); equally explicit non-claims (X and B remain open).
- ADD a methodology paragraph (new short subsection or fold into "Position"): the kernel method / boundary-value tradition (Fayolle, Iasnogorodski & Malyshev; Cohen & Boxma "Boundary Value Problems in Queueing System Analysis") — the analyticity/boundedness pinning arguments of Sections 8-9 belong to it; plus one reference for confluent hypergeometric structure in birth-death/reneging queues and one for Pincherle's theorem (currently only [DLM]).
- ADD 2-4 healthcare-queueing citations (elderly-care waiting lists, patient deterioration as class transition, reneging as mortality) to license the introduction's motivation.
For every reference not already in the .bib file: add a bib entry with a "% VERIFY" comment and list them all in the final report — the author must verify them; do NOT fabricate page numbers or DOIs, leave fields blank with VERIFY comments where unsure.
Acceptance: build passes; every \cite resolves; prose contains no bullet lists; report lists all VERIFY entries.
Commit: "feat: literature review section"
```

### F2 — Conclusion & Future Work

```
Task: Write the missing final section "Conclusion and Future Work" (insert after the Results section, before References; add to the roadmap paragraph in the Introduction with one clause).
Required content, in this order (2.5-3.5 pages, prose, no bullets except possibly the future-work list which MAY be an enumerated list):
1. Restate the hierarchy and the OBSTRUCTION TAXONOMY as the central intellectual contribution: four pinning mechanisms (kernel root inside the disc; interior analyticity at x=y; boundary boundedness at x=1; head-of-line algebraic collapse) and the two irreducible obstructions of X/B (transcendental characteristics; diagonal gradient coupling). Cross-reference the comparison table of Section 12 and the remark from task C1.
2. The mechanism dichotomy with numbers (via the macros): jockeying redistributes delay at fixed work (E[N], pi0, pi(0,0) invariant; E[W2]/E[W1] inflated to 22.38 at rho=0.90); abandonment sheds load (idle up, all queues down) at the price of the loss fraction (~23% at rho=0.70, theta1=0.5). Explicit caveat: improved waiting metrics under abandonment are partly attrition, not service.
3. Close the healthcare loop opened in the Introduction: operational meaning of gamma1 and theta1; ADDRESS THE DIRECTION MISMATCH honestly — the motivation describes deterioration as an upgrade toward higher priority, but the solved model B2 has 1->2 (downgrade) jockeying; either reinterpret (recovery / reclassification / administrative downgrade) or state plainly that the deterioration direction (2->1, i.e. gamma2>0) is exactly the open Volterra case, which strengthens the future-work motivation. What a waiting-list manager should monitor: P(N1>=2), loss fraction, the (rho, theta1) regime of the Figure-16 heatmap.
4. Limitations, stated proactively: exponential assumptions throughout; single server; means only (no waiting-time distributions); the Approximation's validity region (cross-ref Figure 22); CTMC truncation bias at rho >= 0.92 (already flagged in 12.1 — repeat); E[W2] in B2 is per-entrant residence, not end-to-end tagged-customer delay.
5. Future work, concrete and ranked: (i) head-of-line versions of the remaining models (B1, C, C1, and head-of-line X with BOTH mechanisms) — all algebraic and Kernel-Method-solvable with the tools already built; state explicitly this is near-term low-hanging fruit; (ii) numerical inversion of the Model-B Volterra equation (kernel explicit, forcing known — unlike X); (iii) Riemann-Hilbert / boundary-value methods for Model-B (link to the F1 methodology citations); (iv) end-to-end sojourn of a tagged class-2 customer in B2 and conditional time-to-service in C2 (link to the E1 metric); (v) waiting-time distributions via distributional Little's law; (vi) multi-server extension toward Hu/Chan/Dong; (vii) calibration to real elderly-care waiting-list data. Also: the closure of the S-tilde recursion deferred from task C5 — fill its \ref placeholder.
Acceptance: build passes; C5's forward \ref now resolves; macros used for all numbers.
Commit: "feat: conclusion and future work"
```

### F3 — Abstract rewrite + title

```
Task: Rewrite the abstract (keep <= 1 page) now that all content exists. Requirements:
- Fix all grammar (the current abstract has several errors — see A1, but rewrite rather than patch).
- Accurate claims only: the S-tilde analysis is delivered for Model-A as a characterised approximation (per C5); head-of-line models included; X and B open with named obstructions.
- Add ONE sentence on the headline applied finding (mechanism dichotomy + loss fraction) — abstracts that end on "findings are validated numerically" undersell.
- New section ordering reflected (per B2).
Separately: the title is currently the placeholder "Thesis". Propose three candidate titles in the report (descriptive, mentioning two-class M/M/1 priority, jockeying, abandonment, exact PGF analysis) and insert the strongest as the working title with a % TODO-confirm comment.
Acceptance: build passes; abstract <= 1 page; report lists the three title candidates.
Commit: "docs: rewritten abstract + working title"
```

---

## PHASE G — Final integration (run last)

### G1 — Full audit and release build

```
Task: Final integration check.
1. Clean build from scratch (delete aux files first). Zero errors; report every remaining warning.
2. Grep for leftovers: "AUTHOR", "TODO", "FIXME", "VERIFY", "??", "Theorem 2" (must be gone per C5), old head-of-line notation strings (per B1). Report hits; fix only trivial ones, list the rest.
3. Reference audit: every \ref/\eqref/\cite resolves; every figure/table is referenced at least once in prose; every bib entry is cited.
4. Consistency spot-checks: roadmap paragraph vs actual section order; Table 1 vs Table 3 vs Table 9 model lists agree; the abstract's claims vs delivered content; loss-fraction numbers identical everywhere they appear (they should all come from the macro file — grep for hardcoded "0.23"-style numbers near them).
5. Produce a final REVIEW_CHECKLIST.md in docs/ mapping each committee-review point to the commit that addressed it.
Commit: "chore: final integration audit"
```

---

## Dependency graph (what can run in parallel)

```
P0.1
 ├─ A1, A2                     (independent of everything else)
 ├─ B1 ──> D2                  (figures need final notation)
 ├─ B2                         (independent of A, C, D)
 ├─ C1, C2, C3, C4, C5         (mutually independent; C5 touches Table 9)
 ├─ D1 ──> E1, E2, E3          (prose needs the metrics)
 ├─ B2 + E* ──> F1, F2, F3     (new sections need ordering + numbers)
 └─ everything ──> G1
```

Safe parallel batches if running multiple sessions: {A1, B2, C2}, then {A2, C1, C3, C4, D1}, then {B1, C5}, then {D2, E1, E2, E3}, then {F1, F2}, then {F3}, then {G1}.
