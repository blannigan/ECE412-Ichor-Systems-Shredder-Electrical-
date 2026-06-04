# Final Report — Setup & Build Guide

> **Starting fresh or duplicating this layout on another project?**
> Read [`REPORT_TEMPLATE_GUIDE.md`](REPORT_TEMPLATE_GUIDE.md) first — it has the
> reusable preamble, title page, table styles, ladder-logic / HMI section
> patterns, and pitfalls list. This file is the **project-specific** build
> notes for the Universal Plastic Shredder report.

How to build, edit, and regenerate the EE capstone final report
(`src/Final_Report.tex`). The report is a single LaTeX document styled
after the PSU MCECS / Power Engineering Lab report template (green section
headings, blue subsections, HRule title page with the MCECS logo, `fancyhdr`
header/footer).

---

## 1. Files

| File | Purpose |
|---|---|
| `Final_Report.tex` | The report source (everything except the point-list appendix). |
| `appendix_pointlist.tex` | **Auto-generated** Appendix B (the full PLC point list). Do **not** edit by hand — regenerate it (see §4). |
| `gen_pointlist.py` | Generator that turns `PLC/Point_List.xlsx` into `appendix_pointlist.tex`. |
| `images/psuMCECSloghoriz.png` | MCECS horizontal logo used on the title page. |
| `images/image.png` | Operator control-panel drawing (Figure 1). |
| `Final_Report.pdf` | The built output (commit it so reviewers don't need a TeX install). |

The report also reads `../PLC/Point_List.xlsx` indirectly (through the
generator) and `../PLC/Point_List.pdf` is the standalone rendered workbook.

---

## 2. Toolchain

You need a LaTeX distribution with `pdflatex` plus the packages below, and
Python 3 with `openpyxl` for the point-list generator.

**Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended
pip install openpyxl
```

**macOS:** install MacTeX (or BasicTeX + `tlmgr install` the packages below), then `pip install openpyxl`.

### LaTeX packages used
`geometry, graphicx, float, caption, setspace, fancyhdr, enumitem, hyperref,
xcolor, titlesec, colortbl, booktabs, parskip, tabularx, xltabular, tikz,
pdfpages, pdflscape`. All ship with a full TeX Live (`texlive-latex-extra`
covers `xltabular`, `pdflscape`, `pdfpages`).

---

## 3. Build

From `docs/term2_week10_Final_Report/src/`:

```bash
pdflatex -interaction=nonstopmode Final_Report.tex
pdflatex -interaction=nonstopmode Final_Report.tex   # 2nd pass: TOC + table refs
```

Run **twice** so the table of contents and the `Table~\ref{...}` cross-references
resolve. A third pass never hurts. Then clean the aux files:

```bash
rm -f Final_Report.{aux,out,toc,log,lof,lot}
```

The current report is ~48 pages (the point-list appendix is the bulk of it).

---

## 4. Regenerating the point-list appendix (Appendix B)

Appendix B is transcribed from the Excel workbook so it matches the as-built
wiring exactly. **Whenever `PLC/Point_List.xlsx` changes, regenerate it:**

```bash
# from the repo root
python3 docs/term2_week10_Final_Report/src/gen_pointlist.py "PLC/Point_List.xlsx" docs/term2_week10_Final_Report/src/appendix_pointlist.tex
# then rebuild the PDF (§3)
```

The generator emits one landscape, full-grid table per workbook sheet using the
spreadsheet columns: *Point Description · Origin Address · DO · DI · AO · AI ·
Pwr · Destination Address · Destination Description · Notes*. It handles both the
10- and 11-column sheet layouts and escapes special characters for LaTeX.

> The report also keeps a standalone rendered copy of the workbook at
> `PLC/Point_List.pdf`. That one is exported from Excel/LibreOffice, not from
> this script.

---

## 5. Document structure & style

- **Title page** — `titlepage` with `\HRule` rules, the MCECS logo, team /
  sponsor / advisors, and the course line. Labeled "Final Report — Rough Draft".
- **Section colors** — `\titleformat` makes sections PSU green and subsections
  PSU blue. Colors are defined near the top: `PSUgreen` (106,127,16), `PSUblue`
  (0,117,154), `PSUgray` (71,67,52).
- **Header/footer** — `fancyhdr`: running title + course in the header, project
  line + page number in the footer (PSU gray).
- **Draft markers** — three helper macros flag unfinished content:
  - `\todo{...}` → red **[TODO: ...]**
  - `\note{...}` → blue *[NOTE: ...]*
  - `\question{...}` → magenta **[QUESTION: ...]**
  Search the source for `\todo`, `\note`, `\question` to find everything still
  open before the final submission.
- **Tables** — all tables are full grids (`|...|` column specs + `\hline` on
  every row). Wide reference tables use `xltabular` so they break across pages
  with a repeated header.

### Common edits
- **Team / sponsor / advisors:** the title-page `minipage` (each name is wrapped
  in `\mbox{}` so it never splits across a line).
- **Logo / panel figure:** swap the files in `images/`.
- **Final motor:** currently the GE 5KE182BC205B is the *bench/test* motor and
  the production motor is **TBD** (4 places, all marked). Replace the TBD with
  the chosen motor and re-verify the NEC 430 sizing.
- **VFD parameters:** the table in §5.2 (`\label{tab:vfdparams}`) is the single
  source — Appendix D references it.

---

## 6. Quick checklist before the final

- [ ] Regenerate Appendix B if the point list changed (§4).
- [ ] Resolve all `\todo` / `\question` markers.
- [ ] Resolve the NFPA 79 neutral-switching deviation (or document the
      justification).
- [ ] Confirm whether a formal ISO 13849-1 PL verification is in scope (the
      report carries a *preliminary* assessment only).
- [ ] Insert the wiring diagrams in Appendix C and a system block diagram in
      System Architecture.
- [ ] Rebuild the PDF (twice) and commit `Final_Report.pdf`.
