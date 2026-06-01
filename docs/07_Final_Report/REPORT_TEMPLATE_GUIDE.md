# PSU MCECS Final Report — Template Guide for Claude

**Read this first if you are setting up, expanding, or rebuilding a PSU MCECS
capstone-style final report.** It captures the conventions used in this repo
and in the parallel PwrLab Switchgear report (EE 347L, same author), so you can
reproduce the same look-and-feel on any new project.

This document is for **you, future-Claude**: when a user asks "set up a final
report," "add a section like the existing one," or "make it match the template,"
follow what is written here unless the user explicitly overrides.

---

## 0. The shape at a glance

A PSU MCECS final report is one LaTeX document that:

- Uses `article` class, 12 pt.
- Has PSU colors: green section headings, blue subsection headings, gray
  header/footer.
- Has a centered title page with two horizontal rules, the MCECS horizontal
  logo, author list, course code, today's date.
- Has a `fancyhdr` running header (project name left, course code right) and
  footer (lab link left, page number right).
- Has `\listoffigures` and `\listoftables` pages right after the TOC.
- Splits long sections into one `.tex` per section, pulled in via `\input{}`.
- Wraps every `\input` in `\IfFileExists{...}{...}{placeholder}` so a missing
  section file shows a visible placeholder instead of breaking the build.
- Uses an `\showimage` helper macro so a missing image gets a placeholder box
  instead of a hard error.
- Uses `xltabular` with proportional `X` columns for wide reference tables, and
  a PSU-green header row with white bold text.
- Includes draft markers (`\todo`, `\note`, `\question`) that any reviewer can
  grep for before the final pass.

If you reproduce those, the result will look like every other PSU MCECS report
in this lineage.

---

## 1. Files & folder layout

```
07_Final_Report/                          ← deliverable folder
├── Final_Report.pdf                      ← rendered output (commit it)
├── Report_Setup.md                       ← project-specific build notes
├── REPORT_TEMPLATE_GUIDE.md              ← THIS FILE
└── src/
    ├── Final_Report.tex                  ← the main document
    ├── appendix_pointlist.tex            ← auto-generated, do NOT hand-edit
    ├── gen_pointlist.py                  ← generator for the appendix above
    └── images/
        ├── psuMCECSloghoriz.png          ← MCECS horizontal logo (title page)
        ├── hmi_screen_*.png              ← HMI screen renders
        ├── rung_page-*.png               ← exported ladder logic pages
        └── <other figures>.png
```

Follow the parent repo convention (see `REPO_CONVENTIONS.md` at the repo root):
**`src/` for sources, parent for outputs.** PDFs at the deliverable level,
`.tex` / `.py` / images inside `src/`.

---

## 2. The preamble (copy this verbatim)

```latex
\documentclass[hidelinks,12pt]{article}

\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{float}
\usepackage{caption}
\usepackage{setspace}
\usepackage{fancyhdr}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage[table]{xcolor}
\usepackage{titlesec}
\usepackage{colortbl}
\usepackage{booktabs}
\usepackage{parskip}
\usepackage{tabularx}
\usepackage{xltabular}
\usepackage{pdfpages}
\usepackage{pdflscape}

\linespread{1.2}
\widowpenalty=8999
\clubpenalty=8999

% --- PSU palette (official RGB values) ---
\definecolor{PSUgreen}{RGB}{106,127,16}
\definecolor{PSUblue}{RGB}{0,117,154}
\definecolor{PSUgray}{RGB}{71,67,52}
\definecolor{PSUred}{RGB}{210,73,42}
\definecolor{PSUorange}{RGB}{220,155,50}
\definecolor{PSUyellow}{RGB}{230,220,143}

% --- Section coloring ---
\titleformat{\section}
  {\color{PSUgreen}\normalfont\Large\bfseries}
  {\color{PSUgreen}\thesection}{1em}{}
\titleformat{\subsection}
  {\color{PSUblue}\normalfont\large\bfseries}
  {\color{PSUblue}\thesubsection}{1em}{}
\titleformat{\subsubsection}
  {\color{PSUblue}\normalfont\normalsize\bfseries}
  {\color{PSUblue}\thesubsubsection}{1em}{}

% --- Draft markers (search for these before final submission) ---
\newcommand{\todo}[1]{\textcolor{red}{\textbf{[TODO: #1]}}}
\newcommand{\note}[1]{\textcolor{PSUblue}{\textit{[NOTE: #1]}}}
\newcommand{\question}[1]{\textcolor{magenta}{\textbf{[QUESTION: #1]}}}

% --- Graceful-fallback include helper ---
\makeatletter
\newcommand{\showimage}[3][]{%
  \IfFileExists{#2}{\includegraphics[#1]{#2}}{%
    \fbox{\begin{minipage}[c][0.35\textheight][c]{0.85\textwidth}
      \centering \textbf{#3}\\[6pt]\textit{(image not found)}
    \end{minipage}}%
  }%
}
\makeatother
```

