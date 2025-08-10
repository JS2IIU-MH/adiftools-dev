
# adiftools release 0.1.8

This is an official release version.

## Release Date
- 2025-08-10

## Functions
* Read adif file into Pandas DataFrame.
* Generate basic and advanced Matplotlib plots from adif data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.

## New Features
* `adifgraph.monthly_band_qso(df, fname)`
  * Added a new function to generate a stacked bar plot of monthly QSO counts by band. This allows users to visually analyze the number of QSOs per band for each month. The output is saved as a PNG or JPG file.

## Improvements
* Documentation updated: Added usage instructions for the new monthly band QSO plot in the README.
* Improved compatibility with recent versions of pandas and matplotlib.

## Bug Fixes
* None in this release.

## Breaking Changes
* None.

## Known Issues
* None reported.

## Upgrade Notes
* No special upgrade steps required.

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
