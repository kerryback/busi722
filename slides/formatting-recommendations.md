# Slide Formatting Recommendations

**Generated:** 2026-02-28 (post-redesign visual review)
**Scope:** session01.pdf through session06.pdf (159 slides total)

---

## Systemic Issues

### 1. Duplicate PDF Pages (affects sessions 03, 04, 06)

Several frames produce duplicate PDF pages. The root cause is the global `\parskip` of `1.5\baselineskip plus 0.5ex` in `busi722-style.tex`. On frames that are "just full enough," this extra space pushes an invisible empty paragraph past the frame boundary, causing Beamer to emit a second (duplicate) page.

**Affected slides:**
- Session 03: "Predicting Relative Returns," "Decision Trees," "Neural Networks vs. Other Models"
- Session 04: "Computational Cost"
- Session 06: "Drawdowns and Strategy Evaluation"

**Fix:** Reduce `\parskip` in `busi722-style.tex`:
```latex
\setlength{\parskip}{0.8\baselineskip plus 0.3ex}
```
Or reduce `\vspace{0.3cm}` to `\vspace{0.15cm}` on the specific affected frames.

### 2. Tables Missing Booktabs (Session 05)

Two tables in Session 05 still use `\hline` instead of `\toprule`/`\midrule`/`\bottomrule`:
- "Comparing Weight Functions" (lines 164-173)
- "Comparing the Three Metrics" (lines 307-313)

---

## Session 01: Software, Rice Database, Technical Indicators (27 slides)

### Critical

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 10 | Mac -- Install Claude Code | "Step 3: Verify Installation" clipped at bottom | Reduce `\vspace{0.3cm}` between sections to `\vspace{0.2cm}` |
| 24 | Assigning Quantiles Each Month | Bullets below code box pressed against bottom edge | Remove `\vspace{0.3cm}` before bullets (shadedbox already adds spacing) |
| 25 | Computing EW Portfolio Returns | Bullets below code box pressed against bottom edge | Same as slide 24 |

### High

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 9 | Initial Steps | "YouTube Video" link is uninformative; bottom 40% empty | Give link a descriptive label: "Setup walkthrough -- covers Node.js, Claude Code, VS Code" |
| 20 | Querying the Data Portal | Closing paragraph has minimal bottom margin | Reduce `\vspace{0.3cm}` after bullet list to `\vspace{0.15cm}` |

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 6 | The Value Effect | Bottom 45% empty; no closing line unlike parallel slide 5 | Add closing sentence for symmetry |
| 12 | Windows -- Install Claude Code (2/2) | Only 2 bullets; bottom 50% empty | Consider merging with slide 11 |
| 14 | Install Packages | Package list sparse; bottom 55% empty | Add closing note: "Claude Code will run pip install for you" |
| 19 | Database Tables | Extra `\vspace` creates oversized gap before bullets | Remove `\vspace{0.3cm}` before itemize |

### Low

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 1 | Title slide | No session number | Add "Session 1" to subtitle |
| 5-6 | Size/Value Effects | Orange `\alert{}` used for both key findings and hyperlinks | Reserve `\alert{}` for key findings only |
| 23 | Moving Averages | Slide at capacity | Remove one `\vspace{0.3cm}` |

---

## Session 02: Claude Skills, Fundamental Indicators (27 slides)

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 7 | Returns Data: What You Get | Dense verbatim output, tight bottom margin | Show 3 rows instead of 5, or use `\footnotesize` |
| 11 | Precomputed vs. Calculated Variables | Tight bottom margin on "Must calculate" bullets | Reduce `\vspace{0.3cm}` to `\vspace{0.2cm}` |
| 12 | Fetching Fundamental Data | Prompt wraps to 3 lines (longest in deck) | Trim "the precomputed" and shorten "gross-profit-to-assets" to "gp/assets" |
| 16 | Merged Data: What You Get | Wide 9-column table hard to read at projection | Show fewer columns; drop momentum/close from display |
| 19 | How the Skills Handle It | Bottom 65% empty (most whitespace of any content slide) | Consider merging with "Summary of Shifts" table |
| 22 | Data Quality Filters | Table floats with gaps above and below | Remove `\vspace{0.3cm}` between bullets and table |
| 23 | Penny Stocks | Bullet 3 wraps to 3 lines, much longer than others | Shorten: remove "Tell Claude to read the data and" |

### Low

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 18 | The Core Problem | Lower 45% empty | Acceptable for conceptual pause slide |
| 26 | End-to-End Prompts | Item 2 asymmetrically long | Trim wording for visual symmetry |

---

## Session 03: Machine Learning for Return Prediction (24 slides)

### High

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 7/8 | Predicting Relative Returns | Duplicate PDF page | Reduce `\parskip` or `\vspace` on this frame |
| 15/16 | Decision Trees | Duplicate PDF page | Reduce `\vspace{0.3cm}` to `\vspace{0.2cm}` |
| 23/24 | Neural Networks vs. Other Models | Duplicate PDF page | Reduce `\vspace{0.3cm}` to `\vspace{0.2cm}` |

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 3 | Why Standardize? | Bottom two-thirds empty | Accept or add brief example of scale differences |
| 6 | Which Features Are "Good"? | Bottom 60% empty | Accept or add small example |
| 13 | Regularization | Bottom 75% empty (most sparse content slide) | Add loss function formulas, or merge back into Linear Models slide |