---

## 3. Title page (copy and edit names/course only)

```latex
\begin{titlepage}
\newcommand{\HRule}{\rule{\linewidth}{0.5mm}}
\center
\HRule \\[0.4cm]
{\huge \color{PSUgreen}\bfseries <PROJECT NAME>\\[0.4cm]
 \Large \emph{Final Report}}\\[0.4cm]
\HRule \\[1.0cm]

\textsc{\large Portland State University \\
  Maseeh College of Engineering \& Computer Science \\
  Department of Electrical \& Computer Engineering}\\[1.5cm]

\begin{minipage}{0.5\textwidth}
\large
\emph{Authors:}\\
\mbox{First \textsc{Last}}\\
\mbox{First \textsc{Last}}\\
{\large \today}
\end{minipage}\\[0.5cm]
\vfill
\includegraphics[width=3.5in]{images/psuMCECSloghoriz.png}
\vfill
\textsc{\color{PSUgray}\normalsize <COURSE CODE> \\ <COURSE TITLE>}\\[0.5cm]
\end{titlepage}
```

Wrap each name in `\mbox{}` so it never splits across a line.

---

## 4. Header / footer

```latex
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\footnotesize\textcolor{PSUgray}{<PROJECT> --- <SUBTITLE>}}
\fancyhead[R]{\footnotesize\textcolor{PSUgray}{<COURSE CODE>}}
\renewcommand{\footrulewidth}{0.4pt}
\fancyfoot[L]{\footnotesize\color{PSUgray}\sffamily
  <Lab name or sponsor> \textbullet\ <Address line>}
\fancyfoot[R]{\footnotesize\color{PSUgray}\sffamily\thepage}
```

---

## 5. Front matter

```latex
\setcounter{tocdepth}{2}
\tableofcontents
\newpage
\listoffigures
\newpage
\listoftables
\newpage
```

Two-pass build resolves these (three passes if you also have many `\ref`s).

---

## 6. Section structure — one file per section

Don't put 1000 lines in one `.tex`. Split the big sections into their own files
under `src/` and pull them in with `\input{...}` guarded by `\IfFileExists`:

```latex
\section{PLC Ladder Logic Diagram}
\label{sec:ladder}
\IfFileExists{Section_Ladder_Logic.tex}{\input{Section_Ladder_Logic}}{%
  \noindent\textit{Placeholder: create \texttt{Section\_Ladder\_Logic.tex}.}}
\pagebreak
```

Why: a teammate can be drafting `Section_BoM.tex` while you build the PDF —
nothing breaks, the missing section is visibly flagged. This is a hard
convention; do not collapse it back into one monolithic `.tex`.

A typical section list for an EE-build capstone:

1. Introduction
2. Requirements (must / should / may)
3. System Architecture
4. Hardware Design
5. Software / Ladder Logic Design
6. HMI Programming
7. Safety Design (NFPA 79 / ISO 13849-1)
8. Failure Mode Analysis
9. Compliance & Standards (NEC + NFPA + NEMA + ISO table)
10. Operating Instructions
11. Bill of Materials
12. Lessons Learned / Conclusion
13. Appendices (Point List, Wiring Diagrams, etc.)

---

## 7. The Ladder Logic section pattern

Follow this **exact** order — it is what makes the section legible.

### 7.1 Overview paragraph

One paragraph: what the program does, where it runs (which CPU model), how many
rungs, what file it is exported from. End with a one-sentence summary of the
state machine ("normal operation + 3-strike jam recovery + hard lockout").

### 7.2 Variable / coil reference table

A full PSU-green-headered `xltabular` mapping every PLC address used
(X / Y / WX / WY / C / T / CT / V / ST) to its `Name in Ladder`, `Type`, and
`Description`. Use proportional X columns (see §11) so the description column
gets most of the width.

### 7.3 Rung-by-rung description with inline ladder images

For each page of the exported ladder PDF:

```latex
\paragraph{Page N of M --- Rungs X--Y: <topic>}~

\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{images/rung_page-N.png}
\caption{Ladder export page N. <one-line summary> (rungs X--Y).}
\end{figure}

\begin{itemize}
  \item \textbf{Rung X} (<input cond> $\rightarrow$ <output>): <what it does and why>.
  \item \textbf{Rung X+1} ...
\end{itemize}
```

