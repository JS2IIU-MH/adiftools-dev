# adiftools release 0.1.10

This is an official release version.

## Release Date

- 2025-12-31

## Acknowledgement

Thank you to the two people who reported issues related to ADIF parsing.

- @clarljc reported parsing issue #3 on ADIF file from PSK Reporter
- @Singer reported ADIF record parsing issue #2

## Functions

* Read ADIF file into pandas DataFrame.
* Generate basic and advanced Matplotlib plots from ADIF data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.

## New Features

* ADIF record parsing no longer assumes a fixed order for fields. Fields such as `CALL`, `QSO_DATE`, `TIME_ON`, etc., can now appear in any order inside a record and will still be parsed correctly.
* `read_adi`, `read_adi_streaming`, and parallel parsing have been updated to detect records in an order-agnostic, case-insensitive way and to properly identify record terminators (`<EOR>`).

### Compatibility

* This change improves compatibility with ADIF files produced by various logging software that do not guarantee a fixed field order.

## Improvements

* More robust detection of ADIF records: the parser now uses case-insensitive presence checks and `endswith('<EOR>')` to avoid false negatives when `CALL` is not the first token in a record.
* Streaming and parallel processing paths were aligned with the same detection logic to ensure consistent behavior for large files.

## Bug Fixes

* Fixed an issue where records were ignored if the `CALL` field did not appear at the start of the line. This caused some QSOs to be missed when fields were reordered by logging software.

Special thanks to Stefano IZ0MJE for reporting the field-order parsing issue and proposing an approach.

## Upgrade Notes

* No special upgrade steps required. Existing code using `read_adi`, `read_adi_streaming`, or `read_adi_parallel` should continue to work and will benefit from improved parsing robustness.

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

* Please report any issues with the release on the [adiftools issue tracker](issues).
* For Japanese documentation, see the JS2IIU blog: [アマチュア無線局JS2IIU](https://js2iiu.com)

Thank you, JS2IIU
