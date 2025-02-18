<picture align="center">
    <source media="(prefers-color-scheme: dark)" secset="https://js2iiu.com/wp-content/uploads/2024/12/adiftools_logo.png">
    <img alt="adiftools Logo" src="https://js2iiu.com/wp-content/uploads/2024/12/adiftools_logo.png" width=500>
</picture>

----------------------

# adiftools: adif file utility tools for all amateur radio stations

| Item | Status |
| :---: | --- |
| Testing | ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/passing_lints) ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/passing_pytest) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adiftools)  ![GitHub issue custom search in repo](https://img.shields.io/github/issues-search/JS2IIU-MH/adiftools-dev?query=is%3Aclosed&label=closed%20issue) |
| Package | ![GitHub Release](https://img.shields.io/github/v/release/JS2IIU-MH/adiftools-dev) |
| Meta | [![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE) ![](https://byob.yarr.is/JS2IIU-MH/adiftools-dev/time1) |
| Stats | ![PyPI - Downloads](https://img.shields.io/pypi/dm/adiftools?logo=pypi) ![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/JS2IIU-MH/adiftools-dev/total?logo=github) |

## What is it?

**adiftools** is a Python package that provides utilities for ADIF data which is used for the QSO logging file format.

This tool offers the capability to load all QSO data from an ADIF file into a Pandas DataFrame. Additionally, it provides functionalities for graphing the loaded data, along with utility functions for Grid Locator-related latitude and longitude conversion and distance measurement.

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

- **Save ADIF data as adi file**
  - Saves the loaded ADIF data as an adi file conforming to the ADIF standard. adiftools adds a new header to the beginning of the adi file.
  - Fields with no data are filled with `nan`.
  - The header will contain information on the following two fields, CREATED_TIMESTAMP, and PROGRAMID.
  - Call signature:
    ```python
    ADIFParser.to_adi(file_path)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of adi file to save
    - Returns:
      - `None`

- **Save ADIF data as pickle file**: Save the DataFrame with the ADIF loaded to a pickle file.
  - Loading an ADIF file into a DataFrame can be quite time consuming.
  - It is especially long if there are many QSOsin the ADIF file, and it is very cumbersome to read the data every time.
  - It is recommended to serialize the ADIF data once loaded and save it in a pickle format, which is expected to be 50 times faster than loading a raw ADIF file.
  - Call signature:
    ```python
    ADIFParser.to_pickle(file_path)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of pickle file to save
    - Returns:
      - `None`

- **Load Pickle data**
  - Provides a way to read ADIF data once it has been loaded by ADIFParser and saved in a pickle file.
  - The read_pickle method does not check whether the QSO data is saved in the read pickle file.
  - Call signature:
    ```python
    ADIFParser.read_pickle(file_path)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of pickle file to read
    - Returns:
      - `pd.DataFrame`
        - The created pandas.DataFrame instance includes QSO data from ADIF file 

- **Save ADIF data as excel file**: Save the DataFrame with the ADIF loaded to an excel file.
  - Call signature:
    ```python
    ADIFParser.to_excel(file_path)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of excel file to save
    - Returns:
      - `None`

- **Generate Callsign file**
  - Outputs call sign data without duplicates from data read from an ADIF file as a text file. The text file will contain one callsign per line.
  - If the ADIF file has not been read, i.e., `read_adi()` has not been performed, it returns the error `AdifParserError`.
  - Call signature:
    ```python
    ADIFParser.call_to_txt(file_path)
    ```
  - Parameter:
    - `file_path`: str or path-like or binary file-like
      - A path of output txt file
  - Returns:
    - `None`

- **ADIF data monthly plot**: generate manthly QSO plot
  - Call signature:
    ```python
    ADIFParser.plot_monthly(file_path)
    ```
    Generate bar plot of monthly QSOs and save png or jpg file. 
  - Patameters:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of plot's PNG or JPG file
  - Returns:
    - `None`
  
    <img src="https://js2iiu.com/wp-content/uploads/2024/12/monthly_qso_aa.png" width=600>

- **Band percentage plot**: generate pie plot to show QSO-Band percentage
  - Call signature:
    ```python
    ADIFParser.plot_band_percentage(file_path)
    ```
    Generate pie plot of QSO-band counts and save png or jpg file. 
  - Patameters:
    - `file_path`: str or path-like or binary file-like
      - A path, or a Python file-like object of plot's PNG or JPG file
  - Returns:
    - `None`

    <img src="https://js2iiu.com/wp-content/uploads/2025/01/percentage_band.png" width=500>

- **Grid Locator utilities**
  - Calculate geographic coodination from GL
    - Call signature
      ```python
      adiftools.gl2latlon(gridlocator)
      ```
    - Parameter:
      - `gridlocator`: str of gridlocator. 4 or 6 digits, regardless upper case or lower case. 
    - Returns:
      - `(latitude, longitude)`: tuple of latitude and longitude in decimal degree unit (DD/DEG format)

  - Calculate grid locators from latitude and longitude
    - Call signature
      ```python
      adiftools.latlon2gl(latitude, longitude, fourdigit=False)
      ```
    - Parameters:
      - `latitude` in decimal degree unit
      - `longitude` in decimal degree unit
      - `fourdigit` if True, returns 4-digit grid square

  - Reference
    - [Edmund T. Tyson, N5JTY, Conversion Between Geodetic and Grid Locator Systems, QST January 1989, pp. 29-30, 43](http://radio-amador.net/pipermail/cluster/attachments/20120105/3611b154/conversion_geodetic_grid.pdf)

  - Calculate distance from two places' latitude and longitude
    - Call signature
      ```python
      adiftools.get_dist(lat1, lon1, lat2, lon2)
      ```
    - Parameters:
      - `lat1` – latitude of the first point in degrees
      - `lon1` – longitude of the first point in degrees
      - `lat2` – latitude of the second point in degrees
      - `lon2` – longitude of the second point in degrees
    - Returns:
      - the distance from the first point to the second in meters
    - Reference
      - [GeographicLib API — geographiclib 2.0 documentation](https://geographiclib.sourceforge.io/Python/doc/code.html#)

- **Call Sign Utility**
  - Check JA call sign
    - Call signature
      ```python
      adiftools.is_ja(call_sign)
      ```
    - Parameter:
      - `call_sign` call sign in string
    - Returns:
      - `True`: JA call, `False`: other
  - Check Area
    - Call signature
      ```python
      adiftools.get_area(call_sign)
      ```
    - Parameter:
      - `call_sign` call sign in string
    - Returns:
      - `number`: area number, `None`: n/a 

Note: `adiftools` is not support ADX file format at this moment.

## Install

adiftools has been tested against Python 3.11, 3.12, and 3.13. It may work with Python 3 prior to 3.10, but we recommend using 3.11 or higher versions.

It is recommended to create a virtual environment and install adiftools inside the virtual environment.

Binary installers for the latest released version is available via PyPI: [adiftools · PyPI](https://pypi.org/project/adiftools/).

```sh
pip install adiftools
```

If you are using an older version of adiftools, please use the following command to update it to the latest version.
```sh
pip install -U adiftools
```

Unfortunately, if you no longer need adiftools, you can uninstall it with the following command.
```sh
pip uninstall adiftools
```

### Testing version
**We have decided not to update adiftools on the TestPyPI site anymore.**

For detail, please see TestPyPI website: [adiftools · TestPyPI](https://test.pypi.org/project/adiftools/0.0.5/)

```sh
pip install -i https://test.pypi.org/simple/ adiftools==0.0.5
```

## Getting Started
The first step in utilizing adiftools is to load an ADIF file; files that follow the ADIF standard can be loaded. After loading an adif file, you can perform graphing and other operations. Please refer to this page for ADIF standard. [The Independent ADIF Site](https://www.adif.org/)

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
- [GeographicLib API](https://geographiclib.sourceforge.io/Python/doc/code.html)

## Licence
[MIT](LICENSE)

## 日本語での情報提供
Information in Japanese is available on the following blogs. Information updates are prioritised on Github, and information updates on the following blogs are slightly delayed.
- [adiftools | アマチュア無線局JS2IIU](https://js2iiu.com/adiftools/)

TU de JS2IIU 73
