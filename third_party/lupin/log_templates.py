# Adapted Material under CC BY-NC-SA 4.0 — see NOTICE and README.md in this directory.
#
# Follows the shape of LUPIN's own `utility/log_config.py` (a dict keyed by dataset name,
# each entry declaring event_attribute/trace_attribute/event_template/trace_template), but
# the template strings themselves are original content authored for this project's own logs,
# not copied from LUPIN's six dataset configs — see README.md, "What is NOT reused".

TEMPLATES = {
    "rtfm": {
        "event_attribute": ["activity", "resource", "waiting_seconds"],
        "trace_attribute": [
            "outcome",
            "frequency",
            "frequency_pct_display",
            "duration_seconds_median",
            "rework_summary",
        ],
        "event_template": (
            "{{ activity }}"
            "{% if resource %} (handled by resource {{ resource }}){% endif %}, "
            "{{ waiting_seconds }} seconds after the previous step."
        ),
        "trace_template": (
            "This variant covers {{ frequency }} cases ({{ frequency_pct_display }}% of the "
            "log), typically takes about {{ duration_seconds_median }} seconds from start to "
            "finish, and ends in {{ outcome }}."
            "{% if rework_summary %} {{ rework_summary }}{% endif %}"
        ),
    },
}

# rtfm_mini is a small subset of real RTFM cases (see PROGRESS.md / config_mini.yaml) used for
# fast functional testing — same activity vocabulary and event/trace structure as "rtfm", so it
# reuses the same templates rather than duplicating them.
TEMPLATES["rtfm_mini"] = TEMPLATES["rtfm"]

# Every other log in data/logs/ (sepsis, bpic2019, bpic2020_permit) goes through the same Step 2
# profiling code (src/goalcat/extraction/profiling.py) as rtfm, which always emits this exact
# event_attribute/trace_attribute schema regardless of the source log — nothing in the "rtfm"
# template's wording is RTFM-specific (no activity names, no dataset vocabulary). Reusing it here
# follows the same precedent as rtfm_mini above, rather than duplicating an identical template
# under three more keys.
for _log_name in ("sepsis", "bpic2019", "bpic2020_permit"):
    TEMPLATES[_log_name] = TEMPLATES["rtfm"]
