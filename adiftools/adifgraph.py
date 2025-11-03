import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

try:
    from adiftools.errors import AdifParserError
except ModuleNotFoundError or ImportError:
    from errors import AdifParserError

matplotlib.use('Agg')


def monthly_qso(df, fname):
    ''' plot monthly QSO '''
    if len(df) < 0:
        raise AdifParserError('Empty adif data')

    df['QSO_DATE'] = pd.to_datetime(df['QSO_DATE'])
    df['QSO_DATE'] = df['QSO_DATE'].dt.to_period('M')
    df = df.groupby('QSO_DATE').size().reset_index(name='counts')
    df.set_index('QSO_DATE', inplace=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    bar = ax.bar(df.index.astype(str), df['counts'])

    # basic graph elements
    plt.title('Monthly QSO')
    plt.xlabel('Month')
    plt.ylabel('Number of QSO')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    ax.set_axisbelow(True)
    plt.legend(['Number of QSO'], loc='upper right')

    # add value on top of each bar
    if len(df) < 24:
        text_rotation = 0
    else:
        text_rotation = 90

    for rect in bar:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., height + 1,
                '%d' % int(height), ha='center', va='bottom',
                size='small', rotation=text_rotation)

    # set layout and save to file
    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.93)
    plt.savefig(fname)
    plt.close()


def band_percentage(df, fname):
    ''' generate circle graph for band percentage '''
    # caclulate mode percentage
    if len(df) < 0:
        raise AdifParserError('Empty adif data')

    if 'BAND' in df.columns:
        mode_counts = df['BAND'].value_counts()
    else:
        raise ValueError('BAND column not found in DataFrame')

    # plot circle graph
    _, ax = plt.subplots()
    ax.pie(mode_counts, labels=mode_counts.index, autopct='%1.1f%%',
           startangle=90, counterclock=False)
    plt.title('Band Percentage')
    plt.savefig(fname)
    plt.close()


def monthly_band_qso(df, fname):
    '''バンド別の月間QSO数を積み上げ棒グラフで描画'''
    if len(df) < 0:
        raise AdifParserError('Empty adif data')

    if 'BAND' not in df.columns:
        raise ValueError('BAND column not found in DataFrame')

    from pandas.api.types import PeriodDtype
    if isinstance(df['QSO_DATE'].dtype, PeriodDtype):
        df['QSO_DATE'] = df['QSO_DATE'].dt.to_timestamp()
    else:
        df['QSO_DATE'] = pd.to_datetime(df['QSO_DATE'])
    df['QSO_MONTH'] = df['QSO_DATE'].dt.to_period('M').dt.to_timestamp()
    grouped = df.groupby(['QSO_MONTH', 'BAND']).size().unstack(fill_value=0)
    grouped = grouped.reset_index()
    # grouped['QSO_MONTH'] = grouped['QSO_MONTH'].astype(str)
    grouped['QSO_MONTH'] = grouped['QSO_MONTH'].dt.strftime('%Y-%m')

    # BANDごとの色テーブル（必要に応じて編集）
    band_colors = {
        '2M': '#FF1493',
        '4M': '#CC0044',
        '5M': '#E0E0E0',
        '6M': '#FF0000',
        '8M': '#7F00F1',
        '10M': '#FF69B4',
        '11M': '#00FF00',
        '12M': '#B22222',
        '15M': '#CCA166',
        '17M': '#F2F261',
        '20M': '#F2C40C',
        '30M': '#62D962',
        '40M': '#5959FF',
        '60M': '#00008B',
        '80M': '#E550E5',
        '160M': '#7CFC00',
        # 必要に応じて追加
    }

    fig, ax = plt.subplots(figsize=(12, 6))
    bands = [col for col in grouped.columns if col != 'QSO_MONTH']

    # 未定義BANDにはカラーマップから重複しない色を割り当て
    # import itertools
    import matplotlib as mpl
    cmap = plt.get_cmap('tab20')
    used_colors = set(band_colors.values())
    color_cycle = (mpl.colors.to_hex(cmap(i)) for i in range(cmap.N))
    band_color_map = band_colors.copy()
    for band in bands:
        if band not in band_color_map:
            # 未使用色を順に割り当て
            for color in color_cycle:
                if color not in used_colors:
                    band_color_map[band] = color
                    used_colors.add(color)
                    break

    colors = [band_color_map[band] for band in bands]
    grouped.plot(x='QSO_MONTH', y=bands, kind='bar',
                 stacked=True, ax=ax, color=colors)

    plt.title('Monthly QSO by Band')
    plt.xlabel('Month')
    plt.ylabel('Number of QSO')
    plt.xticks(rotation=90)
    plt.grid(axis='y')
    ax.set_axisbelow(True)
    plt.legend(title='Band', loc='upper right')

    # 各バーの上に合計値を表示
    for idx, row in grouped.iterrows():
        total = sum([row[band] for band in bands])
        if len(grouped) < 24:
            text_rotation = 0
        else:
            text_rotation = 90
        ax.text(idx, total + 1, str(int(total)),
                ha='center', va='bottom', size='small',
                rotation=text_rotation)

    plt.subplots_adjust(left=0.08, right=0.98, bottom=0.18, top=0.93)
    plt.savefig(fname)
    plt.close()


def main():
    pass


if __name__ == '__main__':
    main()
