import pandas as pd

import numpy as np

from Data.Analysis.read_database import create_connection

import seaborn as sns


def descriptive_stats(data_frame):
    ret_series = data_frame.Returns
    series_count = ret_series.count().astype(int)
    series_mean = ret_series.mean()
    series_std = ret_series.std()
    series_median = ret_series.median()
    series_skew = ret_series.skew()
    series_kurt = ret_series.kurtosis()
    series_min = ret_series.min()
    series_max = ret_series.max()
    series_sum = ret_series.sum()

    df_stats = pd.DataFrame(index=['Count', 'Average', 'Standard Deviation', 'Median', 'Skewness',
                                   'Kurtosis', 'Minimum', 'Maximum', 'Sum'],
                            data=[series_count, series_mean, series_std, series_median, series_skew,
                                  series_kurt, series_min, series_max, series_sum],
                            columns=['Descriptive Statistics'])

    r1 = ret_series[ret_series <= -0.05].count()
    r2 = ret_series[(ret_series > -0.05) & (ret_series <= -0.025)].count()
    r3 = ret_series[(ret_series > -0.025) & (ret_series <= -0.015)].count()
    r4 = ret_series[(ret_series > -0.015) & (ret_series <= -0.01)].count()
    r5 = ret_series[(ret_series > -0.01) & (ret_series <= -0.008)].count()
    r6 = ret_series[(ret_series > -0.008) & (ret_series <= -0.006)].count()
    r7 = ret_series[(ret_series > -0.006) & (ret_series <= -0.004)].count()
    r8 = ret_series[(ret_series > -0.004) & (ret_series <= -0.002)].count()
    r9 = ret_series[(ret_series > -0.002) & (ret_series < 0)].count()
    r10 = ret_series[(ret_series >= 0) & (ret_series < 0.002)].count()
    r11 = ret_series[(ret_series >= 0.002) & (ret_series < 0.004)].count()
    r12 = ret_series[(ret_series >= 0.004) & (ret_series < 0.006)].count()
    r13 = ret_series[(ret_series >= 0.006) & (ret_series < 0.008)].count()
    r14 = ret_series[(ret_series >= 0.008) & (ret_series < 0.01)].count()
    r15 = ret_series[(ret_series >= 0.01) & (ret_series < 0.015)].count()
    r16 = ret_series[(ret_series >= 0.015) & (ret_series < 0.025)].count()
    r17 = ret_series[(ret_series >= 0.025) & (ret_series < 0.05)].count()
    r18 = ret_series[ret_series >= 0.05].count()

    prob_df = pd.DataFrame(
        index=['Less than or equal -5%', '-5% to -2.5%', '-2.5% to -1.5%', '-1.5% to -1%', '-1% to -0.8%',
               '-0.8% to -0.6%', '-0.6% to -0.4%', '-0.4% to -0.2%', '-0.2% to 0%', '0% to 0.2%',
               '0.2% to 0.4%', '0.4% to 0.6%', '0.6% to 0.8%', '0.8% to 1%', '1% to 1.5%',
               '1.5% to 2.5%', '2.5% to 5%', 'Greater than or equal 5%'],
        data=[r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18],
        columns=['Frequency']
    )

    prob_df['%age Probability'] = (prob_df['Frequency'] / df_stats.loc['Count'].values) * 100

    pos_freq = ret_series[(ret_series > 0)].count()
    neg_freq = ret_series[(ret_series < 0)].count()
    neut_freq = ret_series[(ret_series == 0)].count()

    dir_freq = pd.DataFrame(index=['Positive Returns', 'Negative Returns', 'No Return'],
                            data=[pos_freq, neg_freq, neut_freq],
                            columns=['Frequency'])

    dir_freq['%age Frequency'] = (dir_freq['Frequency'] / df_stats.loc['Count'].values) * 100

    return df_stats, prob_df, dir_freq


sql_stat = ''' SELECT Open, Close FROM stocks.historical_prices where ticker = 'AADI' ORDER BY DATE DESC '''
df = pd.read_sql(sql_stat, create_connection())

df = pd.read_csv(r'Data/crude_oil.csv')
df = pd.read_csv(r'/Users/furqan/Downloads/Crude Oil WTI Futures Historical Data.csv')
df2 = pd.read_csv(r'/Users/furqan/Downloads/Crude Oil WTI Futures Historical Data (1).csv')
df = pd.concat([df, df2])
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')
df.replace('-', np.nan, inplace=True)
df = df[~(df.Open.isna())]
df['Returns'] = (df['Close'].astype(float) - df['Open'].astype(float)) / df['Close'].astype(float)
df.columns = ['Date', 'Close', 'Open', 'High', 'Low', 'Volume', 'Change%']
df['Returns'] = (df['Close'] - df['Open']) / df['Close']
df['year'] = df.Date.dt.year
df.groupby('year').count()[['Open', 'Close']]
stats, probs, freq = descriptive_stats(df)

sns.barplot(x="index", y="Frequency", data=probs.reset_index())

df.sort_values(by='Date', inplace=True)

df.to_csv('CRUDE_OIL.csv')