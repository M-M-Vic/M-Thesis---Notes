# Final Independent Audit — 2026-07-16

> Read-only pre-submission audit of the full thesis at `64032b5` (+ uncommitted `main.pdf`).
> Everything below was verified against the current sources and a fresh compile — not
> against prior audit records. Auditor: Claude (final-audit skill).

---

## A. Verdict

**Very close to submission-ready.** A fresh `latexmk -pdf` compiles with **0 errors, 0
warnings, 0 unresolved references, 0 duplicate labels/destinations**, at **72 pages**;
all 17 bibliography entries are cited; the reviewer's 402 annotations are addressed or
explicitly dispositioned, and every disposition I sampled checks out against the live
text. The top 3 risks, all fixable in under an hour: **(1)** today's Overleaf trim of the
introduction left a dangling promise — "Three complementary proof strategies are used
throughout" with the three strategy paragraphs deleted — and the same edit introduced the
typo **"built bove"** into the §5.1.2 proof (visible on PDF p. 37); **(2)** the author
voice pass is still outstanding on 2 of the 3 Claude-drafted passages (§6 Volterra
paragraph, §8.4 scoping) — the §6 one is the most machine-sounding text in the document;
**(3)** four display equations visibly cross the right margin (11–15 pt, PDF pp. 36, 38,
56, 63). Single most important fix: repair the introduction seam (finding 1).

Page-count history is explained: 67 pp (2026-06-27) → 72 pp (round 2) → 74 pp (round 3)
→ 72 pp now (the §5.1.2 proof trims `ca70e86`/`64032b5` + the intro strategy-paragraph cut).

---

## B. Findings, ranked by severity

**No 🔴 blockers found.** Build is clean, no maths errors surfaced in the checks run, no
π₀/π(0,0) conflation anywhere, no reviewer request unaddressed-and-undispositioned.

### 🟠 Major

