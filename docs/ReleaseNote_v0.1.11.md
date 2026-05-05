# adiftools release 0.1.11

This is an official release version.

## Release Date

- 2026-05-05

## Acknowledgement

Thank you to Dan Dewey for reporting the notebook plotting issue.

- @dan3dewey reported issue #10 where importing `adiftools` in Kaggle/Jupyter notebooks prevented Matplotlib inline plots from being displayed.

## Functions

* Read ADIF file into pandas DataFrame.
* Generate basic and advanced Matplotlib plots from ADIF data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.

## New Features

* `adiftools` no longer changes Matplotlib's global backend at import time. Importing the library in Kaggle, Jupyter, and similar notebook environments now preserves the active plotting backend.
* A regression test was added to ensure importing and reloading `adifgraph` does not call `matplotlib.use()`.

### Compatibility

* This change improves compatibility with notebook environments and interactive Matplotlib sessions while preserving existing file-based graph generation.

## Improvements

* Removed the import-time `matplotlib.use('Agg')` side effect from `adiftools.adifgraph`.
* Cleaned up the now-unused `matplotlib` import related to the backend override.
* Plot generation APIs continue to work without forcing a non-interactive backend globally.

## Bug Fixes

* Fixed an issue where importing `adiftools.adiftools` could disable inline plotting in Kaggle and Jupyter notebooks by overriding the Matplotlib backend with `Agg`.

Special thanks to Dan Dewey (@dan3dewey) for reporting the notebook plotting issue in issue #10 and helping identify the notebook-specific reproduction scenario.

## Upgrade Notes

* No special upgrade steps required. Existing code can continue importing `adiftools` as before, and notebook users should see inline plots behave normally after upgrading.

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
