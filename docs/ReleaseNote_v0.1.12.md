# adiftools release 0.1.12

This is an official release version.

## Release Date

- 2026-05-07

## Functions

* Read ADIF file into pandas DataFrame.
* Generate basic and advanced Matplotlib plots from ADIF data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.

## New Features

* Added support for multiline ADIF records where one QSO record is split across multiple lines and terminated by `<EOR>`.
* `ADIFParser.read_adi`, `ADIFParser.read_adi_streaming`, and `ADIFParser.read_adi_parallel` now use a shared record-assembly pipeline based on `<EOR>` boundaries.

### Compatibility

* QRZ.com-exported ADIF files with multiline records are now supported.
* Existing single-line ADIF records remain supported.

## Improvements

* Improved header handling by preferring `<EOH>` boundary detection while preserving backward-compatible fallback behavior for files without `<EOH>`.
* Improved parallel loader chunking safety by splitting work on complete record boundaries, preventing records from being split across worker chunks.
* Added test coverage for QRZ multiline ADIF parsing and for result consistency across sequential, streaming, and parallel read methods.

## Bug Fixes

* Fixed an issue where valid multiline ADIF records were ignored because `CALL` and `<EOR>` were previously expected on the same line.
* Fixed a potential parallel-loading issue where line-based chunking could split a single record across worker boundaries.

## Breaking Changes

* None.

## Known Constraints

* ADIF records missing a terminating `<EOR>` marker are treated as incomplete and skipped.
* Field values continue to be normalized to uppercase to preserve existing parser behavior and backward compatibility.

## Upgrade Notes

* No special upgrade steps are required.
* If your workflow previously required converting QRZ.com exports into single-line records before import, that preprocessing step is no longer necessary in 0.1.12.

## Install

adiftools can be installed or updated from PyPI:

```shell
pip install adiftools
```

```shell
pip install -U adiftools
```

* If you encounter an error related to subprocess, try installing `wheel` with `pip install wheel`.

## Other

* Changelog entry: [CHANGELOG.md (0.1.12 section)](../CHANGELOG.md#012---2026-05-07)
* Please report any issues with the release on the [adiftools issue tracker](issues).
* For Japanese documentation, see the JS2IIU blog: [アマチュア無線局JS2IIU](https://js2iiu.com)

Thank you, JS2IIU
