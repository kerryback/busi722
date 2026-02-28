# Slide Deck Design Guide

This document describes problems found in a set of Beamer slide decks and the principles used to fix them. Use it as a reference when reviewing or reworking similar decks.

## The Core Problem

The slides read like **reference material** — everything the presenter wants to say is on the slide. For live presentation, slides should be **cues** — just enough to anchor what you're saying out loud. If a slide takes more than 5 seconds to read, it has too much text.

## Specific Issues

### 1. Visual monotony from a single repeating layout

Nearly every content slide used the same template:
- Intro sentence in a rounded box
- Two side-by-side rounded boxes with bullet lists
- Bottom callout in another rounded box

After a few slides the audience stops registering the structure because it never changes.

### 2. Too many containers per slide

A typical slide had **four separate bordered regions** (intro box, left column box, right column box, bottom callout box). That's a lot of visual framing for what's often 8–10 bullet points and a one-liner. The boxes don't add information — they add weight.

### 3. Too many bullets per group

Column boxes frequently had 4–6 bullets each. Combined with the intro and callout boxes, a single slide could contain 15+ text elements competing for attention.

### 4. Key messages buried in callout boxes

Some of the best lines ("Start with the decision, not the data," "AI is the analyst — you're the decision-maker") were crammed into a bottom callout box alongside dense content, instead of being given room to land.

---

## Fixes Applied

### Remove boxes from intro sentences

Intro sentences like "Attaching a code execution tool transforms a chatbot into a computational engine" don't need a bordered container. Make them plain text at the top of the slide.

**Before:**
```latex
\begin{shadedbox}
Attaching a code execution tool transforms a chatbot into a \alert{computational engine}.
\end{shadedbox}
```

**After:**
```latex
Attaching a code execution tool transforms a chatbot into a \alert{computational engine}.
```

### Remove boxes from bottom callouts

Takeaway lines are stronger as plain centered text with `\alert{}` for emphasis. The box wrapper dilutes their impact by making them look like just another content region.

**Before:**
```latex
\begin{shadedbox}
\centering
\alert{Iterate freely.}  Each follow-up is instant.
\end{shadedbox}
```

**After:**
```latex
\alert{Iterate freely.}  Each follow-up is instant.
```

### Remove boxes from column content (most of the time)

Replace `shadedbox[title=...]` columns with a bold header and plain bullets. This cuts visual noise dramatically.

**Before:**
```latex
\begin{shadedbox}[title=\textbf{Analysis Tasks}]
\begin{itemize}\small
  \item Sales trend analysis and forecasting
  \item Customer segmentation and cohort analysis
  \item Inventory optimization and demand patterns
  \item Employee retention and HR metrics
  \item Budget vs.\ actual comparisons
\end{itemize}
\end{shadedbox}
```

**After:**
```latex
\textbf{Analysis Tasks}
\begin{itemize}\small
  \item Sales trends and forecasting
  \item Customer segmentation
  \item Budget vs.\ actual comparisons
\end{itemize}
```

### Keep boxes only for genuine comparisons

Boxes earn their place when the visual pairing communicates something — a before/after contrast, a trade-off, or a structural distinction. Examples worth keeping:
- Without Code Execution **vs.** With Code Execution
- Traditional Dashboard **vs.** Artifact
- Spreadsheet **vs.** Database
- Without Docker **vs.** With Docker
- Low Risk **vs.** High Risk

If removing the boxes wouldn't lose any meaning, remove them.

### Trim bullets to 3 per group

Four or five bullets in a box is reference material. Three is a presentation cue. When trimming:
- Cut the least essential or most redundant item
- Combine two related points into one where natural
- Move detail to your speaker notes or verbal delivery

### Replace dense multi-column boxes with tables

Three side-by-side boxes (e.g., comparing deployment platforms) are hard to scan. A `booktabs` table is cleaner and uses less vertical space.

**Before:** Three `shadedbox` columns with 4 bullets each.

**After:**
```latex
\begin{tabular}{@{}llll@{}}
\toprule
& \textbf{Streamlit Cloud} & \textbf{Koyeb / Render} & \textbf{AWS / GCP} \\
\midrule
\textbf{Best for} & Demos, public data & Team tools & Regulated industries \\
\textbf{Cost} & Free tier & A few \$/month & Enterprise pricing \\
\bottomrule
\end{tabular}
```

### Promote key messages to standalone slides

If a callout line is the real point of a section, give it its own slide with nothing else competing. These "big idea" slides provide visual breathing room and let the message land.

```latex
\begin{frame}{}
\vspace{2cm}
\begin{center}
{\Large\bfseries Start with the decision, not the data.}
\vspace{1cm}

AI is most useful when you know what you're trying to decide.\\
Follow-up questions cost nothing --- just type.
\end{center}
\end{frame}
```

Good candidates for standalone slides: any line you'd want the audience to remember a week later.

### Merge reference-heavy slides

When two consecutive slides cover the same topic at a reference level (e.g., four types of bar charts spread across two slides, or four ML visualization types across two slides), merge them into one lighter slide. Use plain text descriptions instead of boxes.

### Remove `baritemize` / `barenumerate` wrappers

These environments put the entire list inside a bordered box. For most content, a plain `itemize` or `enumerate` is lighter and sufficient. Reserve boxed lists for content that genuinely needs visual separation from its surroundings.

---

## Summary Checklist

When reviewing a slide, ask:

1. **Does every box earn its place?** If removing it wouldn't lose meaning, remove it.
2. **Are there more than 3 bullets per group?** Trim to 3.
3. **Is the layout the same as the last 5 slides?** Vary it — use single-column, plain text, a table, or a standalone message.
4. **Is the best line on the slide buried at the bottom?** Promote it.
5. **Could this slide and the next be merged?** If both are reference material on the same topic, combine them.
6. **Would the audience read this slide in under 5 seconds?** If not, cut text until they can.