The **image goes immediately under** the `\paragraph` header, and the bulleted
rung descriptions go **immediately under the image**. This lets a reviewer
correlate the ladder graphic with the narrative without flipping between body
and appendix.

To extract page images from the ladder PDF:

```bash
pdftoppm -png -r 180 path/to/Circuit_logic.pdf images/rung_page
# → rung_page-1.png, rung_page-2.png, ...
```

### 7.4 Higher-level behaviors (jam recovery, blackstart, etc.)

After the rung-by-rung walk, add a **timeline** or **sequence diagram** of any
multi-rung behavior the operator cares about. Example: a 4-row table showing
`t=0`, `t=2 s`, `t=4 s`, `t=30 s` events through the jam-clear cycle, with the
relevant rungs cited per row.

### 7.5 Appendix C should NOT duplicate the rung images

If you put the ladder images inline in the main body (§7.3), reduce Appendix C
("PLC Ladder Logic Reference") to a one-paragraph pointer back to the section
plus the path to the exported PDF in the repo. Two copies of the same images in
one report is noise.

---

## 8. The HMI section pattern

For each screen:

```latex
\subsubsection{Screen N --- <SCREEN HEADER NAME>}

\begin{figure}[H]
\centering
\includegraphics[width=0.55\textwidth]{images/hmi_screen_N_<slug>.png}
\caption{HMI Screen N --- <description>.}
\label{fig:hmi_screen_N}
\end{figure}

<one-paragraph narrative of what the screen does and when it shows up>

\begin{itemize}
  \item \textbf{<Element name>} (\texttt{<HMI tag> / <PLC address>}, <kind>): <behavior>.
  \item ...
\end{itemize>
```

Width `0.55\textwidth` matches the actual aspect of a small C-more Micro screen
crop — wider just shows gray surround. Adjust if you target a different panel.

### Extracting clean HMI screen images

C-more Micro's "Print to PDF" export produces multi-page documents where the
screen render lives on one specific page surrounded by property dumps. The
clean way to extract just the screen render:

```bash
# 1. Render the page you want at 200 dpi
pdftoppm -png -r 200 -f <page> -l <page> HMI_SCREEN.pdf out -singlefile

# 2. Crop to just the screen panel + F-key row
python3 - <<'PY'
from PIL import Image
img = Image.open("out.png")  # 1700x2200 at 200 dpi letter
# Tune these bounds: x_left, y_top, x_right, y_bottom
img.crop((340, 215, 830, 615)).save("hmi_screen_N_slug.png")
PY
```

Trial the crop on one screen, then loop it over the other pages because all
screens render at the same coordinates on the templated export.

### Tag database

Put the tag database **as a typed `xltabular`**, not as a screenshot.
A typed table is searchable, copyable, indexable. The screenshot of the tag
database page from the HMI export is redundant if you have the typed version.

---

## 9. Tables — proportional widths and the green header

A wide reference table should:

1. Use `xltabular` (multi-page with repeating header), not plain `tabular`.
2. Use proportional `X` columns weighted with `\hsize=` so each column gets the
   width its content needs.
3. Have a PSU-green header row with white bold text.
4. Use full grid borders (`|...|` column specs and `\hline` on every row).

Skeleton:

```latex
\renewcommand{\arraystretch}{1.3}
\begin{xltabular}{\textwidth}{%
  |>{\hsize=.6\hsize\raggedright\arraybackslash}X
  |>{\hsize=1.3\hsize\raggedright\arraybackslash}X
  |>{\hsize=.7\hsize\raggedright\arraybackslash}X
  |>{\hsize=1.4\hsize\raggedright\arraybackslash}X|}
\caption{<Table caption>.}\label{tab:<key>}\\
\hline
\rowcolor{PSUgreen}
  \textcolor{white}{\textbf{Col A}}
& \textcolor{white}{\textbf{Col B}}
& \textcolor{white}{\textbf{Col C}}
& \textcolor{white}{\textbf{Col D}} \\
\hline
\endfirsthead
\hline
\rowcolor{PSUgreen}
  \textcolor{white}{\textbf{Col A}}
& \textcolor{white}{\textbf{Col B}}
& \textcolor{white}{\textbf{Col C}}
& \textcolor{white}{\textbf{Col D}} \\
\hline
\endhead
\hline\multicolumn{4}{r@{}}{\small\itshape continued on next page\,\dots}\\ \hline
\endfoot
\hline
\endlastfoot
% ... rows ...
\end{xltabular}
\renewcommand{\arraystretch}{1.0}
```

