#!/usr/bin/env python3
"""Deterministic, editable research-interest word cloud and topic map."""
import argparse
import json
import math
import random
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
PALETTE = {
    "vision": "#14345A",
    "biology": "#147D83",
    "theory": "#6B53A3",
    "methods": "#BD6841",
}
LABELS = {
    "vision": "Scientific Goals",
    "biology": "Biological Applications",
    "theory": "Causal & Generalization Theory",
    "methods": "Modeling & Reliability",
}

def load(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for item in data["themes"]:
        if item["label"] in seen:
            raise ValueError("Duplicate label: " + item["label"])
        seen.add(item["label"])
        if item["category"] not in PALETTE:
            raise ValueError("Unknown category: " + item["category"])
        if not 1 <= item["weight"] <= 100:
            raise ValueError("Weight must be between 1 and 100")
    return data

def cloud(data, out, seed=17):
    from wordcloud import WordCloud
    # Use underscore tokens so multi-word research topics stay intact.
    phrases = {t["label"].replace(" ", "_"): t["weight"] for t in data["themes"]}
    categories = {t["label"].replace(" ", "_"): t["category"] for t in data["themes"]}
    wc = WordCloud(width=2400, height=1350, background_color="white",
                   collocations=False, prefer_horizontal=0.96,
                   max_words=100, margin=12, random_state=seed,
                   relative_scaling=0.45, min_font_size=16)
    wc.generate_from_frequencies(phrases)
    wc.recolor(color_func=lambda word, **kwargs: PALETTE[categories[word]],
               random_state=seed)
    fig, ax = plt.subplots(figsize=(16, 9), dpi=180)
    ax.imshow(wc.to_array(), interpolation="bilinear")
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(out / "research_word_cloud.png", dpi=180, facecolor="white")
    fig.savefig(out / "research_word_cloud.svg", facecolor="white")
    plt.close(fig)

def topic_map(data, out):
    fig, ax = plt.subplots(figsize=(16, 10), dpi=180)
    fig.patch.set_facecolor("#FAFBFD")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(0.7, 9.42, data["title"], fontsize=29, weight="bold", color="#14345A")
    ax.text(0.72, 8.94, data["subtitle"], fontsize=13, color="#64748B")
    for idx, category in enumerate(LABELS):
        x = 0.7 + (idx % 2) * 7.75
        y = 4.75 if idx < 2 else 0.45
        rect = FancyBboxPatch((x, y), 7.1, 3.9,
                              boxstyle="round,pad=0.18,rounding_size=0.2",
                              facecolor="white", edgecolor="#E2E8F0", linewidth=1.4)
        ax.add_patch(rect)
        ax.text(x + 0.35, y + 3.36, LABELS[category], fontsize=17,
                weight="bold", color=PALETTE[category])
        items = sorted((t for t in data["themes"] if t["category"] == category),
                       key=lambda t: -t["weight"])
        for j, item in enumerate(items[:7]):
            ax.text(x + 0.38, y + 2.83 - j * 0.40,
                    item["label"], fontsize=11.3,
                    color="#334155", va="center")
            ax.plot([x + 5.35, x + 5.35 + item["weight"] / 100 * 1.20],
                    [y + 2.83 - j * 0.40] * 2,
                    color=PALETTE[category], lw=4, solid_capstyle="round")
    fig.savefig(out / "research_topic_map.png", bbox_inches="tight", dpi=180)
    fig.savefig(out / "research_topic_map.svg", bbox_inches="tight")
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "research_topics.json")
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data = load(args.data)
    cloud(data, args.output, args.seed)
    topic_map(data, args.output)
    print("Saved PNG and SVG graphics to", args.output)

if __name__ == "__main__":
    main()