---

## Session 04: Rolling Windows for Train/Test (21 slides)

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 4 | Time-Series Split | "Limitation:" paragraph flush against bottom edge | Reduce one `\vspace{0.3cm}` to `\vspace{0.15cm}` |
| 13 | Spearman Rank Correlation | Third bullet very close to bottom edge | Reduce `\vspace{0.3cm}` between bullet groups |
| 18 | Time-Series Cross-Validation | Concluding sentence very close to bottom edge | Reduce one `\vspace{0.3cm}` to `\vspace{0.15cm}` |
| 20/21 | Computational Cost | Duplicate PDF page | Reduce `\parskip` (systemic fix) |

### Low

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 5 | A Simple Implementation | Bottom 55% empty | Accept or add closing sentence |
| 8 | Expanding vs. Rolling Windows | Gap below table | Accept |
| 12 | Measuring Prediction Quality | Bottom 60% empty | Accept |
| 17 | Cross-Validation Inside the Training Window | Bottom 65% empty | Accept |

---

## Session 05: Forming and Evaluating Portfolios (25 slides)

### High

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 5 | Pros and Cons of Sorting | Last disadvantage bullet nearly touches bottom edge | Remove `\vspace{0.3cm}` between Advantages and Disadvantages sections |

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 4 | Sorting Is a Monotone Weight Function | Bottom 40% empty | Consider merging with Pros/Cons slide |
| 11 | Exponential Tilts and Softmax | Bottom 65% empty | Add 1-2 bullets on softmax behavior, or merge with Exponential Tilts |
| 12 | Comparing Weight Functions | Table uses `\hline` not booktabs | Replace with `\toprule`/`\midrule`/`\bottomrule` |
| 14 | Why Long-Only? | 6 bullets crowded, tight bottom margin | Remove `\vspace{0.3cm}` between groups, or split into two slides |
| 22 | Sharpe vs. Information Ratio | Bottom 75% empty (sparsest slide in deck) | Add intro sentence, or merge into "Comparing the Three Metrics" |
| 23 | Comparing the Three Metrics | Table uses `\hline` not booktabs | Replace with `\toprule`/`\midrule`/`\bottomrule` |
| 24 | Putting It Together | Bottom 70% empty | Add closing takeaway line |

---

## Session 06: Trading Costs, Risk Forecasts (35 slides)

### High

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 11 | Rebalancing Frequency | Last bullet ("buffer rules") runs very close to bottom | Reduce `\vspace{0.3cm}` before table to `\vspace{0.15cm}`, or shorten bullet |

### Medium

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 13 | The Small-Cap Problem | Bottom 70% empty (only 3 short bullets) | Consider re-merging with "Solutions for Small-Cap Exposure" |
| 17 | Mean-Variance: Limitations | Bottom 70% empty (3 short Cons bullets) | Consider re-merging Pros and Cons onto one slide |
| 19 | Minimum Variance: Limitations | Bottom 70% empty (same pattern) | Consider re-merging Pros and Cons onto one slide |
| 21 | Risk Parity: Limitations | Bottom 70% empty (same pattern) | Consider re-merging Pros and Cons onto one slide |
| 26 | The Bias-Variance Tradeoff | Bottom 65% empty | Consider merging into Ledoit-Wolf Shrinkage slide |

### Low

| Slide | Title | Issue | Fix |
|-------|-------|-------|-----|
| 22 | Comparing Portfolio Construction Methods | `\small` font on table | Remove `\small`; narrow column labels instead |
| 29 | Ledoit-Wolf in Python | Code block + 2 bullets fill frame tightly | Monitor; reduce `\vspace` if content grows |
| 34/35 | Drawdowns and Strategy Evaluation | Duplicate PDF page | Systemic `\parskip` fix |

---

## Summary by Priority

| Priority | Count | Key Actions |
|----------|-------|-------------|
| Systemic | 1 | Reduce `\parskip` in style file to fix ~5 duplicate pages |
| Critical | 3 | Session 01 slides 10, 24, 25: content clipped at bottom |
| High | 6 | Session 01 (2), Session 03 duplicates (3), Session 05 (1), Session 06 (1) |
| Medium | 27 | Mostly excessive whitespace from slide splits; some tight margins |
| Low | 10 | Minor table styling, font size, polish items |

### Recommended Next Steps

1. **Fix `\parskip`** in `busi722-style.tex` -- eliminates ~5 duplicate pages across sessions 03, 04, 06
2. **Fix 3 critical overflows** in session 01 -- reduce `\vspace` on slides 10, 24, 25
3. **Add booktabs** to 2 remaining tables in session 05
4. **Consider re-merging** the sparsest "Limitations" slides in session 06 (slides 17, 19, 21, 26) -- these were split to fix overflow but are now too light with just 3 short bullets each
5. **Reduce `\vspace`** on ~5 slides with tight bottom margins across sessions 04-06
