<picture align="center">
    <source media="(prefers-color-scheme: dark)" secset="https://js2iiu.com/wp-content/uploads/2024/12/adiftools_logo.png">
    <img alt="adiftools Logo" src="https://js2iiu.com/wp-content/uploads/2024/12/adiftools_logo.png" width=500>
</picture>

----------------------

# adiftools: adif file utility tools for all amateur radio stations

| Item | Description |
| --- | --- |
| Testing | ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/passing_lints) ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/passing_pytest) ![GitHub issue custom search in repo](https://img.shields.io/github/issues-search/JS2IIU-MH/adiftools-dev?query=is%3Aclosed&label=closed%20issue) |
| Package | ![GitHub Release](https://img.shields.io/github/v/release/JS2IIU-MH/adiftools-dev) |
| Meta | [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE) ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/time1) |

## What is it?

**adiftools** is a Python package that provides utilities for ADIF data which is used for the QSO logging file format.

## Main Features

- **ADIF file parser**: read ADIF file and convert to Pandas DataFrame
  - Call signature:
    ```python
    ADIFParser.read_adi(file_path, enable_timestamp=False)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of ADIF file to read
  - Returns:
    - `pd.DataFrame`
      - The created pandas.DataFrame instance includes QSO data from ADIF file 
  
  - Other Parameter:
    - `enable_timestamp`: bool, default: `False`
      - If True, add row named ['timestamp'] to DataFrame which is generated from ADIF file. The row ['timestamp'] is `datetime64[ns]` type and based on rows `'QSO_DATE'` and `'TIME_ON'`.

- **ADIF data monthly plot**: generate manthly QSO plot
  - Call signature:
    ```python
    ADIFParser.plot_monthly(fname)
    ```
    Generate bar plot of monthly QSOs and save png or jpg file. 
  - Patameters:
    - `fname`: str or path-like or binary file-like
      - A path, or a Python file-like object of plot's PNG or JPG file
  - Returns:
    - `None`
  
    <img src="https://js2iiu.com/wp-content/uploads/2024/12/monthly_qso_aa.png" width=600>

- **Band percentage plot**: generate pie plot to show QSO-Band percentage
  - Call signature:
    ```python
    ADIFParser.plot_band_percentage(fname)
    ```
    Generate pie plot of QSO-band counts and save png or jpg file. 
  - Patameters:
    - `fname`: str or path-like or binary file-like
      - A path, or a Python file-like object of plot's PNG or JPG file
  - Returns:
    - `None`

    <img src="https://js2iiu.com/wp-content/uploads/2025/01/percentage_band.png" width=500>

- **Grid Locator utilities**
  - Calcurate geographic coodination from GL
    - Call signature
      ```python
      adiftools.gl2latlon(gridlocator)
      ```
    - Parameter:
      - `gridlocator`: str of gridlocator. 4 or 6 digits, regardless upper case or lower case. 
    - Returns:
      - `(latitude, longitude)`: tuple of latitude and longitude in decimal degree unit (DD/DEG format)

## Install
Binary installers for the latest released version will be available at the [Python Package Index (PyPI)](https://pypi.org/) soon.

**NOT WORKING AT THIS MOMENT**
```sh
pip install adiftools
```

### testing version early access
For detail, please see TestPyPI website: [adiftools · TestPyPI](https://test.pypi.org/project/adiftools/0.0.3/)

```sh
pip install -i https://test.pypi.org/simple/ adiftools==0.0.3
```

## Getting Started
Example:
```python
import adiftools.adiftools as adiftools

adi = adiftools.ADIFParser()

df_adi = adi.read_adi('sample.adi') # Use your own adi file
print(df)
```

## Dependencies
- [Pandas](https://pandas.pydata.org)
- [numpy](https://numpy.org/doc/stable/index.html)
- [matplotlib](https://matplotlib.org)

## Licence
[MIT](LICENSE)
