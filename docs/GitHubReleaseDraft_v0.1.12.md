# adiftools v0.1.12

Release date: 2026-05-07

## Highlights

- Added support for multiline ADIF records that span multiple lines and end with `<EOR>` (including QRZ.com-style exports).
- Unified parsing behavior across:
  - `ADIFParser.read_adi`
  - `ADIFParser.read_adi_streaming`
  - `ADIFParser.read_adi_parallel`
- Improved parallel chunk safety by splitting on complete record boundaries.

## What Changed

### Added

- Multiline-record support for ADIF parsing.
- New tests to validate QRZ multiline parsing and consistency across sequential, streaming, and parallel parsers.

### Changed

- Record assembly now consistently uses `<EOR>` boundaries across all parser entry points.
- Header detection prefers `<EOH>` with backward-compatible fallback behavior.

### Fixed

- Fixed missed-record behavior caused by requiring `CALL` and `<EOR>` on the same line.
- Fixed potential worker-boundary record split issues in parallel parsing.

## Compatibility and Constraints

- Existing single-line ADIF records remain fully supported.
- Records without terminating `<EOR>` are treated as incomplete and skipped.
- Field values remain uppercase-normalized for backward compatibility.

## Upgrade Notes

- No special migration is required.
- QRZ.com exports no longer need preprocessing to convert multiline records into single-line records.

## Links

- Detailed release note: [docs/ReleaseNote_v0.1.12.md](./ReleaseNote_v0.1.12.md)
- Changelog: [CHANGELOG.md](../CHANGELOG.md)
