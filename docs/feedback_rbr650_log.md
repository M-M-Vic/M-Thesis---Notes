# rbr650 feedback incorporation — disposition log (2026-07-07)

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
