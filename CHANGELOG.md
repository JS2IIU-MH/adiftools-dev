# Changelog

All notable changes to this project are documented in this file.

The format is inspired by Keep a Changelog.

## [0.1.12] - 2026-05-07

### Added

- Added support for multiline ADIF records where one QSO record spans multiple lines and ends with `<EOR>` (for example, QRZ.com exports).
- Added tests for QRZ multiline parsing and consistency across `read_adi`, `read_adi_streaming`, and `read_adi_parallel`.

### Changed

- Unified record parsing flow for `read_adi`, `read_adi_streaming`, and `read_adi_parallel` around `<EOR>`-based record assembly.
- Improved header boundary handling with preferred `<EOH>` detection and backward-compatible fallback behavior.
- Updated package metadata version to 0.1.12.

### Fixed

- Fixed parsing behavior that previously required `CALL` and `<EOR>` to appear on the same line.
- Fixed potential parallel parsing boundary issues caused by line-based chunk splitting.

### Known Constraints

- Incomplete ADIF records without a terminating `<EOR>` marker are skipped.
- Parsed field values are normalized to uppercase to preserve backward compatibility.

Reference: [docs/ReleaseNote_v0.1.12.md](docs/ReleaseNote_v0.1.12.md)

## [0.1.11] - 2026-05-05

### Changed

- Removed import-time Matplotlib backend override from `adifgraph` to preserve active notebook backends (Kaggle/Jupyter compatibility).

### Fixed

- Fixed issue where importing `adiftools` could disable inline plotting by forcing the `Agg` backend.

Reference: [docs/ReleaseNote_v0.1.11.md](docs/ReleaseNote_v0.1.11.md)

## [0.1.10] - 2025-12-31

### Changed

- Improved ADIF record detection to be order-agnostic and case-insensitive across normal, streaming, and parallel readers.

### Fixed

- Fixed issue where records could be ignored when `CALL` was not at the start of the record line.

Reference: [docs/ReleaseNote_v0.1.10.md](docs/ReleaseNote_v0.1.10.md)

## Earlier Releases

- 0.1.9: [docs/ReleaseNote_v0.1.9.md](docs/ReleaseNote_v0.1.9.md)
- 0.1.8: [docs/ReleaseNote_v0.1.8.md](docs/ReleaseNote_v0.1.8.md)
