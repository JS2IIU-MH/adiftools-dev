# adiftools release 0.1.9

This is an official release version.

## Release Date
- 2025-08-11

## Functions
* Read ADIF file into pandas DataFrame.
* Generate basic and advanced Matplotlib plots from ADIF data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.


## New Features
* The `monthly_band_qso` function now supports per-band color assignment for the stacked bar plot. A color table for each BAND is defined inside the function, and any BAND not listed in the table is automatically assigned a unique color from a colormap. This makes the monthly band QSO graph more visually distinct and customizable.

### BAND and Color Code Table (default)

| BAND  | Color Code |
|-------|------------|
| 2M    | #FF1493    |
| 4M    | #CC0044    |
| 5M    | #E0E0E0    |
| 6M    | #FF0000    |
| 8M    | #7F00F1    |
| 10M   | #FF69B4    |
| 11M   | #00FF00    |
| 12M   | #B22222    |
| 15M   | #CCA166    |
| 17M   | #F2F261    |
| 20M   | #F2C40C    |
| 30M   | #62D962    |
| 40M   | #5959FF    |
| 80M   | #E550E5    |
| 160M  | #7CFC00    |


The color codes above are inspired by the color scheme used on the website [PSKReporter](https://pskreporter.info/pskmap.html). We would like to acknowledge and thank PSKReporter for their excellent and informative color palette.

Any BAND not listed above will be assigned a unique color from the colormap automatically.

## Improvements
* Improved the flexibility and visual clarity of the monthly band QSO stacked bar plot.

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