**Hard rule:** the sum of all `\hsize` weights must equal the number of `X`
columns. Above: `0.6 + 1.3 + 0.7 + 1.4 = 4.0` ✓. If the sum is off, `xltabular`
silently distorts widths.

**Common bug:** column too narrow → multi-word cell text breaks one word per
line. Symptom: "Motor rated voltage" renders as three stacked lines in a 3 cm
column. Fix by raising that column's `\hsize` weight (and lowering another).

---

## 10. Auto-generated point-list appendix

For any appendix that is just a transcription of a spreadsheet (point list,
BOM, parameter table), write a Python generator that emits a `.tex` and
`\input{}` it. Never hand-edit the generated file. The skeleton lives in
`gen_pointlist.py` — read it for the exact escaping rules (Unicode → LaTeX
substitutions, special char escaping, sheet looping).

```bash
# from src/
python3 gen_pointlist.py "../../../PLC/src/Point List.xlsx" appendix_pointlist.tex
```

Then rebuild the PDF.

---

## 11. Build workflow

```bash
cd src/
pdflatex -interaction=nonstopmode Final_Report.tex
pdflatex -interaction=nonstopmode Final_Report.tex   # TOC + cross-refs
pdflatex -interaction=nonstopmode Final_Report.tex   # belt-and-suspenders
rm -f *.aux *.log *.out *.toc *.lof *.lot
mv Final_Report.pdf ../Final_Report.pdf
```

**Always three passes.** With `\listoffigures`, `\listoftables`, table
captions, `\ref{tab:...}`, and an auto-generated appendix, references stabilize
on the third pass. Skipping a pass is how you ship a PDF with `Table ??` in it.

**Always move the PDF out of `src/`.** The output belongs at the parent
deliverable level per `REPO_CONVENTIONS.md`. Source folder stays source.

---

## 12. Common pitfalls (in this lineage, real bugs we've hit)

| Symptom | Cause | Fix |
|---|---|---|
| `Table ??` in the rendered PDF | `\label` is fine, but the `.aux` was deleted between passes 2 and 3 | Run 3 full passes, **then** clean the aux files |
| Column with one word per line | `p{Ncm}` or `X` column too narrow | Switch to `\hsize`-weighted `X` columns and re-balance |
| `Underfull \hbox` warnings everywhere | Long URLs / `\texttt{}` strings | Either accept them, or add `\sloppy` in the offending paragraph |
| Image not found at build time | LaTeX is run from the wrong directory | Always build from `src/`; reference images as `images/foo.png` |
| Duplicate rung images in body and appendix | Both `\input` blocks include them | Inline in body; Appendix C points back with one paragraph |
| Orphan PNGs in `images/` | Old screenshots never wired in | Grep for `includegraphics`; delete what is not referenced |
| Final PDF + Final_draft PDF byte-identical | Someone `cp`-ed one over the other | Consolidate to one named PDF |

---

## 13. Naming conventions for `docs/`

The parent `docs/` folder uses numbered chronological prefixes
(`01_Project_Proposal.pdf`, `02_Team_Contract.pdf`, ...,
`07_Final_Report/`). When a new top-level deliverable is added, take the
next number. Within a folder, use `Title_Case_With_Underscores.<ext>` (matches
the rest of the repo: `BOM_Combined_As_Built.pdf`, `Brake_Resistor_Wiring.md`,
`VFD_Decision_Matrix.pdf`).

---

## 14. Quick checklist before final submission

- [ ] All `\todo{}` resolved
- [ ] All `\question{}` either answered (delete) or escalated to advisor
- [ ] `\note{}` reviewed (these stay if they document genuine constraints)
- [ ] Point-list appendix regenerated against the latest workbook (§10)
- [ ] All HMI screens captured at current build state (§8)
- [ ] All ladder pages re-exported if the `.dmd` changed (§7.3)
- [ ] Compile three times, no `Table ??` / no `Figure ??` / no `??` anywhere
- [ ] TOC, LOF, LOT all populated
- [ ] PDF moved out of `src/` to the deliverable folder
- [ ] PDF committed alongside the `.tex` so reviewers don't need TeX installed

---

## 15. Reference implementations to read

When the user asks you to set up a similar report on a different project, **read
these two repos first** so you copy the patterns rather than invent them:

- This repo (`docs/07_Final_Report/src/Final_Report.tex`) — the present
  capstone build.
- The PwrLab Switchgear report (`Switchgear_Project___Task_5.zip` in author's
  Downloads if archived; `Main.tex` + `Section_*.tex` siblings). This is the
  canonical multi-file split with `\IfFileExists` fallback and the `\showimage`
  helper.

If both are unavailable, this file alone is enough to bootstrap.
