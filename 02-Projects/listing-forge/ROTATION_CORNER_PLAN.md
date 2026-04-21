# Rotation + Corner Radius Plan for ListingForge Lane 1

Created: 2026-03-30 03:30 AM EDT
Owner: Ava

## Goal
Advance the ready task `Iris — Production Image Automation (IREN/DRECO)` by defining the next implementation layer after the successful 20-up composite POC.

## Current confirmed state
- Legacy jig coordinate math is verified against `t_jig_measurement` semantics.
- A working composite proof exists at:
  - `projects/listing-forge/output/iph5c_jig_composite_poc.jpg`
- Current POC uses only:
  - canvas size
  - padding
  - rows/cols
  - item width/height
  - inter-item margins
- Still missing from legacy parity:
  - `f_ImageRotation`
  - `f_CornerRadius`

## Recommended implementation order

### 1) Add rotation support first
Why first:
- Rotation changes final placement bounds and can affect clipping/mask behavior.
- Corner radius should be applied after the artwork is transformed into final orientation.

Implementation notes:
- Use Pillow `rotate(..., expand=False)` for strict slot-fit behavior if production expects fixed bounding boxes.
- If legacy output shows rotated art exceeding the original box, test `expand=True` on a duplicate branch, but default to `expand=False` until PH confirms expected behavior.
- Rotate around the center of the case slot, not canvas origin.
- Keep the slot dimensions authoritative (`f_PhoneWidth`, `f_PhoneHeight`).

### 2) Add corner-radius mask second
Why second:
- Radius should clip the already-oriented case art.
- Easier to visually validate once rotation behavior is stable.

Implementation notes:
- Create an RGBA mask matching the slot dimensions.
- Use `ImageDraw.rounded_rectangle` with radius from `f_CornerRadius`.
- Apply the mask before paste, then composite onto the production tray.
- If legacy radius is effectively in production-pixel units, use raw values directly first; only normalize if visual mismatch appears.

### 3) Build a parity test harness
For each test config, output:
- plain rectangle version
- rotated version
- rounded-corner version
- rotated + rounded-corner version

Store in:
- `projects/listing-forge/output/parity-tests/`

This will let PH compare expected manufacturing look vs generated mock.

## Proposed next code changes
Update `projects/listing-forge/lane1_poc_v2.py` to:
1. Move artwork transformation into a helper like `prepare_artwork(artwork, config)`
2. Read optional fields:
   - `f_ImageRotation`
   - `f_CornerRadius`
3. Convert mock artwork to RGBA before masking
4. Paste with alpha preservation

## Suggested validation questions for PH IT / creative
When requesting modern jig rows (IPH16 / IPH17 / S24), also ask:
1. Is `f_ImageRotation` always degrees clockwise, or can it be negative?
2. Is `f_CornerRadius` in final output pixels, or derived from another scale?
3. Should the visible art be clipped to the case silhouette, or only to a rounded rectangle slot?
4. Does production expect bleed beyond the visible mask area?

## Immediate next action
Implement rotation + radius in a v3 prototype and render side-by-side outputs for one legacy device first, then request modern jig rows from PH IT.
