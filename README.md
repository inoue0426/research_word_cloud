# Research Word Cloud

Reproducible, editable visualizations of research interests, centered on **Predictive Biological Modeling**. The primary visualization uses four bounded groups so the topics remain readable on slides and web pages.

## Quick start

```bash
python -m pip install -r requirements.txt
python generate.py
```

Generated files in `output/`:
- `research_word_cloud.png` and `.svg` — grouped, weighted research-interest map
- `research_topic_map.png` and `.svg` — grouped scientific goals, applications, theory, and methods

## Edit research interests

Edit `research_topics.json`. Each entry has:
- `label`: phrase shown in the graphic
- `weight`: relative prominence (1–100), **editorial emphasis**, not a measured frequency
- `category`: `vision`, `biology`, `theory`, or `methods`

Run `python generate.py` again after edits. Use `--seed 42` to try another deterministic layout.

The visualizations intentionally focus on biological modeling, causality, single-cell perturbations, generalization, and therapeutic interventions; protein engineering/design is excluded.

## Design

- Navy: scientific goals
- Teal: biological applications
- Purple: causal/generalization theory
- Terracotta: modeling and reliability

The SVG output is suitable for editing in Illustrator or including in slides. The word cloud uses a deterministic layout for a given seed and dependency version.
