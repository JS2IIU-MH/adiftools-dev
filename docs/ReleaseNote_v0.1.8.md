

# adiftools release 0.1.8

This is an official release.

## Release Date
- 2025-08-10

## Features
* Read ADIF files into pandas DataFrames.
* Generate basic and advanced Matplotlib plots from ADIF data.
* Utility tools for converting Grid Locators to and from geographic coordinates.

## New Features
* `adifgraph.monthly_band_qso(df, fname)`
  * Introduced a new function to generate a stacked bar plot of monthly QSO counts by band. This feature enables users to visually analyze the number of QSOs for each band by month. The output is saved as a PNG or JPG file.

## Improvements
* Documentation updated: Usage instructions for the new monthly band QSO plot have been added to the README.
* Compatibility with recent versions of pandas and matplotlib has been improved.

## Bug Fixes
* No bug fixes in this release.

## Breaking Changes
* None.

## Known Issues
* None reported.

## Upgrade Notes
* No special upgrade steps are required.

## Installation
adiftools can be installed or updated from PyPI:

```shell
pip install adiftools
```

```shell
pip install -U adiftools
```

* If you encounter a subprocess-related error, try installing `wheel` with `pip install wheel`.

## Other
* Please report any issues with this release on the [adiftools issue tracker](issues).
* For Japanese documentation, see the JS2IIU blog: [アマチュア無線局JS2IIU](https://js2iiu.com)

Thank you,
JS2IIU
