# External Visual Asset Boundary

Reviewed policy:

- `docs/architecture/external-frame-atlas-policy.md`

External GIF, image, frame atlas, sprite sheet, video, screenshot, and contact
sheet binaries are forbidden by default.

External visual assets must use repo-external cache unless a future explicit
issue approves another storage path with permission, license, validator, and
bundle boundaries.

External visual assets must not enter public `sf6-agent` bundles by default.
They are not exact current-fact authority and cannot override packaged
`official_raw`.

Do not treat visual descriptor or perceptual hash matches as exact move
confirmation without review.
