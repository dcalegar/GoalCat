# Adapted Material under CC BY-NC-SA 4.0 — see NOTICE and README.md in this directory.
#
# Follows the shape of LUPIN's own `utility/log_config.py` (a dict keyed by dataset name,
# each entry declaring event_attribute/trace_attribute/event_template/trace_template), but
# the template strings themselves are original content authored for this project's own logs,
# not copied from LUPIN's six dataset configs — see README.md, "What is NOT reused".
#
# Two templates, not one aliased across all five logs. `_DEFAULT` keeps a `resource` clause
# (guarded, so it stays silent on today's logs, none of which populate `resource` outside RTFM)
# for any future multi-actor goal model. RTFM's own goal model declares a single actor, so its
# categories can never be resource-discriminated; the clause would only be distractor content in
# a prompt that asks the LLM to find "meaningfully different sub-patterns". Both templates drop
# the LUPIN trace-level sentence's restated frequency/duration/outcome (already present,
# structured, in the Step 5a header line) and render waiting time as a compact inline suffix,
# e.g. "Send Fine (+90d)", instead of raw seconds — computed by
# `src/goalcat/extraction/profiling.py::_format_waiting_display`, not here; unit conversion stays
# out of third_party/, see README.md's isolation contract. Adopted as the pipeline's single
# default narrative rendering (2026-08-25).

_DEFAULT = {
    "event_attribute": ["activity", "resource", "waiting_display"],
    "trace_attribute": ["rework_summary"],
    "event_template": (
        "{{ activity }}"
        "{% if resource %} (handled by resource {{ resource }}){% endif %}"
        "{% if waiting_display %} ({{ waiting_display }}){% endif %}"
    ),
    "trace_template": "{% if rework_summary %}{{ rework_summary }}{% endif %}",
}

_RTFM = {
    "event_attribute": ["activity", "waiting_display"],
    "trace_attribute": _DEFAULT["trace_attribute"],
    "event_template": "{{ activity }}{% if waiting_display %} ({{ waiting_display }}){% endif %}",
    "trace_template": _DEFAULT["trace_template"],
}

# rtfm_mini is a small subset of real RTFM cases (see config_mini.yaml) used for
# fast functional testing — same activity vocabulary and event/trace structure as "rtfm", so it
# reuses the same template rather than duplicating it.
TEMPLATES = {"rtfm": _RTFM, "rtfm_mini": _RTFM}

# sepsis, bpic2019 and bpic2020_permit go through the same Step 2 profiling code
# (src/goalcat/extraction/profiling.py) as rtfm, which always emits this exact
# event_attribute/trace_attribute schema regardless of the source log. None of their goal models
# declare a resource-discriminated alternative today either, but unlike rtfm they are not known to
# be single-actor by construction, so they get the resource-capable default rather than rtfm's
# trimmed template.
for _log_name in ("sepsis", "bpic2019", "bpic2020_permit"):
    TEMPLATES[_log_name] = _DEFAULT