1. **🟠 [chapters/01_introduction.tex:38](../chapters/01_introduction.tex) — dangling
   "Three complementary proof strategies" after today's cut.** Commit `64032b5`/`0d0dc3b`
   (Overleaf, today) deleted the three `\emph{...}` paragraphs describing the strategies
   (Kernel/ODE route, probabilistic P–K route, PPGF route). The Methods subsection now
   promises an enumeration it never gives; the deleted text was also the only *global*
   statement that (a) the PPGF route is a third, partially dependent derivation and (b)
   the probabilistic route dies with jockeying (the latter survives only in §11.2,
   [13_results.tex:133](../chapters/13_results.tex)). Knock-on inconsistency: §5 announces
   "**two** standalone proofs" ([06_model_a.tex:43](../chapters/06_model_a.tex); also "two
   complete proofs", 06:7) yet §5.1.3 is a third `proof` environment that opens "This
   proof follows Cohen's method" and ends "…concludes the proof" (06:217, 06:364). If
   "standalone/complete" is deliberate (the PPGF proof imports $P_y(y)$ from the others,
   06:330–332), say so explicitly. **Fix:** either restore one-sentence versions of the
   three strategy descriptions under Methods, or rewrite the opener ("All proof
   strategies act on a functional equation of the common shape…") *and* reconcile the §5
   proof-count sentence ("two standalone proofs … and a third, partially dependent,
   partial-PGF derivation").

2. **🟠 Voice pass still outstanding on 2 of 3 drafted passages** (round-3 log's own
   condition for closure of N1b/#177-group).
   - [07_model_b.tex:379](../chapters/07_model_b.tex) (Volterra intuition, N18): the most
     machine-sounding paragraph in the thesis — "**It is worth spelling out** why the
     obstruction takes precisely this form …", "**This matters because** first-kind
     equations lack the free copy of the unknown …", "Probabilistically, **the smearing
     \emph{is} the mechanism**", three long em-dash asides, closing "—exactly what the
     integral … expresses". Content is correct and valuable; the register is not the
     author's. Untouched since disposition pass C (`968f19d`).
   - [09_model_c2.tex:245](../chapters/09_model_c2.tex) (§8.4 scoping): one 80-word
     sentence with nested em-dash asides ("a spell begins with a \emph{waiting}, hence
     abandonable, class-$1$ customer …"); milder but still drafted voice. Untouched since
     pass C.
   - §5.1.2 ([06_model_a.tex:180,186](../chapters/06_model_a.tex)) **was** voice-passed
     today — but the edit introduced findings 5 and 6 below.

3. **🟠 Four display equations visibly cross the right margin** (confirmed on rendered
   pages, not just the log):
   | pt over | file:line | PDF p. | fix |
   |---|---|---|---|
   | 14.85 | [06_model_a.tex:142](../chapters/06_model_a.tex) (`align*` row 1) | 36 | break row 1 after the first RHS term: `…\rho(1-\rho)` `\\ &\qquad- \mu x(1-y)\rho(1-\rho)` |
   | 14.85 | [06_model_a.tex:200](../chapters/06_model_a.tex) (same pattern, probabilistic proof) | 38 | same break |
   | 13.48 | [09_model_c2.tex:189](../chapters/09_model_c2.tex) (`align*` row 2) | 56 | break before `-\bigl(1-\zeta(y)\bigr)e^{-\lambda_1t/\theta_1}…` |
   | 11.15 | [11_model_c21.tex:200](../chapters/11_model_c21.tex) (`equation*`) | 63 | `multline*`/`split`, break at the `=` |
   The remaining two overfulls (0.45 pt at 02:35, 2.63 pt at 11:198) are invisible.

### 🟡 Minor

4. **🟡 [chapters/06_model_a.tex:180](../chapters/06_model_a.tex) — typo "the $M/G/1$
   system built bove"** (introduced today; reaches the PDF, p. 37, mid-proof of the
   flagship theorem). → "built above".

5. **🟡 [chapters/06_model_a.tex:180](../chapters/06_model_a.tex) — "birth-death process"
   with a hyphen**, vs "birth--death process" (en-dash) at
   [04_model_description.tex:113](../chapters/04_model_description.tex). Today's edit also
   changed "chain" → "process"; en-dash is the house form. → "birth--death".

6. **🟡 [chapters/11_model_c21.tex:6](../chapters/11_model_c21.tex) — "the class-$1$
   abandonment model Model-$C_2$"** reads as a stutter. → "… abandonment model,
   Model-$C_2$" or drop "model".

7. **🟡 [chapters/13_results.tex:130](../chapters/13_results.tex) — "remains to be that of
   the standard $M/M/1$ queueing model"** — non-idiomatic ("remains to be" = "is yet to
   be"). → "remains that of the standard $M/M/1$ queue".

8. **🟡 [chapters/13_results.tex:238](../chapters/13_results.tex) — hardcoded Model-$B$
   value $0.51$** beside macro-routed neighbours (`\ENoneASeventy`, `\ENoneBtwoSeventy`).
   No `\ENoneB*` macros exist in `results/derived_metrics.tex` (checked); the generated
   table holds 0.5149. Drift risk if the notebooks are re-run with new parameters. →
   extend `Code/compute_derived_metrics.py` with Model-$B$ macros, or accept and note it.

9. **🟡 Terminology drift: "bidirectional" vs "two-way" jockeying.** "Bidirectional" in
   the intro table, §6 preamble, §6 figure caption and conclusion; "two-way" twice in §11
   ([13_results.tex:224,238](../chapters/13_results.tex)). Harmless but a global-consistency
   nit; pick one (the abstract uses neither).

10. **🟡 [chapters/14_conclusion.tex:14](../chapters/14_conclusion.tex) — "not a loose
    collection of cases, but a complete enumeration"** — the antithesis construction plus
    the strong word "complete" (complete relative to *this thesis's* four-mechanism/two-
    obstruction taxonomy, not provably exhaustive) is the one conclusion sentence an
    examiner might push on, and the register is slightly drafted. Consider "…but an
    enumeration: four mechanisms that enable exact solutions and two obstructions that
    prevent them."

11. **🟡 Excluded appendix would not compile if re-enabled.** `15_appendix_numerics.tex`
    carries 4 dangling refs to labels deleted in the 2026-06-27 restructure
    (`eq:comp:lossfrac` :286, `fig:c2:heatmap` :120, `subsec:comp:abandonment` :328, :551)
    and still uses "validation" terminology (round-3 item 32, author-known). Harmless
    while commented out at `main.tex:94`; fix before ever uncommenting.

12. **🟡 17 underfull hboxes (badness 10000)**, all inside the narrow `p{}`-column
    structural-comparison table ([13_results.tex:57–118](../chapters/13_results.tex)) plus
    one at 13:172. Cosmetic; standard for narrow ragged columns. Optional silencer:
    `>{\raggedright\arraybackslash}p{…}` column spec.

13. **🟡 CLAUDE.md §6 template deviation (reviewer-approved):** Model-$B_2$, $\BH$, $\CH$
    have no "Probabilistic approach" heading explaining why that route is inapplicable
    (the convention asks the heading be kept with the explanation). The substance lives in
    §11.2 (13:133 for jockeying; 13:143 for why C₂ keeps it). Given two reviewer rounds
    approved this structure, this is a policy note, not a defect — author's call.

**Clean categories** (checked, nothing to report): π₀ vs π(0,0) discipline (every
occurrence correct, incl. all "$P(1,1)=1-\pi_0$" identities); $N_1,N_2,N$ in-queue
definitions (intro :5, §4); stability stated explicitly and correctly in **all six**
model chapters (strict $\rho<1$ for A/B/B₂/$\BH$; non-trivial conditions with
positive-recurrence framing for C₂/$\CH$); principles named at point of use (PASTA,
Little's Law, memorylessness, P–K, Vieta, implicit function theorem, Cramer's rule);
`\mathcal{I}` clash resolved (indicator is `\mathcal{B}`, integrals 𝓗 uniformly, 𝒥
reserved for C₂'s full integrals); $\widetilde S$ confined to §4/§5 with only
retrospective mentions in §11/§12; zero US spellings; zero scaffolding markers; no
`eqnarray`; no hand-typed equation numbers; no `equation`+`\nonumber` phantom anchors
(0 duplicate destinations in the log); label scheme consistent (`eq:<Model>:*` +
coherent `eq:mm1/pk/kummer/erlangA/ode:*` preliminaries namespaces); every
`\includegraphics`/TikZ file exists; every compiled float is referenced in prose;
16 figures + captions British-spelled; TOC clean; abstract scope matches the final
document (5 solved + B/X open, verification language, `\BH`/`\CH` macros); bibliography
`plain`/numeric as agreed (N129), 17/17 keys cited, no orphans.

---

## C. Reviewer-feedback closure

Sources verified directly: `docs/feedback_rbr650_2026-07-13.pdf` (402 annotations
extracted programmatically; strict superset of `M_Thesis_FeedbackAnnotations.pdf`'s 274 —
only the p. 1 general note was replaced) against the current sources. The reviewer's p. 1
verdict decomposes into N1a (formality), N1b (more intuition, e.g. Volterra), N1c (use
Model-B more in the comparison).

| Reviewer item | Status | Evidence (current text) |
|---|---|---|
| N1a formality pass ("informal or conversational language") | **addressed** | lexicon/connector sweeps clean; all round-2 flagged phrases gone ("cousins", "sit/lie", "low-hanging fruit", "closes the loop", "In words:", "defect", "frozen", "sweep", "true departure", …) |
| N1b intuition (Volterra role) | **addressed, voice pending** | paragraph at 07_model_b.tex:379; flagged for author voice (finding 2) |
| N1c Model-B in comparison | **addressed** | Table 5 column (13_results.tex:59–116); `tab_comparison_main.tex` multirow-6 rows + caption; §11.3 prose 13:209,238; Fig. 8 caption 13:224 |
| N65 §11 retitle | addressed | 13_results.tex:1 "Numerical verification and comparison" |
| N66 "diagonal to 10⁻⁴" made precise | addressed | 13:9 "agree to within $10^{-4}$" |
| N67 T-S row out of Table 4 | addressed | table 13:19–34 has no T-S row; separate prose 13:35 |
| N68–70 validation→verification | addressed | zero "validation/validate(d)" in compiled prose (label names exempt by design) |
| N29 derivative comparison corrected (both terms carry γ₁) | addressed | 10_model_b21.tex:147 |
| N39/N43 μ→μ+θ₁ remark | addressed | rem:C21:mushift, 11_model_c21.tex:47 |
| N50 θ₁→0⁺ recovery outside the theorem | addressed | 11:118–122 (post-corollary) |
| N51 Thm5↔Thm6 comparison (optional) | **removed, round 3, by author decision** | no trace in 11_model_c21.tex (conservative rule) |
| N55 singular-corner remark | addressed | rem:C21:order, 11:162 (incl. the Model-A answer) |
| N56 independent E[BP] argument | **left open per reviewer's own caution** | 11:159 marks it "a by-product of the computation" |
| N96 figure text size | addressed | fig regenerated pass D (`9dccb3e`); caption/grid match |
| N103 waiting-time definition under abandonment | addressed | 13:242 (Little's Law, wait ends at service entry *or abandonment*) |
| N105 log–log + linear companion | addressed | fig_conv_combined panels (a)–(d), caption 13:256–268 |
| N106 slope-1 derivation | addressed | 13:274 (affine generator + Cramer's rule) |
| N110/N118/N121/N104 typos (determins/Walal/cattying/thos) | addressed | zero grep hits |
| N111/N113 conclusion self-containment | addressed | zero `\ref` in 14_conclusion.tex (cites only) |
| N116 §12.2 deletion | **deleted, round 3** | conclusion = 12.1/Limitations/Future work only |
| N120 S̃ rationale at introduction of S̃ | addressed | 04_model_description.tex:33 forward pointer to rem:gen:Stilde_failed |
| N123 k-ladder "first k" | addressed | 14:31 with both rates γ₁min(n₁,k), θ₁min(n₁,k) |
| N125/N126 "Numerical solution" + recast | addressed | 14:32 |
| N127 multi-server exactness (Kella–Yechiali) | addressed in text; **author must confirm the paper is read** | 14:33 + `kella1985waiting` in references.bib:52 |
| N128 Zenios venue fix + tempered calibration | addressed | references.bib:169 (Queueing Systems); 14:35 |
| N129 bibliography ordering | addressed | `\bibliographystyle{plain}`, main.tex:96 |
| Round 1 #3 jockeying footnote | addressed | 01_introduction.tex:3 (de Waal, Hu–Chan–Dong) |
| Round 1 #18 subscript-naming rationale | addressed | 04_model_description.tex:66 |
| Round 1 #177/#179/#265/#271 probabilistic identifications | addressed (round 3) | censoring + autonomy proofs live at 06:180, 06:186; §8.4 scoping 09:245 — voice pending on the latter |
| Round 1 #241 stability ⇔ E[B_C] Kummer link | addressed | 09_model_c2.tex:20–23 (contiguous identity) |
| Round 1 #250 sign error D=−λ₁ | addressed | 09_model_c2.tex:85 |
| Round 1 sampled: p33 "of this collection", p43 dash-brackets, p45 "what part is left open", p53 𝓗₁≠𝒥₀ exponent | all addressed | 06:3–5; old phrasing gone from 07; 07:374 ("Upgrading the claim to a theorem would require, first … second …"); 09:181 |
| Round 1 declined (#20, #21, #53, #79, #115, #135, #169, #234, #260, #262 reorder) | **declined by author, documented** | `docs/feedback_rbr650_log.md`; #20/#53 barred by the no-unread-citations policy |

I found **no reviewer comment that is both unaddressed and undispositioned**. The three
open threads are exactly the ones the round-3 log names: two voice passes (finding 2),
the Kella–Yechiali read-confirmation, and the optional textbook citation for the
censored/watched-chain principle in §5.1.2.

---

## D. What I could not verify

- **Citation sourcing:** whether the author has read Kella & Yechiali (1985)
  (`literature/3`) — required by their own citation policy before submission — and
  whether Wang–Baron–Scheller-Wolf covers the non-preemptive case to their satisfaction
  (N127 residual). Zenios-calibration specifics (N128 residual) likewise.
- **Numerical values:** `results/derived_metrics.tex` and the generated tables/figures
  were CTMC-verified in the disposition sessions (logged to ~1e-14); I confirmed
  internal consistency (prose 0.51 vs table 0.5149, macro wiring) but did not recompute
  the pipeline in this pass.
- **Round-1 annotations item-by-item:** 274 items; I verified a ~10-item risk-weighted
  sample plus every structural/headline item, and relied on the reviewer's own round-2
  re-read (pp. 1–54 unchanged, no re-raised issues) for the remainder.
- **`\bigl…\bigr` visual sizing and display punctuation** were spot-checked on the five
  rendered pages (36–38, 56, 63) and found consistent, not exhaustively audited — TeX
  does not police `\bigl/\bigr` pairing.
- **The defence deck** (`Thesis presentation review/Thesis_Defence.pdf`) was not audited;
  it is outside the thesis document.
