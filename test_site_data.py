"""Smoke tests for the project site data (site/ + static/).

- the static dashboard files are in place (Pages serves site/ at / and
  static/ at /browser/);
- every (experiment, model variant, prompt key) combination announced in
  static/data/index.json has its JSON file on disk, except the known-missing
  fairness arms (qwen was never run with fairness prompts);
- payloads carry the fields the dashboard relies on.

Run:

    uv run --no-project --with pytest -- pytest test_site_data.py -q
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
STATIC = HERE / "static"
INDEX = json.loads((STATIC / "data" / "index.json").read_text())

# answer_grading fairness sweeps only cover the claude / codex graders.
KNOWN_MISSING = {
    ("answer_grading", "qwen", "alpaca_soft"),
    ("answer_grading", "qwen", "alpaca_strict"),
}


def test_landing_page_present():
    html = (HERE / "site" / "index.html").read_text()
    assert "Value Leakage" in html
    assert "Abstract" in html
    assert (HERE / "site" / "figure1.png").stat().st_size > 0


def test_static_dashboard_files_present():
    for name in ("index.html", "app.js", "style.css"):
        p = STATIC / name
        assert p.is_file() and p.stat().st_size > 0, p
    html = (STATIC / "index.html").read_text()
    assert "app.js" in html and "style.css" in html


def test_every_indexed_combination_has_data():
    missing = []
    for exp in INDEX["experiments"]:
        variants = [v["key"] for g in exp["model_groups"]
                    for b in g["bases"] for v in b["variants"]]
        for variant in variants:
            for pk in exp["prompt_keys"]:
                if (exp["id"], variant, pk) in KNOWN_MISSING:
                    continue
                p = STATIC / "data" / exp["id"] / variant / f"{pk}.json"
                if not p.is_file():
                    missing.append(str(p.relative_to(STATIC)))
    assert not missing, missing


def test_payloads_carry_feedback_fields():
    # Spot-check one payload per experiment: covertness judge prompt
    # templates are shipped, and rows are non-empty lists.
    for exp in INDEX["experiments"]:
        g = exp["model_groups"][0]["bases"][0]
        variant = g["variants"][0]["key"]
        pk = exp["prompt_keys"][0]
        d = json.loads(
            (STATIC / "data" / exp["id"] / variant / f"{pk}.json").read_text())
        assert isinstance(d["rows"], list) and d["rows"], exp["id"]
        assert "cov_prompts" in d, exp["id"]
