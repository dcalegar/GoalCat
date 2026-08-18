# Adapted Material under CC BY-NC-SA 4.0.
#
# Source: LUPIN (Pasquadibisceglie, Appice & Malerba, 2024) — https://github.com/vinspdb/LUPIN,
# preprocessing/log_to_history.py, method `__gen_prefix_history`. See NOTICE and README.md in
# this directory for the full citation and the isolation contract governing how this script may
# be called from the rest of the repository (subprocess only — never imported).
#
# What's reused: the two-template rendering loop — for each event in a trace, render
# `event_template` with that event's attributes and append it to a running text; render
# `trace_template` once with trace-level attributes and append it at the end. LUPIN re-renders
# `trace_template` after every event (to capture every prefix length, for suffix-prediction
# training); this adaptation renders it once, after the loop, since this project has no
# suffix-prediction step and only needs one narrative per complete variant.
#
# What's not reused: LUPIN's `Log` class (train/test split, label encoding, suffix generation,
# torch tensors, pickling) and its six dataset templates — none of that applies here.

import argparse
import json

from jinja2 import Template
from log_templates import TEMPLATES


def render_narrative(record: dict, template_config: dict) -> str:
    event_template = Template(template_config["event_template"])
    trace_template = Template(template_config["trace_template"])

    event_text = ""
    for event in record["events"]:
        event_vars = {key: event.get(key) for key in template_config["event_attribute"]}
        event_text += event_template.render(event_vars) + " "

    trace_vars = {key: record["trace_attrs"].get(key) for key in template_config["trace_attribute"]}
    trace_text = trace_template.render(trace_vars)

    return (event_text + trace_text).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render variant profiles as narratives (LUPIN mechanism).")
    parser.add_argument("--input", required=True, help="Path to input JSON (list of variant records).")
    parser.add_argument("--output", required=True, help="Path to write output JSON (list of narratives).")
    parser.add_argument("--log", required=True, help="Key into TEMPLATES selecting which templates to use.")
    args = parser.parse_args()

    template_config = TEMPLATES[args.log]

    with open(args.input, "r", encoding="utf-8") as f:
        records = json.load(f)

    narratives = [
        {"variant_id": record["variant_id"], "narrative": render_narrative(record, template_config)}
        for record in records
    ]

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(narratives, f, indent=2)


if __name__ == "__main__":
    main()
