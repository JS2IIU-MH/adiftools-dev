import datetime
import re
import multiprocessing as mp

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
    from adiftools.gridlocator import gl_to_latlon, latlon_to_gl, get_distance
except ModuleNotFoundError or ImportError:
    from gridlocator import gl_to_latlon, latlon_to_gl, get_distance

try:
    from adiftools.callsign import is_ja_call, get_area_num
except ModuleNotFoundError or ImportError:
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

    def read_adi(self, file_path, enable_timestamp=False):
        ''' read adi file and return a DataFrame '''
        records_list = []

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # skip adif header part
        start_line = 0
        for i, line in enumerate(lines):
            if ("<CALL" in line) or ("<call" in line):
                start_line = i
                break

        adif_data = lines[start_line:]

        for record in adif_data:
            record = record.strip()
            record = record.upper()

            # ADIF fields may appear in any order; check presence of CALL
            # anywhere in the record (case-insensitive) and ensure record
            # ends with <EOR> (case-insensitive).
            if '<CALL' in record and record.endswith('<EOR>'):
                d = self._parse_adif_record(record)
                records_list.append(d)

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
        in_header = True

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                # Skip header until first CALL record
                if in_header:
                    if ("<CALL" in line) or ("<call" in line):
                        in_header = False
                    else:
                        continue

                # Process ADIF record. ADIF fields can be in any order,
                # so look for CALL anywhere and ensure record ends with <EOR>.
                if '<CALL' in line.upper() and line.upper().endswith('<EOR>'):
                    d = self._parse_adif_record(line)
                    records_list.append(d)

                    # Process in chunks to manage memory
                    if len(records_list) >= chunk_size:
                        if not hasattr(self, '_temp_dfs'):
                            self._temp_dfs = []
                        chunk_df = pd.DataFrame(records_list)
                        self._temp_dfs.append(chunk_df)
                        records_list = []

        # Process remaining records
        if records_list:
            if not hasattr(self, '_temp_dfs'):
                self._temp_dfs = []
            chunk_df = pd.DataFrame(records_list)
            self._temp_dfs.append(chunk_df)

        # Combine all chunks
        if hasattr(self, '_temp_dfs') and self._temp_dfs:
            df = pd.concat(self._temp_dfs, ignore_index=True)
            del self._temp_dfs  # Clean up
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

        # Read entire file content
        with open(file_path, 'r') as file:
            content = file.read()

        # Find start of data (skip header)
        header_end = content.upper().find('<EOH>')
        if header_end != -1:
            content = content[header_end + 5:]  # Skip <EOH> tag

        # Split by record terminator to get individual records
        # Use case-insensitive split for <EOR> or <eor>
        records_raw = re.split(r'<EOR>|<eor>', content, flags=re.IGNORECASE)
        
        # Filter out empty records and records without CALL field
        adif_records = []
        for record in records_raw:
            record = record.strip()
            if record and ('<CALL' in record.upper()):
                adif_records.append(record)

        if not adif_records:
            raise AdifParserError('No records found in ADIF file')

        # Determine optimal chunk size, avoiding chunk_size == 0
        num_records = len(adif_records)
        actual_processes = min(num_processes, num_records)
        chunk_size = max(1, num_records // actual_processes)
        
        # Split records into chunks for parallel processing
        chunks = []
        for i in range(0, num_records, chunk_size):
            chunks.append(adif_records[i:i + chunk_size])

        # Process chunks in parallel
        with mp.Pool(processes=actual_processes) as pool:
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
        ''' Process a chunk of ADIF records and return list of parsed records '''
        parsed_records = []
        # More robust regex pattern that handles various field formats
        # Matches: <FIELD_NAME:LENGTH[:TYPE]>VALUE
        # The pattern allows for optional type indicator and flexible whitespace
        pattern = re.compile(r'<([^:>]+):([^:>]+)(?::[^>]*)?>([^<]*)', re.IGNORECASE)

        for record in chunk_records:
            record = record.strip()
            if not record:
                continue
                
            # Parse all fields in the record
            fields = pattern.findall(record)
            d = {}
            for field in fields:
                field_name = field[0].upper().strip()
                # field[1] is the length indicator (we don't use it for parsing)
                field_value = field[2].strip()
                # Only uppercase the value, preserving original case sensitivity where needed
                # But ADIF spec typically uses uppercase for field values
                d[field_name] = field_value.upper()
            
            # Only add records that have a CALL field
            if 'CALL' in d:
                parsed_records.append(d)

        return parsed_records


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
