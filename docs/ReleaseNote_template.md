# adiftools release 0.1.1

This is an official release version.

## Functions
* Read adif file into Pandas DataFrame.
* Generate basic Matplotlib plots from adif data.
* Utility tool to calculate Grid Locator from/to geographic coordinate.
  

## New

* `adiftools.latlon2gl(latitude, longitude)`
  * In this release, a function called latlon2gl() has been added. This function calculates a grid locator from latitude and longitude. The grid locator is output in 6-digit string format.

## Install
adiftools can now officially pip install from PyPI. If you have already installed a previous version, please update it with the following command All previous functions can still be used with this update.

```shell
pip install adiftools
```

```shell
pip install -U adiftools
```

* When you got an error from subprocess, try to install `wheel` by `pip install wheel` command


## Other
* Please report any issues with the release on the [adiftools issue tracker](issues).
* 日本語での説明はJS2IIUのブログをご覧ください：[アマチュア無線局JS2IIU](https://js2iiu.com)

Thank you, JS2IIU
