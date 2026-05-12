# Video Observation Boundary

Reviewed policy:

- `docs/architecture/sf6-video-analysis-protocol.md`

Video observations are draft input. They must record source fps uncertainty,
tool availability, tool limitations, direct observations, not-inferred values,
and review status.

Do not infer exact frame values from video alone. Do not treat observed damage
labels as current-system authority. Observed damage labels are review/eval
context only unless accepted by a separate authority path.

Packaged `official_raw` remains authority for current facts.
