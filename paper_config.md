# Paper Configuration Record — N-Queens SAT Solver Comparison

## Core Configuration

| Field | Value |
|-------|-------|
| **Paper Type** | Course Assignment Report (BTL số 1) — Elsevier `cas-sc` format |
| **Discipline** | Computer Science / Artificial Intelligence / Constraint Programming |
| **Target Venue** | University course submission (HK I 2026-2027) — Elsevier template |
| **Citation Format** | APA 7.0 (author-date) |
| **Output Format** | LaTeX (.tex + .bib) → PDF via `cas-sc` class |
| **Language** | Vietnamese (body), English (abstract + keywords) |
| **Target Word Count** | ~6000 words (body), ~250 words (abstract per language) |

## Research Question & Contribution

**Primary RQ:** How do different SAT encoding methods (binary, commander, product, sequential counter) and SAT solvers (CaDiCaL, Glucose, Kissat, CryptoMiniSAT) compare against CP/ILP baselines (CP-SAT, CPLEX CP, CPLEX MIP, Gurobi) for solving N-Queens across board sizes N = 8..30?

**Contributions:**
1. Systematic empirical evaluation of 4 AMO/ALO encoding methods × 4 SAT solvers × 9 board sizes
2. Comparison against 4 exact-method baselines (CP and MIP paradigms)
3. Analysis of clause/variable growth vs. solving time trade-offs
4. Open-source reproducible framework with PySAT + OR-Tools

## Existing Materials

- **Codebase:** `src/n_queens_solver/` (encoding, experiment runner, baselines, report generation)
- **Results:** `results/summary.csv` + raw JSON per experiment + plots (scaling, heatmaps, clause counts)
- **References:** `references.bib` (8 key references: Sinz 2005, Eén & Sörensson 2005, Biere et al. 2020/2021, Audemard & Simon 2009, Soos et al. 2009, Perron & Furnon 2019, Ignatiev et al. 2018)
- **ADRs:** 3 Architecture Decision Records documenting design choices

## Structural Preferences

- **Template:** IMRaD adapted for empirical CS paper (Introduction, Related Work, Methodology, Experimental Setup, Results, Discussion, Conclusion)
- **Figures:** 4-6 figures (scaling plots, heatmaps, clause/variable analysis, comparison table)
- **Tables:** 2-3 tables (encoding characteristics, main results summary, best configurations)

## Mandatory Sections (per course requirements)

- [ ] Data Availability Statement (GitHub link)
- [ ] Ethics Declaration
- [ ] Author Contributions (CRediT)
- [ ] Conflict of Interest Statement
- [ ] Funding Acknowledgment
- [ ] AI Usage Statement

## Special Requirements

- **Template:** `\documentclass[a4paper,fleqn]{cas-sc}` (Elsevier)
- **Bilingual Abstract:** Vietnamese + English (independently written, structurally aligned)
- **Keywords:** 4-6 per language

---

**Awaiting user confirmation before proceeding to Phase 1 (Literature Search).**