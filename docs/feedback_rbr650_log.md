# rbr650 feedback incorporation — disposition log

# Round 2 (2026-07-13) — final feedback, §§9–12 + references

Source: `docs/feedback_rbr650_2026-07-13.pdf` (402 annotations total). Diffed against the
round-1 PDF: 273/274 round-1 annotations are byte-identical (pp. 1–54 untouched, so §§1–8
needed no re-work); the reviewer replaced the p.1 general note and added **128 new
annotations on pp. 55–68** — §9 (Model-B₂ᴴ), §10 (Model-C₂ᴴ), §11 (Results), §12
(Conclusion) and the references. Numbered N1–N129 in this log (N1 = new general note).
Branch: `feedback-rbr650`. Build after incorporation: 72 pp, 0 errors, 0 undefined refs,
0 duplicate labels; 6 overfull hboxes, all pre-existing (§§2, 5, 8 displays; none from the
new tables/aligns).

## Applied (summary by area)

| Area | Annotations | Highlights |
|---|---|---|
| §9 Model-B₂ᴴ | N2–N32 | Title bare (`Analysis of Model-B₂ᴴ`, restriction moved into first sentence, matching §§5–8); Devos et al. flagged as *discrete-time* randomly-alternating-service model + sentence split (N2); "flat rate"→constant rate (N3); simplification paragraph moved to §9.2 before Lemma 4 (N4); balance equations rebuilt as one `align` with all `=` aligned (N5); P(x,y) definition dropped from Lemma 4 and Theorem 5 (N6/N18); proof wording: Equations capitalised, "are identical to", γ₁-terms neglected explicitly, out/in-flow → "γ₁-term on the left/right-hand side", "and" for comma, "(out minus in)" dropped (N7–N13); §9.3 retitled "…for the PGF" (N14); intro "applies the Kernel Method, similarly to" (N15/N16); theorem descriptor removed (N17, matches §§5–8); "kernel quadratic"→"quadratic equation" + duplicate kernel display removed (N19/N23/N57-parallel); corollary-framing sentence and proof-note recast as instance of Cor. `cor:gen:no_abandon` (N20/N21); "y≠0 gives" (N22); missing space + root-location argument restructured, inequality moved to text, "we obtain"/"we determine" (N24–N27); implicit differentiation split into steps and the **implicit function theorem named** (N28); comparison with Model-A's derivative now explicitly "Eq. (5.6) evaluated at y=1 gives λ₂/(μ−λ₁)" — and corrected: *both* numerator and denominator carry the extra γ₁ (N29); vanishing-RHS reason restated (boundedness) + relation displayed (N30); "bracket collapses"→identity-based reduction + "cancelling the common factor" (N31/N32) |
| §10 Model-C₂ᴴ | N33–N64 | Title bare + restriction in first sentence (N33); "flat rate"→constant rate + "to the fundamental equation" (N34/N35); "True departure…"→conservation-no-longer-applies sentence (N36); stability paragraph: "regardless of the queue length", contrast with Model-C₂'s length-proportional self-stabilising rate, "non-trivial stability condition" (N37/N38); **new Remark (rem:C21:mushift)**: balance equations = Model-A with μ→μ+θ₁ on transitions out of n₁≥1 states; substitution acts on the P-coefficient of (10.4) but not on boundary terms nor stability (N39/N43/N44-adjacent); "land in"→"lead to", "coefficient on the in-flows"→"common in-flow coefficient" (N40/N41); balance equations aligned (N42); lemma proof made precise ("deleting every term that contains θ₁") + θ₁-term phrasing + "Adding this" (N44–N46); §10.3 intro sentence added + title "…for the PGF" (N47); E[x^{N₁}y^{N₂}] dropped (N48); "quadratic equation" (N49); θ₁→0⁺ recovery sentence moved out of Theorem 6 into post-corollary text (N50); **new paragraph comparing Thm 6 with Thm 5** (same rational architecture; kernels differ in constant term; π(0,0) input differs) (N51); ρ_C re-definition dropped from (10.8) + stability-paragraph duplication deduplicated (N52); "cut identity"→idle-boundary balance equation (10.3) (N53/N54); **new Remark (rem:C21:order)** explaining why the two evaluations at the singular corner (1,1) give different equations, incl. the Model-A answer to the reviewer's parenthetical (two evaluations + cut identity ⇒ π₀=1−ρ without Thm 2) (N55); E[BP] identification marked "a by-product of the computation, not an independent argument" (N56; the effective-service-time intuition left open per the reviewer's own note); duplicate kernel display removed (N57); f(1) inequality moved to text (N58); "Hence," (N59); "we obtain" (N60); boundedness reason at x=x*(y) (N61); x*(y) kept unabbreviated in the regrouping (N62); RHS→right-hand side (N63); "it simplifies"→"the braced expression simplifies" (N64) |
| §11 Results | N65–N109 | Section retitled **"Numerical verification and comparison"** (N65) + intro-roadmap sentence in §1 updated; validation→verification / validate→confirm / validated→verified throughout incl. abstract (N68–N70); "lie on the diagonal to 10⁻⁴" made precise (N66); Table 4: T-S approximation row moved last behind a rule + caption explains it is an accuracy assessment, not a verification (N67); **Model-B column added to Table 5** (mechanism γ₁n₁+γ₂n₂, 1st-order PDE, pinning open/Volterra, integral form with unknown P_y, conserves N, ρ(1−ρ), 1−ρ, ρ<1) + intro prose explaining why the open model can join the comparison (N72, also N1c); "further simplifications"→companion models with modified mechanism (N71); Model-A paragraph split + "all performance measures" enumerated (N73/N74); "defect"→"transition" (N75; also in §7's figure caption) + queue-1 slip fixed ("waiting in Queue 1"); "The consequences"→"effect on the two classes" (N76); run-in headings now questions "What is preserved?" etc. (N77); P-K route made concrete (M/G/1 on Queue 2 with class-1 busy-period services, ref §5.1.2) (N78); P→P(x,y) (N79); "true departure" phrasing removed everywhere (N80/N100/N36-parallel); "as in Model-B"→Model-B₂ (N81, confirmed correct); "close in"→"solutions expressed in terms of" (N82); "exactly" dropped from contrast table (N83); β(y)/μ_I defined before the contrast table with refs to (7.x)/(8.x) (N84); leftover "Convection coefficient" row renamed "Derivative-term coefficient" (round-1 cross-cutting item that had survived); "In words:" dropped + sentence split + sits→lies + analyticity typo (N85/N86); Model-c₂→C₂ (N87); "appears in the PGF of both" (N88); Erlang-A paragraph pronouns re-anchored + \mbox{Model-C₂} + final period (N89/N90); k-ladder made precise (γ₁min(n₁,k), family A(k=0)→H(k=1)→parent(k→∞), forward-ref to future work) (N91); "sweep"→"vary over" (N92); Table 6: model letters uniformly math-italic (N93), "primed models"→head-of-line models with explicit rates (N94), missing space in "E[N],E[N₁]" (N95); fig_sweep regenerated: bottom-left E[W₁]-values annotation + arrow removed, all panel text enlarged (labels 13pt/ticks 11pt/legends 10.5pt), bottom-right note repositioned off the curves — `Code/build_nb_exhaustive.py` edited and `nb_exhaustive.ipynb` rebuilt (N96); cousins→counterparts, sit→lie (N97/N98); renege-rate clause dropped + "removes customers from the system" + measurable→direct (N99–N101); "lighten"→"reduce the total number of customers" (N102); E[W] under abandonment made precise via Little's Law with full λᵢ, wait ends at service-entry *or abandonment* (N103); "thos work's" fixed (N104); log–log justified (order = slope) (N105); slope-1 claim now derived: affine generator + Cramer's-rule rationality of the stationary vector ⇒ ‖π(ε)−π_A‖₁=Θ(ε) (N106); sensitivity-analysis reading added as one sentence (N107); frozen→fixed (N108); "appears at the convergence endpoint" corrected to "visible along the entire parameter range" (N109); plus typos: appries→applies, "set at"→"occupy", discretize-sentence removed |
| §12 Conclusion | N110–N126 | **Self-containment sweep (N111/N113): every \ref to lemmas/sections/tables/approximations removed from §12**, objects named in words instead; determins→determines (N110); "intended at the beginning of this thesos" recast without process-narration (N112); §12.2 merged into §12.1 "The obstruction and the mechanism dichotomy" (N114); duplicated healthcare-loop sentence deleted + "closes the loop" phrasing dropped (N115); "most consequential"→"most restrictive" (N117); Walal→Waal (N118); "escapes closed-form reach"→"ceases to admit closed-form solutions" (N119); cattying→carrying (N121); "low-hanging fruit"→"within reach of the tools developed here" (N122); k-customer item: "first two, then three, and so on"→"first k" with both rates (N123); POTENTIAL→potential (N124); "Numerical inversion"→"Numerical solution" + informal "person with more advanced mathematical resources" sentence recast (N125/N126); multi-server item corrected per N127: exact two-class M/M/c analyses with common rate exist (Wang–Baron–Scheller-Wolf, already in the bibliography) so exactness need not be surrendered; calibration item tempered per N128 (Zenios model differs; extensions likely needed); "unsolvable cases" em-dash pair fixed; "not unreal"→"not unrealistic"; "The same, can"→"The same can" |
| Cross-cutting | N1, N69 | Formality pass = the individual rephrasings above; validation→verification also in the abstract (main.tex) and §1 roadmap; `defect`→`transition` in §7 figure caption (same objection, consistency) |

Praise/no-action: none in this round (the p.1 note is a general verdict, split into N1a formality / N1b explanations / N1c Model-B-in-comparison — N1c partially applied via the Table 5 column, remainder under "needs the author").

## Skipped / needs the author — round 2

18. **N1b (partial)** — "more intuition, e.g. the Volterra discussion": §6's presentation was
    already expanded in round 1; a further interpretive paragraph on the *role* of the
    Volterra equation in §6 is drafting the author may want to do in their own voice.
19. **N1c (partial)** — "use Model-B a bit more in the comparison": the structural Table 5
    column is done; adding Model-B to the *quantitative* comparison (§11.3 figures/tables)
    is possible via the CTMC (no closed form needed) but requires rerunning the
    notebook pipeline with a Model-B configuration and regenerating
    `tab_comparison_main.tex` + `fig_sweep_EN_vs_rho` — author's call.
20. **N2 (partial)** — Devos et al. now flagged as discrete-time with randomly alternating
    service (title-verifiable); please confirm from the paper that the described
    "inspiration" wording matches what you took from it (it is not a priority queue with
    jockeying).
21. **N51 (partial)** — the Thm 5 vs Thm 6 comparison was added as a short paragraph; if
    it reads as too much, the reviewer himself marked it optional.
22. **N56** — an *independent* intuitive argument for E[BP] via an effective service time
    for class 2: reviewer suggests leaving it open ("care is required"); left open.
23. **N67 (alternative)** — T-S is now separated by a rule within Table 4; if you prefer,
    it could move out of the table entirely into a sentence.
24. **N96 (residual)** — fig_sweep text enlarged and the bottom-left annotation removed;
    if you want the same font treatment for the *other* notebook figures (fig 9 etc.),
    the rcParams in `Code/build_nb_exhaustive.py` (line ~126) are the place.
25. **N105** — reviewer wonders if log–log is the most insightful for fig 9(a); a
    justification sentence was added (order = slope). Replacing/augmenting the panel with
    a linear-scale variant is a design decision left to you.
26. **N107** — "present §11.4 as a sensitivity analysis": one reading-sentence added; a
    full reframe (axes in terms of ∂π/∂γ₁, ∂π/∂θ₁) not attempted.
27. **N116** — omit §12.3 (Operational reading) entirely? Reviewer sees limited added
    value beyond the Introduction. Content kept (deduplicated + dereferenced) — deciding
    to delete the subsection is yours.
28. **N120** — present the S̃ rationale when the alternative state space is *introduced*
    (§4) rather than (only) in Limitations: touches the frozen §§1–8 text; the §12.4
    passage already summarises the rationale, so this is a §4 editorial decision for you.
29. **N127 (residual)** — the multi-server sentence now cites Wang–Baron–Scheller-Wolf for
    exact two-class M/M/c; skim the paper again to confirm the non-preemptive case is
    covered to your satisfaction before the final hand-in.
30. **N128 (residual)** — confirm from Zenios (1999) which extensions a calibration would
    actually need (the added sentence stays deliberately unspecific).
31. **N129** — [ZM05] vs [ZK23] ordering: with `\bibliographystyle{alpha}` the list is
    sorted by *label* (ZK < ZM), which inverts author order here (Zeltyn should precede
    Zuk). Fixing it means changing the bibliography style (e.g. `plain`/`abbrv` numeric,
    or a natbib author–year style) — a global presentational change left to you.
32. **§15 appendix** — `15_appendix_numerics.tex` (currently commented out of the build)
    still uses "validation" terminology throughout; align it with N69 if it is ever
    re-enabled.

---

# Round 1 (2026-07-07)

Source: `M_Thesis_FeedbackAnnotations.pdf` (274 annotations, reviewer read up to §8/Model-C₂).
Branch: `feedback-rbr650`, commits `408bf4b` (front matter + §§1–4) and `a54ea98` (§§5–8 + renames).
Build after incorporation: 72 pp, 0 errors, 0 undefined refs, 0 duplicate labels; 7 overfull
hboxes remain, all pre-existing on the base commit (one pre-existing overfull in §7 was fixed
by the review's own space correction).

## Applied (summary by area)

| Area | Annotations | Highlights |
|---|---|---|
| Title/abstract | #2, #4–#6 | Title page first; abstract loses unused `P(x,y)` / `x=1` coordinates |
| §1 Introduction | #7–#17, #19, #22–#28 | Motivation heading dropped; healthcare refs (Zenios, Hu–Chan–Dong); Model-X named early; PGF defined with in-queue N₁,N₂; table gains Section column; generic functional-equation shape displayed in Methods; complete-transform vs boundary-only clarified; asymmetry (#15/#16) explained via the y-argument of the boundary function |
| §2 Literature | #30, #32–#51, #54–#60 | Cohen-trick coinage attributed; Stanford moved to priority-changes; §2.4 folded into §2.6; special functions attributed to the *exact* Erlang-A law (#44); J&R symmetric-classes assumption added (#56, verified from the paper); "non-claims" → partial-results framing |
| §3 Preliminaries | #61–#86 | §3.2 = PASTA only (priority/memorylessness moved to §4); Erlang-A genericised to (λ,θ) with C₂ mapping notes; Kummer subsection moved before Erlang-A; I(p) parameter caveat; b⁽ⁿ⁾ defined; PDE coefficients a(x,y)…; P_x-vs-P_h notation collision removed |
| §4 General model | #87–#114, #116–#134, #136–#163 | Opening reordered (model → parameters → states → variants); orphan dagger removed; E[B]→E[BP] (BP collision with M/G/1 service time B, #103); no-abandonment corollary moved after Thm 1 (#107/#144); diagonal split into new corollary + geometric reading (#146/#147); reading-remark → prose (#122) with conclusion ref updated; proofs gain LHS/RHS definitions, `\intertext` step narration, level-one transform definitions (𝟙 fixed to **1**, #118), closing sentences |
| §5 Model A | #164–#168, #170–#176, #178, #180–#197 | Reviewer-caught typo `π(n₁,y)→π(n₁,n₂)`; titles shortened; kernel proof re-staged; equation arrays; PPGF completeness note (#189); S̃-root difference note (#196); forcing "exponentially small **as n grows**" (#195); stray `\qedhere` removed (#197) |
| §6 Model B | #199–#216 | "Left open" made precise; Step (iv) F≡0 argument made rigorous; y(t;z) and w(z) explained; Volterra kernel/datum presentation as definitions + what a theorem would need |
| §7 Model B₂ | #217–#233, #235, #237 | PFD ansatz displayed; α(y)/β(y) convention note; μ_I check removed (#229); analyticity claim stated as part of the theorem (#222); singular-limit "convection term itself" specified (#237) |
| §8 Model C₂ | #238–#264, #266–#270, #272–#274 | Reviewer-caught sign error `D=−λ₁` (#250); stability ⇔ E[B_C] contiguous-identity link verified & added (#241); C₁ mirror note (#239); Cor 5 deferral announced + Thm 1 relation (#245/#266); probabilistic subsection retitled and rewired (#262–#264, #267–#270) |
| Cross-cutting | #103, #124/#145 | E[BP] rename through §§9–11 & results; "convection" terminology removed everywhere |

Praise notes (no action): #29, #104, #121, #187, #236.

## Skipped / needs the author — with reasons

1. **#2 (partial)** — a standard `\maketitle` front page was added; the reviewer's pointer to a
   Canvas template is the author's call.
2. **#3** — is "jockeying" the right term for class-switching? Classically it means switching
   between *parallel* queues; the priority-change literature (de Waal, Hu–Chan–Dong) says
   "priority change". Consider a footnote defining the thesis's usage, or confirm a source.
3. **#18** — why subscript 2 in C₂ when class 1 abandons? No rationale exists in the text and
   none could be reconstructed confidently (B₂ reads "jockeys *to* queue 2"; C₂ has no parallel
   reading). Suggest one naming-convention sentence in §4.
4. **#20** — reference for discrete-time / head-of-line-type mechanisms: no vetted source in
   `references.bib` (policy: no unread citations). Candidate: Walraevens et al., discrete-time
   priority jumps.
5. **#21** — "§§ → Chapters?": conflicts with the standing §-symbol convention (RC pass
   decision). Unchanged.
6. **#53** — cite Cohen's boundary-value tradition (Cohen & Boxma 1983) in §2.5: not in the
   bibliography; needs reading/vetting first.
7. **#79** — `eq:kummer:ratio` is a numbered *expression*: it is referenced as "a ratio of the
   form (…)", which is why it is displayed; give it a defined symbol only if you prefer.
8. **#115** — indent after the P(x,y) display in §4.2: ambiguous typographic nit; unchanged.
9. **#135** — a text line before *every* LHS_i/RHS_i block: covered globally by the new
   defining sentences and `\intertext` lines; full per-term narration left to the author.
10. **#169** — drop Corollary `cor:A:pi0` as repetitive: conflicts with the canonical section
    template (uniform π₀/π(0,0) corollary per model, CLAUDE.md §6). Kept.
11. **#171** — implemented as a wording fix ("for each fixed y∈(0,1]"); if the reviewer meant
    the (0,1] vs [0,1) domain interplay at y=1, that deeper point is open.
12. **#177, #179, #265 (and #271)** — requests to *justify* the probabilistic identifications:
    E[y^{N₂}|busy,N₁=0]=L₂(y) (§5.1.2/§8.4), P(N₁=0|busy)=1−ρ₁ (§5.1.2), and the
    "conditional on no class-2 present" renewal construction (Cor 5 proof). These are correct
    (CTMC-validated) but a rigorous elaboration needs the classical Cohen/Adan–Resing
    derivation; improvising it risks unsound text inside verified proofs. **Main remaining
    author task from this review.**
13. **#198** — "failure mechanism" paragraph density: reviewer says "not really a problem";
    unchanged.
14. **#234** — merge B₂'s Step (iii) into a two-step layout: tentative suggestion, conflicts
    with the deliberate three-step template of the June restructure. Unchanged.
15. **#260** — evaluate the 𝓗/𝓙 integrals once for both: their relation is now stated
    precisely (#261); a full merge would restructure Steps (ii)/(iii).
16. **#262 (partial)** — moving §8.3 wholesale before Cor 5's proof: addressed inline instead
    (proof restates the M/G/1 structure); the reorder remains an option.
17. **#52 — no change needed** — reviewer thought Zuk & Kirszenblat allow class-dependent
    rates; verified from the paper: "Equal service rates are assumed." Current text correct.
