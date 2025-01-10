import re

import pandas as pd

try:
    from adiftools.errors import AdifParserError
except ModuleNotFoundError or ImportError:
    from errors import AdifParserError

try:
    from adiftools.adifgraph import monthly_qso, band_percentage
except ModuleNotFoundError or ImportError:
    from adifgraph import monthly_qso, band_percentage

try:
    from adiftools.gridlocator import gl_to_latlon, latlon_to_gl
except ModuleNotFoundError or ImportError:
    from gridlocator import gl_to_latlon, latlon_to_gl

try:
    from adiftools.callsign import is_ja_call
except ModuleNotFoundError or ImportError:
    from callsign import is_ja_call


class ADIFParser():
    ''' ADIFParser class '''

    def __init__(self):
        ''' initialize ADIFParser class '''
        self._fields = []
        self._number_of_records = 0

        self.df_adif = pd.DataFrame()

    def read_adi(self, file_path, enable_timestamp=False):
        ''' read adi file and return a DataFrame '''
        df = pd.DataFrame()

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # skip adif header part
        start_line = 0
        for i, line in enumerate(lines):
            if ("<CALL" in line) or ("<call" in line):
                start_line = i
                break

        adif_data = lines[start_line:]

        for i, record in enumerate(adif_data):
            record = record.strip()

            if record[:5].upper() == '<CALL' and\
                    record[-5:].upper() == '<EOR>':
                d = self._parse_adif_record(record)
                series = pd.Series(d)

                if i == 0:
                    df = pd.DataFrame(series.to_frame().T, index=[i])
                else:
                    r_df = series.to_frame().T
                    r_df.index = [i]
                    df = pd.merge(df, r_df, how='outer')

        # reset index
        # df.reset_index(drop=True, inplace=True)
        self.df_adif = df
        self._fields = df.columns.tolist()
        self._number_of_records = len(df)

        if len(df) == 0:
            raise AdifParserError('No records found in ADIF file')

        if enable_timestamp:
            # add timestamp column to DataFrame
            df = self._add_timestamp(df)

        return df

    def to_csv(self, fname):
        ''' save ADIF DataFrame to csv file '''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        self.df_adif.to_csv(fname, index=False)

    @classmethod
    def _add_timestamp(cls, df):
        ''' add timestamp column to DataFrame '''
        if 'QSO_DATE' not in df.columns or 'TIME_ON' not in df.columns:
            raise AdifParserError(
                'QSO_DATE and TIME_ON columns not found in DataFrame')

        df['timestamp'] = pd.to_datetime(
            df['QSO_DATE'] + df['TIME_ON'], format='%Y%m%d%H%M%S')
        return df

    @classmethod
    def _parse_adif_record(cls, record):
        ''' parse adif record and return a dictionary '''
        fields = re.findall(r'<(.*?):(\d+)>([^<]*)', record)
        d = {field[0].upper().strip(): field[2].upper().strip()
             for field in fields}
        return d

    @property
    def fields(self):
        return self._fields

    @property
    def number_of_records(self):
        return self._number_of_records

    # Plot related methods
    def plot_monthly(self, fname):
        ''' plot monthly QSO bar chart'''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        monthly_qso(self.df_adif, fname)

    def plot_band_percentage(self, fname):
        ''' plot band percentage pie chart'''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        band_percentage(self.df_adif, fname)


# grid locator
def gl2latlon(gridlocator):
    ''' convert grid locator to latitude and longitude in degrees '''
    lat, lon = gl_to_latlon(gridlocator)
    return (lat, lon)


def latlon2gl(latitude, longitude, fourdigit=False):
    ''' convert lat/lon to grid locator '''
    if fourdigit:
        gridlocator = latlon_to_gl(latitude, longitude, fourdigit)
    else:
        gridlocator = latlon_to_gl(latitude, longitude)

    return gridlocator


# call sign
def is_ja(call_sign):
    return is_ja_call(call_sign)


def main():
    file_path = 'tests/sample.adi'
    parser = ADIFParser()
    _ = parser.read_adi(file_path)

    # df.to_csv('tests/sample.csv')
    # print(df.head(50))


if __name__ == '__main__':
    main()
