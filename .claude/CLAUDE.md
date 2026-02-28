# BUSI 722: Data-Driven Finance II

## Overview
Course website for quantitative investing, Fall 2025 at Rice Business. Focus: stock selection via ML with quantitative signals. Built with Quarto, deployed to GitHub Pages.

## Build
- `quarto render` renders the site to `docs/`
- Deployed at busi722.kerryback.com

## Structure
- `*.qmd` pages (syllabus, slides, assignments, exercises)
- `slides/` contains numbered Beamer slide PDFs
- `exercises/` contains exercise files and PDFs
- `files/` contains data files for exercises
- `solutions/` contains solution files
- `docs/` is the rendered site

## Skills
This repo has custom Claude skills in `.claude/skills/`:
- **rice-data-query** — query the Rice Business stock market database
- **fetch-returns** — fetch return data
- **fetch-fundamentals** — fetch fundamental data
- **merge-data** — merge returns and fundamentals

## Conventions
- Uses Rice Business stock market data via MotherDuck
- Covers technical and fundamental indicators, ML models, rolling windows
- Weekly Zoom sessions (Mondays, 8pm)
