import re

import pandas as pd

from adiftools.errors import AdifParserError

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
            if "<CALL" in line:
                start_line = i
                break

        adif_data = lines[start_line:]

        for i, record in enumerate(adif_data):
            record = record.strip()

            if record[:5] == '<CALL':
                d = self._parse_adif_record(record)
                series = pd.Series(d)

                if i == 0:
                    df = pd.DataFrame(series.to_frame().T, index=[i])
                else:
                    r_df = series.to_frame().T
                    r_df.index = [i]
                    print(r_df)
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
    
    def to_csv(self, file_path):
        ''' save ADIF DataFrame to csv file '''
        self.df_adif.to_csv(file_path, index=False)

    @classmethod
    def _add_timestamp(cls, df):
        ''' add timestamp column to DataFrame '''
        df['timestamp'] = pd.to_datetime(df['QSO_DATE'] + df['TIME_ON'], format='%Y%m%d%H%M%S')
        return df

    @classmethod
    def _parse_adif_record(cls, record):
        ''' parse adif record and return a dictionary '''
        fields = re.findall(r'<(.*?):(\d+)>([^<]*)', record)
        d = {field[0].upper().strip(): field[2].strip() for field in fields}
        return d
    
    @property
    def fields(self):
        return self._fields
    
    @property
    def number_of_records(self):
        return self._number_of_records


def main():
    file_path = 'tests/sample.adi'
    parser = ADIFParser()
    df = parser.read_adi(file_path)

    df.to_csv('tests/sample.csv')


if __name__ == '__main__':
    main()
