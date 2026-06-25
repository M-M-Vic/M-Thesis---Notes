# Prompt — Humanise Prose (Results, Comparison, Conclusion)

**Scope:** `chapters/13_results.tex`, `chapters/12_comparison.tex`, `chapters/14_conclusion.tex` only.

---

## Task

Rewrite the prose in the three target files to make it more direct and readable,
without changing any mathematical content.

---

## Hard constraints (never violate)

1. **Do not add, remove, or alter any theorem statement, equation, proof step, or
   numerical claim.** Every number, formula, and citation that exists must remain exactly
   as-is or be passed through verbatim inside its LaTeX command.
2. **Do not introduce new claims, generalisations, or interpretations** that are not
   already present in the text.
3. **Preserve every `\ref`, `\eqref`, `\label`, `\cite`, and cross-reference** — never
   drop or rewrite one.
4. **Keep British English throughout:** `-ise`/`-isation`, `-our`, `-re`, doubled `l`
   (analyse, behaviour, modelling, etc.). LaTeX command names (e.g. `\centering`,
   `\itemize`) are exempt.
5. **No bullet lists in running prose.** The `enumerate` environments in the Future Work
   subsection may stay as they are.
6. **Do not add section headings, subsection headings, or new paragraphs** beyond what
   already exists.
7. After editing, the document must compile clean with `latexmk -pdf main.tex`; do not
   introduce undefined references, duplicate labels, or syntax errors.

---

## Style targets (what "humanised" means here)

**Sentence length.** Break sentences that exceed roughly 40 words into two or more
shorter ones. Remove nested relative clauses where a new sentence works just as well.

**Active voice.** Prefer active constructions. Replace "is collected", "is validated",
"is deferred" with constructions that name the actor or action directly, unless the
passive is genuinely more natural in context.

**Cut throat-clearing.** Remove or shorten phrases that exist only to announce what
the text is about to say, such as:
- "The first is …; the second is …; the third is …" scaffolding that restates the
  structure rather than stating the result.
- "As a further, assumption-free check, …" — just state the check.
- "This section reports the numerical study underpinning the analysis" — either omit
  or compress to one clause.

**Cut over-justification.** If a claim is clear from the context, do not add a
sentence explaining why it is true at the paragraph level — the proofs and equations
already do that. Trust the reader.

**Retain precision.** Do not soften qualifications that carry mathematical weight
("only for", "exactly one", "strictly inside"). These are not hedges — they are claims.

**One idea per paragraph.** If a paragraph covers two distinct ideas, split it.
If a paragraph is already tight, leave it.

**Do not change** the tone from formal academic to casual. The goal is *cleaner*
academic prose, not colloquial writing.

---

## Suggested workflow

1. Read each section in full before editing.
2. Edit paragraph by paragraph, not sentence by sentence in isolation — check that the
   surrounding context still flows after each change.
3. Where a sentence can be cut entirely without losing information, cut it.
4. Run `latexmk -pdf main.tex` and confirm zero new errors.
5. Output: (a) a unified diff of every changed paragraph, (b) build status.

---

## What NOT to touch

- Table content (caption prose is fine to lightly edit, table cell text is not).
- Anything inside `\begin{proof}…\end{proof}`.
- Mathematical display environments (`align`, `equation`, `multline`, etc.).
- The validation table (`tab:validation_summary`) cell entries.
- The Future Work `enumerate` list — only the lead-in prose before the list is in scope.
- File `chapters/12_comparison.tex` below the `\begin{table}` for `tab:comparison` —
  the table itself is out of scope; the prose surrounding it is in scope.
