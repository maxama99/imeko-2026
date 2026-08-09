---
name: update-conference-program
description: Update the IMEKO 2026 website conference schedule, speakers, session titles, timing, tracks, or rooms. Use when editing the local program YAML or regenerating the Sessionize-compatible JSON consumed by Hugo.
---

# Update Conference Program

1. Read `README.md` and edit `data/program.example.yaml`, the source of truth for the local schedule.
2. Preserve unique speaker/session IDs. Reference a declared speaker by exact name or ID; undeclared names are generated as minimal speaker records.
3. Use unquoted `YYYY-MM-DD HH:MM` values for `start` and `end`. Keep sessions chronological and ensure times do not overlap unintentionally.
4. Regenerate the Hugo data from the repository root:

   ```shell
   python scripts/generate_sessionize_view_all.py \
     --input data/program.example.yaml \
     --output themes/event/assets/test/sessionize-view-all.json
   ```

5. Treat the generated JSON as an artifact: never edit it by hand. Review both YAML and JSON in the diff.
6. Validate with:

   ```shell
   python -m py_compile scripts/generate_sessionize_view_all.py
   hugo --minify
   ```

If `yaml` cannot be imported, install the Python dependency with `python -m pip install PyYAML` before regeneration.
