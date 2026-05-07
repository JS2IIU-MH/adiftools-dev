import datetime
import re
import multiprocessing as mp

import pandas as pd


try:
    from adiftools.errors import AdifParserError
except (ModuleNotFoundError, ImportError):
    from errors import AdifParserError

try:
    from adiftools.adifgraph import monthly_qso, band_percentage
except (ModuleNotFoundError, ImportError):
    from adifgraph import monthly_qso, band_percentage

try:
    from adiftools.gridlocator import gl_to_latlon, latlon_to_gl, get_distance
except (ModuleNotFoundError, ImportError):
    from gridlocator import gl_to_latlon, latlon_to_gl, get_distance

try:
    from adiftools.callsign import is_ja_call, get_area_num
except (ModuleNotFoundError, ImportError):
    from callsign import is_ja_call, get_area_num


class ADIFParser():
    ''' ADIFParser class '''

    def __init__(self):
        ''' initialize ADIFParser class '''
        self._fields = []
        self._number_of_records = 0
        # Pre-compile regex pattern for better performance
        self._adif_pattern = re.compile(r'<(.*?):([^>]+)>([^<]*)')
        self.df_adif = pd.DataFrame()

    def _iter_record_texts(self, file_path):
        ''' yield ADIF records separated by <EOR> from a file '''
        in_header = True
        record_buffer = ''

        def process_text(text):
            nonlocal record_buffer
            record_buffer += f' {text.strip()}'

            # Extract all complete records currently in the buffer.
            while '<EOR>' in record_buffer.upper():
                upper_buffer = record_buffer.upper()
                eor_idx = upper_buffer.find('<EOR>')
                record = upper_buffer[:eor_idx + 5].strip()
                record_buffer = record_buffer[eor_idx + 5:]

                if '<CALL' in record:
                    yield record

        with open(file_path, 'r') as file:
            for raw_line in file:
                line = raw_line.strip()
                if len(line) == 0:
                    continue

                upper_line = line.upper()

                if in_header:
                    if '<EOH>' in upper_line:
                        in_header = False
                        eoh_idx = upper_line.find('<EOH>')
                        remainder = line[eoh_idx + 5:].strip()
                        if remainder:
                            for record in process_text(remainder):
                                yield record
                        continue

                    # Backward-compatible fallback for files without <EOH>.
                    if '<CALL' in upper_line:
                        in_header = False
                        for record in process_text(line):
                            yield record
                    continue

                for record in process_text(line):
                    yield record

    def _iter_parsed_records(self, file_path):
        ''' yield parsed ADIF record dicts from file '''
        for record_text in self._iter_record_texts(file_path):
            yield self._parse_adif_record(record_text)

    def read_adi(self, file_path, enable_timestamp=False):
        ''' read adi file and return a DataFrame '''
        records_list = list(self._iter_parsed_records(file_path))

        # Build DataFrame once from all records
        if records_list:
            df = pd.DataFrame(records_list)
        else:
            df = pd.DataFrame()

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
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        self.df_adif.to_csv(file_path, index=False)

    def to_excel(self, file_path):
        ''' save ADIF DataFrame to excel file '''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        self.df_adif.to_excel(file_path, index=False)

    def read_pickle(self, file_path):
        ''' read DataFrame from pickle file '''
        df = pd.read_pickle(file_path)
        self.df_adif = df
        self._fields = df.columns.tolist()
        self._number_of_records = len(df)

        return df

    def to_pickle(self, file_path):
        ''' save DataFrame to pickle file '''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        self.df_adif.to_pickle(file_path)

    def call_to_txt(self, file_path='./call.txt') -> None:
        ''' output callsign in DataFrame to text file '''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')

        calls = set(self.df_adif['CALL'].tolist())

        with open(file_path, 'w') as f:
            for call in calls:
                f.write(f'{call}\n')

    def to_adi(self, file_path):
        ''' save DataFrame to adi file '''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')

        # file extension check
        if file_path[-4:] != '.adi' and file_path[-4:] != '.ADI':
            file_path += '.adi'

        # generate adif header
        header = self._create_adif_header()
        with open(file_path, 'w') as f:
            f.write(header)
            for i in range(len(self.df_adif)):
                record = self.df_adif.iloc[i].to_dict()
                for key, value in record.items():
                    f.write(f'<{key}:{len(str(value))}>{str(value)} ')
                f.write('<EOR>\n')

    @classmethod
    def _add_timestamp(cls, df):
        ''' add timestamp column to DataFrame '''
        if 'QSO_DATE' not in df.columns or 'TIME_ON' not in df.columns:
            raise AdifParserError(
                'QSO_DATE and TIME_ON columns not found in DataFrame')

        df['timestamp'] = pd.to_datetime(
            df['QSO_DATE'] + df['TIME_ON'], format='%Y%m%d%H%M%S')
        return df

    def _parse_adif_record(self, record):
        ''' parse adif record and return a dictionary '''
        fields = self._adif_pattern.findall(record)
        d = {field[0].upper().strip(): field[2].upper().strip()
             for field in fields}
        return d

    def _create_adif_header(self):
        ''' create ADIF header '''
        timestamp = datetime.datetime.now(datetime.UTC)\
            .strftime('%Y%m%d %H%M%S')
        header = f'Generated by adiftools on {timestamp}\n'
        header += f'Total records: {self._number_of_records}\n'
        header += 'visit https://github.com/JS2IIU-MH/adiftools-dev '
        header += 'for more information\n'
        header += f'<CREATED_TIMESTAMP:15>{timestamp}\n'
        header += '<PROGRAMID:9>adiftools\n'
        header += '<EOH>\n\n'
        return header

    @property
    def fields(self):
        return self._fields

    @property
    def number_of_records(self):
        return self._number_of_records

    @property
    def is_loaded(self):
        if len(self.df_adif) > 0:
            return True
        else:
            return False

    # Plot related methods
    def plot_monthly(self, file_path):
        ''' plot monthly QSO bar chart'''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        monthly_qso(self.df_adif, file_path)

    def plot_band_percentage(self, file_path):
        ''' plot band percentage pie chart'''
        if len(self.df_adif) == 0:
            raise AdifParserError('No records found in ADIF file')
        band_percentage(self.df_adif, file_path)

    def read_adi_streaming(self, file_path, enable_timestamp=False,
                           chunk_size=1000):
        ''' read adi file using streaming approach for large files '''
        records_list = []
        temp_dfs = []

        for record in self._iter_parsed_records(file_path):
            records_list.append(record)

            # Process in chunks to manage memory
            if len(records_list) >= chunk_size:
                chunk_df = pd.DataFrame(records_list)
                temp_dfs.append(chunk_df)
                records_list = []

        # Process remaining records
        if records_list:
            chunk_df = pd.DataFrame(records_list)
            temp_dfs.append(chunk_df)

        # Combine all chunks
        if temp_dfs:
            df = pd.concat(temp_dfs, ignore_index=True)
        else:
            df = pd.DataFrame()

        self.df_adif = df
        self._fields = df.columns.tolist()
        self._number_of_records = len(df)

        if len(df) == 0:
            raise AdifParserError('No records found in ADIF file')

        if enable_timestamp:
            df = self._add_timestamp(df)

        return df

    def read_adi_parallel(self, file_path, enable_timestamp=False,
                          num_processes=None):
        ''' read adi file using parallel processing for very large files '''
        if num_processes is None:
            num_processes = mp.cpu_count()

        records = list(self._iter_record_texts(file_path))

        if len(records) == 0:
            raise AdifParserError('No records found in ADIF file')

        num_processes = max(1, min(num_processes, len(records)))

        # Split records into chunks for parallel processing
        chunk_size = max(1, len(records) // num_processes)
        chunks = []
        for i in range(0, len(records), chunk_size):
            chunks.append(records[i:i + chunk_size])

        if num_processes == 1:
            results = [self._process_chunk(chunk) for chunk in chunks]
        else:
            # Process chunks in parallel
            with mp.Pool(processes=num_processes) as pool:
                results = pool.map(self._process_chunk, chunks)

        # Combine results
        all_records = []
        for chunk_records in results:
            all_records.extend(chunk_records)

        # Build final DataFrame
        if all_records:
            df = pd.DataFrame(all_records)
        else:
            df = pd.DataFrame()

        self.df_adif = df
        self._fields = df.columns.tolist()
        self._number_of_records = len(df)

        if len(df) == 0:
            raise AdifParserError('No records found in ADIF file')

        if enable_timestamp:
            df = self._add_timestamp(df)

        return df

    def _process_chunk(self, chunk_records):
        ''' Process a chunk of records and return list of parsed records '''
        records = []

        for record in chunk_records:
            if '<CALL' in record and record.endswith('<EOR>'):
                d = self._parse_adif_record(record)
                records.append(d)

        return records


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


def get_dist(lat1, lon1, lat2, lo2):
    return get_distance(lat1, lon1, lat2, lo2)


# call sign
def is_ja(call_sign):
    return is_ja_call(call_sign)


def get_area(call_sign):
    return get_area_num(call_sign)


def main():
    file_path = 'tests/sample.adi'
    parser = ADIFParser()
    _ = parser.read_adi(file_path)

    # df.to_csv('tests/sample.csv')
    # print(df.head(50))


if __name__ == '__main__':
    main()
